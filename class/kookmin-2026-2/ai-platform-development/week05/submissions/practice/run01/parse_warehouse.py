"""Shared parser for warehouse inventory markdown files.

Each warehouse file is a Markdown document containing one table:

    # 창고 X 재고

    | 품목 | 수량 |
    |---|---:|
    | mug | 12 |
    | bottle | 3 |

parse_warehouse(md_path) reads such a file and returns a list of
{"item": str, "quantity": int} rows. It tolerates a UTF-8 BOM and
silently skips malformed rows (header, separator, non-integer quantity,
wrong column count, blank lines).
"""

from __future__ import annotations

import re
from pathlib import Path


# A separator row looks like: |---|---:| (only -, :, |, spaces).
_SEPARATOR_RE = re.compile(r"^[\s|:\-]+$")


def parse_warehouse(md_path):
    """Parse a warehouse markdown file into a list of inventory rows.

    Args:
        md_path: path to the warehouse markdown file.

    Returns:
        list[dict]: rows of {"item": str, "quantity": int} in file order.
        Malformed rows are skipped.
    """
    path = Path(md_path)
    # utf-8-sig transparently strips a leading BOM if present.
    text = path.read_text(encoding="utf-8-sig")

    rows = []
    for line in text.splitlines():
        stripped = line.strip()
        # Only table rows are pipe-delimited.
        if not stripped.startswith("|"):
            continue
        # Skip the markdown separator row (|---|---:|).
        if _SEPARATOR_RE.match(stripped):
            continue

        # Split cells and drop the empty edges from leading/trailing pipes.
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) != 2:
            continue

        item, qty_raw = cells[0], cells[1]
        if not item:
            continue

        # Skip the header row and any non-integer quantity.
        try:
            quantity = int(qty_raw)
        except ValueError:
            continue

        rows.append({"item": item, "quantity": quantity})

    return rows


if __name__ == "__main__":
    import json
    import sys

    for arg in sys.argv[1:]:
        print(arg)
        print(json.dumps(parse_warehouse(arg), ensure_ascii=False, indent=2))
