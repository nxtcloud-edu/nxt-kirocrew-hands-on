# 창고 재고 집계 보고서

입력 파일: warehouse-a.json, warehouse-b.json, warehouse-c.json
전체 수량(grand_total): **54**

## 창고별 합계

| 창고 | 합계 |
| --- | ---: |
| A | 22 |
| B | 16 |
| C | 16 |

## 품목별 합계 (전체 창고 기준)

| 품목 | 총수량 |
| --- | ---: |
| bottle | 12 |
| cable | 1 |
| hub | 13 |
| mug | 17 |
| sensor | 11 |

## 저재고 목록

적용 기준: `low_stock_basis=item_total`, `threshold=5` (품목별 총수량 < 5 인 품목)

| 품목 | 총수량 |
| --- | ---: |
| cable | 1 |
