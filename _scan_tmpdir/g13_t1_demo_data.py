# -*- coding: utf-8 -*-
"""G13 demo-data.js 综合改动（读取-精确替换+assert，禁整页写）+ verify_listfull.py 期望值同步"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
F = ROOT / "P3-R01-包装租赁管理后台原型/_data/demo-data.js"
raw = F.read_bytes().decode('utf-8')
CRLF = '\r\n' in raw
NL = '\r\n' if CRLF else '\n'
orig = raw

def rep(s, old, new, cnt, tag):
    n = s.count(old)
    assert n == cnt, f"[{tag}] 期望 {cnt} 处，实际 {n} 处: {old[:80]!r}"
    return s.replace(old, new)

def section(s, start_mark, end_mark):
    i = s.index(start_mark)
    j = s.index(end_mark, i)
    return i, j

# ============ A. stockFlows：10 行加 status 字段+成本单价格 ============
STOCK = [
    # key, 总量, 单位, 成本, 状态
    ("XNC-AJZX-WBX", "640", "只", "340.00", "客户端(租出)"),
    ("LJ-A100", "7,260", "件", "1.60", "在库"),
    ("LJ-B200", "4,640", "件", "1.10", "在库"),
    ("LJ-C300", "3,460", "件", "8.20", "在库"),
    ("LJ-D400", "1,860", "件", "3.60", "退租待入库"),
    ("LJ-F600", "1,640", "件", "0.90", "在库"),
    ("WBX-1210L", "2,480", "只", "340.00", "客户端(租出)"),
    ("WBX-1210M", "1,000", "只", "296.00", "客户端(租出)"),
    ("PLT-1210P", "1,700", "块", "98.00", "客户端(租出)"),
    ("BTC-6040", "3,940", "只", "76.50", "客户端(租出)"),
]
si, sj = section(raw, "  stockFlows: {", "  rentTracks: {")
sec = raw[si:sj]
for key, total, unit, cost, status in STOCK:
    keyline = f"'{key}': {{"
    assert sec.count(keyline) == 1, f"stockFlows 键定位失败: {key}"
    # status 进 fields（行内替换，逐行找 row 行）
    lines = sec.split(NL)
    for idx, ln in enumerate(lines):
        if keyline in ln:
            rowln = lines[idx + 1]
            assert rowln.lstrip().startswith("'row':"), f"{key} row 行不符: {rowln[:60]}"
            assert '"fields": {' in rowln, f"{key} fields 锚缺失"
            rowln2 = rowln.replace('"fields": {', f'"fields": {{"status": "{status}", ', 1)
            needle = f'<b>{total}</b></span>", "{unit}"'
            assert rowln2.count(needle) == 1, f"{key} 总量/单位锚失败"
            rowln2 = rowln2.replace(needle, f'<b>{total}</b></span>", "<span class=\\"td-num\\">{cost}</span>", "{unit}"', 1)
            lines[idx + 1] = rowln2
            break
    else:
        raise AssertionError(f"未找到 {key}")
    sec = NL.join(lines)
raw = raw[:si] + sec + raw[sj:]

# ============ A2. stockFlows 追加 3 行「客户端(转租)」演示行 ============
def zz_row(code, name, qty, unit, cost):
    return (
f"""   '{code}': {{
      'row': {{"fields": {{"name": "{name}（安吉智行·转租终端用户）", "cls": "租赁器具", "project": "PRJ-2605", "area": "安吉智行·转租终端仓", "status": "客户端(转租)"}}, "cells": ["{name}（安吉智行·转租终端用户）", "<span class=\\"tag tag-blue\\">租赁器具</span>", "PRJ-2605", "<span class=\\"td-num\\">0</span>", "<span class=\\"td-num\\">0</span>", "<span class=\\"td-num\\">{qty}</span>", "<span class=\\"td-num\\">0</span>", "<span class=\\"td-num\\"><b>{qty}</b></span>", "<span class=\\"td-num\\">{cost}</span>", "{unit}", "安吉智行·转租终端仓"], "ops": [{{"t": "库存流水", "detail": true}}, {{"t": "客户在租", "act": "openModal('rentDrillModal')"}}]}},
      'title': '库存流水',
      'titleNo': '{code} {name}（转租终端用户）',
      'info': [
        {{
          'label': '物料编码',
          'text': '{code}'
        }},
        {{
          'label': '名称规格',
          'text': '{name}（安吉智行·转租终端用户）',
          'full': True
        }},
        {{
          'label': '物料类别',
          'text': '租赁器具'
        }},
        {{
          'label': '适用项目',
          'text': 'PRJ-2605',
          'full': True
        }},
        {{
          'label': '库存状态',
          'text': '客户端(转租)'
        }},
        {{
          'label': '在租数量',
          'text': '{qty} {unit}（客户安吉智行转租给终端用户）',
          'full': True
        }},
        {{
          'label': '成本单价',
          'text': '{cost} 元（未税 · 最近采购入库价）'
        }},
        {{
          'label': '库区',
          'text': '安吉智行·转租终端仓'
        }}
      ],
      'feeSecTitle': '进出流水（时间倒序）',
      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],
      'fees': [
        {{
          'cells': ['09-06', '组合出库·转租', 'CK-20260905-012', '+{qty}', '{qty}'],
          'links': {{
            2: '租赁管理/组合出库列表.html'
          }}
        }}
      ],
      'chain': [
        {{
          'role': '租入单',
          'name': 'RZD-20260815-005 · 路凯',
          'url': '租赁管理/租入单列表.html'
        }},
        {{
          'role': '租赁单',
          'name': 'ZL-20260905-034 · 客户安吉智行',
          'url': '租赁管理/租赁单列表.html'
        }},
        {{
          'role': '转租终端仓（本仓）',
          'name': '{code} · 转租 {qty} {unit}',
          'self': True
        }}
      ],
      'timeline': [
        {{
          't': '09-06',
          'text': '客户安吉智行转租终端用户 · {qty} {unit}（客户端(转租)＝在租子状态）',
          'who': '王琳'
        }}
      ]
    }},
