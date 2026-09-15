# -*- coding: utf-8 -*-
"""G37 回写：A02 v6/A05 实体登记/A03 新页键/P1-R01 附录10.2/P1-R08 页数口径"""
import io, os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'
PROTO = os.path.join(ROOT, 'P3-R01-包装租赁管理后台原型')

def rd(p): return io.open(os.path.join(PROTO, p), encoding='utf-8', newline='').read()
def wr(p, s): io.open(os.path.join(PROTO, p), 'w', encoding='utf-8', newline='').write(s)

# ============ A02 ============
p = 'P3-R01-A02-页面类型与入口对照表.md'
s = rd(p)
if 'G37' not in s:
    # 版本行追加
    anchor = '·4 保留**）'
    assert s.count(anchor) == 1
    s = s.replace(anchor, anchor + '｜ 2026-09-15 v6 增订（**G37：+转移出库 3 页（列表/新建/详情·租赁管理组）·128→131 页口径·菜单 v6 37 项·D-146**；**D1 术语三条全站替换（银行回单/损益/收款·D-142）**）')
    # 菜单树租赁行加转移出库
    old = '租赁出库 → `租赁管理/租赁出库列表.html`；退租入库'
    assert s.count(old) == 1
    s = s.replace(old, '租赁出库 → `租赁管理/租赁出库列表.html`；转移出库（G37 v6·客户转租承载·D-146）→ `租赁管理/转移出库列表.html`；退租入库')
    # G36 B5 新页节后加 G37 节
    anchor2 = '## 六、v3 相对 v2 的结构性变更注记'
    assert s.count(anchor2) == 1
    g37_sec = '''### G37 新页（3·2026-09-15·D-146 转移出库落地）

| 页面 | 载体 | 入口 | 备注 |
|---|---|---|---|
| `租赁管理/转移出库列表.html` | 菜单内（租赁管理组·v6） | 菜单「转移出库」＋库存查询行内「转移出库/终止转移」 | renderListPage 数据驱动（transferOutbounds）·状态流 待转移→已转移→已终止 |
| `租赁管理/转移出库新建.html` | 菜单外表单页 | 列表「新建转移出库」＋库存查询行内带参跳转（?mat=&cust= 预填） | 结算方式默认取项目档案可覆盖（D-132）·物料下拉动态取 products |
| `租赁管理/转移出库单详情.html` | 菜单外详情页 | 列表/库存行内 ?id= | detail-generic 按单号渲染·财务口径两模式注记 |

> G37 同步：转租登记/转租还回弹窗退场（D-78 被替代·库存查询）；D1 术语三条全站替换（水单→银行回单 290／盈亏→损益 171／回款→收款 314·文件名 5 个不改）；D2 角色 7→6（主管并入部门＋采购/项目经理）。

'''
    s = s.replace(anchor2, g37_sec + anchor2)
    wr(p, s)
    print('A02 v6 增订 OK')

# ============ A05 ============
p2 = 'P3-R01-A05-字段字典.md'
s2 = rd(p2)
if '### transferOutbounds' not in s2:
    anchor3 = '| todoItems | 付款确认 1 条 link→确认页'
    i = s2.index(anchor3)
    a = s2.rfind('\n\n', 0, i)
    ent = '''

### transferOutbounds · 转移出库单（G37·D-146·租赁管理/转移出库列表.html）

| 字段键 | 中文标签 | 类型 | 取值域 / 演示值 | 覆盖行数 |
|---|---|---|---|---|
| `_key` | 转移单号 ¹ | 文本 | ZY-2026MMDD-NNN | 5/5 |
| `from` | 转出方（直接客户） ¹ | 文本 | 安吉智行物流 / 长丰锂电科技 | 5/5 |
| `to` | 接收方（终端客户） ¹ | 文本 | 博世汽车部件（苏州）等·档案可选或手工录入（D-108） | 5/5 |
| `material` | 物料 ¹ | 文本 | 围板箱 1200×1000×970 等（products 动态） | 5/5 |
| `qty` | 数量 ¹ | 数值 | 200 只 / 240 只 / 80 张 等 | 5/5 |
| `settle` | 结算方式 ¹ | 枚举 | 按租出结算（默认·不生成应收账单）/ 按终端结算（后续账单主体切终端·历史不回改） | 5/5 |
| `date` | 转移日期 ¹ | 日期 | 2026-09-xx | 5/5 |
| `project` | 关联项目 | 文本 | PRJ-2605 / PRJ-2603 | 5/5 |
| `status` | 状态 ¹ | 枚举 | 待转移 → 已转移 →（终止转移）已终止 | 5/5 |

> 红线遵守：不勾稽原租赁单（D-106·无「关联租赁单」字段）；不碰计费字段（D-122）。
> projects 同步：+`settle` 转租结算方式（8/8·PRJ-2603=按终端结算·其余按租出结算）；stockFlows：+XNC-ZZ-PLT2（PRJ-2603·客户转租出 80 张·ZY-002 驱动）、XNC-ZZ-PLT 回「客户端(租出)」（ZY-004 已终止）。
> D1 术语（D-142）：水单→银行回单／盈亏→损益／回款→收款 全站替换（文件名 5 个不改·账面口径=菜单名）；D2 角色（D-143）：roles 7→6、users +2（徐文·采购/沈婷·项目经理）。

'''
    s2 = s2[:a] + ent + s2[a+1:]
    wr(p2, s2)
    print('A05 +transferOutbounds 节 OK')

