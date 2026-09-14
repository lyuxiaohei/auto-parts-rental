# -*- coding: utf-8 -*-
"""G30 验证门 1：g30_verify 逐行 PASS（三查复核/dictItems 终态/node/库位档案 4 值 0 占位/A05 13 组/差集档在）。
计数口径更正：任务书「46 项/98 项」系早期 7 组草稿算术沿留（46=前 6 组 30+DJ16），T2 分配表实辖
13 组 65 项，终态 49+65+3=117 项 24 组——本脚本按 117/24 断言（偏差已登记 A05 注记+失败清单）。"""
import io, sys, re, os, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'
PROT = ROOT + r'\P3-R01-包装租赁管理后台原型'
ok_all = True

def chk(name, cond, detail=''):
    global ok_all
    print(('PASS' if cond else 'FAIL'), '|', name, ('| ' + detail) if detail else '')
    if not cond: ok_all = False

# ---- 需求三查复核 ----
t = io.open(ROOT + r'\agent-handoff\拍板登记.md', encoding='utf-8', newline='').read()
chk('查① 拍板登记 G30 条目在（已归并 D-93）',
    '2026-09-14' in t and 'G30' in t and 'D-93' in t and '写死枚举值收敛' in t)
ls = subprocess.run(['git', 'ls-files', '--', '_scan_tmpdir/g29_enum_scan.json'],
                    capture_output=True, text=True, cwd=ROOT)
d = json.load(io.open(ROOT + r'\_scan_tmpdir\g29_enum_scan.json', encoding='utf-8'))
chk('查② g29_enum_scan.json git 跟踪+135 组', 'g29_enum_scan.json' in ls.stdout and len(d) == 135,
    'len=%d' % len(d))
t = io.open(ROOT + r'\P2-R01-产品需求文档.md', encoding='utf-8', newline='').read()
nums = sorted(set(int(x) for x in re.findall(r'\| D-(\d+) \|', t)))
chk('查③ P2-R01 V1.1+台账 D 行=93（≥93 无漂移）',
    'V1.1' in t[:400] and len(nums) == 93 and nums == list(range(1, 94)), 'max=D-%02d n=%d' % (nums[-1], len(nums)))

# ---- dictItems 终态（node 实读·走临时 JS 文件避免嵌套引号）----
JS = ROOT + r'\_scan_tmpdir\g30_dump.js'
io.open(JS, 'w', encoding='utf-8', newline='').write(
    'global.window={};global.document={};\n'
    'require(' + json.dumps(PROT.replace('\\', '/') + '/_data/demo-data.js') + ');\n'
    'var di=window.DEMO_DATA.dictItems,ks=Object.keys(di),g={};\n'
    'for(var i=0;i<ks.length;i++){var c=di[ks[i]].row.fields.category;g[c]=(g[c]||0)+1;}\n'
    'console.log(JSON.stringify({n:ks.length,g:Object.keys(g).length,kc:g["库存状态"],rku:g["入库类型"],'
    'cku:g["出库类型"],arb:g["应收账单类型"],apb:g["应付账单类型"],fy:g["费用分类"],fp:g["发票类型"],'
    'kst:g["客商类型"],sjq:g["数据权限范围"],pdk:g["盘点口径"],zq:g["周期单位"],fl:g["物料分类"],'
    'dj:g["待办单据类型"],dw:g["计量单位"],zf:g["支付方式"],zf02:di["ZF-02"].row.fields.name,'
    'dj01:di["DJ-01"].row.fields.name,dj16:di["DJ-16"].row.fields.name}));\n')
r = subprocess.run(['node', JS], capture_output=True, text=True, cwd=PROT)
st = json.loads(r.stdout.strip())
chk('dictItems 终态=117 项 24 组（49+65 新增+DW-07+ZF-03/04）', st['n'] == 117 and st['g'] == 24,
    'n=%d g=%d（任务书 98 系草稿算术·已按分配表 117 断言）' % (st['n'], st['g']))