"""
    ).replace("True", "true")

zz_block = zz_row("XNC-ZZ-WBX", "围板箱 1200×1000×970", "240", "只", "340.00") \
         + zz_row("XNC-ZZ-PLT", "塑料托盘 1200×1000", "120", "块", "98.00") \
         + zz_row("XNC-ZZ-BTC", "料箱 600×400×340", "360", "只", "76.50")
zz_block = zz_block.replace("\n", NL)
si, sj = section(raw, "  stockFlows: {", "  rentTracks: {")
sec = raw[si:sj]
anchor = NL + "  },"
pos = sec.rindex(anchor)
sec = sec[:pos] + NL + zz_block + sec[pos:]
raw = raw[:si] + sec + raw[sj:]
assert raw.count("客户端(转租)") >= 3

# ============ B. leaseOrders：billing 字段 + 退回对比 op + 计费方式 info 行 ============
BILLING = {"ZL-20260816-029": "按次套数", "ZL-20260610-015": "按次套数"}
si, sj = section(raw, "  leaseOrders: {", "  rentInOrders: {")
sec = raw[si:sj]
# B1 ops 插入（全 9 行，锚=ops 数组起始，逐行 ops 结构不一）
old_ops = '"ops": [{'
new_ops = '"ops": [{"t": "退回对比", "act": "openModal(\'cmpModal\')"}, {'
sec = rep(sec, old_ops, new_ops, 9, "leaseOrders ops")
# B2 billing 字段（逐行状态机：key 行 → row 行 fields 前插）
lines = sec.split(NL)
cur = None
n_bill = 0
for idx, ln in enumerate(lines):
    k = None
    for key in ["ZL-20260823-033", "ZL-20260901-032", "ZL-20260828-031", "ZL-20260816-029",
                "ZL-20260815-028", "ZL-20260720-022", "ZL-20260610-015", "ZL-20260301-006", "ZL-20260115-002"]:
        if f"'{key}': {{" in ln:
            k = key
            break
    if k:
        cur = k
        rowln = lines[idx + 1]
        assert rowln.lstrip().startswith("'row':"), f"{cur} row 行不符"
        b = BILLING.get(cur, "按月定期")
        assert '"fields": {' in rowln
        lines[idx + 1] = rowln.replace('"fields": {', f'"fields": {{"billing": "{b}", ', 1)
        n_bill += 1
assert n_bill == 9, f"billing 插入 {n_bill}/9"
sec = NL.join(lines)
# B3 计费方式 info 行（状态 info 块后插；逐记录文本）
lines = sec.split(NL)
cur = None
n_info = 0
out = []
for ln in lines:
    for key in BILLING.keys() | {k for k in ["ZL-20260823-033", "ZL-20260901-032", "ZL-20260828-031",
                                             "ZL-20260815-028", "ZL-20260720-022", "ZL-20260301-006", "ZL-20260115-002"]}:
        if f"'{key}': {{" in ln:
            cur = key
            break
    out.append(ln)
    if ln.rstrip().endswith("'tag': '已退租'} ,") or False:
        pass
    # 状态 info 块闭合行特征：上一行是 'tag': '...'，本行是 '},'
    if cur and ln.rstrip() == "},":  # 需要确认前一行是 tag 行
        pass
# 改用直接正则按记录分块处理
import re
chunks = re.split(r"(?=\n\s*'ZL-\d{8}-\d+'\s*:\s*\{)", sec)
n_info = 0
for ci, ch in enumerate(chunks):
    m = re.match(r"\n\s*'(ZL-[\d-]+)'\s*:", ch)
    if not m:
        continue
    key = m.group(1)
    b = BILLING.get(key, "按月定期")
    txt = "按次套数对账（验收后按套数生成应收）" if b == "按次套数" else "按月定期生成应收（默认）"
    pat = re.compile(r"(\{\s*'label': '状态',\s*'tag': '[^']+'\s*\},)")
    ch2, n = pat.subn(lambda mm: mm.group(1) + NL + f"        {{'label': '计费方式', 'text': '{txt}'}},", ch, count=1)
    assert n == 1, f"{key} 计费方式 info 插入失败"
    chunks[ci] = ch2
    n_info += 1
assert n_info == 9, f"info 插入 {n_info}/9"
sec = "".join(chunks)
raw = raw[:si] + sec + raw[sj:]

# ============ C. rentInOrders：returnItems + 草稿演示行 ============
RET_ITEMS = {
    "RZD-20260815-003": "[{'item': 'WBX-1210L 围板箱 1200×1000×970', 'rentQty': 30, 'returned': 0, 'unit': '只'}]",
    "RZD-20260815-005": "[{'item': 'WBX-1210L 围板箱 1200×1000×970', 'rentQty': 10, 'returned': 4, 'unit': '只'}]",
    "RZD-20260902-008": "[{'item': 'PLT-1210P 塑料托盘 1200×1000', 'rentQty': 60, 'returned': 0, 'unit': '块'}]",
}
si, sj = section(raw, "  rentInOrders: {", "  comboOutbounds: {")
sec = raw[si:sj]
lines = sec.split(NL)
n_ri = 0
for idx, ln in enumerate(lines):
    for key, items in RET_ITEMS.items():
        if f"'{key}': {{" in ln:
            rowln = lines[idx + 1]
            assert rowln.lstrip().startswith("'row':")
            lines[idx + 1] = rowln + NL + f"      'returnItems': {items},"
            n_ri += 1
assert n_ri == 3, f"returnItems {n_ri}/3"
sec = NL.join(lines)
draft = (
f"""   'RZD-20260910-009': {{
      'row': {{"fields": {{"operator": "供应商待选（背靠背自动生成）", "appliance": "WBX-1210L 围板箱 1200×1000×970", "period": "—", "status": "新建(草稿)", "agent": "系统", "date": "2026-09-10"}}, "cells": ["供应商待选（背靠背自动生成）", "WBX-1210L 围板箱 1200×1000×970", "200 只", "—", "—", "0.00", "0.00", "<span class=\\"tag tag-gray\\">新建(草稿)</span>", "系统", "2026-09-10 20:30"], "ops": [{{"t": "选供应商", "act": "showToast('已选供应商：路凯包装运营（上海）有限公司 · 草稿待修改后提交')"}}, {{"t": "修改", "act": "showToast('草稿修改：器具/数量/租期可改，改后点提交进入待审核')"}}, {{"t": "提交", "act": "showToast('已提交审核 · RZD-20260910-009 → 待审核')"}}]}},
      'title': '租入单详情',
      'info': [
        {{'label': '租入单号', 'text': 'RZD-20260910-009', 'full': True}},
        {{'label': '状态', 'tag': '新建(草稿)'}},
        {{'label': '供应商', 'text': '待选（来源：租赁单 ZL-20260910-036 审核确认背靠背自动生成）', 'full': True}},
        {{'label': '器具', 'text': 'WBX-1210L 围板箱 1200×1000×970', 'full': True}},
        {{'label': '数量', 'text': '200 只'}},
        {{'label': '经办人', 'text': '系统（自动生成）'}},
        {{'label': '创建时间', 'text': '2026-09-10 20:30'}}
      ],
      'feeSecTitle': '租入明细（背靠背草稿 · 供应商待选）',
      'feeCols': ['产品', '数量', '计费方式', '未税单价(元)', '税率', '含税单价(元)', '首期应付(元)'],
      'fees': [
        {{'cells': ['WBX-1210L 围板箱 1200×1000×970（租入）', '200 只', '月租', '—', '13%', '—', '—']}}
      ],
      'chain': [
        {{'role': '租赁单（来源）', 'name': 'ZL-20260910-036 · 背靠背', 'url': '租赁管理/租赁单列表.html'}},
        {{'role': '租入单（本单·草稿）', 'name': 'RZD-20260910-009', 'self': True}},
        {{'role': '下一步', 'name': '选供应商 → 修改 → 提交审核'}}
      ],
      'timeline': [
        {{'t': '09-10', 'text': '租赁单审核确认 · 背靠背自动生成租入单草稿（供应商待选）', 'who': '系统'}}
      ]
    }},
