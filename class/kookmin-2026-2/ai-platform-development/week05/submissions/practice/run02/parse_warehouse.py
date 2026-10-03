"""공유 파서 모듈.

warehouse-*.md (마크다운 표) 를 코드로 파싱해
{품목: 수량} 딕셔너리와 창고 합계를 반환하는 순수 함수를 제공한다.

md 행 형식 (step 1 확정):
    # 창고 X 재고
    | 품목 | 수량 |
    |---|---:|
    | mug | 12 |
    ...

- 헤더 행(품목/수량)과 구분선 행(--- 등)은 건너뛴다.
- 수량이 정수가 아니거나 셀 개수가 맞지 않는 알 수 없는/빈 행도 건너뛴다.
"""

from __future__ import annotations


def _split_row(line: str) -> list[str]:
    """마크다운 표 한 행을 셀 목록으로 분리한다. 표 행이 아니면 빈 목록."""
    s = line.strip()
    if not s.startswith("|"):
        return []
    # 양끝 파이프 제거 후 분리
    parts = s.strip("|").split("|")
    return [p.strip() for p in parts]


def _is_separator(cells: list[str]) -> bool:
    """구분선 행( |---|---:| 등 ) 인지 판정."""
    if not cells:
        return False
    for c in cells:
        stripped = c.replace(":", "").replace("-", "")
        if stripped != "" or "-" not in c:
            return False
    return True


def parse_warehouse(path: str) -> tuple[dict[str, int], int]:
    """warehouse md 파일을 파싱한다.

    Returns:
        (item_qty, total)
        item_qty: {품목명: 수량(int)} — 등장 순서 유지
        total: 창고 전체 수량 합계(int)

    알 수 없는/빈 행, 헤더 행, 구분선 행은 건너뛴다.
    """
    item_qty: dict[str, int] = {}

    with open(path, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    for line in lines:
        cells = _split_row(line)
        if len(cells) != 2:
            # 표 행이 아니거나 셀 개수 불일치 → 건너뛴다
            continue
        if _is_separator(cells):
            continue

        name, qty_str = cells[0], cells[1]
        if not name:
            continue
        # 헤더 행 (품목/수량 라벨) 건너뛰기: 수량이 정수가 아니면 스킵
        try:
            qty = int(qty_str)
        except ValueError:
            continue

        # 동일 품목이 여러 번 나오면 합산
        item_qty[name] = item_qty.get(name, 0) + qty

    total = sum(item_qty.values())
    return item_qty, total


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("usage: python parse_warehouse.py <warehouse.md>")
        sys.exit(1)
    items, tot = parse_warehouse(sys.argv[1])
    print("items:", items)
    print("total:", tot)
