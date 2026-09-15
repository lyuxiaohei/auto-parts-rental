# -*- coding: utf-8 -*-
"""G37 修正：转移出库列表页数据驱动接线（底版残留 purchaseReturns 渲染）＋行内动作重写＋静态骨架换 ZY 行"""
import io, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
p = os.path.join(ROOT, '租赁管理', '转移出库列表.html')
s = io.open(p, encoding='utf-8', newline='').read()

# 1. renderListPage 接线替换
old = """renderListPage({
  entity: 'purchaseReturns',
  stabs: true,
  filters: [
    { label: '退货单号', field: '_key', match: 'contains' },
    { label: '供应商', field: 'supplier' },
    { label: '退货类型', field: 'type' },
    { label: '关联原单号', field: 'ref' },
    { label: '退货状态', field: 'status' },
    { label: '退货日期', field: 'date', range: true }
  ]
});"""
new = """renderListPage({
  entity: 'transferOutbounds',
  stabs: true,
  filters: [
    { label: '转移单号', field: '_key', match: 'contains' },
    { label: '转出方', field: 'from' },
    { label: '接收方', field: 'to', match: 'contains' },
    { label: '结算方式', field: 'settle' },
    { label: '状态', field: 'status' },
    { label: '转移日期', field: 'date', range: true }
  ]
});"""
for oe, ne in ((old, new), (old.replace('\n', '\r\n'), new.replace('\n', '\r\n'))):
    if s.count(oe) == 1:
        s = s.replace(oe, ne)
        break
else:
    raise AssertionError('renderListPage 接线未命中')

# 2. zyConfirm/zyStop 重写（数据驱动行无 .zy-status·tag 定位＋行键动态取）
old2 = re.search(r'<script>\r?\n/\* G37 状态流.*?</script>', s, re.S)
assert old2, 'zy 函数块未命中'
new2 = """<script>
/* G37 状态流：确认转移（待转移→已转移·库存状态转「客户转租出」）/ 终止转移（已转移→已终止·回「在客户（租出）」） */
function zyKey(a) {
  var lk = a.closest('tr').querySelector('.lk');
  return lk ? lk.textContent.trim() : '';
}
function zyTag(a) {
  return a.closest('tr').querySelector('.tag');
}
function zyConfirm(a) {
  var t = zyTag(a);
  if (!t || t.textContent.indexOf('待转移') < 0) return;
  t.textContent = '已转移';
  t.className = 'tag tag-green';
  a.closest('.ops').innerHTML = '<a onclick="go(\\'../租赁管理/转移出库单详情.html?id=' + zyKey(a) + '\\')">详情</a><a onclick="zyStop(this)">终止转移</a>';
}
function zyStop(a) {
  var t = zyTag(a);
  if (!t || t.textContent.indexOf('已转移') < 0) return;
  t.textContent = '已终止';
  t.className = 'tag tag-gray';
  a.closest('.ops').innerHTML = '<a onclick="go(\\'../租赁管理/转移出库单详情.html?id=' + zyKey(a) + '\\')">详情</a>';
}
</script>"""
s = s[:old2.start()] + new2 + s[old2.end():]

# 3. 静态骨架 5 行换 ZY（与 transferOutbounds 演示数据一致）
ROWS = [
    ('ZY-20260915-005', '安吉智行物流', '博世汽车部件（苏州）', '围板箱 1200×1000×970', '200 只', '按租出结算', '2026-09-15', 'tag-orange', '待转移',
     '<a onclick="zyConfirm(this)">确认转移</a><a onclick="go(\'../租赁管理/转移出库单详情.html?id=ZY-20260915-005\')">详情</a>'),
    ('ZY-20260914-003', '安吉智行物流', '博世汽车部件（苏州）', '料箱 600×400×340', '360 只', '按租出结算', '2026-09-14', 'tag-green', '已转移',
     '<a onclick="go(\'../租赁管理/转移出库单详情.html?id=ZY-20260914-003\')">详情</a><a onclick="zyStop(this)">终止转移</a>'),
    ('ZY-20260914-002', '长丰锂电科技', '星辉动力电池有限公司', '塑料托盘 1200×1000', '80 张', '按终端结算', '2026-09-14', 'tag-green', '已转移',
     '<a onclick="go(\'../租赁管理/转移出库单详情.html?id=ZY-20260914-002\')">详情</a><a onclick="zyStop(this)">终止转移</a>'),
    ('ZY-20260914-001', '安吉智行物流', '博世汽车部件（苏州）', '围板箱 1200×1000×970', '240 只', '按租出结算', '2026-09-14', 'tag-green', '已转移',
     '<a onclick="go(\'../租赁管理/转移出库单详情.html?id=ZY-20260914-001\')">详情</a><a onclick="zyStop(this)">终止转移</a>'),
    ('ZY-20260912-004', '安吉智行物流', '延锋汽车饰件（苏州）', '塑料托盘 1200×1000', '120 张', '按租出结算', '2026-09-12', 'tag-gray', '已终止',
     '<a onclick="go(\'../租赁管理/转移出库单详情.html?id=ZY-20260912-004\')">详情</a>'),
]
tb = []
for k, frm, to, mat, qty, st, dt, cls, tag, ops in ROWS:
    tb.append('        <tr>\n          <td><input type="checkbox" class="cb"></td>\n'
              '          <td><span class="lk">%s</span></td>\n'
              '          <td>%s</td>\n          <td>%s</td>\n          <td>%s</td>\n'
              '          <td><span class="td-num">%s</span></td>\n          <td>%s</td>\n          <td>%s</td>\n'
              '          <td><span class="tag %s">%s</span></td>\n'
              '          <td class="sticky-op"><span class="ops">%s</span></td>\n        </tr>'
              % (k, frm, to, mat, qty, st, dt, cls, tag, ops))
new_tb = '<tbody>\n' + '\n'.join(tb) + '\n      </tbody>'
i = s.index('<tbody>')
j = s.index('</tbody>', i) + len('</tbody>')
s = s[:i] + new_tb + s[j:]

io.open(p, 'w', encoding='utf-8', newline='').write(s)
# 验证
import re as _re
o = len(_re.findall(r'<div\b', s)); c = len(_re.findall(r'</div>', s))
print('列表页接线/骨架已改·div %d/%d' % (o, c))
assert o == c
print('OK')
