import json
import tempfile
import unittest
from pathlib import Path

from green_ai_simulator.adapters.persistence.run_logger import RunLogger


class RunLoggerContextTests(unittest.TestCase):
    def test_normal_exit_closes_file_and_preserves_status(self):
        """(a) salida normal cierra el archivo y conserva el estado"""
        with tempfile.TemporaryDirectory() as temp_dir:
            with RunLogger(temp_dir, "offline", 1, 10, 1, "inv.json", "scn.json") as logger:
                logger.update_status("RUNNING")
                self.assertFalse(logger.samples_f.closed)

            self.assertTrue(logger.samples_f.closed)
            self.assertEqual(logger.status, "RUNNING")

            manifest_path = Path(logger.manifest_file)
            self.assertTrue(manifest_path.exists())
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)

            self.assertEqual(manifest_data["status"], "RUNNING")
            self.assertIsNone(manifest_data["stop_reason"])

    def test_exception_sets_failed_status_closes_file_and_propagates(self):
        """(b) excepción dentro del with deja status FAILED en manifest.json, archivo cerrado y la excepción se propaga"""
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(RuntimeError) as ctx:
                with RunLogger(temp_dir, "offline", 1, 10, 1, "inv.json", "scn.json") as logger:
                    logger.update_status("RUNNING")
                    raise RuntimeError("simulated error")

            self.assertEqual(str(ctx.exception), "simulated error")
            self.assertTrue(logger.samples_f.closed)
            self.assertEqual(logger.status, "FAILED")

            manifest_path = Path(logger.manifest_file)
            self.assertTrue(manifest_path.exists())
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)

            self.assertEqual(manifest_data["status"], "FAILED")
            self.assertIn("RuntimeError", manifest_data["stop_reason"])
            self.assertIsNotNone(manifest_data["completed_at_utc"])

    def test_prior_terminal_status_not_overwritten_on_exception(self):
        """(c) un estado terminal previo (COMPLETED) no se sobrescribe si luego ocurre una excepción"""
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(ValueError) as ctx:
                with RunLogger(temp_dir, "offline", 1, 10, 1, "inv.json", "scn.json") as logger:
                    logger.update_status("COMPLETED", "Duration reached")
                    raise ValueError("subsequent failure")

            self.assertEqual(str(ctx.exception), "subsequent failure")
            self.assertTrue(logger.samples_f.closed)
            self.assertEqual(logger.status, "COMPLETED")

            manifest_path = Path(logger.manifest_file)
            self.assertTrue(manifest_path.exists())
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)

            self.assertEqual(manifest_data["status"], "COMPLETED")
            self.assertEqual(manifest_data["stop_reason"], "Duration reached")

    def test_double_close_does_not_fail(self):
        """(d) doble close no falla"""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger = RunLogger(temp_dir, "offline", 1, 10, 1, "inv.json", "scn.json")
            self.assertFalse(logger.samples_f.closed)

            # Primer close
            logger.close()
            self.assertTrue(logger.samples_f.closed)

            # Segundo close - debe ser idempotente y no fallar
            logger.close()
            self.assertTrue(logger.samples_f.closed)

            # También verificar dentro de un context manager si close se llama antes de salir
            with RunLogger(temp_dir, "offline", 2, 10, 1, "inv.json", "scn.json") as logger2:
                logger2.close()
                self.assertTrue(logger2.samples_f.closed)

            self.assertTrue(logger2.samples_f.closed)


if __name__ == "__main__":
    unittest.main()
