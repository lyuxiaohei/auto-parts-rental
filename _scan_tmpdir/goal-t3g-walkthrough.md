# 任务三g：租赁单编辑表单逐字段走查（2026-09-05）

- 页面：包装管理/租赁单列表.html → 首行「编辑」→ createModal 打开 ✅
- JS 错误：0 
- 字段总数：18；footer 按钮：取消 / 保存草稿 / 提交审核

| # | 区 | 字段 | 控件 | 预填值 | 走查结果 |
|---|---|---|---|---|---|
| 1 | form-row | 客户 | select | 一汽解放汽车有限公司 | 切换 OK（4 项：一汽解放汽车有限公司 / 上汽大众汽车有限公司宁波 / 小鹏汽车科技有限公司 / 东风本田汽车有限公司） |
| 2 | form-row | 所属项目 | select | PRJ-2601 一汽解放·长春 | 切换 OK（5 项：PRJ-2601 一汽解 / PRJ-2601 一汽解 / PRJ-2602 上汽大 / PRJ-2603 小鹏 / PRJ-2604 东风 |
| 3 | form-row | 起租日期 | input/text | 2026-09-05 | 聚焦+输入+还原 OK |
| 4 | form-row | 约定归还日期 | input/text | 2026-12-05 | 聚焦+输入+还原 OK |
| 5 | form-row | 押金(元) | input/text | 50,000.00 | 聚焦+输入+还原 OK |
| 6 | form-row | 备注 | input/text |  | 聚焦+输入+还原 OK |
| 7 | detail-tbl | 器具编码 | input/text | ZH-2601-A | 聚焦+输入+还原 OK |
| 8 | detail-tbl | 器具名称 | input/text | 驾驶室围板箱整箱套件 | 聚焦+输入+还原 OK |
| 9 | detail-tbl | 类型 | input/text | 组合单元 | 聚焦+输入+还原 OK |
| 10 | detail-tbl | 单位 | input/text | 套 | 聚焦+输入+还原 OK |
| 11 | detail-tbl | 数量 | input/text | 180 | 聚焦+输入+还原 OK |
| 12 | detail-tbl | 日租金(元) | input/text | 2.40 | 聚焦+输入+还原 OK |
| 13 | detail-tbl | 器具编码 | input/text | PLT-1210P | 聚焦+输入+还原 OK |
| 14 | detail-tbl | 器具名称 | input/text | 塑料托盘 1200×1000 | 聚焦+输入+还原 OK |
| 15 | detail-tbl | 类型 | input/text | 散件 | 聚焦+输入+还原 OK |
| 16 | detail-tbl | 单位 | input/text | 块 | 聚焦+输入+还原 OK |
| 17 | detail-tbl | 数量 | input/text | 180 | 聚焦+输入+还原 OK |
| 18 | detail-tbl | 日租金(元) | input/text | 0.15 | 聚焦+输入+还原 OK |

**结论：全部通过（聚焦/输入/还原三步 + select 逐项切换）**