# -*- coding: utf-8 -*-
"""R4：绑定 script 块（radio/checkbox/overlay forEach）移动到全部 modal markup 之后（</body> 前）。
结构判定：绑定块结束位置 < 最后一个 modal-overlay 起始位置 -> 需移动。幂等。"""
import io, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

moved, skip = [], []
for p in sorted(glob.glob(f'{BASE}/**/*.html', recursive=True)):
    s = io.open(p, encoding='utf-8', newline='').read()
    # 找包含 overlay forEach 的 script 块
    bind = None
    for m in re.finditer(r'<script>(.*?)</script>', s, re.S):
        if ".modal-overlay').forEach" in m.group(1) or '.modal-overlay").forEach' in m.group(1):
            bind = m
            break
    if not bind:
        continue
    mods = list(re.finditer(r'class="modal-overlay[ "]', s))
    if not mods:
        continue
    last_modal = max(m.start() for m in mods)
    if bind.end() > last_modal:
        skip.append(p.replace(BASE + '\\', ''))
        continue
    block = bind.group(0)
    s2 = s[:bind.start()] + s[bind.end():]                      # 剪切
    idx = s2.rfind('</body>')
    assert idx > 0, p
    s2 = s2[:idx] + block + '\r\n' + s2[idx:]                   # 插到 </body> 前
    # 校验：标签配平不变
    for tag in ('script', 'div'):
        assert s.count(f'<{tag}') == s2.count(f'<{tag}') and s.count(f'</{tag}>') == s2.count(f'</{tag}>'), (p, tag)
    assert s2.count('.modal-overlay\').forEach') == s.count(".modal-overlay').forEach")
    io.open(p, 'w', encoding='utf-8', newline='').write(s2)
    moved.append((p.replace(BASE + '\\', ''), bind.end() < last_modal and f'绑定块@{bind.end()} < 末modal@{last_modal}'))

print(f'=== R4 移动 {len(moved)} 页 ===')
for p, info in moved: print(' MOVED', p, '|', info)
print(f'已就位跳过 {len(skip)} 页:', ', '.join(skip[:6]), '...' if len(skip) > 6 else '')
