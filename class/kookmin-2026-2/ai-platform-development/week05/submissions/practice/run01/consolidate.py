"""Consolidation task (DAG sink node).

Depends on all three per-warehouse intermediates being present:
run01/warehouse-a.json, warehouse-b.json, warehouse-c.json. It does NOT
read the raw markdown again -- it merges only the intermediate outputs,
so the A/B/C aggregation tasks stay independent and this task is the
single node that fans them back in.

It produces:
  - warehouse_totals : {warehouse: total}
  - item_totals      : {item: quantity summed across all warehouses}
  - grand_total      : sum of all quantities
  - low_stock        : combined per-warehouse-row low-stock list
                       (basis = warehouse_row), preserving each entry's
                       warehouse, item, and quantity.

Writes result.json (matching 출력형식.md) and report.md into run01/.

Usage:
    python consolidate.py [--in-dir DIR] [--out-dir DIR] [--threshold N]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

LOW_STOCK_THRESHOLD = 5
LOW_STOCK_BASIS = "warehouse_row"
WAREHOUSE_IDS = ("a", "b", "c")


def load_intermediate(in_dir, warehouse_id):
    """Load one warehouse-<id>.json intermediate.

    Raises FileNotFoundError if the intermediate is missing, since this
    task depends on all three being produced first.
    """
    path = Path(in_dir) / f"warehouse-{warehouse_id}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"missing intermediate {path.name}; run aggregate_warehouse.py "
            f"for warehouse {warehouse_id.upper()} first"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def consolidate(in_dir, threshold=LOW_STOCK_THRESHOLD):
    """Merge the three warehouse intermediates into a combined result.

    Args:
        in_dir: directory holding warehouse-a/b/c.json.
        threshold: low-stock upper bound, carried into result.json. The
            intermediates already applied it per row; we surface the same
            value and re-assert it as a guard.

    Returns:
        dict matching the 출력형식.md structure.
    """
    intermediates = [load_intermediate(in_dir, wid) for wid in WAREHOUSE_IDS]

    source_files = []
    warehouse_totals = {}
    item_totals = {}
    grand_total = 0
    low_stock = []

    for data in intermediates:
        warehouse = data["warehouse"]
        source_files.append(data["source_file"])
        warehouse_totals[warehouse] = data["total"]
        grand_total += data["total"]

        for item, qty in data["items"].items():
            item_totals[item] = item_totals.get(item, 0) + qty

        # Combined low-stock keeps the warehouse_row basis: each entry
        # is an original warehouse row with quantity < threshold.
        for entry in data["low_stock"]:
            # Guard against an intermediate produced with a different threshold.
            if entry["quantity"] < threshold:
                low_stock.append(
                    {
                        "warehouse": entry["warehouse"],
                        "item": entry["item"],
                        "quantity": entry["quantity"],
                    }
                )

    # Stable, readable ordering.
    low_stock.sort(key=lambda e: (e["warehouse"], e["item"]))

    return {
        "source_files": source_files,
        "warehouse_totals": warehouse_totals,
        "item_totals": item_totals,
        "grand_total": grand_total,
        "low_stock_basis": LOW_STOCK_BASIS,
        "threshold": threshold,
        "low_stock": low_stock,
    }


def build_report(result):
    """Render a short Markdown report consistent with result.json."""
    lines = []
    lines.append("# 창고 재고 집계 보고서")
    lines.append("")
    lines.append(f"- 입력 파일: {', '.join(result['source_files'])}")
    lines.append(f"- 저재고 기준(low_stock_basis): {result['low_stock_basis']}")
    lines.append(f"- 저재고 임계값(threshold): 수량 < {result['threshold']}")
    lines.append(f"- 전체 합계(grand_total): {result['grand_total']}")
    lines.append("")

    lines.append("## 창고별 합계")
    lines.append("")
    lines.append("| 창고 | 합계 |")
    lines.append("| --- | ---: |")
    for warehouse, total in result["warehouse_totals"].items():
        lines.append(f"| {warehouse} | {total} |")
    lines.append("")

    lines.append("## 품목별 총수량")
    lines.append("")
    lines.append("| 품목 | 총수량 |")
    lines.append("| --- | ---: |")
    for item, qty in sorted(result["item_totals"].items()):
        lines.append(f"| {item} | {qty} |")
    lines.append("")

    lines.append("## 저재고 목록 (창고별 행 기준)")
    lines.append("")
    if result["low_stock"]:
        lines.append("| 창고 | 품목 | 수량 |")
        lines.append("| --- | --- | ---: |")
        for entry in result["low_stock"]:
            lines.append(
                f"| {entry['warehouse']} | {entry['item']} | {entry['quantity']} |"
            )
    else:
        lines.append("저재고 항목 없음.")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Consolidate warehouse intermediates into result.json + report.md."
    )
    here = Path(__file__).resolve().parent
    parser.add_argument(
        "--in-dir",
        default=str(here),
        help="Directory holding warehouse-a/b/c.json (default: this script's dir)",
    )
    parser.add_argument(
        "--out-dir",
        default=str(here),
        help="Directory to write result.json + report.md (default: this script's dir)",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=LOW_STOCK_THRESHOLD,
        help="Low-stock upper bound (quantity < threshold). Default 5.",
    )
    args = parser.parse_args()

    result = consolidate(args.in_dir, args.threshold)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    result_path = out_dir / "result.json"
    result_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    report_path = out_dir / "report.md"
    report_path.write_text(build_report(result) + "\n", encoding="utf-8")

    print(f"wrote {result_path}")
    print(f"wrote {report_path}")


if __name__ == "__main__":
    main()
