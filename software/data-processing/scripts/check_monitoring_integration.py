"""Read-only smoke check against live Monitoring and Data Processing on their private network."""
from datetime import datetime, timedelta, timezone
import os

import httpx


def main():
    monitoring = os.getenv("MONITORING_BASE_URL", "http://monitoring:8080").rstrip("/")
    processing = os.getenv("PROCESSING_BASE_URL", "http://data-processing:8000").rstrip("/")
    end = datetime.now(timezone.utc).replace(microsecond=0) - timedelta(seconds=30)
    params = {"start": (end - timedelta(minutes=5)).isoformat(), "end": end.isoformat(), "stepSeconds": 15}
    with httpx.Client(timeout=15) as client:
        catalog = client.get(f"{monitoring}/api/v1/metrics/catalog")
        catalog.raise_for_status()
        cpu = None
        for metric in catalog.json():
            query = {**params, "metric": metric["id"], "resourceType": "node"}
            original = client.get(f"{monitoring}/api/v1/metrics/history", params=query)
            processed = client.get(f"{processing}/api/v1/metrics/history", params=query,
                                   headers={"X-Request-Id": "integration-monitoring-processing"})
            original.raise_for_status()
            processed.raise_for_status()
            source, result = original.json(), processed.json()
            expected = [(series, sample) for series in source["series"] for sample in series["samples"]]
            assert result["recordCount"] == len(expected)
            assert result["unit"] == source["unit"]
            assert processed.headers["X-Request-Id"] == "integration-monitoring-processing"
            for series, sample in expected:
                matches = [r for r in result["records"] if r["cluster"] == series["resource"]["cluster"]
                           and r["resource_id"] == series["resource"]["id"] and r["labels"] == series["labels"]
                           and r["origin"] == series["origin"] and r["timestamp"] == sample["timestamp"]]
                assert len(matches) == 1 and matches[0]["value"] == sample["value"]
                assert matches[0]["quality"] == sample["quality"]
            print(f"{metric['id']}: HTTP 200, {len(expected)} samples preserved")
            if metric["id"] == "node.cpu.utilization":
                cpu = next((r for r in result["records"] if r["quality"] == "valid"), None)
        if cpu is None:
            raise RuntimeError("No valid CPU yet. Wait for scrapes and rerun; this is not a successful data check.")
        dataset = client.get(f"{processing}/api/v1/prediction/dataset", params={
            **params, "cluster": cpu["cluster"], "resourceId": cpu["resource_id"]})
        dataset.raise_for_status()
        payload = dataset.json()
        assert payload["features"] and payload["units"]["cpu_utilization"] == "%"
        assert all(0 <= f["cpu_utilization"] <= 100 for f in payload["features"])
        print(f"Dataset: HTTP 200, {len(payload['features'])} CPU samples; no inference executed")


if __name__ == "__main__":
    main()
