"""통합 스크립트 (DAG 의 통합 작업 노드).

세 창고 중간 파일(warehouse-a.json / warehouse-b.json / warehouse-c.json)을
읽어 전체 창고 기준 품목별 총수량(item_total)을 계산하고, item_total < 5 인
품목을 저재고(low_stock)로 판정한다.

메타 필드는 low_stock_basis="item_total", threshold=5 로 기록한다.
결과는 practice/출력형식.md 형식에 맞춰 result.json 으로 run02 아래에 저장한다.

이 작업은 세 창고 집계(aggregate_warehouse.py 로 만든 중간 파일) 모두에
의존한다 — 세 파일이 준비된 뒤에 실행해야 한다.

사용 예:
    python consolidate.py
    python consolidate.py --output result.json
"""

from __future__ import annotations

import argparse
import json
import os

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 통합 대상 창고와 중간 파일 이름.
_WAREHOUSES = ("A", "B", "C")
_THRESHOLD = 5
_LOW_STOCK_BASIS = "item_total"


def intermediate_path(warehouse: str) -> str:
    """창고 식별자로부터 중간 파일(run02 아래) 경로를 유도한다."""
    return os.path.join(_SCRIPT_DIR, f"warehouse-{warehouse.lower()}.json")


def load_intermediate(path: str) -> dict:
    """창고 중간 파일을 읽어 검증 후 dict 로 반환한다."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"중간 파일이 없습니다: {path} — 먼저 aggregate_warehouse.py 로 생성하세요."
        )
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for key in ("warehouse", "item_qty", "total"):
        if key not in data:
            raise ValueError(f"중간 파일 스키마 오류: '{key}' 누락 ({path})")
    return data


def consolidate() -> dict:
    """세 창고 중간 파일을 합쳐 result 구조를 만든다.

    Returns:
        practice/출력형식.md 형식을 따르는 result dict.
    """
    source_files: list[str] = []
    warehouse_totals: dict[str, int] = {}
    item_totals: dict[str, int] = {}

    for wh in _WAREHOUSES:
        path = intermediate_path(wh)
        data = load_intermediate(path)

        name = data["warehouse"]
        source_files.append(os.path.basename(path))

        # 창고별 합계는 원본 md 로부터 파싱된 정수 합계를 그대로 사용한다.
        warehouse_totals[name] = int(data["total"])

        # 품목별 총수량을 세 창고에 걸쳐 누적한다.
        for item, qty in data["item_qty"].items():
            item_totals[item] = item_totals.get(item, 0) + int(qty)

    grand_total = sum(item_totals.values())

    # 저재고: 전체 창고 기준 item_total < threshold 인 품목.
    low_stock = [
        {"item": item, "quantity": qty}
        for item, qty in sorted(item_totals.items())
        if qty < _THRESHOLD
    ]

    result = {
        "source_files": source_files,
        "warehouse_totals": warehouse_totals,
        "item_totals": item_totals,
        "grand_total": grand_total,
        "low_stock_basis": _LOW_STOCK_BASIS,
        "threshold": _THRESHOLD,
        "low_stock": low_stock,
    }
    return result


def build_report(result: dict) -> str:
    """result dict 로부터 짧은 Markdown 보고서(report.md) 문자열을 만든다.

    practice/출력형식.md 요구대로 창고별 합계, 품목별 합계, 저재고 목록과
    적용 기준(low_stock_basis, threshold)을 포함한다. 표의 모든 수치는
    result.json 값과 그대로 대조된다.
    """
    lines: list[str] = []
    lines.append("# 창고 재고 집계 보고서")
    lines.append("")
    lines.append(
        f"입력 파일: {', '.join(result['source_files'])}"
    )
    lines.append(f"전체 수량(grand_total): **{result['grand_total']}**")
    lines.append("")

    # 창고별 합계
    lines.append("## 창고별 합계")
    lines.append("")
    lines.append("| 창고 | 합계 |")
    lines.append("| --- | ---: |")
    for name, total in result["warehouse_totals"].items():
        lines.append(f"| {name} | {total} |")
    lines.append("")

    # 품목별 합계 (전체 창고 기준)
    lines.append("## 품목별 합계 (전체 창고 기준)")
    lines.append("")
    lines.append("| 품목 | 총수량 |")
    lines.append("| --- | ---: |")
    for item, qty in sorted(result["item_totals"].items()):
        lines.append(f"| {item} | {qty} |")
    lines.append("")

    # 저재고 목록
    lines.append("## 저재고 목록")
    lines.append("")
    lines.append(
        f"적용 기준: `low_stock_basis={result['low_stock_basis']}`, "
        f"`threshold={result['threshold']}` "
        f"(품목별 총수량 < {result['threshold']} 인 품목)"
    )
    lines.append("")
    if result["low_stock"]:
        lines.append("| 품목 | 총수량 |")
        lines.append("| --- | ---: |")
        for row in result["low_stock"]:
            lines.append(f"| {row['item']} | {row['quantity']} |")
    else:
        lines.append("저재고 품목이 없습니다.")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="세 창고 중간 파일을 통합해 result.json 을 생성한다."
    )
    parser.add_argument(
        "--output",
        "-o",
        default=os.path.join(_SCRIPT_DIR, "result.json"),
        help="출력 result.json 경로 (기본: run02/result.json)",
    )
    parser.add_argument(
        "--report",
        "-r",
        default=os.path.join(_SCRIPT_DIR, "report.md"),
        help="출력 report.md 경로 (기본: run02/report.md)",
    )
    args = parser.parse_args()

    result = consolidate()

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    report = build_report(result)
    os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"[consolidate] grand_total={result['grand_total']}")
    print(f"  warehouse_totals: {result['warehouse_totals']}")
    print(f"  item_totals: {result['item_totals']}")
    print(f"  low_stock (< {result['threshold']}): {result['low_stock']}")
    print(f"  saved: {args.output}")
    print(f"  saved: {args.report}")


if __name__ == "__main__":
    main()
