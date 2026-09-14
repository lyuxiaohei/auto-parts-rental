# -*- coding: utf-8 -*-
"""G30 T3.1：数据字典.html 分类侧栏 dic-item 追加 13 组 + createModal「字典分类」select 追加 13 option。
页无 stabs 分组页签（实测）→ 跳过 stabs；本页不在 verify_listfull 批次 → 由 g30_verify.py 自写断言。"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\系统管理\数据字典.html'
t = io.open(P, encoding='utf-8', newline='').read()
orig = len(t)
assert t.count('\r\n') > 500, 'CRLF 基线异常'
assert t.count('class="stabs"') == 0, '本页存在 stabs（任务书按无页签预期，需人工复核）'

CATS = [('库存状态', 5), ('入库类型', 3), ('出库类型', 4), ('应收账单类型', 6), ('应付账单类型', 5),
        ('费用分类', 7), ('发票类型', 2), ('客商类型', 3), ('数据权限范围', 3), ('盘点口径', 2),
        ('周期单位', 3), ('物料分类', 6), ('待办单据类型', 16)]

# 侧栏锚点：物料类型（现末项）
A_ITEM = ('          <div class="dic-item"><span>物料类型</span><span class="cnt">2</span></div>\r\n'
          '  </div>')
assert t.count(A_ITEM) == 1, 'dic-list 末项锚点命中 %d' % t.count(A_ITEM)
NEW_ITEM = '          <div class="dic-item"><span>物料类型</span><span class="cnt">2</span></div>\r\n' + \
    ''.join('          <div class="dic-item"><span>%s</span><span class="cnt">%d</span></div>\r\n' % (c, n)
            for c, n in CATS) + '  </div>'
t = t.replace(A_ITEM, NEW_ITEM)

# createModal 字典分类 select 锚点：缺损类型(selected)/全部/待定选项（演示数据）
A_SEL = '<option selected>缺损类型</option><option>全部</option><option>待定选项（演示数据）</option>'
assert t.count(A_SEL) == 1, 'select 锚点命中 %d' % t.count(A_SEL)
NEW_SEL = A_SEL + ''.join('<option>%s</option>' % c for c, _ in CATS)
t = t.replace(A_SEL, NEW_SEL)

# 改后断言（DOM 行计数：dic-item 与 dic-item active 两种形态，旧 10+1active+13 新=24）
n_dom = t.count('<div class="dic-item">') + t.count('<div class="dic-item active">')
assert n_dom == 24, 'dic-item DOM 行 %d≠24（11 旧含 1 active+13 新）' % n_dom
for c, n in CATS:
    assert t.count('<span>%s</span><span class="cnt">%d</span>' % (c, n)) == 1, c + ' dic-item 断言失败'
    assert t.count('<option>%s</option>' % c) == 1, c + ' option 断言失败'
# 标签配平
assert t.count('<div') - t.count('</div>') == t.count('<div class="dic-item">') * 0 + (
    t.count('<div') - t.count('</div>')), ''
opens = t.count('<option'); closes = t.count('</option>')
print('option 开/闭: %d/%d（改前 3+2 页内其余 select 保持）' % (opens, closes))
d_open = t.count('<div'); d_close = t.count('</div>')
assert d_open == d_close, 'div 配平 %d/%d' % (d_open, d_close)

io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('写入完成 %d → %d 字节 (+%d) · CRLF 保持' % (orig, len(t), len(t) - orig))
print('PASS T3.1 dic-item 24 行（+13）· createModal select +13 option · div 配平 %d/%d' % (d_open, d_close))
