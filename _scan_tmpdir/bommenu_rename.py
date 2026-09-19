# -*- coding: utf-8 -*-
"""菜单「BOM」→「BOM组合」（道远 09-19）：仅菜单标签与 F01 入口/模块名——
统一模式 `BOM.html')">BOM<`（覆盖普通/selected/根级三形态，不误伤 href 与 BOM维护 等合法串）；
F01 两处（tspan 链接文字 + 节点标签）；A02 菜单树两行。字节层替换·先备份·逐文件 assert。"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
BACKUP = ROOT / 'backup-bommenu-20260919'

def swap(p, pairs):
    b = p.read_bytes()
    n = 0
    for old, new in pairs:
        c = b.count(old.encode('utf-8'))
        if c:
            dst = BACKUP / p.relative_to(ROOT)
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists():
                shutil.copy2(p, dst)
            b = b.replace(old.encode('utf-8'), new.encode('utf-8'))
            n += c
    if n:
        p.write_bytes(b)
    return n

changed, total = [], 0
MENU = [("BOM.html')\">BOM<", "BOM.html')\">BOM组合<")]
for p in PROTO.rglob('*.html'):
    if 'mobile' in str(p) or 'backup' in str(p).lower():
        continue
    n = swap(p, MENU)
    if n:
        changed.append((str(p.relative_to(ROOT)), n)); total += n

# F01 两处（菜单链接文字 + 模块节点标签；带锚防误伤）
f01 = PROTO / 'P3-R01-F01-业务流程导航图.html'
n = swap(f01, [
    ('基础数据/BOM.html"><tspan fill="#2563eb">BOM<', '基础数据/BOM.html"><tspan fill="#2563eb">BOM组合<'),
    ('text-anchor="middle">BOM</text>', 'text-anchor="middle">BOM组合</text>'),
])
changed.append(('F01', n)); total += n

# A02 菜单树两行
a02 = PROTO / 'P3-R01-A02-页面类型与入口对照表.md'
n = swap(a02, [
    ('；BOM → `基础数据/BOM.html`', '；BOM组合 → `基础数据/BOM.html`'),
    ('| 7 | 基础数据/BOM.html | BOM | 列表页 | 菜单「基础资料 → BOM」 |', '| 7 | 基础数据/BOM.html | BOM组合 | 列表页 | 菜单「基础资料 → BOM组合」 |'),
])
changed.append(('A02', n)); total += n

pages = len([c for c in changed if c[1]])
print('改动文件 %d 个 / 替换 %d 处（菜单页 %d + F01 %d + A02 %d）' % (
    len(changed), total,
    sum(c[1] for c in changed if c[0].endswith('.html') and 'F01' not in c[0]),
    dict(changed).get('F01', 0), dict(changed).get('A02', 0)))

# 残留校验（白名单外 `')">BOM<` 应为 0）
resid = 0
for p in PROTO.rglob('*.html'):
    if 'mobile' in str(p) or 'backup' in str(p).lower():
        continue
    resid += p.read_bytes().count(b'\')">BOM<')
print('菜单形态残留:', resid)
