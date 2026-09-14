# -*- coding: utf-8 -*-
"""G30 T1c：库位档案.html 筛选/表单「平面库位/立体库位/待定选项」占位 → 字典 KW 组 4 值。
演示行/详情「平面库位」→「存储位」同构替换（assert 计数；实测 0 命中=数据本就干净，零改动）。"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\基础数据\库位档案.html'
t = io.open(P, encoding='utf-8', newline='').read()
orig = len(t)
crlf = t.count('\r\n')
assert crlf > 500, 'CRLF 基线异常'

# 筛选 select（库位类型 ff）：全部/平面库位/立体库位 → 全部 + KW 4 值
A_FILTER = ('<div class="ff ff-row-extra"><span class="ff-label">库位类型：</span>\r\n'
            '      <select><option selected>全部</option><option>平面库位</option><option>立体库位</option></select>')
NEW_FILTER = ('<div class="ff ff-row-extra"><span class="ff-label">库位类型：</span>\r\n'
              '      <select><option selected>全部</option><option>存储位</option><option>拣选位</option>'
              '<option>暂存位</option><option>不合格品位</option></select>')
assert t.count(A_FILTER) == 1, '筛选锚点命中 %d 次' % t.count(A_FILTER)

# createModal 表单 select（库位类型）：平面库位/全部/待定选项（演示数据） → KW 4 值（存储位默认）
A_FORM = ('<option selected>平面库位</option><option>全部</option><option>待定选项（演示数据）</option>')
NEW_FORM = ('<option selected>存储位</option><option>拣选位</option><option>暂存位</option>'
            '<option>不合格品位</option>')
assert t.count(A_FORM) == 1, '表单锚点命中 %d 次' % t.count(A_FORM)

# 演示行/详情「平面库位」值→存储位（同构替换，先读现状）
n_td = t.count('<td>平面库位</td>')
n_plain = t.count('平面库位')
print('改前计数：<td>平面库位</td>=%d · 平面库位全文=%d（2 处均在 select option 内）' % (n_td, n_plain))

t = t.replace(A_FILTER, NEW_FILTER).replace(A_FORM, NEW_FORM)

# 改后断言：4 值在、占位清零
for v in ['存储位', '拣选位', '暂存位', '不合格品位']:
    assert t.count(v) >= 2, v + ' 出现不足'
assert t.count('平面库位') == 0, '平面库位残留 %d' % t.count('平面库位')
assert t.count('立体库位') == 0, '立体库位残留 %d' % t.count('立体库位')
assert t.count('待定选项') == 0, '待定选项残留 %d' % t.count('待定选项')
# 标签配平自检
for tag in ['select', 'option', 'div']:
    o = t.count('<' + tag) - t.count('</' + tag + '>')
    assert o == t.count('<' + tag + ' ') * 0 + (1 if tag == 'div' else 0) * 0, ''  # 占位不启用
opens = t.count('<select'); closes = t.count('</select>')
assert opens == closes == t.count('<select') , 'select 配平 %d/%d' % (opens, closes)
print('PASS select 配平 %d/%d' % (opens, closes))

io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('写入完成 %d → %d 字节 · CRLF 保持 %d 行' % (orig, len(t), t.count('\r\n')))
print('PASS T1c：筛选=全部+KW4值 · 表单=存储位默认+KW4值 · 平面库位/立体库位/待定选项=0 · td 值替换命中 0（数据本就无该值）')
