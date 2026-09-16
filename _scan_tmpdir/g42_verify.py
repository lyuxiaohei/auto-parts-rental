#!/usr/bin/env python3
# G42 验证门 1+2：语法门（JXA 等价 node --check·G22 先例）＋ T1~T11 全断言 ＋ 旧 token 扫描
import io, re, subprocess, sys

ROOT = '/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental'
P = ROOT + '/P3-R01-包装租赁管理后台原型'
results = []

def check(name, ok, detail=''):
    results.append((name, ok, detail))
    print(('[PASS]' if ok else '[FAIL]'), name, ('—— ' + detail) if detail else '')

def read(p):
    return io.open(P + '/' + p, encoding='utf-8').read()

def jxa(snippet):
    """运行 JXA 数据断言，返回 OUT JSON"""
    sp = ROOT + '/_scan_tmpdir/g42_verify_snippet.js'
    io.open(sp, 'w', encoding='utf-8').write(snippet)
    r = subprocess.run(['osascript', '-l', 'JavaScript', ROOT + '/_scan_tmpdir/g42_jxa.js', sp],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[:300])
    import json
    return json.loads(r.stdout)

# ---------- 验证门 1 · 语法门（node 无机 → JXA new Function 编译等价·G22 先例） ----------
r = subprocess.run(['osascript', '-l', 'JavaScript', ROOT + '/_scan_tmpdir/g42_jxa.js'],
                   capture_output=True, text=True)
check('门1 语法门 demo-data.js（JXA new Function 编译等价 node --check·退出 0·输出含 syntax-check ok）',
      r.returncode == 0 and '"ok": true' in r.stdout, 'stderr=' + r.stderr[:120] if r.returncode else 'compile OK')

# ---------- T1 ----------
s = read('基础数据/BOM维护.html')
check('T1 BOM维护 提交审核=0 · 暂存/取消仍在', s.count('提交审核') == 0 and '暂 存' in s and '取 消' in s)

# ---------- T2 ----------
d = jxa("""
OUT.push({name:'t2', ok: JSON.stringify(D.payments).indexOf('AP-20260810-002')<0 && Object.keys(D.payableBills).indexOf('AP-20260815-003')>=0 && D.payments['PAY-20260818-001'].row.fields.ref==='AP-20260815-003', detail:''});
""")
check('T2 付款死引用→AP-20260815-003（实有键）·旧号全库数据=0', d[0]['ok'])

# ---------- T3 ----------
s = read('租赁管理/租赁单新建.html')
m = re.findall(r'<option[^>]*>(PRJ-\d{4}[^<]*)</option>', s)
codes = [x.split()[0] for x in m]
sel = re.search(r'所属项目：</div>.*?</select>', s, re.S).group(0)
check('T3 新建页六项目各 1 次·PRJ-2601 恰 1·select 内旧称 0',
      sorted(codes) == sorted(['PRJ-2601','PRJ-2602','PRJ-2603','PRJ-2604','PRJ-2605','PRJ-2606'])
      and codes.count('PRJ-2601') == 1
      and s.count('PRJ-2601 华骏重卡·长春基地 驾驶室围板箱租赁') == 1
      and all(sel.count(t) == 0 for t in ['东海商用', '星途', '长风汽制'])
      and sel.count('<option') == 6,
      'options=' + '|'.join(x[:14] for x in m))
s = read('租赁管理/租赁单列表.html')
check('T3 列表筛选含 PRJ-2606', '<option>PRJ-2606</option>' in s)

# ---------- T4 ----------
s = read('财务协同/应收账单.html')
check('T4 应收筛选含预收（预付款（保证金）后）', '预付款（保证金）</option><option>预收</option>' in s)
d = jxa("""
var arb=[];Object.keys(D.dictItems).forEach(function(k){var f=D.dictItems[k].row.fields;if(f.category==='应收账单类型')arb.push(f.name);});
OUT.push({name:'t4a', ok: arb.indexOf('预收')>=0 && arb.length===7, detail: arb.join('|')});
OUT.push({name:'t4b', ok: JSON.stringify(D.receivableBills['AR-2026-09-PRJ2601-YS']).indexOf('预收')>=0, detail:'演示行不动·仍在'});
""")
check('T4 ARB 组 7 值含预收', d[0]['ok'], d[0]['detail'])
check('T4 演示行 AR-2026-09-PRJ2601-YS 不动', d[1]['ok'])
s = read('系统管理/数据字典.html')
check('T4 数据字典 应收账单类型 cnt=7', '<span>应收账单类型</span><span class="cnt">7</span>' in s)

