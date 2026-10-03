"""창고별 집계 스크립트 (DAG의 독립 작업 노드).

parse_warehouse 를 사용해 인자로 받은 단일 창고(A/B/C)의
합계와 품목별 수량을 계산하고, 창고별 별도 중간 파일
(warehouse-a.json / warehouse-b.json / warehouse-c.json)을 저장한다.

CLI 인자로 창고 식별자·입력 경로·출력 경로를 받으므로
A·B·C 가 서로 의존하지 않고 독립적으로 실행될 수 있다.

사용 예:
    python aggregate_warehouse.py --warehouse A \
        --input ../../../practice/data/warehouse-a.md \
        --output warehouse-a.json

--input / --output 를 생략하면 창고 식별자로부터 기본 경로를 유도한다.
"""

from __future__ import annotations

import argparse
import json
import os

from parse_warehouse import parse_warehouse

# run02/ 기준 상대 위치. 이 스크립트가 있는 디렉터리를 기준으로 해석한다.
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# submissions/practice/run02 -> 프로젝트 루트로 3단계 상위
_PROJECT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, "..", "..", ".."))
_DATA_DIR = os.path.join(_PROJECT_ROOT, "practice", "data")


def default_input(warehouse: str) -> str:
    """창고 식별자로부터 기본 입력 md 경로를 유도한다."""
    return os.path.join(_DATA_DIR, f"warehouse-{warehouse.lower()}.md")


def default_output(warehouse: str) -> str:
    """창고 식별자로부터 기본 출력 json 경로(run02 아래)를 유도한다."""
    return os.path.join(_SCRIPT_DIR, f"warehouse-{warehouse.lower()}.json")


def aggregate(warehouse: str, input_path: str, output_path: str) -> dict:
    """단일 창고를 집계해 중간 결과 dict 를 만들고 output_path 에 저장한다.

    Returns:
        저장한 중간 결과 dict:
        {
          "warehouse": "A",
          "item_qty": {품목: 수량, ...},
          "total": 합계
        }
    """
    item_qty, total = parse_warehouse(input_path)

    result = {
        "warehouse": warehouse.upper(),
        "item_qty": item_qty,
        "total": total,
    }

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="단일 창고(A/B/C)의 합계·품목별 수량을 집계해 중간 파일로 저장한다."
    )
    parser.add_argument(
        "--warehouse",
        "-w",
        required=True,
        help="창고 식별자 (A / B / C)",
    )
    parser.add_argument(
        "--input",
        "-i",
        default=None,
        help="입력 warehouse md 경로 (생략 시 창고 식별자로 유도)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="출력 중간 json 경로 (생략 시 run02/warehouse-<x>.json)",
    )
    args = parser.parse_args()

    input_path = args.input or default_input(args.warehouse)
    output_path = args.output or default_output(args.warehouse)

    result = aggregate(args.warehouse, input_path, output_path)

    print(f"[warehouse {result['warehouse']}] total={result['total']}")
    print(f"  items: {result['item_qty']}")
    print(f"  saved: {output_path}")


if __name__ == "__main__":
    main()
