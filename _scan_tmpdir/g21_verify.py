#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G21 验证门 1：全量断言（逐行 PASS/FAIL）。
覆盖：demo-data 四键/字典/feeSecTitle · 数据字典静态卡+pin-2 · 两表单页三段式 · 租入单域两页 · 项目详情 · 全站按天/元天清零 · HTML 总数 115。
"""
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROT = os.path.join(ROOT, 'P3-R01-包装租赁管理后台原型')
results = []


def chk(name, cond, detail=''):
    results.append(('PASS' if cond else 'FAIL', name, detail))


dd = open(os.path.join(PROT, '_data/demo-data.js'), encoding='utf-8').read()
dzd = open(os.path.join(PROT, '系统管理/数据字典.html'), encoding='utf-8').read()
cp = open(os.path.join(PROT, '基础数据/产品档案.html'), encoding='utf-8').read()
tpl = open(os.path.join(PROT, '基础数据/弹窗/新建产品.html'), encoding='utf-8').read()
rzx = open(os.path.join(PROT, '租赁管理/弹窗/租入单新建.html'), encoding='utf-8').read()
rzb = open(os.path.join(PROT, '租赁管理/租入单列表.html'), encoding='utf-8').read()
xmxq = open(os.path.join(PROT, '项目管理/项目详情.html'), encoding='utf-8').read()

# ===== demo-data =====
chk('demo rentInMode=12', dd.count('rentInMode') == 12, str(dd.count('rentInMode')))
chk('demo rentalMode=12', dd.count('rentalMode') == 12, str(dd.count('rentalMode')))
chk("demo 'BF-04'=1", dd.count("'BF-04'") == 1, str(dd.count("'BF-04'")))
chk("demo 'BF-05'=1", dd.count("'BF-05'") == 1, str(dd.count("'BF-05'")))
bf03 = [l for l in dd.splitlines() if "'BF-03'" in l]
chk('demo BF-03 行停用+tag-gray', len(bf03) == 1 and '"status": "停用"' in bf03[0] and 'tag-gray' in bf03[0])
chk('demo feeSecTitle 旧=0', dd.count('租入明细（多货品 · 月租/按套 · 无日租金）') == 0)
chk('demo feeSecTitle 新=5', dd.count('租入明细（多货品 · 按月/按次 · 无日租金）') == 5, str(dd.count('租入明细（多货品 · 按月/按次 · 无日租金）')))

# ===== 数据字典.html =====
chk('字典 按年计租=1', dzd.count('按年计租') == 1, str(dzd.count('按年计租')))
chk('字典 按日计租=1', dzd.count('按日计租') == 1, str(dzd.count('按日计租')))
azhang = re.search(r'<tr>\s*<td>按张</td>.*?</tr>', dzd, re.S)
chk('字典 按张行 tag-gray=1', azhang is not None and azhang.group(0).count('tag-gray') == 1)
chk('字典 cnt=5 串=1', dzd.count('计费方式</span><span class="cnt">5') == 1, str(dzd.count('计费方式</span><span class="cnt">5')))
chk('字典 （暂估）=0', dzd.count('（暂估）') == 0 and dzd.count('暂估') == 0, str(dzd.count('暂估')))
pin2 = re.search(r'id="proto-pin-2".*', dzd, re.S).group(0)[:2000]
chk('字典 pin-2 无「预留」', '预留' not in pin2)

# ===== 产品档案 / 新建产品 =====
for tag, s in [('产品档案', cp), ('新建产品', tpl)]:
    chk('%s rentInModeSel=1' % tag, s.count('id="rentInModeSel"') == 1)
    chk('%s rentalModeSel=1' % tag, s.count('id="rentalModeSel"') == 1)
    chk('%s unitSel=1' % tag, s.count('id="unitSel"') == 1)
    chk('%s g21RentHint 定义=1' % tag, s.count('function g21RentHint') == 1)
    chk('%s 两旧 placeholder=0' % tag, s.count('如 45.00 元/只·月（无租入来源留空）') == 0 and s.count('按周期或按次，如 60.00 元/只·月 / 15.00 元/块·次') == 0)

# ===== 租入单域两页 =====
for tag, s in [('租入单新建', rzx), ('租入单列表', rzb)]:
    chk('%s 新段标题=1' % tag, s.count('租入明细（多货品 · 计费方式：按月 / 按次）') == 1)
    chk('%s <option selected>按月=1' % tag, s.count('<option selected>按月</option>') == 1)
    chk('%s <option selected>按次=1' % tag, s.count('<option selected>按次</option>') == 1)
    chk('%s 月租/按套 option=0' % tag, s.count('月租</option>') == 0 and s.count('按套</option>') == 0)

# ===== 项目详情 =====
chk('项目详情 按月计租·按次计费=1', xmxq.count('<div class="dval">按月计租 · 按次计费</div>') == 1)

# ===== 全站 按天/元/天 清零 =====
hits = []
for dp, dn, fn in os.walk(PROT):
    dn[:] = [d for d in dn if d not in ('.git',)]
    for f in fn:
        if f.endswith(('.html', '.js')):
            p = os.path.join(dp, f)
            t = open(p, encoding='utf-8').read()
            for kw in ['按天', '元/天']:
                if kw in t:
                    hits.append('%s(%s×%d)' % (p.replace(PROT + '/', ''), kw, t.count(kw)))
chk('全站 按天=0 元/天=0', not hits, '; '.join(hits))

# ===== HTML 总数 115 =====
n = sum(1 for dp, dn, fn in os.walk(PROT) for f in fn if f.endswith('.html') and '.git' not in dp)
chk('原型 HTML 总数=115', n == 115, str(n))

fails = [r for r in results if r[0] == 'FAIL']
for st, name, detail in results:
    print(st, name, ('(%s)' % detail) if detail else '')
print('====', 'ALL PASS' if not fails else 'FAIL %d 项' % len(fails), '共 %d 项' % len(results))
sys.exit(1 if fails else 0)
