# -*- coding: utf-8 -*-
"""G19b T2：38 业务页注入 pc-auth.js（dry-run 默认 → --apply）
锚=</body> 前插 <script src="{prefix}_data/pc-auth.js"></script>；
prefix：根级页=''，一级子目录页='../'。assert 注入数=38。"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROT = ROOT / 'P3-R01-包装租赁管理后台原型'
APPLY = '--apply' in sys.argv

BIZ = [l.strip() for l in (ROOT/'_scan_tmpdir'/'g19b_bizpages.txt').read_text(encoding='utf-8').splitlines() if l.startswith('  ')]
BIZ = [b.strip() for b in BIZ]
assert len(BIZ) == 38, f'业务页清单 {len(BIZ)} ≠ 38'

results, bad = [], []
plan = []
for rel in BIZ:
    f = PROT / rel
    s = f.read_text(encoding='utf-8')
    prefix = '../' if '/' in rel else ''
    tag = f'<script src="{prefix}_data/pc-auth.js"></script>'
    if 'pc-auth.js' in s:
        bad.append(f'{rel}: 已存在 pc-auth 引用')
        continue
    n_body = s.count('</body>')
    if n_body != 1:
        bad.append(f'{rel}: </body> 锚 {n_body} 处')
        continue
    plan.append((rel, f, s, tag))

print(f"dry-run：可注入 {len(plan)}/38；异常 {len(bad)}")
for b in bad:
    print('  ' + b)
if len(plan) != 38 or bad:
    print('!! 计数不符，未写回')
    sys.exit(3)

if APPLY:
    for rel, f, s, tag in plan:
        assert s.count('</body>') == 1
        f.write_text(s.replace('</body>', tag + '\n</body>'), encoding='utf-8')
    print(f"APPLY 完成：38 页注入")
    # 复检：每页恰 1 处引用
    ok = 0
    for rel, f, s, tag in plan:
        s2 = f.read_text(encoding='utf-8')
        assert s2.count('pc-auth.js') == 1, f'{rel} 引用数异常'
        assert '</body>' in s2 and '</html>' in s2, f'{rel} 尾标签缺失'
        ok += 1
    print(f"复检 PASS：{ok}/38 页各恰 1 处引用+尾标签在")
    # 排除面复检：弹窗/F01/mobile/登录页 = 0
    excl = 0
    for f in sorted(PROT.rglob('*.html')):
        p = f.as_posix()
        rel2 = p.split('P3-R01-包装租赁管理后台原型/', 1)[1]
        if 'backup' in p or '_scan_tmpdir' in p: continue
        if rel2 in BIZ: continue
        if 'pc-auth.js' in f.read_text(encoding='utf-8'):
            print(f'!! 排除面命中: {rel2}')
            excl += 1
    print(f"排除面（弹窗/F01/mobile/登录页/其他）引用数 = {excl}")
    assert excl == 0, '排除面存在引用'
else:
    print('dry-run 模式（未写回）。加 --apply 执行。')
