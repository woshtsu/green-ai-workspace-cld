"""Valida un JSON exportado de Trello frente a lo que revisa el docente (prompt de evaluación Scrum).

Uso:
  python herramientas_IA/trello/validar_trello.py "<export.json>" [--max-inactividad-dias 7]

Revisa, por tarjeta abierta: fecha, checklist con ítems, miembros, etiquetas, descripción y comentarios.
Revisa el tablero: PMV1 en Done/Review/Retro, PMV2 en To Do/In Progress/QA/Done, duplicados, HU sin
formato «Como… necesito/quiero… para…» o sin criterios de aceptación, tarjetas abandonadas, movimientos
entre listas, participación por integrante y comentarios distintos por persona en el Daily Scrum.
Solo lee el archivo; no se conecta a Trello. Sale con código 1 si hay errores.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROLE_LIST = "ROLES"
NO_FLOW_LISTS = ("ROLES", "DAILY", "REVIEW", "RETROSPECTIVE", "REFINAMIENTO", "PRODUCT BACKLOG", "SPRINT BACKLOG")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip().upper()


def pmv_of(card: dict) -> str | None:
    for lab in card.get("labels", []):
        n = norm(lab.get("name", "")).replace(" ", "").replace("-", "").replace("MVP", "PMV")
        m = re.search(r"PMV0?([123])", n)
        if m:
            return "PMV" + m.group(1)
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("json", type=Path)
    ap.add_argument("--max-inactividad-dias", type=int, default=7)
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    d = json.loads(a.json.read_text(encoding="utf-8"))

    members = {m["id"]: m["fullName"] for m in d.get("members", [])}
    lists = {l["id"]: norm(l["name"]) for l in d.get("lists", []) if not l.get("closed")}
    checklists = {c["id"]: c for c in d.get("checklists", [])}
    cards = [c for c in d.get("cards", []) if not c.get("closed") and c["idList"] in lists]
    actions = d.get("actions", [])
    export_time = max((dt.datetime.fromisoformat(x["date"].replace("Z", "+00:00")) for x in actions),
                      default=dt.datetime.now(dt.timezone.utc))

    comments = defaultdict(list)
    moves = Counter()
    last_activity: dict[str, dt.datetime] = {}
    per_member = Counter()
    per_member_type = defaultdict(Counter)
    for x in actions:
        cid = (x.get("data", {}).get("card") or {}).get("id")
        who = x.get("memberCreator", {}).get("fullName", "?")
        per_member[who] += 1
        per_member_type[who][x["type"]] += 1
        when = dt.datetime.fromisoformat(x["date"].replace("Z", "+00:00"))
        if cid:
            last_activity[cid] = max(last_activity.get(cid, when), when)
        if x["type"] == "commentCard" and cid:
            comments[cid].append((who, x["data"].get("text", "")))
        if x["type"] == "updateCard" and "listAfter" in x.get("data", {}):
            moves[cid] += 1

    errors, warns = [], []
    rows = []
    for c in cards:
        lst = lists[c["idList"]]
        if ROLE_LIST in lst:
            continue
        cks = [checklists[i] for i in c.get("idChecklists", []) if i in checklists]
        items = sum(len(k.get("checkItems", [])) for k in cks)
        miss = []
        if not c.get("due") and not c.get("start"):
            miss.append("fecha")
        if items == 0:
            miss.append("checklist")
        if not c.get("idMembers"):
            miss.append("miembros")
        if not c.get("labels") and "DAILY" not in lst:
            miss.append("etiquetas")
        if len((c.get("desc") or "").strip()) < 80:
            miss.append("descripción")
        if not comments.get(c["id"]):
            miss.append("comentarios")
        rows.append((c["name"], lst, miss))
        if miss:
            errors.append(f"«{c['name']}» ({lst}): falta {', '.join(miss)}")
        name = norm(c["name"])
        desc = (c.get("desc") or "").lower()
        if name.startswith("HU"):
            if not (re.search(r"\bcomo\b", desc) and re.search(r"necesito|quiero", desc) and re.search(r"\bpara\b", desc)):
                errors.append(f"«{c['name']}»: historia sin formato Como / necesito / para")
            if not re.search(r"ca-\d|given|dado|criterios de aceptaci", desc):
                errors.append(f"«{c['name']}»: sin criterios de aceptación")
        if "DAILY" in lst:
            authors = {w for w, _ in comments.get(c["id"], [])}
            texts = [t.strip().lower() for _, t in comments.get(c["id"], [])]
            if len(authors) < 3:
                warns.append(f"Daily «{c['name']}»: comentan {len(authors)} integrantes (se esperan todos)")
            if len(texts) != len(set(texts)):
                warns.append(f"Daily «{c['name']}»: comentarios idénticos")
        if any(k in lst for k in ("IN PROGRESS", "QA")):
            last = last_activity.get(c["id"])
            if last and (export_time - last).days > a.max_inactividad_dias:
                warns.append(f"«{c['name']}» ({lst}): sin actividad hace {(export_time - last).days} días (abandonada)")

    dup = [n for n, k in Counter(norm(c["name"]) for c in cards).items() if k > 1 and not n.startswith("DAILY")]
    for n in dup:
        errors.append(f"Tarjeta duplicada: «{n}»")

    by_pmv = defaultdict(Counter)
    for c in cards:
        p = pmv_of(c)
        if p:
            by_pmv[p][lists[c["idList"]]] += 1
    pmv1_bad = [l for l in by_pmv["PMV1"] if not any(k in l for k in ("DONE", "REVIEW", "RETROSPECTIVE"))]
    if pmv1_bad:
        errors.append(f"PMV1 con tarjetas fuera de Done/Review/Retro: {pmv1_bad}")
    for need in ("TO DO", "IN PROGRESS", "QA", "DONE"):
        if not any(need in l for l in by_pmv["PMV2"]):
            errors.append(f"PMV2 sin tarjetas en la lista «{need}»")

    flow_cards = [c for c in cards if not any(k in lists[c["idList"]] for k in NO_FLOW_LISTS)]
    no_move = [c["name"] for c in flow_cards if moves[c["id"]] == 0]
    if no_move:
        warns.append(f"{len(no_move)} tarjetas del flujo sin movimiento registrado entre listas: {no_move[:10]}")

    humans = {n: k for n, k in per_member.items() if not n.lower().startswith(("uc_es", "trello"))}
    total = sum(humans.values()) or 1
    for m in members.values():
        if m.lower().startswith(("uc_es", "trello")):
            continue
        share = humans.get(m, 0) / total
        if share < 0.12:
            warns.append(f"Participación baja de {m}: {humans.get(m, 0)} acciones ({share:.0%})")
        if per_member_type[m]["commentCard"] == 0:
            warns.append(f"{m} no tiene comentarios")

    print(f"Tablero: {d.get('name')} | tarjetas abiertas: {len(cards)} | acciones en el JSON: {len(actions)}")
    print("Nota: el JSON exportado incluye como máximo las últimas 1000 acciones.")
    print("\nDistribución por PMV y lista:")
    for p in sorted(by_pmv):
        print(f"  {p}: " + ", ".join(f"{l}={n}" for l, n in sorted(by_pmv[p].items())))
    print("\nActividad por integrante (acciones / comentarios / movimientos):")
    for m in sorted(humans, key=humans.get, reverse=True):
        t = per_member_type[m]
        print(f"  {m}: {humans[m]} / {t['commentCard']} / {t['updateCard']}")
    print(f"\nTarjetas completas: {sum(1 for r in rows if not r[2])} de {len(rows)}")
    print(f"\nERRORES ({len(errors)}):")
    for e in errors:
        print("  - " + e)
    print(f"\nAVISOS ({len(warns)}):")
    for w in warns:
        print("  - " + w)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
