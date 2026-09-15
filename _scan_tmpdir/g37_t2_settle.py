# -*- coding: utf-8 -*-
"""G37 T2：项目档案「转租结算方式」属性（两值·默认按租出结算）
1. demo-data projects 8 行：fields +settle ＋ cells 插格（供应商 tags 后、项目状态前）
2. 项目档案.html：thead 插「转租结算方式」列（供应商后）
3. 项目新建.html：项目负责人行后加 radio 行
4. 项目详情.html：计费方式 drow 后加 drow
口径：PRJ-2603=按终端结算（ZY-002 带出源），其余默认按租出结算。"""
import io, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def rd(p): return io.open(os.path.join(ROOT, p), encoding='utf-8', newline='').read()
def wr(p, s): io.open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='').write(s)

def swap(s, old, new, n=1):
    for oe, ne in ((old, new), (old.replace('\n', '\r\n'), new.replace('\n', '\r\n'))):
        c = s.count(oe)
        if c == n:
            return s.replace(oe, ne)
    raise AssertionError('expect %d got %d/%d for %r' % (n, s.count(old), s.count(old.replace('\n', '\r\n')), old[:60]))

# ---------- 1. demo-data projects（幂等守卫） ----------
p = os.path.join('_data', 'demo-data.js')
s = rd(p)
if '"settle"' not in s:
    i = s.index('projects: {')
    j = s.index('\n  },', i)
    blk = s[i:j]
    lines = blk.split('\n')
    keys = ['PRJ-2601', 'PRJ-2602', 'PRJ-2603', 'PRJ-2604', 'PRJ-2605', 'PRJ-2606', 'PRJ-2599', 'PRJ-2598']
    nf = nc = 0
    for idx, ln in enumerate(lines):
        k = None
        for kk in keys:
            if ("'" + kk + "': {") in ln:
                k = kk
                break
        if not k:
            continue
        val = '按终端结算' if k == 'PRJ-2603' else '按租出结算'
        # fields：在 "status": 前插 settle
        m = re.search(r'("fields": \{.*?)"status"', ln)
        assert m, k + ' fields/status not found'
        ln = ln[:m.end(1)] + '"settle": "%s", ' % val + ln[m.end(1):]
        nf += 1
        # cells：在「项目状态 tag」格（字面 <span class=\"tag tag-xx\">进行中…·双引号转义）前插结算方式格
        anchor2 = ', "<span class=\\"tag tag-'
        pa = ln.find(anchor2)
        assert pa > -1, k + ' cells status tag not found'
        ln = ln[:pa] + ', "%s"' % val + ln[pa:]
        nc += 1
        lines[idx] = ln
    assert nf == 8 and nc == 8, (nf, nc)
    s = s[:i] + '\n'.join(lines) + s[j:]
    wr(p, s)
    print('demo-data projects：fields +settle %d 行 / cells +格 %d 行' % (nf, nc))
else:
    print('demo-data projects：已含 settle（跳过）')

# ---------- 2. 项目档案.html thead（幂等守卫） ----------
p2 = os.path.join('项目管理', '项目档案.html')
s2 = rd(p2)
if s2.count('<th>转租结算方式</th>') == 0:
    assert s2.count('<th>供应商</th>') == 1
    nl2 = '\r\n' if '\r\n' in s2[s2.index('<th>供应商</th>')-5:s2.index('<th>供应商</th>')] else '\n'
    s2 = s2.replace('<th>供应商</th>', '<th>供应商</th>' + nl2 + '<th>转租结算方式</th>')
    wr(p2, s2)
    print('项目档案.html：thead +转租结算方式列（供应商后）')
else:
    print('项目档案.html：已含（跳过）')

# ---------- 3. 项目新建.html radio 行（项目负责人为末行：行块尾=卡片闭合前） ----------
p3 = os.path.join('项目管理', '项目新建.html')
s3 = rd(p3)
if '转租结算方式' not in s3:
    m3 = re.search(r'(<option selected>江强</option><option>江强·其他</option></select><span class="caret">▾</span></div>\s*</div>\s*</div>)', s3)
    assert m3, '项目负责人行块未命中'
    ins = ('\n  <div class="form-row">\n    <div class="form-label">转租结算方式：</div>\n    <div>\n'
           '      <div><span class="radio checked"><span class="dot"></span>按租出结算</span><span class="radio" style="margin-right:0;"><span class="dot"></span>按终端结算</span></div>\n'
           '      <div class="pn-hint">客户转租（转移出库）后的租金结算主体：按租出结算＝租金仍向直接客户计收（默认·转移单不进财务链路）；按终端结算＝转移生效后后续账单主体切换为终端客户（历史账单不回改）。转移出库单可按单覆盖此默认值。</div>\n'
           '    </div>\n  </div>')
    nl = '\r\n' if '\r\n' in s3[m3.end()-30:m3.end()] else '\n'
    s3 = s3[:m3.end(1)] + ins.replace('\n', nl) + s3[m3.end(1):]
    wr(p3, s3)
    print('项目新建.html：+转租结算方式 radio 行')
else:
    print('项目新建.html：已含（跳过）')

# ---------- 4. 项目详情.html drow（幂等守卫） ----------
p4 = os.path.join('项目管理', '项目详情.html')
s4 = rd(p4)
if '转租结算方式' not in s4:
    m4 = re.search(r'(<div class=\"drow\"><div class=\"dlabel\">计费方式</div><div class=\"dval\">[^<]*</div></div>)', s4)
    assert m4, '计费方式 drow not found'
    ins4 = '<div class="drow"><div class="dlabel">转租结算方式</div><div class="dval">按租出结算</div></div>'
    s4 = s4[:m4.end(1)] + ins4 + s4[m4.end(1):]
    wr(p4, s4)
    print('项目详情.html：+转租结算方式 drow')
else:
    print('项目详情.html：已含（跳过）')
print('T2 DONE')
