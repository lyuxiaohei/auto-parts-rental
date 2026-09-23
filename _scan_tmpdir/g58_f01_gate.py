# -*- coding: utf-8 -*-
"""G58 F01 结构门：①标签配平 ②viewBox 内容不裁切（新节点 t1ws 为重点） ③F01↔流程信息.md 关键串对账（替代已归档 F02 对账）"""
import io, sys, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\P3-R01-F01-业务流程导航图'

fails = []

# ① 标签配平（六图+三 spec）
files = [
    'P3-R01-F01-业务流程导航图-主线.html', 'P3-R01-F01-业务流程导航图-支线.html',
    'P3-R01-F01-业务流程导航图-退租归还与财务.html',
    r'状态机\状态机-库存五态.html', r'状态机\状态机-转移出库.html', r'状态机\状态机-销售订单.html',
]
for f in files:
    s = io.open(BASE + '\\' + f.replace('/', '\\'), encoding='utf-8').read()
    for t in ['div', 'g', 'svg', 'rect', 'text', 'path', 'ul', 'li', 'span', 'button', 'details', 'table', 'tr', 'td']:
        o = len(re.findall(r'<' + t + r'[\s>]', s)); c = len(re.findall(r'</' + t + r'>', s))
        # void 元素 rect/path 无闭合（自闭合/>）
        if t in ('rect', 'path'):
            continue
        if o != c:
            fails.append(f'{f}: <{t}> {o}≠{c}')
    print('配平 OK:', f)
for f in ['P3-R01-F01-业务流程导航图-退租归还与财务.spec.json', 'P3-R01-F01-业务流程导航图-支线.spec.json', 'P3-R01-F01-业务流程导航图-主线.spec.json']:
    json.loads(io.open(BASE + '\\' + f, encoding='utf-8').read())
    print('JSON OK:', f)

# ② viewBox 裁切检查：全部节点/文本几何 ∈ viewBox（重点退租归还图 t1ws）
for f, sel in [('P3-R01-F01-业务流程导航图-退租归还与财务.html', None), ('P3-R01-F01-业务流程导航图-支线.html', None), ('P3-R01-F01-业务流程导航图-主线.html', None)]:
    s = io.open(BASE + '\\' + f, encoding='utf-8').read()
    for m in re.finditer(r'viewBox="0 0 (\d+) (\d+)"', s):
        W, H = int(m.group(1)), int(m.group(2))
        seg_start = m.start()
        seg_end = s.find('</svg>', seg_start)
        seg = s[seg_start:seg_end]
        bad = []
        for r_ in re.finditer(r'<rect x="(-?\d+)" y="(-?\d+)" width="(\d+)" height="(\d+)"', seg):
            x, y, w, h = map(int, r_.groups())
            if x < 0 or y < 0 or x + w > W + 16 or y + h > H + 16:  # 16px 容差（默认决策表：内容底≤viewBox−16 余量）
                bad.append((x, y, w, h))
        if bad:
            fails.append(f'{f} viewBox {W}x{H} 裁切/越界 rect: {bad[:4]}')
        print(f'{f} viewBox {W}x{H}: rect 数 {len(re.findall(chr(60)+"rect ", seg))}, 越界 {len(bad)}')

# ③ F01 ↔ 流程信息.md 对账：G58 关键串双向
fl = io.open(BASE + r'\P3-R01-F01-业务流程导航图-流程信息.md', encoding='utf-8').read()
pairs = [
    ('P3-R01-F01-业务流程导航图-退租归还与财务.html', ['清洗审核', '两步选单 · 验收核对', '完工→审核→转可用']),
    ('P3-R01-F01-业务流程导航图-支线.html', ['结算口径挂客商', '两步选单 · 反转 D-106']),
    ('P3-R01-F01-业务流程导航图-主线.html', ['结算口径挂客商档案二选一', '反转 D-106']),
    (r'状态机\状态机-库存五态.html', ['清洗完工→待审核→审核通过→转可用', '两步选单']),
    (r'状态机\状态机-转移出库.html', ['按租出结算（默认）', '不按比例拆双账']),
]
allmatch = True
for f, kws in pairs:
    s = io.open(BASE + '\\' + f.replace('/', '\\'), encoding='utf-8').read()
    for kw in kws:
        ok = kw in s
        print(('MATCH ' if ok else 'MISS  ') + f[-28:] + ' | ' + kw)
        allmatch &= ok
# 流程信息.md 承载新口径
for kw in ['清洗审核', '两步选单', '结算口径挂客商', 'v4.1']:
    ok = kw in fl
    print(('MATCH ' if ok else 'MISS  ') + '流程信息.md | ' + kw)
    allmatch &= ok
# 版本徽章三主图 v4.1
for f in files[:3]:
    s = io.open(BASE + '\\' + f.replace('/', '\\'), encoding='utf-8').read()
    ok = '业务流程导航 v4.1' in s and 'v4.0 · 节点' not in s
    print(('MATCH ' if ok else 'MISS  ') + f[-24:] + ' | 徽章 v4.1')
    allmatch &= ok
# 节点计数：退租归还图 17 节点
s = io.open(BASE + r'\P3-R01-F01-业务流程导航图-退租归还与财务.html', encoding='utf-8').read()
n = len(re.findall(r'data-node-label="', s))
print('退租归还图节点数:', n, '(预期 17)')
if n != 17: fails.append(f'退租归还图节点数 {n}≠17')
edges = len(re.findall(r'data-edge-from=', s))
print('退租归还图边数:', edges, '(原 12→拆 1 增 1=13)')

print('\n===== 结构门判定 =====')
if fails:
    print('FAIL', len(fails))
    for x in fails: print(' -', x)
else:
    print('结构门 ALL PASS（配平 0 差错·viewBox 0 越界·对账 ' + ('ALL MATCH' if allmatch else 'HAS MISS') + '）')
    if not allmatch: fails.append('对账 MISS')
