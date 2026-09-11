# -*- coding: utf-8 -*-
"""G16a：A06 第 5 节拆分（方案 A：1 底图 + 4 流程线）+ 同名 HTML 渲染版（内嵌 mermaid 自包含）
道远 2026-09-11 拍板：A + html 要
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROT = ROOT / 'P3-R01-包装租赁管理后台原型'
MM = (ROOT / '_scan_tmpdir/mermaid.min.js').read_text(encoding='utf-8')

GRAY = 'classDef gray fill:#f5f5f5,stroke:#bfbfbf,stroke-dasharray:4 3,color:#8c8c8c;'

# ---------- 7 张图（md 与 HTML 共用） ----------
D = {}
D['d51'] = ('5.1 主档与仓储底图', '全站静态结构：主档域 + 仓储库存域。系统域（roles/users/opLogs/todoItems/dictItems）与履历视图（rentTracks/assetTracks/projectDocs/boardRows/profitRows）不入图，见第 1 节分域清单。',
f'''flowchart LR
  subgraph MASTER["主档域"]
    PROJECTS["projects·项目档案 (8)"]
    PARTNERS["partners·客商 (8)"]
    PRODUCTS["products·物料档案 (12)"]
    BOMLIST["bomList·BOM (6)"]
    BOMVER["bomVersions·BOM版本 (3)"]
  end
  subgraph WH["仓储域"]
    LOCATIONS["locations·库位档案 (11)"]
    STOCK["stockFlows·库存查询 (16)"]
    STK["stocktakes·盘点记录 (5)"]
    OIN["otherInbounds·其他入库 (3)"]
    OOUT["otherOutbounds·其他出库 (5)"]
    TRF["transfers·库存调拨 (3)"]
  end
  PROJECTS <-."M:N 上下游绑定（未落数据层·缺口#4）".-> PARTNERS
  PARTNERS -->|"供应商维护（名字外键·缺口#3）"| PRODUCTS
  BOMLIST -->|"父项⇄子项 自引用"| BOMLIST
  BOMVER -->|"版本挂父项 ZH-（3/3）"| BOMLIST
  LOCATIONS -->|"客户虚拟仓 XNC-（4 行）"| STOCK
  STK -->|"盘盈生成（PD-）"| OIN
  STK -->|"盘亏生成（PD-）"| OOUT
  {GRAY}
  class PROJECTS,PARTNERS anchor;
''')
D['d52'] = ('5.2 销售线', '销售订单 → 出库 → 应收 → 收款/开票/核销。灰节点=跨图复现（真身见 5.1 / 5.5）。',
f'''flowchart LR
  SO["salesOrders·销售订单 (8)"]
  XSC["salesOutbounds·销售出库 (6)"]
  AR["receivableBills·应收账单 (14)"]
  RC["receipts·回款登记 (5)"]
  IV["invoices·开票登记 (6)"]
  WO["writeoffs·水单核销 (4)"]
  ZL0["leaseOrders·租赁单"]
  PO0["purchaseOrders·采购订单"]
  PG["projects〔复现〕"]
  CUG["partners·客户〔复现〕"]
  SO -->|"出库（6/6 含 SO-）"| XSC
  XSC -->|"销售费应收（XSCK-·3 行）"| AR
  AR -->|"收款分期（AR-）"| RC
  AR -->|"开票（AR-·6/6）"| IV
  AR <-."核销冲抵（3 行 AR-）".-> WO
  SO -. "代下租赁（流程口径·无外键）" .-> ZL0
  SO -. "联动采购（2 行 SO-）" .-> PO0
  PG -. "所属项目（8/8）" .- SO
  CUG -. "客户（名字外键）" .- SO
  {GRAY}
  class ZL0,PO0,PG,CUG gray;
''')
D['d53'] = ('5.3 租赁线（租出）', '租赁单 → 租赁出库 / 退租入库 + 客户转租（与租入线 M:N）。灰节点=跨图复现。',
f'''flowchart LR
  ZL["leaseOrders·租赁单 (9)"]
  ZUC["comboOutbounds·租赁出库/组合出库 (8)"]
  TUI["returnInbounds·退租入库 (8)"]
  RT["rentTracks·出租履历 (10)"]
  AT["assetTracks·资产轨迹 (10)"]
  AR0["receivableBills·应收账单〔复现〕"]
  RZD0["rentInOrders·租入单〔复现〕"]
  PG["projects〔复现〕"]
  CUG["partners·客户〔复现〕"]
  ZL -->|"租赁出库（8/8 ZL-）"| ZUC
  ZL -->|"退租入库（8/8 TZRK→ZL-）"| TUI
  ZUC -->|"租赁费应收（7 行）"| AR0
  ZL <-."客户转租（XNC-ZZ 3 行）".-> RZD0
  RT -. "履历视图聚合" .-> ZL
  AT -. "资产轨迹视图" .-> ZL
  PG -. "所属项目（9/9）" .- ZL
  CUG -. "客户（名字外键）" .- ZL
  {GRAY}
  class AR0,RZD0,PG,CUG gray;
''')
D['d54'] = ('5.4 租入线', '租入单 → 入库 / 归还 → 应付 → 付款。灰节点=跨图复现。',
f'''flowchart LR
  RZD["rentInOrders·租入单 (6)"]
  ZR["rentInbounds·租入入库 (3)"]
  GH["rentInReturns·租入归还 (3)"]
  AP["payableBills·应付账单 (11)"]
  PM["payments·付款登记 (5)"]
  ZL0["leaseOrders·租赁单〔复现〕"]
  SG["partners·供应商（路凯）〔复现〕"]
  RZD -->|"租入入库（3/3 RZD-）"| ZR
  RZD -->|"租入归还（3/3 RZD-·明细同步分批）"| GH
  RZD -->|"租金应付（2 行 RZD-）"| AP
  GH -->|"赔付应付"| AP
  AP -->|"付款分期（5/5 AP-·自由笔数）"| PM
  RZD -. "转租出（2 行 ZL-）" .-> ZL0
  SG -. "供应商（名字外键）" .- RZD
  {GRAY}
  class ZL0,SG gray;
''')
D['d55'] = ('5.5 采购线', '采购订单 → 采购入库 → 应付 → 付款（尾段复现 5.4）。灰节点=跨图复现。',
f'''flowchart LR
  PO["purchaseOrders·采购订单 (7)"]
  CGR["purchaseInbounds·采购入库 (8)"]
  AP0["payableBills·应付账单〔复现 5.4〕"]
  PM0["payments·付款登记〔复现 5.4〕"]
  SO0["salesOrders·销售订单〔复现 5.2〕"]
  PG["projects〔复现〕"]
  SG["partners·供应商〔复现〕"]
  PO -->|"采购入库（8/8 PO-·凭单验收）"| CGR
  PO -. "采购应付（5 行 PO-）" .-> AP0
  AP0 -. "付款分期" .-> PM0
  PO <-. "联动采购（2 行 SO-）" .- SO0
  PG -. "所属项目（数据缺列·缺口#1）" .- PO
  SG -. "供应商（名字外键）" .- PO
  {GRAY}
  class AP0,PM0,SO0,PG,SG gray;
''')
D['d31'] = ('3.1 单据审核流（全模块统一口径）', '术语表第四节定版：待提交→待审核→待发货→已完成；各单据执行态变体见 3.1 附表。',
'''stateDiagram-v2
    [*] --> 待提交
    待提交 --> 待审核: 提交
    待审核 --> 待发货: 审核通过
    待审核 --> [*]: 驳回
    待发货 --> 已完成: 执行完成
    已完成 --> 已关闭: 关闭
''')
D['d33'] = ('3.3 账单生命周期（四来源 → 分期收付 → 核销）', '应付侧与应收侧各自的单据→账单→收付→核销链。',
'''flowchart LR
    subgraph AP["应付侧"]
    PO["采购订单"] & RZ["租入单/归还"] --> APB["应付账单·未付款"]
    APB -->|部分付款| APB2["部分付款"] -->|付清| APB3["已付款"]
    APB --> PM["付款登记·分期多笔"]
    end
    subgraph AR["应收侧"]
    SX["销售/租赁出库"] --> ARB["应收账单·未开票/部分收款"]
    ARB -->|收清| ARB2["已结清/已收"]
    ARB --> RC["回款登记"] --> WO["水单核销·已核销/部分核销"]
    ARB --> IV["开票登记·已登记/已红冲"]
    end
''')

LEGEND = '- `-->` 实线＝1:N 数据外键（单号互引，括注=引用记录数证据） ｜ `-.->` 虚线＝M:N / 视图 / 流程口径（数据层无外键） ｜ 灰色虚框节点＝跨图复现实体（真身见 5.1 或所属线图）'

# ---------- 1. md 第 5 节替换 ----------
md_path = PROT / 'P3-R01-A06-实体关系与状态机.md'
s = md_path.read_text(encoding='utf-8')
i = s.find('## 5. 实体关系图')
assert i > 0 and s.count('## 5. 实体关系图') == 1
assert s.count('```mermaid') == 3  # 3.1 + 3.3 + 旧 5
new5 = ['## 5. 实体关系图（拆分版 · 2026-09-11 道远拍板方案 A：1 底图 + 4 流程线）', '',
        f'> **图例**：{LEGEND}', '',
        '> **浏览器看图**：同名渲染版 `P3-R01-A06-实体关系与状态机.html`（原型根目录·双击打开·含本节 5 图 + 3.1/3.3 状态机共 7 图）', '']
for k in ['d51', 'd52', 'd53', 'd54', 'd55']:
    t, desc, code = D[k]
    new5 += [f'### {t}', '', desc, '', '```mermaid', code.strip(), '```', '']
new5 += ['> 跨线关系速查：销售⇄采购（联动采购 2 行 SO-）｜租赁⇄租入（客户转租 XNC-ZZ 3 行）｜盘点⇄其他出入库（盈亏生成）——均为虚线口径，证据详见第 2 节关系表 #12/#17/#24。', '']
md_path.write_text(s[:i] + '\n'.join(new5), encoding='utf-8')
print('md 第 5 节已拆分，mermaid 总数 =', (s[:i] + '\n'.join(new5)).count('```mermaid'))

# ---------- 2. HTML 渲染版 ----------
CSS = '''
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:"Microsoft YaHei","PingFang SC",sans-serif; background:#f5f7fa; color:#1f2329; padding:32px 16px 64px; }
.wrap { max-width:1160px; margin:0 auto; }
h1 { font-size:24px; color:#1677ff; margin-bottom:8px; }
.meta { font-size:13px; color:#8c8c8c; margin-bottom:20px; line-height:1.7; }
.legend { background:#fff; border-left:4px solid #1677ff; border-radius:8px; padding:14px 18px; font-size:13.5px; line-height:2; margin-bottom:26px; box-shadow:0 1px 4px rgba(0,0,0,.05); }
.card { background:#fff; border-radius:10px; padding:22px 26px; margin-bottom:26px; box-shadow:0 1px 4px rgba(0,0,0,.05); }
.card h2 { font-size:17px; color:#1677ff; margin-bottom:6px; }
.card p { font-size:13px; color:#595959; margin-bottom:14px; line-height:1.7; }
.mermaid { display:flex; justify-content:center; overflow-x:auto; padding:8px 0; }
.footer { text-align:center; font-size:12px; color:#bfbfbf; margin-top:8px; }
'''
parts = ['<!DOCTYPE html>', '<html lang="zh-CN">', '<head>', '<meta charset="UTF-8">',
'<meta name="viewport" content="width=device-width, initial-scale=1">',
'<title>A06 实体关系与状态机 · 渲染版 - 包装租赁管理后台</title>',
f'<style>{CSS}</style>', '</head>', '<body>', '<div class="wrap">',
'<h1>P3-R01-A06 · 实体关系与状态机（渲染版）</h1>',
'<div class="meta">V1.1（2026-09-11 · G16a 拆图版 · 道远拍板方案 A：1 底图 + 4 流程线）｜ 真值源=同名 .md（第 1-4 节：分域清单/29 条关系表/状态机/数据缺口）｜ 37 实体 · demo-data dump 实测</div>',
f'<div class="legend"><b>图例</b><br>{LEGEND.replace("`","")}</div>']
order = ['d51', 'd52', 'd53', 'd54', 'd55', 'd31', 'd33']
for k in order:
    t, desc, code = D[k]
    parts += [f'<div class="card">', f'<h2>{t}</h2>', f'<p>{desc}</p>',
              '<pre class="mermaid">', code.strip(), '</pre>', '</div>']
parts += ['<div class="footer">P3-R01-包装租赁管理后台原型 · A06 渲染版 · mermaid 10.9 内嵌（file:// 离线可用）</div>',
'</div>', '<script>', MM, '</script>',
'<script>mermaid.initialize({startOnLoad:true, theme:"base", themeVariables:{primaryColor:"#e8f1ff", primaryBorderColor:"#1677ff", primaryTextColor:"#1f2329", lineColor:"#8c8c8c", fontSize:"14px"}, flowchart:{curve:"basis", htmlLabels:true}});</script>',
'</body>', '</html>']
html_path = PROT / 'P3-R01-A06-实体关系与状态机.html'
html_path.write_text('\n'.join(parts), encoding='utf-8')
print('HTML written:', html_path.name, html_path.stat().st_size, 'bytes')
