# -*- coding: utf-8 -*-
"""批2 Script A：全站引用改名（器具档案→产品档案 路径+菜单标签+页签）+ 零部件档案菜单项/页签删除"""
from pathlib import Path
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
PROTO = ROOT / "P3-R01-包装租赁管理后台原型"

files = sorted(PROTO.rglob("*.html")) + sorted((PROTO / "_data").glob("*.js")) + \
        [PROTO / "P3-R01-A04-流程链标注数据.json"] + [ROOT / "_scan_tmpdir" / "verify_listfull.py"]

cnt_path = cnt_label = cnt_tab = cnt_menu_del = 0
for f in files:
    if not f.exists():
        continue
    raw = f.read_bytes()
    txt = raw.decode('utf-8')
    nl = '\r\n' if '\r\n' in txt else '\n'
    orig = txt
    # 1) 路径：器具档案.html → 产品档案.html
    n = txt.count('基础数据/器具档案.html')
    if n:
        txt = txt.replace('基础数据/器具档案.html', '基础数据/产品档案.html')
        cnt_path += n
    # 2) 侧边栏菜单标签：>器具档案</div> → >产品档案</div>（仅菜单项形态，路径已改）
    LBL_OLD = "go('../基础数据/产品档案.html')" + '">器具档案<'
    LBL_NEW = "go('../基础数据/产品档案.html')" + '">产品档案<'
    n = txt.count(LBL_OLD)
    if n:
        txt = txt.replace(LBL_OLD, LBL_NEW)
        cnt_label += n
    # 3) 页签：>器具档案 < → >产品档案 <（tab 形态）
    n = txt.count('class="tab">器具档案 <span')
    if n:
        txt = txt.replace('class="tab">器具档案 <span', 'class="tab">产品档案 <span')
        cnt_tab += n
    # 4) 菜单项删除：零部件档案（侧边栏行）
    menu_line = ('   <li><div class="sm-link" onclick="go(\'../基础数据/零部件档案.html\')">零部件档案</div></li>' + nl)
    n = txt.count(menu_line)
    if n:
        txt = txt.replace(menu_line, '')
        cnt_menu_del += n
    # 5) 页签删除：零部件档案 tab
    tab_line = '  <span class="tab">零部件档案 <span class="close">×</span></span>' + nl
    n = txt.count(tab_line)
    if n:
        txt = txt.replace(tab_line, '')
        cnt_tab += n
    if txt != orig:
        f.write_bytes(txt.encode('utf-8'))

print(f'路径替换 器具档案→产品档案: {cnt_path}')
print(f'菜单标签 器具档案→产品档案: {cnt_label}')
print(f'页签处理（含零部件删除）: {cnt_tab}')
print(f'零部件档案菜单项删除: {cnt_menu_del}')

# 校验
left = []
for f in files:
    if not f.exists():
        continue
    txt = f.read_bytes().decode('utf-8')
    for pat in ['基础数据/零部件档案.html', '器具档案.html']:
        if pat in txt:
            left.append((str(f.relative_to(PROTO)), pat))
assert not left, f'残留: {left}'
print('PASS: 无 器具档案.html / 零部件档案.html 路径残留')
