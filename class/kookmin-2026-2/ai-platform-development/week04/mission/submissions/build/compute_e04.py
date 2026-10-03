#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""E04 빛담 가을사진전 운영 집계. week04/data CSV 3개를 전체 읽어 규칙대로 계산.

규칙 근거(week04/documents):
  - 구매 기본 인원 = 확정 인원 (CLUB-01 제1조). 대기/취소는 전환 시나리오로 별도.
  - 승인 정원 160명 (APPROVAL-SPACE-04). 홍보 180명은 미승인.
  - 회계 120건에 E01~E04 혼재. 기초잔액 지원금 0, 회비 800,000 (ACCOUNT-01 제1조).
  - 재원별 현재잔액 = 기초 + 수입 + 환불입금 - 지출 - 환불지급 (전체 거래, 제3조).
  - E04 재원별 순지출 = E04의 지출 + 환불지급 - 환불입금 (수입 제외, 제3조).
  - 구매계획: 참가자=확정×계수, 고정=계수. 예정비용=수량×단가. 회계에 합산 안 함 (제4·5조).

사용:
  py -3 compute_e04.py --apply 참가신청.csv --ledger 회계내역.csv --plan 구매계획.csv --out compute_result.json
"""
import csv, json, argparse
from collections import defaultdict

기초잔액 = {"학교지원금": 0, "동아리회비": 800_000}
승인정원 = 160
홍보정원 = 180
확대_시나리오 = 180  # 대기자 전환 검토 상한(홍보 정원)


def read_csv(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return [{(k or "").strip(): (v or "").strip() for k, v in r.items()}
                for r in csv.DictReader(f)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", required=True)
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    apply_rows = read_csv(a.apply)
    ledger_rows = read_csv(a.ledger)
    plan_rows = read_csv(a.plan)

    현황 = defaultdict(int)
    for r in apply_rows:
        if r["행사_ID"] == "E04":
            현황[r["신청상태"]] += 1
    현황 = dict(현황)
    확정 = 현황.get("확정", 0)
    대기 = 현황.get("대기", 0)

    인화_신청 = sum(1 for r in apply_rows
                  if r["행사_ID"] == "E04" and r["신청상태"] == "확정" and r["인화체험"] == "신청")
    식음료_신청 = sum(1 for r in apply_rows
                    if r["행사_ID"] == "E04" and r["신청상태"] == "확정" and r["식음료"] == "신청")

    유형들 = ["수입", "지출", "환불입금", "환불지급"]
    전체 = {k: {t: 0 for t in 유형들} for k in 기초잔액}
    e04 = {k: {t: 0 for t in 유형들} for k in 기초잔액}
    for r in ledger_rows:
        재원, 유형, 금액 = r["재원"], r["유형"], int(r["금액"])
        전체.setdefault(재원, {t: 0 for t in 유형들})
        e04.setdefault(재원, {t: 0 for t in 유형들})
        if 유형 in 유형들:
            전체[재원][유형] += 금액
            if r["행사_ID"] == "E04":
                e04[재원][유형] += 금액

    재원 = {}
    for name, v in 전체.items():
        기초 = 기초잔액.get(name, 0)
        현재잔액 = 기초 + v["수입"] + v["환불입금"] - v["지출"] - v["환불지급"]
        e = e04.get(name, {t: 0 for t in 유형들})
        재원[name] = {"기초잔액": 기초, **v, "현재잔액": 현재잔액,
                      "E04_지출": e["지출"], "E04_환불지급": e["환불지급"],
                      "E04_환불입금": e["환불입금"],
                      "E04_순지출": e["지출"] + e["환불지급"] - e["환불입금"]}

    def plan_cost(인원):
        재원별 = defaultdict(int)
        항목 = []
        for p in plan_rows:
            계수, 단가 = int(p["계수"]), int(p["단가"])
            수량 = 인원 * 계수 if p["수량기준"] == "참가자" else 계수
            비용 = 수량 * 단가
            재원별[p["예정재원"]] += 비용
            항목.append({"물품": p["물품"], "수량기준": p["수량기준"], "수량": 수량,
                        "단가": 단가, "예정비용": 비용, "재원": p["예정재원"], "용도": p.get("용도", "")})
        return dict(재원별), 항목

    기본_재원별, 기본_항목 = plan_cost(확정)
    확대_재원별, 확대_항목 = plan_cost(확대_시나리오)

    판정 = {}
    for name, info in 재원.items():
        잔액 = info["현재잔액"]
        판정[name] = {"현재잔액": 잔액,
                      "기본안_예정비용": 기본_재원별.get(name, 0),
                      "기본안_충분": 잔액 >= 기본_재원별.get(name, 0),
                      "확대안_예정비용": 확대_재원별.get(name, 0),
                      "확대안_충분": 잔액 >= 확대_재원별.get(name, 0)}

    result = {
        "행사": "E04 빛담 가을사진전과 인화 체험",
        "승인정원": 승인정원, "홍보정원": 홍보정원,
        "참가_현황": 현황, "구매_기본_인원_확정": 확정, "대기": 대기,
        "확대_시나리오_인원": 확대_시나리오,
        "인화체험_신청_확정자": 인화_신청, "식음료_신청_확정자": 식음료_신청,
        "재원": 재원,
        "구매계획_기본안": {"인원": 확정, "재원별_예정비용": 기본_재원별, "항목": 기본_항목},
        "구매계획_확대안": {"인원": 확대_시나리오, "재원별_예정비용": 확대_재원별, "항목": 확대_항목},
        "재원_판정": 판정,
        "회계_거래수": len(ledger_rows), "참가신청_건수": len(apply_rows),
    }
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"[compute] 확정={확정} 대기={대기} 취소={현황.get('취소',0)} → {a.out}")


if __name__ == "__main__":
    main()
