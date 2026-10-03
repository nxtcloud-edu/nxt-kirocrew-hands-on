"""Per-warehouse aggregation task (DAG node).

Independent of the other warehouse tasks: it only depends on the shared
parser and its own input file. Given a warehouse id and its markdown
path, it computes for that warehouse:

  - total  : total quantity (sum of all row quantities)
  - items  : per-item quantity {item: quantity}
  - low_stock : rows whose quantity is < threshold (default 5),
                recorded with basis=warehouse_row so each entry carries
                its warehouse, item, and quantity.

The result is written to run01/warehouse-<id>.json (id lowercased).

Usage:
    python aggregate_warehouse.py <warehouse_id> <input_md_path> [--out-dir DIR] [--threshold N]

Example:
    python aggregate_warehouse.py A ../../../practice/data/warehouse-a.md
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from parse_warehouse import parse_warehouse

LOW_STOCK_THRESHOLD = 5
LOW_STOCK_BASIS = "warehouse_row"


def aggregate_warehouse(warehouse_id, md_path, threshold=LOW_STOCK_THRESHOLD):
    """Aggregate a single warehouse's inventory.

    Args:
        warehouse_id: warehouse label, e.g. "A".
        md_path: path to that warehouse's markdown file.
        threshold: low-stock upper bound; a row is low stock when its
            quantity is strictly less than this value.

    Returns:
        dict with keys: warehouse, source_file, threshold,
        low_stock_basis, total, items, low_stock.
    """
    warehouse = str(warehouse_id).strip().upper()
    rows = parse_warehouse(md_path)

    total = 0
    items = {}
    low_stock = []
    for row in rows:
        item = row["item"]
        qty = row["quantity"]
        total += qty
        # Same item may appear on multiple rows within a warehouse; sum them.
        items[item] = items.get(item, 0) + qty
        # Low stock is judged per original warehouse row (warehouse_row basis).
        if qty < threshold:
            low_stock.append(
                {"warehouse": warehouse, "item": item, "quantity": qty}
            )

    return {
        "warehouse": warehouse,
        "source_file": Path(md_path).name,
        "threshold": threshold,
        "low_stock_basis": LOW_STOCK_BASIS,
        "total": total,
        "items": items,
        "low_stock": low_stock,
    }


def main():
    parser = argparse.ArgumentParser(description="Aggregate one warehouse's inventory.")
    parser.add_argument("warehouse_id", help="Warehouse label, e.g. A")
    parser.add_argument("md_path", help="Path to the warehouse markdown file")
    parser.add_argument(
        "--out-dir",
        default=str(Path(__file__).resolve().parent),
        help="Directory to write warehouse-<id>.json into (default: this script's dir)",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=LOW_STOCK_THRESHOLD,
        help="Low-stock upper bound (quantity < threshold). Default 5.",
    )
    args = parser.parse_args()

    result = aggregate_warehouse(args.warehouse_id, args.md_path, args.threshold)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"warehouse-{result['warehouse'].lower()}.json"
    out_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