# ---------- T5 ----------
s = read('系统管理/用户权限.html')
m = re.search(r'<div class="head-btns">.*?</div>', s)
check('T5 头部按钮=权限配置·无角色管理', m and '权限配置</button>' in m.group(0) and '角色管理' not in m.group(0))

# ---------- T6 ----------
s = read('财务协同/应收生成.html')
check('T6 FP3-01=0·pin/fab/样式/脚本全清·业务词在',
      s.count('FP3-01') == 0 and s.count('proto-pin') == 0 and s.count('protoNotesFab') == 0
      and s.count('f01-fab') == 0 and '账单类型' in s and '生成方式' in s)
opens = len(re.findall(r'<div\b', s)); closes = s.count('</div>')
check('T6 div 配平', opens == closes, '%d/%d' % (opens, closes))

# ---------- T7a ----------
d = jxa("""
var ok=0;Object.keys(D.partners).forEach(function(k){var f=D.partners[k].row.fields;var t=f.invoiceTaxNo||'';
if(/^9[A-Z0-9]131015MA1F[A-Z0-9]{5}\\d$/.test(t)&&t.length===18&&(D.partners[k].info2||[]).length===5)ok++;});
OUT.push({name:'t7a', ok: ok===Object.keys(D.partners).length, detail: ok+'/'+Object.keys(D.partners).length});
""")
check('T7a partners 8/8 invoiceTaxNo 18 位＋info2 五行', d[0]['ok'], d[0]['detail'])

# ---------- T7b ----------
rep = io.open(ROOT + '/_scan_tmpdir/g42_detail_newfield_diff.md', encoding='utf-8').read()
check('T7b 复查报告末行=修复后差集：0', rep.rstrip().endswith('**修复后差集：0**'))

# ---------- T8 ----------
d = jxa("""
OUT.push({name:'t8', ok: Object.keys(D.returnInbounds).length===10 && Object.keys(D.stockEvents).length===23 && !!D.returnInbounds['TZRK-20260915-012'] && !!D.stockEvents['EV-20260915-023'], detail:'ri='+Object.keys(D.returnInbounds).length+' ev='+Object.keys(D.stockEvents).length});
OUT.push({name:'t8b', ok: Object.keys(D.stockFlows).length===18, detail:'快照未动 18'});
""")
check('T8 returnInbounds=10·stockEvents=23·新键在', d[0]['ok'], d[0]['detail'])
check('T8 stockFlows 快照未动', d[1]['ok'], d[1]['detail'])

# ---------- T9 ----------
d = jxa("""
var n=0;Object.keys(D.rentInReturns).forEach(function(k){if((D.rentInReturns[k].info||[]).some(function(x){return (x.label+x.text).indexOf('押金')>=0;}))n++;});
OUT.push({name:'t9', ok: n===3, detail: n+'/3'});
""")
check('T9 rentInReturns 3/3 押金表达', d[0]['ok'], d[0]['detail'])
s = read('租入管理/租入归还审核.html')
check('T9 审核页 hint 含「押金随归还审核原路退还」', '押金随归还审核原路退还' in s)

# ---------- T10 ----------
d = jxa("""
var arKeys=Object.keys(D.receivableBills), apKeys=Object.keys(D.payableBills);
function collect(o){var c={};Object.keys(o).forEach(function(k){var js=JSON.stringify(o[k]);(js.match(/A[RP]-[0-9]{8}-[0-9A-Za-z\\-]+|A[RP]-[0-9]{4}-[0-9]{2}-[A-Za-z0-9\\-]+/g)||[]).forEach(function(m){c[m]=(c[m]||0)+1;});});return c;}
var bad=[],tot=0;[collect(D.projectDocs),collect(D.boardRows),collect(D.profitRows)].forEach(function(c){Object.keys(c).forEach(function(m){tot+=c[m];if(m[0]+m[1]==='AR'&&arKeys.indexOf(m)<0)bad.push(m);if(m[0]+m[1]==='AP'&&apKeys.indexOf(m)<0)bad.push(m);});});
OUT.push({name:'t10', ok: bad.length===0, detail:'引用'+tot+'·假号'+bad.length});
""")
check('T10 三实体 AR/AP 引用 100% 实有键（Counter）', d[0]['ok'], d[0]['detail'])

