# -*- coding: utf-8 -*-
"""R4b：radio/checkbox 绑定块（统一脚本）后移到全部 modal markup 之后。幂等。"""
import io, re, sys, glob, os
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
moved = []
for p in sorted(glob.glob(f'{BASE}/**/*.html', recursive=True)):
    if '弹窗' in p: continue
    s = io.open(p, encoding='utf-8', newline='').read()
    mods = list(re.finditer(r'class="modal-overlay[ "]', s))
    if not mods: continue
    last_modal = max(m.start() for m in mods)
    bind = None
    for m in re.finditer(r'<script[^>]*>(.*?)</script>', s, re.S):
        if ".radio').forEach" in m.group(1):
            bind = m; break
    if bind and bind.end() < last_modal:
        block = bind.group(0)
        s2 = s[:bind.start()] + s[bind.end():]
        idx = s2.rfind('</body>')
        assert idx > 0, p
        s2 = s2[:idx] + block + '\r\n' + s2[idx:]
        for tag in ('script', 'div'):
            assert s.count(f'<{tag}') == s2.count(f'<{tag}'), (p, tag)
        io.open(p, 'w', encoding='utf-8', newline='').write(s2)
        moved.append(os.path.relpath(p, BASE))
print('radio 绑定块后移:', len(moved), '页')
for x in moved: print(' ', x)
