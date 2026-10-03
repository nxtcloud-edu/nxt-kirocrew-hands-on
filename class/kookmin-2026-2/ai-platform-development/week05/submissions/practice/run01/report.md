# 창고 재고 집계 보고서

- 입력 파일: warehouse-a.md, warehouse-b.md, warehouse-c.md
- 저재고 기준(low_stock_basis): warehouse_row
- 저재고 임계값(threshold): 수량 < 5
- 전체 합계(grand_total): 54

## 창고별 합계

| 창고 | 합계 |
| --- | ---: |
| A | 22 |
| B | 16 |
| C | 16 |

## 품목별 총수량

| 품목 | 총수량 |
| --- | ---: |
| bottle | 12 |
| cable | 1 |
| hub | 13 |
| mug | 17 |
| sensor | 11 |

## 저재고 목록 (창고별 행 기준)

| 창고 | 품목 | 수량 |
| --- | --- | ---: |
| A | bottle | 3 |
| B | hub | 2 |
| C | cable | 1 |
| C | sensor | 4 |