# ---------- T11 ----------
s1 = read('财务协同/退款新建.html')
s2 = read('财务协同/退款登记.html')
check('T11 两页各含 4 值',
      all(t in s1 for t in ['采购退货退款', '销售退货退款', '预收退回', '多付退回'])
      and all(t in s2 for t in ['采购退货退款', '销售退货退款', '预收退回', '多付退回']))
d = jxa("""
var tkl=[],thc=[];Object.keys(D.dictItems).forEach(function(k){var f=D.dictItems[k].row.fields;if(f.category==='退款类型')tkl.push(f.name);if(f.category==='退货类型')thc.push(f.name);});
OUT.push({name:'t11a', ok: tkl.join(',')==='采购退货退款,销售退货退款,预收退回,多付退回' && thc.length===2, detail:'TKL:'+tkl.join('|')+' THC:'+thc.length});
OUT.push({name:'t11b', ok: Object.keys(D.refunds).length===5 && !!D.refunds['TKD-20260916-004'] && !!D.refunds['TKD-20260916-005'], detail:'n='+Object.keys(D.refunds).length});
OUT.push({name:'t11c', ok: JSON.stringify(D).indexOf('应付退款（对供应商）')<0 && JSON.stringify(D).indexOf('应收退款（对客户）')<0, detail:'demo-data 旧方向词=0'});
OUT.push({name:'t11d', ok: JSON.stringify(D.payableBills['AP-20260905-012']).indexOf('TKD-20260916-005')>=0, detail:'AP-012 timeline 引用 005'});
""")
check('T11 TKL=4·THC=2 不受扰', d[0]['ok'], d[0]['detail'])
check('T11 refunds=5·两新键在', d[1]['ok'], d[1]['detail'])
check('T11 demo-data 旧方向词=0', d[2]['ok'])
check('T11 AP-012 timeline 引用 TKD-005', d[3]['ok'])
s = read('系统管理/数据字典.html')
check('T11 数据字典 退款类型 cnt=4', '<span>退款类型</span><span class="cnt">4</span>' in s)

# ---------- 旧 token 全库（原型运行文件＋F01 开发规则；文档沿革记载豁免） ----------
import os
tokens = ['AP-20260810-002', '待转移', '确认转移', '应付退款（对供应商）', '应收退款（对客户）']
hits = []
for dirpath, dirnames, filenames in os.walk(P):
    dirnames[:] = [x for x in dirnames if x not in ('.prompts',)]
    for fn in filenames:
        if not fn.endswith(('.html', '.js', '.md')):
            continue
        fp = os.path.join(dirpath, fn)
        if 'backup-' in fp:
            continue
        try:
            t = io.open(fp, encoding='utf-8').read()
        except Exception:
            continue
        for tok in tokens:
            if tok in t:
                hits.append(fp.replace(P + '/', '') + ':' + tok)
# A05/A06 md 沿革注记白名单（D-151 拍板记载）
wl = ['P3-R01-A05-字段字典.md', 'P3-R01-A06-实体关系与状态机.md']
real = [h for h in hits if not any(h.startswith(w) for w in wl)]
check('旧 token 全库=0（原型运行文件；A05/A06 沿革注记白名单）', len(real) == 0, '; '.join(real[:6]) or '残留 0')
wl_hits = [h for h in hits if any(h.startswith(w) for w in wl)]
print('  （白名单沿革注记 %d 处：%s）' % (len(wl_hits), '; '.join(wl_hits[:4])))

fails = [r for r in results if not r[1]]
print()
print('总判定：', len(results) - len(fails), 'PASS /', len(fails), 'FAIL')
sys.exit(1 if fails else 0)
