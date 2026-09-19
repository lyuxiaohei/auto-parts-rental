# -*- coding: utf-8 -*-
"""G 待办#14：租入归还→归还出库 全站精确替换（字节层·保行尾·每文件 assert·先备份）。
白名单：项目沟通记录/.prompts/_scan_tmpdir/99-归档/backup-*/agent-handoff(历史任务书·活文件手工加行)/skills/.git"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD, NEW = '租入归还', '归还出库'
BACKUP = ROOT / 'backup-ghck-rename-20260919'

targets = []
proto = ROOT / 'P3-R01-包装租赁管理后台原型'
for pat in ('*.html', '*.js', '*.json', '*.md'):
    targets += [p for p in proto.rglob(pat) if 'backup' not in str(p).lower()]
targets += list(ROOT.glob('*.html'))
for f in ['P2-R01-产品需求文档.md', 'P1-R01-需求梳理与功能框架.md', 'P1-R04-术语表.md',
          'P1-R07-租赁管理行业调研.md', 'P2-R02-决策落实与场景闭环检查报告.md',
          'P3-R04-演示场景覆盖梳理.md', 'P3-R06-单据三态字段与板块统一梳理（讨论稿）.md']:
    p = ROOT / f
    if p.exists():
        targets.append(p)

WL = ('项目沟通记录', '.prompts', '_scan_tmpdir', '99-归档', 'backup-', 'agent-handoff', 'skills', '.git')
changed, total_hits = [], 0
for p in targets:
    s = str(p).replace('\\', '/').replace(str(ROOT).replace('\\', '/') + '/', '')
    if any(w in s for w in WL):
        continue
    b = p.read_bytes()
    if OLD.encode('utf-8') not in b:
        continue
    n = b.count(OLD.encode('utf-8'))
    dst = BACKUP / p.relative_to(ROOT)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, dst)
    nb = b.replace(OLD.encode('utf-8'), NEW.encode('utf-8'))
    assert OLD.encode('utf-8') not in nb
    p.write_bytes(nb)
    changed.append((str(p.relative_to(ROOT)), n))
    total_hits += n

print('改动文件数:', len(changed), ' 替换总处数:', total_hits)
few = [c for c in changed if c[1] >= 3]
for f, n in sorted(few):
    print('  %3d  %s' % (n, f))
print('  其余 %d 个文件各 1-2 处（侧边栏菜单/引用/单处提及）' % (len(changed) - len(few)))
