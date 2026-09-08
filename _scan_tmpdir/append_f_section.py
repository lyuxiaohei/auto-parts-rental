# -*- coding: utf-8 -*-
"""P1-R05 十二节追加 F 节（连跑条款+完成记录）+ 文末变更记录（三）+ P1-R01 附录 10.2 同步"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
P5 = ROOT / 'P1-R05-agent交接文档.md'
P1 = ROOT / 'P1-R01-需求梳理与功能框架.md'

F_SECTION = """### F. 全量推广连跑条款（2026-09-08 道远拍板）——【已执行完毕：30 页三批连跑，失败 0 项】

- **节奏覆盖**：D 节"做完汇报等确认"作废，改 **3 批连跑**（批1 仓储 12 → 批2 财务+买卖 9 → 批3 租赁+基础 9），每批硬门（全量 audit 相对基线新增 0 + 本批 verify 断言全绿）→ git 一批一提交 → 直接下一批
- **✅ 完成记录（2026-09-08）**：
  1. **批1 仓储作业 12 页 64 行**（其他入库/租入入库/销售出库/组合出库/其他出库/租入归还/退租入库/组装/拆卸/盘点/调拨/库存查询）：拆卸次表（散件预览）与库存查询租入在库表（tbody1）维持静态；库存查询=flowModal+noCheckbox（键列首位）；组合出库「拣货中」页签 1 行真实匹配；提交 c72e9b4
  2. **批2 财务+买卖 9 页 61 行**：应付/应收账单走 detailFn 专用渲染器（openPayableBillDetail/openReceivableBillDetail，list-generic 新增 detailFn 钩子）；水单核销驱动表③核销记录（h xTable id 注入 + noCheckbox），表①银行回单/表②待核销单据维持静态；采购订单「所属项目」筛选无对应列不过滤；提交 a7a93f6
  3. **批3 租赁+基础 9 页 67 行**：BOM维护驱动版本表（bomVerTable，keyHtml 富键格保真「V2.1+已生效」tag）；在租台账 noCheckbox+trackModal、顶部四态卡维持静态、「即将到期(7天)」页签 fallback 全量（表无到期日列，口径注明）；客商管理 stabField='type'（类型语义页签，渲染器新增 stabField 配置）；器具档案行内缺「租金单价」格（页面既有状态）按行位映射；丢损「发生时间」/零件「建档时间」/在租「是否超期」筛选无列映射不过滤；提交 d4274d2
  4. **渲染器增强 5 项**（全部向后兼容，试点 2 页回归全绿）：keysAll 过滤无 row 键 / noCheckbox 布局 / row.keyHtml 富键格 / cfg.stabField 页签字段 / cfg.detailFn 专用详情函数
  5. **执行中拦截的执行器缺陷 3 起**（当场修复+备份重放+跨批回归收口，未流入任何提交前的最终态）：apply 生成器对非 range 筛选项的跳项 bug、filters 空时 extra 清空 bug、demo-data 注入锚全文 find 跨实体同名键错命中（BS-20260828-004→receivableBills / ZL-20260823-033→leaseOrders / ZH-260x→stockFlows 污染）——修复=实体段内定位+按文件位置倒序注入
  6. **验证门**：verify_listfull.py 三批 96+70+67=233 项断言全绿（行数=实体条数/行单号=实体键/详情标题=行单号或 titleNo/真过滤 select+input/重置恢复/stab 计数/pin 抽验 6 页/JS 错 0）；三批全量 audit 均死链 0/JS 错 0/相对基线新增 0（问题 42→41 条，库存查询一条 modal-unreachable 误报随列表驱动自然消除，31 误报+10 豁免口径不变）；失败清单 goal-failures-listfull.html 空（失败 0 项）
- **边界**：弹窗模板 24 个预览页回归正常（批批实点）；demo-data.js 仅增量 row 字段（192 条新注入，既有内容零改动）；A04 JSON 未动（pin note 以 row.note 随行注入，与试点同模式）；stab 点击维持仅切视觉态不过滤（试点定型口径）

"""

CHGLOG = """
## 变更记录 · 2026-09-08（三）（列表数据驱动全量推广 · 第十二节 D/F 节三批连跑）

**背景**：十二节试点（2 页）定型后，道远拍板全量推广 30 页连跑（F 节条款）。开工前置校验过（mtime 131 分钟/git clean/audit 基线自跑 42 条=32 误报+10 豁免）。

