#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""data-to-html: 문서 요약(JSON)과 CSV를 받아 하나의 HTML 리포트로 조립한다.

역할 분담:
  - AI가 여러 MD 문서를 읽고 요약을 만들어 요약 JSON으로 넘긴다(판단).
  - 이 스크립트가 요약 JSON을 검증하고 CSV를 파싱해 HTML을 조립한다(결정적 처리).

요약 JSON 스키마(고정):
  {
    "제목": "리포트 제목 문자열",
    "문서_요약": [
      {"문서명": "파일이름 또는 제목", "요약": "요약 문장"}
    ]
  }

CSV 핵심 표: CSV 헤더와 행을 그대로 표로 렌더한다.
  --max-rows 로 표에 넣을 행 수를 제한한다(기본 전체).
"""
import argparse
import csv
import html
import json
import sys
from datetime import datetime


REQUIRED_TOP = {"제목", "문서_요약"}
REQUIRED_DOC = {"문서명", "요약"}


def fail(msg):
    print(f"[data-to-html] 오류: {msg}", file=sys.stderr)
    sys.exit(1)


def load_summary(path):
    if path == "-":
        raw = sys.stdin.read()
    else:
        with open(path, "r", encoding="utf-8-sig") as f:
            raw = f.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        fail(f"요약 JSON 파싱 실패: {e}")

    if not isinstance(data, dict):
        fail("요약 JSON 최상위는 객체여야 한다.")
    keys = set(data.keys())
    if keys != REQUIRED_TOP:
        missing = REQUIRED_TOP - keys
        extra = keys - REQUIRED_TOP
        parts = []
        if missing:
            parts.append(f"누락: {sorted(missing)}")
        if extra:
            parts.append(f"불필요: {sorted(extra)}")
        fail("요약 JSON 최상위 키가 스키마와 다르다. " + ", ".join(parts))
    if not isinstance(data["제목"], str) or not data["제목"].strip():
        fail("'제목'은 비어있지 않은 문자열이어야 한다.")
    if not isinstance(data["문서_요약"], list) or not data["문서_요약"]:
        fail("'문서_요약'은 1개 이상의 항목을 가진 목록이어야 한다.")
    for i, doc in enumerate(data["문서_요약"]):
        if not isinstance(doc, dict) or set(doc.keys()) != REQUIRED_DOC:
            fail(f"문서_요약[{i}] 키는 {sorted(REQUIRED_DOC)} 이어야 한다.")
        for k in REQUIRED_DOC:
            if not isinstance(doc[k], str) or not doc[k].strip():
                fail(f"문서_요약[{i}]['{k}']는 비어있지 않은 문자열이어야 한다.")
    return data


def load_csv(path, max_rows):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        rows = [r for r in reader if any(c.strip() for c in r)]
    if not rows:
        fail("CSV에 데이터가 없다.")
    header = [c.strip() for c in rows[0]]
    body = [[c.strip() for c in r] for r in rows[1:]]
    if max_rows is not None and max_rows >= 0:
        body = body[:max_rows]
    return header, body


def esc(s):
    return html.escape(str(s), quote=True)


def render_html(summary, header, body, total_rows):
    docs = "".join(
        f"    <li><strong>{esc(d['문서명'])}</strong> — {esc(d['요약'])}</li>\n"
        for d in summary["문서_요약"]
    )
    thead = "".join(f"<th>{esc(h)}</th>" for h in header)
    trows = ""
    for r in body:
        cells = "".join(f"<td>{esc(c)}</td>" for c in r)
        trows += f"      <tr>{cells}</tr>\n"
    note = ""
    if len(body) < total_rows:
        note = (
            f'  <p class="note">표에는 {len(body)}행만 표시했습니다 '
            f'(전체 {total_rows}행).</p>\n'
        )
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(summary['제목'])}</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font-family: -apple-system, "Segoe UI", "Malgun Gothic", sans-serif;
         margin: 0 auto; max-width: 860px; padding: 2rem 1.25rem; line-height: 1.6; }}
  h1 {{ font-size: 1.6rem; margin-bottom: .25rem; }}
  h2 {{ font-size: 1.2rem; margin-top: 2rem; border-bottom: 2px solid #4457ff;
        padding-bottom: .3rem; }}
  ul {{ padding-left: 1.2rem; }}
  li {{ margin: .4rem 0; }}
  table {{ border-collapse: collapse; width: 100%; margin-top: .75rem; font-size: .95rem; }}
  th, td {{ border: 1px solid #ccc; padding: .5rem .6rem; text-align: left; }}
  th {{ background: #4457ff; color: #fff; }}
  tr:nth-child(even) td {{ background: rgba(68,87,255,.06); }}
  .meta {{ color: #888; font-size: .85rem; }}
  .note {{ color: #888; font-size: .85rem; }}
</style>
</head>
<body>
  <h1>{esc(summary['제목'])}</h1>
  <p class="meta">생성: {generated}</p>

  <h2>문서 요약</h2>
  <ul>
{docs}  </ul>

  <h2>CSV 핵심 표</h2>
  <table>
    <thead><tr>{thead}</tr></thead>
    <tbody>
{trows}    </tbody>
  </table>
{note}</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description="문서 요약 JSON + CSV → HTML 리포트")
    ap.add_argument("--summary", required=True,
                    help="요약 JSON 경로('-'면 표준입력)")
    ap.add_argument("--csv", required=True, help="핵심 표로 만들 CSV 경로")
    ap.add_argument("--out", help="HTML 저장 경로(생략 시 표준출력)")
    ap.add_argument("--max-rows", type=int, default=None,
                    help="표에 넣을 최대 행 수(기본 전체)")
    args = ap.parse_args()

    summary = load_summary(args.summary)
    header, body = load_csv(args.csv, args.max_rows)
    # total_rows: max-rows 적용 전 실제 행 수를 다시 세기 위해 재로드 없이 계산
    with open(args.csv, "r", encoding="utf-8-sig", newline="") as f:
        total_rows = sum(
            1 for i, r in enumerate(csv.reader(f))
            if i > 0 and any(c.strip() for c in r)
        )
    out_html = render_html(summary, header, body, total_rows)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out_html)
        print(f"[data-to-html] HTML 저장: {args.out} "
              f"(문서 {len(summary['문서_요약'])}건, 표 {len(body)}/{total_rows}행)")
    else:
        sys.stdout.write(out_html)


if __name__ == "__main__":
    main()
