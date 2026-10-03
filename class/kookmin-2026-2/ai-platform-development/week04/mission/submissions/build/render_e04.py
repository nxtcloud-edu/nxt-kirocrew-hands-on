#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compute_result.json + summary.json → E04 운영 보고서 HTML.

data-to-html 스킬의 조립 단계를 E04 미션에 맞게 구성한 렌더러.
문서 요약(AI 판단)과 계산 결과(compute_e04.py)를 합쳐 HTML 한 파일로 만든다.

사용:
  py -3 render_e04.py --compute compute_result.json --summary summary.json --out W04_자료요약리포트.html
"""
import json, html, argparse
from datetime import datetime


def esc(s): return html.escape(str(s), quote=True)
def won(n): return f"{int(n):,}원"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--compute", required=True)
    ap.add_argument("--summary", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    with open(a.compute, encoding="utf-8-sig") as f: d = json.load(f)
    with open(a.summary, encoding="utf-8-sig") as f: s = json.load(f)

    현황, 확정, 재원, 판정 = d["참가_현황"], d["구매_기본_인원_확정"], d["재원"], d["재원_판정"]
    기본, 확대 = d["구매계획_기본안"], d["구매계획_확대안"]
    승인정원, 홍보정원 = d["승인정원"], d["홍보정원"]

    현황_rows = "".join(f"<tr><td>{esc(k)}</td><td class='num'>{v}명</td></tr>" for k, v in 현황.items())
    재원_rows = "".join(
        f"<tr><td>{esc(n)}</td><td class='num'>{won(v['기초잔액'])}</td><td class='num'>{won(v['수입'])}</td>"
        f"<td class='num'>{won(v['지출'])}</td><td class='num'>{won(v['환불입금'])}</td><td class='num'>{won(v['환불지급'])}</td>"
        f"<td class='num strong'>{won(v['현재잔액'])}</td><td class='num strong'>{won(v['E04_순지출'])}</td></tr>"
        for n, v in 재원.items())

    def plan_rows(scn):
        return "".join(
            f"<tr><td>{esc(i['물품'])}</td><td>{esc(i['수량기준'])}</td><td class='num'>{i['수량']}</td>"
            f"<td class='num'>{won(i['단가'])}</td><td class='num'>{won(i['예정비용'])}</td>"
            f"<td>{esc(i['재원'])}</td><td>{esc(i.get('용도',''))}</td></tr>"
            for i in scn["항목"])

    def chip(ok):
        return f"<span class='chip {'ok' if ok else 'warn'}'>{'충분' if ok else '부족 ⚠'}</span>"

    판정_rows = "".join(
        f"<tr><td>{esc(n)}</td><td class='num'>{won(v['현재잔액'])}</td><td class='num'>{won(v['기본안_예정비용'])}</td>"
        f"<td>{chip(v['기본안_충분'])}</td><td class='num'>{won(v['확대안_예정비용'])}</td><td>{chip(v['확대안_충분'])}</td></tr>"
        for n, v in 판정.items())

    ev = "".join(f"<li><strong>{esc(x['문서명'])}</strong> — {esc(x['요약'])}</li>" for x in s["문서_요약"])
    qa = "".join(f"<li><strong>{esc(x['질문'])}</strong><br>{esc(x['답변'])}</li>" for x in s.get("질문_답변", []))
    gen = datetime.now().strftime("%Y-%m-%d %H:%M")
    title = esc(s["제목"])

    doc = f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
 body {{ font-family:-apple-system,"Segoe UI","Malgun Gothic",sans-serif;max-width:960px;margin:0 auto;padding:2rem 1.25rem;line-height:1.6;color:#1a1a2e; }}
 h1 {{ font-size:1.7rem;margin-bottom:.2rem; }}
 h2 {{ font-size:1.2rem;margin-top:2.2rem;border-bottom:2px solid #4457ff;padding-bottom:.3rem; }}
 .meta {{ color:#888;font-size:.85rem; }}
 table {{ border-collapse:collapse;width:100%;margin-top:.6rem;font-size:.9rem; }}
 th,td {{ border:1px solid #d0d0e0;padding:.45rem .55rem;text-align:left; }}
 th {{ background:#4457ff;color:#fff; }}
 td.num {{ text-align:right;font-variant-numeric:tabular-nums; }}
 td.strong {{ font-weight:700; }}
 tr:nth-child(even) td {{ background:#f5f6ff; }}
 ul.ev li,ol.qa li {{ margin:.55rem 0; }}
 .chip {{ padding:.1rem .5rem;border-radius:1rem;font-size:.82rem;font-weight:600; }}
 .chip.ok {{ background:#e3f9e5;color:#1b7a2f; }}
 .chip.warn {{ background:#fdeaea;color:#c0392b; }}
 .callout {{ background:#fff8e1;border-left:4px solid #f0ad00;padding:.7rem 1rem;margin:.8rem 0;border-radius:4px; }}
 .kpi {{ display:flex;gap:1rem;flex-wrap:wrap;margin-top:.6rem; }}
 .kpi div {{ background:#eef0ff;border-radius:8px;padding:.6rem .9rem;min-width:120px; }}
 .kpi b {{ display:block;font-size:1.3rem;color:#2a35c0; }}
</style></head><body>
<h1>{title}</h1>
<p class="meta">생성 {gen} · 확정 참가자 {확정}명 기준 · 원본 CSV 전체 집계 (참가신청 {d['참가신청_건수']}건 / 회계내역 {d['회계_거래수']}건 E01~E04 혼재 / 구매계획 12개)</p>
<div class="kpi">
 <div>승인 정원<b>{승인정원}명</b><span class="meta">홍보 {홍보정원}명</span></div>
 <div>확정<b>{현황.get('확정',0)}명</b></div>
 <div>인화체험 신청<b>{d['인화체험_신청_확정자']}명</b><span class="meta">확정자 중</span></div>
 <div>식음료 신청<b>{d['식음료_신청_확정자']}명</b><span class="meta">확정자 중</span></div>
</div>

<h2>1. 참가 현황</h2>
<table><thead><tr><th>신청상태</th><th>인원</th></tr></thead><tbody>{현황_rows}</tbody></table>
<p>물품 구매의 기본 인원은 <strong>확정 참가자 {확정}명</strong>입니다(운영규칙 CLUB-01 제1조). 대기 {d['대기']}명은 전환 시나리오로 별도 계산하며 확정에 미리 더하지 않습니다.</p>
<div class="callout">장소 사용 승인서(APPROVAL-SPACE-04)의 <strong>승인 정원은 160명</strong>입니다. 행사안내의 홍보 정원 180명은 승인 조건과 다르며, 유효한 변경 승인서 발급 전까지 정원은 160명입니다.</div>

<h2>2. 재원별 현재 잔액과 E04 순지출</h2>
<table><thead><tr><th>재원</th><th>기초잔액</th><th>수입</th><th>지출</th><th>환불입금</th><th>환불지급</th><th>현재잔액(전체)</th><th>E04 순지출</th></tr></thead>
<tbody>{재원_rows}</tbody></table>
<p class="meta">현재잔액은 동아리 전체(E01~E04) 기준입니다. E04 순지출 = E04의 지출 + 환불지급 − 환불입금(수입 제외, 회계기준 제3조).</p>
<div class="callout">학교지원금 총 승인 한도는 1,500,000원이나 <strong>입금된 1차 1,000,000원만 반영</strong>됩니다(거래 T091). 잔여 500,000원은 정산 승인 후 지급 예정이라 현재 가용 현금에 더하지 않습니다(RULE-01 제5조, APPROVAL-FUND-04).</div>

<h2>3. 구매계획 — 기본안(확정 {확정}명)</h2>
<table><thead><tr><th>물품</th><th>수량기준</th><th>수량</th><th>단가</th><th>예정비용</th><th>재원</th><th>용도</th></tr></thead><tbody>{plan_rows(기본)}</tbody></table>
<p class="meta">구매계획.csv는 앞으로 필요한 수량 계산입니다. 회계 거래나 이미 지급된 비용에 합산하지 않습니다(회계기준 제4·5조).</p>

<h2>4. 구매계획 — 180명 확대(대기자 전환) 시나리오</h2>
<table><thead><tr><th>물품</th><th>수량기준</th><th>수량</th><th>단가</th><th>예정비용</th><th>재원</th><th>용도</th></tr></thead><tbody>{plan_rows(확대)}</tbody></table>

<h2>5. 재원별 잔액 대비 판정</h2>
<table><thead><tr><th>재원</th><th>현재잔액</th><th>기본안 비용</th><th>기본안</th><th>확대안 비용</th><th>확대안</th></tr></thead><tbody>{판정_rows}</tbody></table>

<h2>6. 판단 근거 (문서 요약)</h2>
<ul class="ev">{ev}</ul>

<h2>7. 보고서 질문에 대한 답</h2>
<ol class="qa">{qa}</ol>
</body></html>
"""
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"[render] saved {a.out}")


if __name__ == "__main__":
    main()