**改动**：
1. `demo-data.js` 30 页对应实体全部补 row 字段（批1 64 + 批2 61 + 批3 67 = 192 条；fields 语义字段/cells 原行 innerHTML 照抄/ops 原样迁入含 detail 锚/note A04 角标随行），32 个业务实体全部接入列表驱动（含试点 2 实体）
2. `list-generic.js` 增强 5 项（向后兼容）：keysAll 过滤无 row 键（多表共用实体的次表键不渲染）、noCheckbox 布局（库存查询/在租台账/水单核销/BOM维护四类无复选列表头）、row.keyHtml 富键格（BOM 版本「V2.1+已生效」保真）、cfg.stabField（客商类型页签）、cfg.detailFn（应付/应收专用渲染器）
3. 30 列表页 wireDetailModal/自定义接线 → renderListPage 配置段接线（filters 按筛选区 label 精确映射、stabs 按页签语义、特殊页 modalId/tbodySel/无复选布局参数化）；列表静态行保留作无 JS 兜底
4. 水单核销表③注入 id=hxTable、BOM维护版本表注入 id=bomVerTable（多表定位锚）

**特殊处理（F 节默认决策注明）**：水单核销只驱动表③核销记录（writeoffs 实体对应表），表①②静态；在租台账四态卡静态、即将到期页签 fallback；采购订单「所属项目」/丢损「发生时间」/零件「建档时间」/在租「是否超期」筛选无对应列不过滤；应收「已开票」/开票「已作废」页签无该状态行走渲染器 fallback 全量并 console.warn（试点定型口径）；器具档案行内缺「租金单价」格为页面既有状态按行位映射（F 节注明，未改页面）。

**验证**：verify_listfull.py 三批 96+70+67=233 断言全绿（含逐行实点详情标题）；三批全量 audit 死链 0/JS 错 0/相对基线新增 0（42→41：库存查询 1 条 modal-unreachable 误报随列表驱动自然消除；31 误报+10 豁免口径不变）；批1/批2 回归复跑全绿；git 三批提交 c72e9b4 / a7a93f6 / d4274d2；改前备份 backup-listfull-batch1|2|3-20260908（原相对路径）；失败清单 goal-failures-listfull.html 空清单。

**遗留**：audit modal-unreachable 检测维度待补 JS 动态绑定识别（第四节⑦既有遗留）；stab 点击仍仅切视觉态不过滤（如需联动另行拍板）；根目录 zip 快照未重打（对外发版需重打，必须含 _data/）。

"""

# --- P1-R05：F 节插入（E. 边界 之后、变更记录（二）之前）+ 文末变更记录 ---
raw = P5.read_bytes().decode('utf-8')
anchor = '## 变更记录 · 2026-09-08（二）（租赁单列表菜单展开态修复）'
assert raw.count(anchor) == 1, '变更记录（二）锚不唯一'
raw = raw.replace(anchor, F_SECTION + '---\n\n' + anchor)
assert raw.endswith('\n')
raw = raw + CHGLOG
P5.write_bytes(raw.encode('utf-8'))
print('P1-R05：F 节插入 + 变更记录（三）追加 OK')

# --- P1-R01 附录 10.2：P3-R01 行追加列表驱动段 ---
r1 = P1.read_bytes().decode('utf-8')
old_tail = '**09-08·列表数据驱动试点（2 页，P1-R05 第十二节）**：新增 `_data/list-generic.js`（renderListPage 行渲染+真筛选+stab 自动统计+pinsRefresh），租赁单列表/采购入库列表 tbody 改由数据集渲染（17 条既有实体补 row 字段，行 HTML 保留作无 JS 兜底）；audit_interaction.py 加 tbody 渲染等待；Playwright 18 断言全绿、全量审计与基线逐页 diff 零变化；全量推广（剩余 30 页）待拍板|'
add_tail = '**09-08·列表数据驱动全量推广（30 页，P1-R05 第十二节 D/F 节三批连跑）**：剩余 30 列表页 tbody 全部数据集渲染（批1 仓储 12/批2 财务买卖 9/批3 租赁基础 9，demo-data.js 增量 row 192 条，32 业务实体全覆盖）；list-generic.js 增强 5 项（无 row 键过滤/noCheckbox/keyHtml/stabField/detailFn，向后兼容）；水单核销驱动表③核销记录、BOM维护驱动版本表、在租台账/库存查询无复选布局等特殊页参数化处理（F 节注明）；verify_listfull.py 三批 233 断言全绿、三批全量审计死链 0/JS 错 0/新增 0；失败清单空|'
assert r1.count(old_tail) == 1, f'P1-R01 尾锚不唯一: {r1.count(old_tail)}'
r1 = r1.replace(old_tail, old_tail[:-1] + '；' + add_tail)
P1.write_bytes(r1.encode('utf-8'))
print('P1-R01 附录 10.2 同步 OK')