# ============ A03 新页键 ============
p3 = 'P3-R01-A03-标注数据.json'
j = json.loads(io.open(os.path.join(PROTO, p3), encoding='utf-8').read())
if '租赁管理/转移出库列表.html' not in j:
    j['租赁管理/转移出库列表.html'] = [
        {"id": 1, "selector": "<span class=\"lk\">ZY-20260914-002</span>", "title": "转移出库单（D-146）", "note": "直接客户→终端客户的器具转移，一步式·不勾稽原租赁单（D-106）。确认转移后库存状态转「客户转租出」；「终止转移」后回「在客户（租出）」。转租登记/转租还回弹窗已退场，由本单承载。结算方式默认取项目档案「转租结算方式」可按单覆盖（D-132）。", "fp": "FP3-06", "req": "REQ-06"},
    ]
    j['租赁管理/转移出库新建.html'] = [
        {"id": 1, "selector": "<div class=\"form-label\" style=\"padding-top:6px;\"><span class=\"req\">*</span>结算方式：</div>", "title": "结算方式两值（D-132）", "note": "默认取项目档案「转租结算方式」，可单据级覆盖。按租出结算＝租金仍向直接客户计收，转移单不进财务链路；按终端结算＝生效后后续账单主体切终端客户，历史账单不回改。终端客户可选客商档案或手工录入（D-108·不强制建档）。", "fp": "FP4-02", "req": "REQ-03"},
    ]
    j['租赁管理/转移出库单详情.html'] = [
        {"id": 1, "selector": "<h3 class=\"card-title\" id=\"dtTitle\">转移出库单详情</h3>", "title": "转移出库单（D-146）", "note": "转出方（直接客户）→ 本单 → 接收方（终端客户）三段链。财务口径：按租出结算不生成应收账单；按终端结算后续账单主体切换为终端客户（历史账单不回改）。", "fp": "FP3-06", "req": "REQ-06"},
    ]
    io.open(os.path.join(PROTO, p3), 'w', encoding='utf-8', newline='\n').write(json.dumps(j, ensure_ascii=False, indent=2))
    print('A03 +3 新页键 OK')
else:
    print('A03：已含（跳过）')

# ============ P1-R01 附录 10.2 ============
p4 = os.path.join(ROOT, 'P1-R01-需求梳理与功能框架.md')
s4 = io.open(p4, encoding='utf-8').read()
if '转移出库列表.html' not in s4:
    anchor4 = '### 10.2'
    i4 = s4.index(anchor4)
    j4 = s4.index('\n## ', i4) if '\n## ' in s4[i4:] else len(s4)
    # 找附录10.2 表尾——直接在 10.2 节首段后插一行说明
    k = s4.index('\n', s4.index('10.2'))
    ins = '\n> G37（2026-09-15）：+租赁管理/转移出库列表.html、转移出库新建.html、转移出库单详情.html 3 页（D-146·菜单 v6 37 项·131 页口径）。\n'
    s4 = s4[:k] + ins + s4[k:]
    io.open(p4, 'w', encoding='utf-8').write(s4)
    print('P1-R01 附录10.2 追加 OK')

# ============ P1-R08 页数口径 ============
p5 = os.path.join(ROOT, 'P1-R08-项目文件索引.md')
s5 = io.open(p5, encoding='utf-8').read()
if '131 页' not in s5 and '129' in s5:
    s5 = s5.replace('129 HTML', '132 HTML').replace('129 页', '131 页（PC）+mobile 5=132 HTML')
    io.open(p5, 'w', encoding='utf-8').write(s5)
    print('P1-R08 页数口径同步（尽力替换）')
else:
    print('P1-R08：检查（129/131 字样）', '129' in s5, '131' in s5)
print('回写脚本 DONE')
