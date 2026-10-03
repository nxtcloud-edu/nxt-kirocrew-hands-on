"""Final verification for the warehouse DAG pipeline (task 10/10).

Confirms file presence, DAG independence, intermediate structure,
low-stock (<5, warehouse_row) correctness, result.json shape vs
출력형식.md, and result.json <-> report.md consistency.
Exits 0 with "ALL CHECKS PASSED" or 1 listing failures.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WIDS = ("a", "b", "c")
THRESHOLD = 5
errs = []


def need(cond, msg):
    if not cond:
        errs.append(msg)


# 1. File presence.
required = [
    "parse_warehouse.py",
    "aggregate_warehouse.py",
    "consolidate.py",
    "warehouse-a.json",
    "warehouse-b.json",
    "warehouse-c.json",
    "result.json",
    "report.md",
]
for name in required:
    need((HERE / name).exists(), f"missing file: {name}")

imm = {w: json.loads((HERE / f"warehouse-{w}.json").read_text(encoding="utf-8")) for w in WIDS}
res = json.loads((HERE / "result.json").read_text(encoding="utf-8"))
rep = (HERE / "report.md").read_text(encoding="utf-8")
agg_src = (HERE / "aggregate_warehouse.py").read_text(encoding="utf-8")
con_src = (HERE / "consolidate.py").read_text(encoding="utf-8")

# 2. DAG independence: aggregate task must not reference a specific sibling
# warehouse file in EXECUTABLE code. Strip module docstring + comments first,
# since the usage example legitimately names warehouse-a.md.
import ast

agg_ast = ast.parse(agg_src)
agg_doc = ast.get_docstring(agg_ast) or ""
agg_code = "\n".join(
    line for line in agg_src.splitlines()
    if line.strip() not in agg_doc.splitlines() and not line.strip().startswith("#")
)
# More robust: remove the docstring block and comments explicitly.
agg_no_doc = agg_src.replace(agg_doc, "") if agg_doc else agg_src
agg_exec = "\n".join(
    l for l in agg_no_doc.splitlines() if not l.strip().startswith("#")
)
need(
    not re.search(r"warehouse-[abc]\.(?:json|md)", agg_exec),
    "DAG violation: aggregate_warehouse.py references a specific sibling warehouse file in executable code",
)
# Positively assert the aggregate task is parametric (id + path via CLI args).
need(
    "warehouse_id" in agg_src and "md_path" in agg_src,
    "aggregate_warehouse.py is not parameterized by warehouse id + path",
)
# Consolidation must fan in on all three intermediates.
for w in WIDS:
    need(f"warehouse-{w}" in con_src or "WAREHOUSE_IDS" in con_src, f"consolidate.py does not load warehouse-{w}")
need("raise FileNotFoundError" in con_src, "consolidate.py does not require all intermediates to exist")

# 3. Each intermediate has total, per-item quantity, low-stock (<5, warehouse_row).
for w in WIDS:
    data = imm[w]
    for k in ("total", "items", "low_stock", "low_stock_basis"):
        need(k in data, f"warehouse-{w}: missing key {k}")
    need(data.get("low_stock_basis") == "warehouse_row", f"warehouse-{w}: low_stock_basis != warehouse_row")
    need(data["total"] == sum(data["items"].values()), f"warehouse-{w}: total != sum(items)")
    expected_low = sorted((i, q) for i, q in data["items"].items() if q < THRESHOLD)
    actual_low = sorted((e["item"], e["quantity"]) for e in data["low_stock"])
    need(expected_low == actual_low, f"warehouse-{w}: low_stock list wrong (exp {expected_low}, got {actual_low})")
    for e in data["low_stock"]:
        need(e["quantity"] < THRESHOLD, f"warehouse-{w}: low_stock entry {e} not <{THRESHOLD}")
        need(e.get("warehouse") == data["warehouse"], f"warehouse-{w}: low_stock entry missing/wrong warehouse")

# 4. result.json structure matches 출력형식.md keys.
spec_keys = {"source_files", "warehouse_totals", "item_totals", "grand_total", "low_stock_basis", "threshold", "low_stock"}
need(set(res) == spec_keys, f"result.json key mismatch: {set(res) ^ spec_keys}")
need(res.get("low_stock_basis") == "warehouse_row", "result.json low_stock_basis != warehouse_row")
need(res.get("threshold") == THRESHOLD, "result.json threshold != 5")

# Integers, not strings.
need(isinstance(res["grand_total"], int), "grand_total is not int")
need(all(isinstance(v, int) for v in res["warehouse_totals"].values()), "warehouse_totals has non-int")
need(all(isinstance(v, int) for v in res["item_totals"].values()), "item_totals has non-int")

# 5. result.json consistent with intermediates.
wt = {imm[w]["warehouse"]: imm[w]["total"] for w in WIDS}
need(res["warehouse_totals"] == wt, f"warehouse_totals mismatch: {res['warehouse_totals']} vs {wt}")
it = {}
for w in WIDS:
    for i, q in imm[w]["items"].items():
        it[i] = it.get(i, 0) + q
need(res["item_totals"] == it, f"item_totals mismatch: {res['item_totals']} vs {it}")
need(res["grand_total"] == sum(wt.values()), "grand_total != sum(warehouse_totals)")
ls_res = sorted((e["warehouse"], e["item"], e["quantity"]) for e in res["low_stock"])
ls_imm = sorted((e["warehouse"], e["item"], e["quantity"]) for w in WIDS for e in imm[w]["low_stock"])
need(ls_res == ls_imm, f"low_stock mismatch: {ls_res} vs {ls_imm}")

# 6. report.md consistent with result.json.
need(str(res["grand_total"]) in rep, "grand_total not in report.md")
for wh, t in res["warehouse_totals"].items():
    need(f"| {wh} | {t} |" in rep, f"warehouse total {wh}:{t} not in report.md")
for i, q in res["item_totals"].items():
    need(f"| {i} | {q} |" in rep, f"item total {i}:{q} not in report.md")
for e in res["low_stock"]:
    need(f"| {e['warehouse']} | {e['item']} | {e['quantity']} |" in rep, f"low_stock {e} not in report.md")
need("warehouse_row" in rep, "report.md does not state low_stock_basis warehouse_row")

if errs:
    print("FAILURES:")
    for e in errs:
        print("  -", e)
    sys.exit(1)
print("ALL CHECKS PASSED")
