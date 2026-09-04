# -*- coding: utf-8 -*-
"""D组：回款登记审核流对称性补齐（幂等版）。
1. 回款登记.html 注入 ?audit=1 auto-open（抄付款登记现成块）——已完成则跳过
2. 我的待办 增"收款确认"类（17→18）：表格行/下拉/chips/统计卡/副标题/分页/标注pin（CRLF 行尾适配）
3. F01 S7 计数 17→18；A04 JSON note 同步（唯一维护处）
"""
import sys, json, re
sys.path.insert(0, r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir")
from detail_modal_lib import *

AUTO_OPEN = '\r\n'.join([
'<script>',
'/* ?audit=1 自动打开审核弹窗（我的待办跳转支持） */',
'(function(){',
'  if (location.search.indexOf("audit=1") < 0) return;',
'  var t = setInterval(function(){',
'    if (typeof openModal === "function" && document.getElementById("auditModal")) {',
'      clearInterval(t); openModal("auditModal");',
'    }',
'  }, 120);',
'  setTimeout(function(){ clearInterval(t); }, 4000);',
'})();',
'</script>',
''])

# ---------- 1. 回款登记 auto-open ----------
page = '财务协同/回款登记.html'
t = read_page(page)
if 'audit=1' in t:
    print('SKIP(已完成) 回款登记 auto-open')
else:
    i = t.find('<script>/*ia-fix: tab-switch + btn-feedback')
    assert i > 0, page + ': 找不到 ia-fix 锚点'
    t2 = t[:i] + AUTO_OPEN + '\r\n' + t[i:]
    write_page(page, t2)
    print('OK 回款登记 auto-open 注入')

# ---------- 2. 我的待办 17→18 类 ----------
page = '首页/我的待办.html'
t = read_page(page)
EOL = '\r\n' if '\r\n' in t else '\n'

row_new = EOL.join([
'        <tr data-type="收款确认">',
'          <td><span class="tag tag-blue">收款确认</span></td>',
'          <td><span class="lk">HK-20260830-014</span></td>',
'          <td>一汽解放 · 租赁费回款 286,500 元</td>',
'          <td>PRJ-2601</td>',
'          <td>财务-周敏</td>',
'          <td>08-30 10:35</td>',
'          <td><span class="tag tag-orange">待确认</span></td>',
'          <td><span class="ops"><a onclick="go(\'../财务协同/回款登记.html?audit=1\')">去审核</a></span></td>',
'        </tr>',
])

reps = [
    ('<b id="todoCount">14</b>', '<b id="todoCount">18</b>', 1),
    ('覆盖 17 类单据 · 点击"去审核"直达审核弹窗', '覆盖 18 类单据 · 点击"去审核"直达审核弹窗', 1),
    ('<div class="st-label"><span>待确认</span></div><div class="st-num">1<span class="unit">单</span></div><div class="st-foot">付款登记确认</div>',
     '<div class="st-label"><span>待确认</span></div><div class="st-num">2<span class="unit">单</span></div><div class="st-foot">付款 / 收款登记确认</div>', 1),
    ('<option>拆卸</option><option>盘点</option>', '<option>拆卸</option><option>收款确认</option><option>盘点</option>', 1),
    ("<span class=\"todo-chip\" onclick=\"pickType('拆卸')\">拆卸</span> <span class=\"todo-chip\" onclick=\"pickType('盘点')\">盘点</span>",
     "<span class=\"todo-chip\" onclick=\"pickType('拆卸')\">拆卸</span> <span class=\"todo-chip\" onclick=\"pickType('收款确认')\">收款确认</span> <span class=\"todo-chip\" onclick=\"pickType('盘点')\">盘点</span>", 1),
    # 表格行：插在付款登记行之后、租入单行之前
    (EOL.join(['        </tr>', '        <tr data-type="租入单">']),
     EOL.join(['        </tr>', row_new, '        <tr data-type="租入单">']), 1),
    ('<div class="pager"><span class="pg-info">第 1-14 条 / 总共 14 条待办</span></div>',
     '<div class="pager"><span class="pg-info">第 1-18 条 / 总共 18 条待办</span></div>', 1),
    ('S7 审核与待办支线：17 类单据统一进待办', 'S7 审核与待办支线：18 类单据统一进待办', 1),
]
t2 = t
skipped = 0
for old, new, cnt in reps:
    c = t2.count(old)
    if c == 0 and new in t2:
        skipped += 1
        continue  # 幂等：该条已完成
    assert c == cnt, page + ' 计数不符(%d): %r' % (c, old[:40])
    t2 = t2.replace(old, new)
rows = len(re.findall(r'<tr data-type="', t2))
assert rows == 18, '待办行数 %d != 18' % rows
if t2 != t:
    write_page(page, t2)
print('OK 我的待办 17→18 类（行/下拉/chips/统计卡/副标题/分页/pin，幂等跳过 %d 条）' % skipped)

# ---------- 3. F01 S7 计数 ----------
page = 'P3-R01-F01-业务流程导航图.html'
t = read_page(page)
reps = [
    ('>审核弹窗（17 类）</text>', '>审核弹窗（18 类）</text>', 1),
    ('17 类单据统一进待办（订单/出入库/租赁/退租/赔偿/盘点/调拨/拆卸/付款/租入单据）',
     '18 类单据统一进待办（订单/出入库/租赁/退租/赔偿/盘点/调拨/拆卸/付款、收款/租入单据）', 1),
]
t2 = t
for old, new, cnt in reps:
    c = t2.count(old)
    if c == 0 and new in t2:
        continue
    assert c == cnt, page + ' 计数不符: ' + old[:40]
    t2 = t2.replace(old, new)
if t2 != t:
    write_page(page, t2)
print('OK F01 S7 计数 17→18')

# ---------- 4. A04 JSON（唯一维护处） ----------
p = ROOT / 'P3-R01-A04-流程链标注数据.json'
with open(p, 'r', encoding='utf-8', newline='') as f:
    raw = f.read()
if '18 类单据统一进待办' not in raw:
    assert raw.count('17 类单据统一进待办') == 1
    raw = raw.replace('17 类单据统一进待办', '18 类单据统一进待办')
    json.loads(raw)
    with open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(raw)
print('OK A04 JSON note 17→18')
print('D 组完成')