"""
).replace("True", "true").replace("\n", NL)
anchor = NL + "  },"
pos = sec.rindex(anchor)
sec = sec[:pos] + NL + draft + sec[pos:]
raw = raw[:si] + sec + raw[sj:]
assert raw.count("新建(草稿)") >= 2

# ============ D. receivableBills：usage 演示行 ============
si, sj = section(raw, "  receivableBills: {", "  payments: {")
sec = raw[si:sj]
usage = (
f"""    'AR-2026-09-PRJ2603-U1': {{
      'row': {{"fields": {{"period": "2026-09", "project": "PRJ-2603", "customer": "小鹏汽车科技有限公司", "btype": "租赁费（按实际使用量生成）", "docs": "按客户对账量录入 · 数量×单价", "gen": "按实际使用量", "date": "2026-09-08", "status": "未开票"}}, "cells": ["2026-09", "PRJ-2603", "小鹏汽车科技有限公司", "租赁费（按实际使用量生成）", "按客户对账量录入 · 数量×单价", "<span class=\\"td-num\\"><b>186,400.00</b></span>", "<span class=\\"td-num\\">0.00</span>", "<span class=\\"tag tag-orange\\">未开票</span>", "<span class=\\"tag tag-blue\\">按实际使用量</span>", "2026-09-08 14:20"], "ops": [{{"t": "账单确认", "act": "openModal('auditModal')"}}, {{"t": "详情", "detail": true}}, {{"t": "开票", "act": "go('../财务协同/开票登记.html')"}}, {{"t": "核销", "act": "go('../财务协同/银行水单核销.html')"}}]}},
      billNo: 'AR-2026-09-PRJ2603-U1',
      billType: '租赁费',
      status: '未开票',
      customer: '小鹏汽车科技有限公司',
      project: 'PRJ-2603',
      period: '2026-09',
      amount: 186400,
      verified: 0,
      genMode: '按实际使用量',
      genDate: '2026-09-08',
      feeType: '租赁费（按实际使用量生成 · 按客户对账量录入）',
      fees: [
        {{ src: '客户对账量 ×26 张', desc: '租赁费 · 2026-09（按实际使用量：46,600 套·日 × 4.00 元）', qty: '46,600', price: '4.00', amount: 186400, url: '租赁管理/组合出库列表.html' }}
      ],
      chain: [
        {{ role: '组合出库', name: '实际使用量 ×26 张', url: '租赁管理/组合出库列表.html' }},
        {{ role: '应收账单（本单）', name: 'AR-2026-09-PRJ2603-U1 · 按实际使用量', self: true }},
        {{ role: '开票登记', name: '待开票', url: '财务协同/开票登记.html' }},
        {{ role: '回款 / 核销', name: '回款登记 → 银行水单核销', url: '财务协同/银行水单核销.html' }}
      ],
      timeline: [
        {{ t: '09-08', text: '按客户对账量录入生成 · 数量×单价（46,600 × 4.00）', who: '王芳' }},
        {{ t: '—', text: '待开票 → 回款 → 水单核销', off: true }}
      ]
    }},
