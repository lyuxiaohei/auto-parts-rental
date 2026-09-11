# -*- coding: utf-8 -*-
"""G19a T2 补：登录页表单区包 m-card（卡片容器化）"""
import pathlib
p = pathlib.Path(r'P3-R01-包装租赁管理后台原型/mobile/登录.html')
s = p.read_text(encoding='utf-8')

o1 = '  <div style="padding: 0 28px;">'
n1 = '  <div style="padding: 0 20px;">\n    <div class="m-card" style="padding:20px 16px;">'
assert s.count(o1) == 1, f'anchor1 {s.count(o1)}'
s = s.replace(o1, n1)

o2 = '    <div style="text-align:center;color:#bfbfbf;font-size:11px;margin-top:26px;">P3-R01 移动端 H5 · v1.0 · 2026-09-11</div>'
n2 = '    </div>\n    <div style="text-align:center;color:#bfbfbf;font-size:11px;margin-top:26px;">P3-R01 移动端 H5 · v1.0 · 2026-09-11</div>'
assert s.count(o2) == 1, f'anchor2 {s.count(o2)}'
s = s.replace(o2, n2)

p.write_text(s, encoding='utf-8')
# 标签配平自检
for tag in ('div',):
    o, c = s.count('<' + tag), s.count('</' + tag + '>')
    print(f'  <{tag}> open={o} close={c} balanced={o==c}')
print('LOGIN CARD WRAP OK')
