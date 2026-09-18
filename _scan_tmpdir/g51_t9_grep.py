# -*- coding: utf-8 -*-
"""G51 T9.3: 术语 grep 门——三组旧词（范围=原型目录+根级活文档+agent-handoff·G40 先例口径）"""
import os, io, re, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = '.'
SCAN_DIRS = ['./P3-R01-包装租赁管理后台原型', './agent-handoff']
SCAN_ROOT_FILES = True  # 根级 *.md

PATTERNS = {
    '组1 父项编码|父项名称': re.compile(r'父项编码|父项名称'),
    '组2 正品仓|次品仓': re.compile(r'正品仓|次品仓'),
    '组3 (入库|出库|调出|调入)库房': re.compile(r'(入库|出库|调出|调入)库房'),
}

def classify(path):
    """返回 (是否扫描, 白名单依据 or '' or 'OUT' or 'NEWFIND')"""
    p = path.replace('\\', '/')
    if p.startswith('./.prompts') or '/99-归档' in p or '/backup-' in p:
        return False, '排除目录'
    if p == './agent-handoff/拍板登记.md':
        return True, '拍板登记历史行'
    if p == './P3-R05-列表详情表单弹窗字段一致性排查.md':
        return True, 'P3-R05 历史排查记录'
    if p == './P2-R01-产品需求文档.md':
        return True, 'P2-R01 台账行转述'
    if p == './P1-R04-术语表.md':
        return True, 'P1-R04 改称沿革注记/禁用写法列'
    if re.match(r'\./P3-R01-包装租赁管理后台原型/P3-R01-A0[256]', p):
        return True, 'A02/A05/A06 沿革注记/禁用写法列/概念行文（T8 拍板保留）'
    if p == './P2-R02-决策落实与场景闭环检查报告.md':
        return True, 'NEWFIND（0917 改称未刷·登记新发现）'
    if p == './P3-R01-包装租赁管理后台原型/P3-R01-A03-标注数据.json':
        return True, 'NEWFIND（BOM维护 pin3 note 次品仓漏刷·标注层零写入红线·登记失败清单不修）'
    if p == './P1-R01-需求梳理与功能框架.md':
        return True, 'P1-R01 附录 10.2＝P3-R05 排查记录转述（同源白名单）'
    if p.startswith('./agent-handoff/') and re.search(r'/2026\d{4}-G\d+', p):
        return True, 'agent-handoff 历史 G 号任务档（留档）'
    if p.startswith('./agent-handoff/goal-failures'):
        return True, '历史失败清单留档'
    if p == './agent-handoff/20260917-G51-施工后文档落后修正.md':
        return True, 'G51 任务书 token/白名单定义性引用'
    if p.startswith('./_scan_tmpdir/g51_'):
        return True, 'NEWFIND? 执行者脚本'
    return True, 'OUT'

total = {k: 0 for k in PATTERNS}
wl_hits, out_hits, newfind = {k: [] for k in PATTERNS}, {k: [] for k in PATTERNS}, {k: [] for k in PATTERNS}

targets = []
for d in SCAN_DIRS:
    for dirpath, dirnames, filenames in os.walk(d):
        dirnames[:] = [x for x in dirnames if x not in ('backup-arap-modal-20260910', '__pycache__') and not x.startswith('backup-')]
        for fn in filenames:
            targets.append(os.path.join(dirpath, fn))
if SCAN_ROOT_FILES:
    for fn in os.listdir(ROOT):
        if fn.endswith('.md'):
            targets.append(os.path.join(ROOT, fn))

for full in targets:
    rel = './' + os.path.relpath(full, ROOT).replace('\\', '/')
    if not full.lower().endswith(('.html', '.md', '.js', '.json', '.py')):
        continue
    ok, why = classify(rel)
    if not ok:
        continue
    try:
        txt = io.open(full, encoding='utf-8', errors='ignore').read()
    except Exception:
        continue
    for k, pat in PATTERNS.items():
        n = len(pat.findall(txt))
        if n == 0:
            continue
        total[k] += n
        if why.startswith('NEWFIND'):
            newfind[k].append((rel, n))
        elif why == 'OUT':
            out_hits[k].append((rel, n))
        else:
            wl_hits[k].append((rel, n, why))

print('===== G51 T9.3 术语 grep 门（范围=原型目录+根级 md+agent-handoff·排除 .prompts/99-归档/backup-*） =====')
allok = True
for k in PATTERNS:
    out_n = sum(n for _, n in out_hits[k])
    nf_n = sum(n for _, n in newfind[k])
    print('\n[%s] 全量=%d 白名单内=%d 白名单外=%d 新发现登记=%d' % (
        k, total[k], sum(n for _, n, _ in wl_hits[k]), out_n, nf_n))
    for rel, n, why in sorted(wl_hits[k]):
        print('   WL  %s ×%d —— %s' % (rel, n, why))
    for rel, n in sorted(out_hits[k]):
        print('   OUT %s ×%d' % (rel, n))
    for rel, n in sorted(newfind[k]):
        print('   NEW %s ×%d（登记·不修）' % (rel, n))
    if out_n > 0:
        allok = False
print('\n判定：白名单外=%s' % ('0 PASS' if allok else '非 0 FAIL'))