chk('13 新组计数 5/3/4/6/5/7/2/3/3/2/3/6/16',
    [st['kc'], st['rku'], st['cku'], st['arb'], st['apb'], st['fy'], st['fp'], st['kst'], st['sjq'],
     st['pdk'], st['zq'], st['fl'], st['dj']] == [5, 3, 4, 6, 5, 7, 2, 3, 3, 2, 3, 6, 16])
chk('T1a/T1b 双源统一（DW=7 含托/ZF=4·ZF-02=承兑）', st['dw'] == 7 and st['zf'] == 4 and st['zf02'] == '承兑')
chk('DJ 值序=todoItems 实读序（DJ-01 销售订单/DJ-16 租赁出库）', st['dj01'] == '销售订单' and st['dj16'] == '租赁出库')

r = subprocess.run(['node', '--check', PROT + r'\_data\demo-data.js'], capture_output=True, text=True)
chk('node --check demo-data.js 退出码 0', r.returncode == 0, r.stderr[:120])

# ---- 库位档案 4 值 0 占位 ----
t = io.open(PROT + r'\基础数据\库位档案.html', encoding='utf-8', newline='').read()
chk('库位档案 option 含 KW 4 值且 平面库位/立体库位/待定选项=0',
    all(v in t for v in ['存储位', '拣选位', '暂存位', '不合格品位'])
    and t.count('平面库位') == 0 and t.count('立体库位') == 0 and t.count('待定选项') == 0)

# ---- 数据字典页 ----
t = io.open(PROT + r'\系统管理\数据字典.html', encoding='utf-8', newline='').read()
n_dom = t.count('<div class="dic-item">') + t.count('<div class="dic-item active">')
chk('数据字典页 dic-item=24 行（11+13）', n_dom == 24, 'n=%d' % n_dom)
CATS = ['库存状态', '入库类型', '出库类型', '应收账单类型', '应付账单类型', '费用分类', '发票类型',
        '客商类型', '数据权限范围', '盘点口径', '周期单位', '物料分类', '待办单据类型']
chk('createModal 字典分类 select 含 13 新组 option', all(t.count('<option>%s</option>' % c) == 1 for c in CATS))

# ---- A05 ----
t = io.open(PROT + r'\P3-R01-A05-字段字典.md', encoding='utf-8', newline='').read()
g30note = t[t.find('G30 枚举值字典化'):]
n_groups = sum(1 for p in ['KC-01~05', 'RKU-01~03', 'CKU-01~04', 'ARB-01~06', 'APB-01~05', 'FY-01~07',
                           'FP-01~02', 'KST-01~03', 'SJQ-01~03', 'PDK-01~02', 'ZQ-01~03', 'FL-01~06',
                           'DJ-01~16'] if p in t)
chk('A05 新组行登记=13 组+记录数 117', n_groups == 13 and '记录数 117' in t, '组=%d' % n_groups)

# ---- 差集档 ----
p = ROOT + r'\_scan_tmpdir\g30_接线差集.md'
t = io.open(p, encoding='utf-8', newline='').read() if os.path.exists(p) else ''
chk('g30_接线差集.md 在档（A 20 组+B 未接线清单）', '主数据引用型 20 组' in t and '未接线' in t and t.count('| 20 |') >= 1)

# ---- 白名单门（P3-R01 前缀 ⊆ 4 文件）----
r = subprocess.run(['git', '-c', 'core.quotepath=false', 'status', '--porcelain'],
                   capture_output=True, text=True, encoding='utf-8', cwd=ROOT)
wl = {'P3-R01-包装租赁管理后台原型/_data/demo-data.js',
      'P3-R01-包装租赁管理后台原型/系统管理/数据字典.html',
      'P3-R01-包装租赁管理后台原型/基础数据/库位档案.html',
      'P3-R01-包装租赁管理后台原型/P3-R01-A05-字段字典.md'}
p3 = []
for ln in r.stdout.splitlines():
    fp = ln[3:].strip().strip('"').replace('\\', '/')
    if fp.startswith('P3-R01'):
        p3.append(fp)
chk('白名单门：P3-R01 前缀改动 ⊆ 4 文件', set(p3) <= wl, '改动=%s' % (p3,))

print()
print('g30_verify 总结：', 'ALL PASS' if ok_all else '存在 FAIL')
sys.exit(0 if ok_all else 1)
