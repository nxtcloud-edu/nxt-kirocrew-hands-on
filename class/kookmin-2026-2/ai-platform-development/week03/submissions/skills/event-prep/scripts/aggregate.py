"""event-prep 집계 스크립트.

참가신청 CSV를 행사안내 규칙대로 집계해 항상 같은 JSON 구조로 저장한다.
숫자는 사람이 세면 실수가 나므로 이 스크립트가 정확히 담당한다.

사용법:
    python aggregate.py <참가신청.csv> <정원 또는 행사안내.md> [결과.json]

예시:
    python aggregate.py ../../mission/참가신청.csv 12 ../result.json
"""

import csv
import json
import re
import sys
from pathlib import Path

# CSV 열 이름 (참가신청.csv 기준)
COL_NO = "신청번호"
COL_NAME = "이름"
COL_STATUS = "참가 여부"
COL_SNACK = "간식 선택"

# 값 상수
JOIN = "참가"
SANDWICH = "샌드위치"
RICEBALL = "주먹밥"
NONE_SNACK = "받지 않음"


def read_capacity(arg: str) -> int:
    """정원 인자를 읽는다. 숫자면 그대로, 파일이면 '정원: 12명'에서 숫자를 뽑는다."""
    if arg.isdigit():
        return int(arg)
    path = Path(arg)
    if path.exists():
        text = path.read_text(encoding="utf-8")
        m = re.search(r"정원[:：]?\s*(\d+)", text)
        if m:
            return int(m.group(1))
    raise ValueError(f"정원을 확인할 수 없습니다: {arg}")


def aggregate(csv_path: Path, capacity: int) -> dict:
    """CSV를 규칙대로 집계해 결과 dict를 만든다."""
    snacks = {SANDWICH: 0, RICEBALL: 0, NONE_SNACK: 0}
    attendees = 0
    pending = []   # 참가자인데 간식 빈칸 → 확인 필요
    absentees = []  # 불참자

    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            status = (row.get(COL_STATUS) or "").strip()
            snack = (row.get(COL_SNACK) or "").strip()
            no = (row.get(COL_NO) or "").strip()
            name = (row.get(COL_NAME) or "").strip()

            if status != JOIN:
                # 불참: 간식 선택이 있어도 제외. 빈칸은 무시.
                absentees.append({"신청번호": no, "이름": name})
                continue

            # 여기부터는 참가자
            attendees += 1
            if snack == "":
                pending.append({"신청번호": no, "이름": name})
            elif snack in snacks:
                snacks[snack] += 1
            else:
                # 예상 밖의 값은 확인 대상으로 둔다
                pending.append({"신청번호": no, "이름": name})

    over = attendees > capacity

    prep = [
        f"참가 명단과 이름표 {attendees}명분",
        f"생수 {attendees}개",
        f"샌드위치 {snacks[SANDWICH]}개",
        f"주먹밥 {snacks[RICEBALL]}개",
        "사진용 노트북·HDMI 연결 확인",
        "테이블 배치와 행사 후 정리 담당 확인",
    ]
    if pending:
        names = ", ".join(f"{p['이름']}({p['신청번호']})" for p in pending)
        prep.insert(0, f"간식 미응답 {len(pending)}명 확인: {names}")
    if over:
        prep.insert(0, f"정원 초과({attendees}/{capacity}) — 추가 장소 확인")

    return {
        "정원": capacity,
        "참가_인원": attendees,
        "정원_초과": over,
        "간식_주문": {
            "샌드위치": snacks[SANDWICH],
            "주먹밥": snacks[RICEBALL],
            "받지_않음": snacks[NONE_SNACK],
        },
        "생수": attendees,
        "미응답_확인_필요": pending,
        "불참": absentees,
        "준비할_일": prep,
    }


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1

    csv_path = Path(sys.argv[1])
    if not csv_path.exists():
        print(f"CSV 파일을 찾을 수 없습니다: {csv_path}")
        return 1

    capacity = read_capacity(sys.argv[2])
    out_path = Path(sys.argv[3]) if len(sys.argv) > 3 else csv_path.with_name("집계결과.json")

    result = aggregate(csv_path, capacity)
    out_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # 화면에도 요약 출력
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n저장 완료: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
