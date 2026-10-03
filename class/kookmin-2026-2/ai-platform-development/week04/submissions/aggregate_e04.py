# -*- coding: utf-8 -*-
"""
빛담 가을사진전(E04) 회계·참가·구매계획 집계 스크립트
근거 문서/조항:
  ACCOUNT-01  회계 집계 기준 및 잔액 산정 규정
    제1조 기간/기초잔액(지원금 0, 회비 800,000), 제2조 부호(수입/환불입금 +, 지출/환불지급 -),
    제3조 현재잔액 및 E04 순지출(순지출=지출+환불지급-환불입금, 수입 제외),
    제4조 판단(구매계획은 회계에 합산하지 않음), 제5조 구매계획(참가자=확정인원*계수, 고정=계수)
  CLUB-01     운영 규칙
    제1조 구매 기본인원=확정인원, 제3조 대기자는 확정에 미리 더하지 않음
  APPROVAL-FUND-04  지원금 승인서 (한도 1,500,000 / 1차 1,000,000=T091 / 잔여 500,000 미가용)
  MEMO-04     승인 정원 160명(180명 미승인), NOTICE-04 홍보 180명
원본 CSV는 읽기 전용. 결과는 aggregate_result.json 으로 저장.
"""
import csv, json, io, os
from collections import defaultdict

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUT_PATH = os.path.join(os.path.dirname(__file__), "aggregate_result.json")

EVENT = "E04"