"""
).replace("true", "true").replace("\n", NL)
anchor = NL + "  },"
pos = sec.rindex(anchor)
sec = sec[:pos] + NL + usage + sec[pos:]
raw = raw[:si] + sec + raw[sj:]
assert "按实际使用量" in raw

# ============ E. todoItems：auditor 字段 ============
AUD = {
    'SO-20260910-0047': '王琳', 'PO-20260910-019': '徐蔚', 'LZ-20260909-012': '王琳',
    'CK-20260909-021': '陈金', 'TK-20260908-006': '袁明', 'PD-20260907-003': '李国栋',
    'RK-20260906-014': '袁丽晶', 'RZ-20260905-004': '王强', 'GH-20260904-002': '王强',
    'QT-20260903-001': '徐蔚', 'FK-20260902-005': '袁丽晶', 'SK-20260901-003': '袁丽晶',
}
si, sj = section(raw, "  todoItems: {", "  projects: {")
sec = raw[si:sj]
lines = sec.split(NL)
n_a = 0
for idx, ln in enumerate(lines):
    for k, a in AUD.items():
        if f"'{k}': {{ 'row'" in ln and '"auditor"' not in ln:
            assert '"fields": {' in ln
            lines[idx] = ln.replace('"fields": {', f'"fields": {{"auditor": "{a}", ', 1)
            n_a += 1
assert n_a == 12, f"auditor {n_a}/12"
sec = NL.join(lines)
raw = raw[:si] + sec + raw[sj:]

# ============ 落盘 ============
assert raw != orig
F.write_bytes(raw.encode('utf-8'))
print("demo-data.js OK：stockFlows 10行状态+成本 / 3转租行 / leaseOrders billing9+ops9+info9 / rentInOrders returnItems3+草稿1 / receivableBills usage1 / todoItems auditor12")

# ============ F. verify_listfull.py 期望值同步 ============
VF = ROOT / "_scan_tmpdir/verify_listfull.py"
v = VF.read_bytes().decode('utf-8')
v2 = rep(v,
    "stabs={'全部': 5, '待审核': 1, '履行中': 1, '部分归还': 1, '已归还': 1, '已终止': 1}, pin=2)",
    "stabs={'全部': 6, '新建(草稿)': 1, '待审核': 1, '履行中': 1, '部分归还': 1, '已归还': 1, '已终止': 1}, pin=2),  # G13：+草稿演示行",
    1, "verify 租入单 stabs")
v2 = rep(v2,
    "stabs={'全部': 13, '未开票': 6, '已开票': 13, '部分收款': 2, '已结清': 4}, pin=3)",
    "stabs={'全部': 14, '未开票': 7, '已开票': 14, '部分收款': 2, '已结清': 4}, pin=3),  # G13：+usage 演示行",
    1, "verify 应收 stabs")
VF.write_bytes(v2.encode('utf-8'))
print("verify_listfull.py OK：租入单/应收账单 stab 期望值已随 G13 演示数据同步")
