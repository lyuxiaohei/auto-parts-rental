# -*- coding: utf-8 -*-
"""G10-D 验证门 grep 证据"""
import os, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
os.chdir(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")

F_DASH = "go('../财务协同/盈亏报表.html')\">财务看板</div>"
F_ROOT = "go('财务协同/盈亏报表.html')\">财务看板</div>"
F_SEL = 'sm-link selected">财务看板</div>'

c = {'dash': 0, 'root': 0, 'sel': 0}
old_pages, new_pages = [], []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ('弹窗', '_data') and not d.startswith('backup')]
    for f in files:
        if not f.endswith('.html'):
            continue
        p = os.path.join(root, f)
        s = open(p, encoding='utf-8').read()
        if '>项目损益</div>' in s:
            old_pages.append(p)
        c['dash'] += s.count(F_DASH)
        c['root'] += s.count(F_ROOT)
        c['sel'] += s.count(F_SEL)
        n = s.count('>财务看板</div>')
        assert n <= 1, (p, n)
        if n:
            new_pages.append(p)

print('==== grep 证据（38 业务页 + F01 独立计） ====')
print('>项目损益</div> 命中页数 =', len(old_pages))
print(">财务看板</div> 总数 =", c['dash'] + c['root'] + c['sel'],
      f"（形态分行：../ 形态 {c['dash']} + 根目录形态 {c['root']} + selected 形态 {c['sel']}）")
print('财务看板 命中页数 =', len(new_pages))

print()
print('==== 全站剩余「项目损益」语境盘点（含弹窗/F01，逐条） ====')
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ('_data',) and not d.startswith('backup')]
    for f in files:
        if not f.endswith('.html'):
            continue
        p = os.path.join(root, f).replace(chr(92), '/')
        s = open(p, encoding='utf-8').read()
        for m in re.finditer(r'.{0,30}项目损益.{0,30}', s):
            print('REM|', p, '|', repr(m.group(0)[:96]))
