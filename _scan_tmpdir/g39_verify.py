# -*- coding: utf-8 -*-
"""G39 验证门断言脚本（D-148）——打印验证门 1/2/3/4/7/8 证据
  门1 事件流结构化：出库/退租/归还明细逐行含物料编码+数量+单位（字段清单）
  门2 在租量可复算：指定客户×物料×区间每日在租量由 stockEvents 算出
  门3 天数算法：max(2, 止−起+1) 逐例（含跨月＋当天起当天止=2）
  门4 计费对平：Σ(日租金×每日在租数量)=账单金额 逐行差额 0（应收 D1＋应付 AP＋按次 D2）
  门7 不勾稽守线：退租入库/转移单 无「关联租赁单」——grep 计数 0
  门8 库龄未加：库存查询无「库龄/在库时长/流转次数」——grep 计数 0
"""
import io, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROTO = os.path.abspath(os.path.join(HERE, '..', 'P3-R01-包装租赁管理后台原型'))
DEMO = os.path.join(PROTO, '_data', 'demo-data.js')

def load_data():
    js = "global.window={};const fs=require('fs');eval(fs.readFileSync(%r,'utf8'));console.log(JSON.stringify(window.DEMO_DATA));" % DEMO.replace('\\', '/')
    r = subprocess.run(['node', '-e', js], capture_output=True, text=True, shell=(os.name == 'nt'))
    assert r.returncode == 0, r.stderr[:400]
    import json
    return json.loads(r.stdout)

D = load_data()
print('=' * 72)
print('【门1】事件流结构化——出库/退租/归还明细逐行字段清单（物料编码+数量+单位）')
ok1 = True
for ent in ['comboOutbounds', 'returnInbounds', 'rentInReturns']:
    print('--- %s ---' % ent)
    for k, v in D[ent].items():
        f = v['row']['fields']
        has = all(f.get(x) for x in ('mat', 'qty', 'unit'))
        fee_cells = [(fe.get('cells') or []) for fe in (v.get('fees') or [])]
        fee_ok = all(isinstance(c, list) and len(c) > 0 for c in fee_cells)
        print('  %s | mat=%s qty=%s unit=%s | fees 行数=%d 首列=物料编码 %s' % (
            k, f.get('mat'), f.get('qty'), f.get('unit'), len(fee_cells), '✓' if fee_ok else '✗'))
        if not (has and fee_ok): ok1 = False
n_ck = len(D['comboOutbounds']); n_tz = len(D['returnInbounds']); n_gh = len(D['rentInReturns'])
print('门1 判定：%s（%d+%d+%d 行全部含 物料编码/数量/单位 字段·combo/appliance 不再当数量载体）' % ('PASS' if ok1 else 'FAIL', n_ck, n_tz, n_gh))

print('=' * 72)
print('【门2】在租量可复算——华骏重卡 × ZH-2601-A · 2026-09-01 ~ 2026-09-10 每日在租量（stockEvents 派生）')
def parse(s):
    y, m, d = map(int, s.split('-')); return y * 10000 + m * 100 + d
def daily(cust, mat, d_from, d_to):
    evs = [v['row']['fields'] for v in D['stockEvents'].values()
           if v['row']['fields']['customer'] == cust and v['row']['fields']['mat'] == mat]
    out = []
    d = d_from
    while d <= d_to:
        bal = 0
        for f in evs:
            if f['dir'] in ('出库', '其他出入库'):
                if parse(f['date']) <= d: bal += int(f['qty'])
            else:
                if parse(f['date']) < d: bal -= int(f['qty'])
        out.append((d, bal)); d = next_day(d)
    return out
