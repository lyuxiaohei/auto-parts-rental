# -*- coding: utf-8 -*-
"""G39 重打包 · 包装租赁管理后台原型-20260916.zip（覆盖 11:50 含旧文件名的过期包）
口径＝同 20260911-3：132 HTML + _data + mobile + 根级交付文档；排除旧 zip / .prompts
新增校验：包内链接自洽（onclick go('…') / href 目标必须在包内存在·跨页与页内锚豁免）
"""
import os, re, zipfile
from urllib.parse import unquote

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'P3-R01-包装租赁管理后台原型'))
OUT = os.path.join(ROOT, '包装租赁管理后台原型-20260916.zip')
if os.path.exists(OUT):
    os.remove(OUT)
SEP = chr(92)

files = []
for dp, ds, fs in os.walk(ROOT):
    ds[:] = [d for d in ds if d != '.prompts']
    for f in sorted(fs):
        rel = os.path.relpath(os.path.join(dp, f), ROOT).replace(SEP, '/')
        if f.endswith('.zip') or '/.prompts/' in rel:
            continue
        files.append(rel)

htmls = [f for f in files if f.endswith('.html')]
assert len(htmls) == 132, 'html=%d' % len(htmls)
assert '_data/demo-data.js' in files
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for rel in files:
        z.write(os.path.join(ROOT, rel), rel)

z = zipfile.ZipFile(OUT)
names = set(n for n in z.namelist() if not n.endswith('/'))

# ---- 包内链接自洽校验 ----
dead, checked = [], 0
for n in sorted(names):
    if not n.endswith('.html'):
        continue
    txt = z.read(n).decode('utf-8', 'ignore')
    targets = re.findall(r"go\(\s*['\"]([^'\"]+)['\"]", txt)
    targets += re.findall(r"href=\"([^\"#][^\"]*)\"", txt)
    for t in targets:
        t = unquote(t.split('#')[0].split('?')[0]).strip()
        if not t or t.startswith(('http', 'mailto:', 'tel:', 'javascript:', '#')):
            continue
        base = os.path.dirname(n)
        cand = os.path.normpath(os.path.join(base, t)).replace(SEP, '/')
        checked += 1
        if cand not in names:
            dead.append((n, t))

print('=== 包装租赁管理后台原型-20260916.zip（重打·覆盖过期包） ===')
print('文件总数 %d | HTML %d | _data %d | mobile %d | 交付文档 %d' % (
    len(names), len([n for n in names if n.endswith('.html')]), len([n for n in names if n.startswith('_data/')]),
    len([n for n in names if n.startswith('mobile/')]),
    len([n for n in names if n.endswith(('.md', '.json')) and '/' not in n])))
print('嵌套 zip %d | .prompts %d' % (sum(1 for n in names if n.endswith('.zip')), sum(1 for n in names if '.prompts' in n)))
print('改名后新名在包内:', {k: (k in names) for k in ['财务协同/损益报表.html', '财务协同/收款登记.html', '财务协同/银行回单核销.html', '财务协同/银行回单核销详情.html']})
print('旧名残留文件:', [n for n in names if '水单' in n or '盈亏' in n or '回款' in n])
print('链接自洽校验: 检查 %d 条 | 死链 %d' % (checked, len(dead)))
for d in dead[:8]:
    print('   DEAD', d)
print('下拉修复包内验证（appearance:none 次数）:', z.read('租赁管理/转移出库新建.html').decode('utf-8').count('appearance:none;'))
print('大小 %.1f MB | testzip %s' % (os.path.getsize(OUT) / 1048576, 'OK' if z.testzip() is None else 'FAIL'))
