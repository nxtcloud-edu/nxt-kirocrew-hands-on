# WEEK 04 산출물 — 자료 요약 HTML (E04 빛담 가을사진전)

`data-to-html` 스킬을 적용해 `week04/documents`(문서 8개) + `week04/data`(CSV 3개:
참가신청 200건 / 회계내역 120건 / 구매계획 12개)를 요약·집계한 운영 보고서입니다.
week04 관련 모든 산출물을 이 `submissions/` 폴더에 모았습니다.

## 파일 구성

- `W04_자료요약리포트.html` — 최종 결과물. 브라우저로 열어 확인.
- `data-to-html-skill/` — 사용한 스킬의 사본
  - `SKILL.md` — 스킬 정의(입출력, 요약 JSON 스키마, 실행 절차)
  - `scripts/build_html.py` — 범용 조립기(요약 JSON 검증 + CSV 표 렌더)
  - `scripts/_sample_summary.json` — 동작 확인용 예시
- `build/` — 이 리포트 생성에 사용한 산출물(재현용)
  - `compute_e04.py` — 원본 CSV 3개를 규칙대로 집계(참가 현황·재원 잔액·E04 순지출·구매계획)
  - `summary.json` — 문서 8개 요약 + 보고서 질문 답변(AI 판단 결과)
  - `render_e04.py` — 계산 결과 + 요약을 HTML로 조립
  - `compute_result.json` — compute_e04.py의 집계 결과(중간 산출물)

## 재현 방법 (Windows PowerShell)

```powershell
$data  = "..\..\..\week04\data"   # 원본 CSV 폴더
$sub   = "."                       # 이 submissions 폴더
py -3 build\compute_e04.py --apply "$data\참가신청.csv" --ledger "$data\회계내역.csv" `
    --plan "$data\구매계획.csv" --out build\compute_result.json
py -3 build\render_e04.py --compute build\compute_result.json --summary build\summary.json `
    --out W04_자료요약리포트.html
```

## 핵심 집계 결과 (원본 대조 검증됨)

- 참가: 확정 140 / 대기 40 / 취소 20 (구매 기본 인원 = 확정 140)
- 승인 정원 160명 (홍보 180명은 미승인 — 장소 변경 승인서 필요)
- 재원 현재잔액(E01~E04 전체): 학교지원금 250,000원, 동아리회비 1,843,000원
- E04 순지출: 지원금 750,000원, 회비 146,000원
- 구매계획 기본안(140): 지원금 256,000원(잔액 250,000 → 6,000원 부족), 회비 204,000원(충분)
- 확대안(180): 지원금 312,000원(부족), 회비 248,000원(충분)

> 모든 규정·행사·거래는 수업용 가상 자료입니다. 원본 문서와 CSV는 변경하지 않았습니다.