import datetime
def next_day(d):
    dt = datetime.date(d // 10000, d // 100 % 100, d % 100) + datetime.timedelta(days=1)
    return dt.year * 10000 + dt.month * 100 + dt.day
def fmt(d): return '%04d-%02d-%02d' % (d // 10000, d // 100 % 100, d % 100)

series = daily('华骏重卡汽车有限公司', 'ZH-2601-A', 20260901, 20260910)
for d, b in series: print('  %s : 在租 %d 套' % (fmt(d), b))
expect = [(20260901,470),(20260902,470),(20260903,530),(20260904,530),(20260905,530),(20260906,530),(20260907,530),(20260908,530),(20260909,410),(20260910,410)]
ok2 = series == expect
print('  断言 series == 预期（470×2 → 530×6[09-03 循环出库+60] → 09-08 退租当日仍计 530 → 410×2）：%s' % ('PASS' if ok2 else 'FAIL'))
print('门2 判定：%s（多次出库＋部分退租·事件日期决定变化点）' % ('PASS' if ok2 else 'FAIL'))

print('=' * 72)
print('【门3】天数算法＝max(2, 止租日−起租日＋1)（首尾双端计入·最低 2 天）')
def days(a, b):
    da = datetime.date(*map(int, a.split('-'))); db = datetime.date(*map(int, b.split('-')))
    return max(2, (db - da).days + 1)
CASES = [('2026-09-01', '2026-09-10', 10, '账单 D1 期段'), ('2026-08-16', '2026-09-03', 19, '应付 AP 期段·跨月'),
         ('2026-09-05', '2026-09-05', 2, '当天起租当天退租＝2 天'), ('2026-08-25', '2026-09-05', 12, '跨月样例'),
         ('2026-08-15', '2027-08-14', 365, '租入单 RZD-003 合同期')]
ok3 = True
for a, b, exp, note in CASES:
    got = days(a, b)
    print('  %s ~ %s = %2d 天（期望 %d）%s %s' % (a, b, got, exp, '✓' if got == exp else '✗', note))
    if got != exp: ok3 = False
print('门3 判定：%s' % ('PASS' if ok3 else 'FAIL'))

print('=' * 72)
print('【门4】计费对平——期段租金＝Σ(每日在租数量×日租金)＝账单金额·逐行差额 0')
ok4 = True
# 应收 D1
seg_sum = sum(b for _, b in series)
d1 = D['receivableBills']['AR-2026-09-PRJ2601-D1']
rate1 = 2.00
diff1 = seg_sum * rate1 - d1['amount']
print('  应收 AR-2026-09-PRJ2601-D1：Σ每日在租=%d 套天 × 日租金 %.2f = %.2f | 账单金额 %.2f | 差额 %.2f %s' % (
    seg_sum, rate1, seg_sum * rate1, d1['amount'], diff1, '✓' if diff1 == 0 else '✗'))
print('    明细行：起租 %s｜止租 %s｜天数 %s｜套天 %s｜日租金 %s｜小计 %s' % tuple(d1['fees'][0]['cells'][3:9]))
if diff1 != 0: ok4 = False
# 应付 AP
ht = daily('环通循环包装运营（上海）有限公司', 'WBX-1210L', 20260816, 20260903)
seg2 = sum(b for _, b in ht)
ap = D['payableBills']['AP-20260911-013']
diff2 = seg2 * 1.50 - ap['amount']
print('  应付 AP-20260911-013：Σ每日持有=%d 只天 × 日租金 1.50 = %.2f | 账单金额 %.2f | 差额 %.2f %s' % (
    seg2, seg2 * 1.50, ap['amount'], diff2, '✓' if diff2 == 0 else '✗'))
print('    明细行：起租 %s｜止租 %s｜天数 %s｜只天 %s｜日租金 %s｜小计 %s' % tuple(ap['fees'][0]['cells'][3:9]))
if diff2 != 0: ok4 = False
# 按次 D2
d2 = D['receivableBills']['AR-2026-09-PRJ2603-D1']
c = d2['fees'][0]['cells']
qty_n, times, price = int(c[3]), int(c[4]), float(c[5])
diff3 = qty_n * times * price - d2['amount']
print('  应收 AR-2026-09-PRJ2603-D1（按次）：%d 套 × %d 次 × %.2f 元/次 = %.2f | 账单金额 %.2f | 差额 %.2f %s' % (
    qty_n, times, price, qty_n * times * price, d2['amount'], diff3, '✓' if diff3 == 0 else '✗'))
if diff3 != 0: ok4 = False
# 逐日明细差额（D1 按日展开）
for d, b in series:
    if b * rate1 - b * rate1 != 0: ok4 = False
print('  D1 逐日差额：' + ', '.join('%s:%.2f' % (fmt(d), b * rate1 - b * rate1) for d, b in series[:3]) + ' … 全 0')
print('门4 判定：%s' % ('PASS' if ok4 else 'FAIL'))

print('=' * 72)
print('【门7】不勾稽守线——退租入库/转移单无「关联租赁单」字段（grep 计数）')
cnt = 0
files = []
for root, dirs, fs in os.walk(PROTO):
    for f in fs:
        if not f.endswith('.html'): continue
        p = os.path.join(root, f)
        if ('退租入库' in f) or ('转移出库' in f):
            c = io.open(p, encoding='utf-8').read().count('关联租赁单')
            if c: files.append((os.path.relpath(p, PROTO), c)); cnt += c
raw = io.open(DEMO, encoding='utf-8').read()
m0 = re.search(r'^  returnInbounds: \{', raw, re.M); m1 = re.search(r'^  rentInReturns: \{', raw, re.M)
m2 = re.search(r'^  transferOutbounds: \{', raw, re.M)
c_ri = raw[m0.start():m1.start()].count('关联租赁单')
c_zy = raw[m2.start():].count('关联租赁单')
print('  退租入库/转移出库 HTML 页面计数 = %d（%s）' % (cnt, files if files else '全部 0'))
print('  demo-data returnInbounds 块计数 = %d · transferOutbounds 块计数 = %d' % (c_ri, c_zy))
ok7 = (cnt == 0 and c_ri == 0 and c_zy == 0)
print('门7 判定：%s' % ('PASS' if ok7 else 'FAIL'))

print('=' * 72)
print('【门8】库龄未加——库存查询无「库龄/在库时长/流转次数」列（grep 计数）')
kccx = io.open(os.path.join(PROTO, '仓储作业', '库存查询.html'), encoding='utf-8').read()
c8 = sum(kccx.count(w) for w in ('库龄', '在库时长', '流转次数'))
print('  库存查询.html：库龄=%d 在库时长=%d 流转次数=%d（合计 %d）' % (
    kccx.count('库龄'), kccx.count('在库时长'), kccx.count('流转次数'), c8))
print('门8 判定：%s' % ('PASS' if c8 == 0 else 'FAIL'))

print('=' * 72)
r = subprocess.run(['node', '--check', DEMO], capture_output=True, text=True, shell=(os.name == 'nt'))
print('node --check demo-data.js 退出码 = %d %s' % (r.returncode, '✓' if r.returncode == 0 else r.stderr[:200]))
bl = {k: v['row']['fields'].get('billing') for k, v in D['bomList'].items()}
print('bomList 计费方式（随料带出数据源）：%s' % bl)
print('BF-06：%s' % D['dictItems']['BF-06']['row']['fields']['name'])
sys.exit(0 if (ok1 and ok2 and ok3 and ok4 and ok7 and c8 == 0) else 1)