def read_csv(name):
    path = os.path.join(DATA_DIR, name)
    with io.open(path, "r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    return rows, path

def main():
    apply_rows, apply_path = read_csv("참가신청.csv")
    acct_rows, acct_path = read_csv("회계내역.csv")
    plan_rows, plan_path = read_csv("구매계획.csv")

    read_counts = {
        "참가신청.csv": len(apply_rows),
        "회계내역.csv": len(acct_rows),
        "구매계획.csv": len(plan_rows),
    }

    # ---- 1) 참가 상태별 인원 (E04만) ----
    e04_apply = [r for r in apply_rows if r["행사_ID"] == EVENT]
    status_counts = defaultdict(int)
    for r in e04_apply:
        status_counts[r["신청상태"]] += 1

    confirmed = [r for r in e04_apply if r["신청상태"] == "확정"]
    n_confirmed = len(confirmed)  # CLUB-01 제1조: 구매 기본인원 = 확정인원

    # ---- 2) 확정자의 선택 (인화체험/식음료) ----
    def count_choice(col, value):
        return sum(1 for r in confirmed if r.get(col) == value)
    choices = {
        "인화체험_신청": count_choice("인화체험", "신청"),
        "인화체험_미신청": count_choice("인화체험", "미신청"),
        "식음료_신청": count_choice("식음료", "신청"),
        "식음료_받지않음": count_choice("식음료", "받지않음"),
    }

    # ---- 3) 재원별 현재 잔액 (ACCOUNT-01 제1~3조, 전체 E01~E04) ----
    base = {"학교지원금": 0, "동아리회비": 800000}  # 제1조 기초잔액
    bal = dict(base)
    for r in acct_rows:
        fund = r["재원"]
        if fund not in bal:
            bal[fund] = 0
        amt = int(r["금액"])
        t = r["유형"]
        if t in ("수입", "환불입금"):
            bal[fund] += amt
        elif t in ("지출", "환불지급"):
            bal[fund] -= amt
        else:
            # 알 수 없는 유형은 확인 필요로 남김
            pass
    # 유형 종류 수집 (검증용)
    seen_types = sorted({r["유형"] for r in acct_rows})

    # ---- 4) E04 순지출 (ACCOUNT-01 제3조: 지출+환불지급-환불입금, 수입 제외) ----
    e04_acct = [r for r in acct_rows if r["행사_ID"] == EVENT]
    net_spend = defaultdict(int)
    for r in e04_acct:
        fund = r["재원"]
        amt = int(r["금액"])
        t = r["유형"]
        if t == "지출":
            net_spend[fund] += amt
        elif t == "환불지급":
            net_spend[fund] += amt
        elif t == "환불입금":
            net_spend[fund] -= amt
        # 수입은 순지출 계산에서 제외

    # ---- 5) 구매계획: 140/160/180명 시나리오 (ACCOUNT-01 제5조) ----
    #   참가자 기준 = 인원 * 계수 * 단가, 고정 = 계수 * 단가
    #   140=확정, 160=승인정원(MEMO-04), 180=홍보정원(NOTICE-04, 미승인)
    scenarios = {"140_확정": n_confirmed, "160_승인정원": 160, "180_홍보정원_미승인": 180}
    plan_result = {}
    for label, headcount in scenarios.items():
        by_fund = defaultdict(int)
        for p in plan_rows:
            basis = p["수량기준"]
            k = int(p["계수"])
            price = int(p["단가"])
            fund = p["예정재원"]
            if basis == "참가자":
                qty = headcount * k
            elif basis == "고정":
                qty = k
            else:
                qty = 0  # 알 수 없는 기준 -> 확인 필요
            by_fund[fund] += qty * price
        plan_result[label] = dict(by_fund)

    # ---- 지원금 가용 현금 (APPROVAL-FUND-04): 잔여 500,000은 미가용 ----
    # 지원금 현재잔액(bal)은 실제 입금 기준. 가용 = 현재잔액 그대로 사용(잔여 미지급분은 애초에 미반영).
    fund_note = {
        "1차지급": 1000000,
        "1차지급_거래ID": "T091",
        "잔여_미가용": 500000,
        "총승인한도": 1500000,
        "기념품_지원제외": "APPROVAL-FUND-04 / RULE-01",
    }

    # 구매계획 vs 잔액 판정
    def verdict(label):
        need = plan_result[label]
        need_fund = need.get("학교지원금", 0)
        need_fee = need.get("동아리회비", 0)
        return {
            "지원금_필요": need_fund,
            "지원금_잔액": bal.get("학교지원금", 0),
            "지원금_충분": bal.get("학교지원금", 0) >= need_fund,
            "회비_필요": need_fee,
            "회비_잔액": bal.get("동아리회비", 0),
            "회비_충분": bal.get("동아리회비", 0) >= need_fee,
        }
    plan_verdict = {label: verdict(label) for label in scenarios}

    result = {
        "행사": EVENT,
        "읽은_행수": read_counts,
        "원본경로": {
            "참가신청": os.path.abspath(apply_path),
            "회계내역": os.path.abspath(acct_path),
            "구매계획": os.path.abspath(plan_path),
        },
        "참가_상태별_인원": dict(status_counts),
        "확정_인원": n_confirmed,
        "확정자_선택": choices,
        "재원별_현재잔액": bal,
        "회계_유형종류": seen_types,
        "E04_순지출": dict(net_spend),
        "구매계획_시나리오": plan_result,
        "구매계획_판정": plan_verdict,
        "지원금_승인정보": fund_note,
        "정원_대조": {
            "승인정원": 160, "근거": "MEMO-04",
            "홍보정원": 180, "홍보근거": "NOTICE-04(홍보용, 승인서 아님)",
            "차이": 20, "180_상태": "미승인",
        },
        "확인필요": [],
    }

    # 검증: 알 수 없는 유형/기준이 있었는지
    known_types = {"수입", "환불입금", "지출", "환불지급"}
    unknown_types = [t for t in seen_types if t not in known_types]
    if unknown_types:
        result["확인필요"].append("알수없는_회계유형:" + ",".join(unknown_types))
    known_basis = {"참가자", "고정"}
    unknown_basis = sorted({p["수량기준"] for p in plan_rows if p["수량기준"] not in known_basis})
    if unknown_basis:
        result["확인필요"].append("알수없는_수량기준:" + ",".join(unknown_basis))
    # 외부인 참가: MEMO-04 미결정
    result["확인필요"].append("외부인_참가조건: MEMO-04에서 미결정(확인 필요)")

    with io.open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
