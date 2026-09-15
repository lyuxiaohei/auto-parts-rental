# -*- coding: utf-8 -*-
"""G34 验证脚本：完成判定 1-5 证据输出（配平/字段序列/改名计数/字典/组件断言）"""
import io, re, json, subprocess, sys

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
F = {
    'page_prod': ROOT + r'\基础数据\产品档案.html',
    'tpl_prod':  ROOT + r'\基础数据\弹窗\新建产品.html',
    'page_kst':  ROOT + r'\基础数据\客商管理.html',
    'tpl_inv':   ROOT + r'\基础数据\弹窗\客商开票资料.html',
    'page_loc':  ROOT + r'\基础数据\库位档案.html',
    'tpl_loc':   ROOT + r'\基础数据\弹窗\新建库位.html',
    'dict_page': ROOT + r'\系统管理\数据字典.html',
    'demo_data': ROOT + r'\_data\demo-data.js',
}

def load(p):
    with io.open(p, encoding='utf-8', newline='') as f:
        return f.read()

print('=== 判定1：配平断言（六文件 <div>==</div>）===')
ok = True
for k, p in F.items():
    if k == 'demo_data':
        continue
    t = load(p)
    a, b = t.count('<div'), t.count('</div>')
    tag = 'PASS' if a == b else 'FAIL'
    if a != b: ok = False
    print('%s  %-22s <div=%d  </div>=%d  %s' % (tag, p.split('\\')[-1], a, b, '==' if a == b else '!='))
assert ok, '配平失败'

print()
print('=== 判定2：新建物料弹窗 form-label 序列（双层）===')
EXPECT = ['物料编码', '物料名称', '物料类型', '供应商内部编码', '物料型号', '规格', '单位', '参考未税采购价(元)', '参考未税销售价(元)', '参考未税租入价', '参考未税租赁价', '备注']
for k in ('page_prod', 'tpl_prod'):
    t = load(F[k])
    i = t.find('<div class="modal-body">')
    j = t.find('tax-sec-title', i)
    body = t[i:j]
    labels = re.findall(r'<span class="form-label">(?:<span class="req">\*</span>)?([^<]+)</span>', body)
    labels = [x.strip() for x in labels]
    seq_ok = labels == EXPECT
    print('%s  %-14s %s' % ('PASS' if seq_ok else 'FAIL', k, ' → '.join(labels)))
    assert seq_ok, '%s 字段序列不符' % k

print()
print('=== 判定3：改名全站（旧标签残留=0·新标签计数）===')
import os
tot_old_i, tot_old_m, tot_new_i, tot_new_m = 0, 0, 0, 0
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        if not f.endswith(('.html', '.js', '.md')):
            continue
        p = os.path.join(dp, f)
        t = load(p)
        oi = len(re.findall(r'(?<!供应商)内部编码', t))
        om = len(re.findall(r'型号', t)) - t.count('物料型号') - t.count('规格型号') - t.count('一个型号')
        ni = t.count('供应商内部编码')
        nm = t.count('物料型号')
        if oi or om or ni or nm:
            print('  %-46s 旧内部编码=%d 旧型号=%d 新供应商内部编码=%d 新物料型号=%d' % (p.replace(ROOT, '.').replace('\\', '/'), oi, om, ni, nm))
        tot_old_i += oi; tot_old_m += om; tot_new_i += ni; tot_new_m += nm
print('全站合计：旧「内部编码」残留=%d（期望 0·A05 台账历史行除外）旧「型号」残留=%d 新「供应商内部编码」=%d 新「物料型号」=%d' % (tot_old_i, tot_old_m, tot_new_i, tot_new_m))

print()
print('=== 判定4：字典（node --check + 组数/项数 + SL/JSQ 值域）===')
r = subprocess.run(['node', '--check', F['demo_data']], capture_output=True, text=True)
print('node --check 退出码 = %d %s' % (r.returncode, '(0=PASS)' if r.returncode == 0 else r.stderr))
assert r.returncode == 0
t = load(F['demo_data'])
# 用 node 提取 dictItems 结构（避免手写解析器误判）
js = ("var D=require(%r);" % F['demo_data'].replace('\\', '/')) if False else None
node_code = ("const fs=require('fs');const src=fs.readFileSync(%r,'utf8');" % F['demo_data'].replace('\\', '/')
    + "const window={};eval(src);const D=window.DEMO_DATA.dictItems||{};"
    + "const g={};let n=0;for(const k of Object.keys(D)){const f=(D[k].row||{}).fields||{};g[f.category]=g[f.category]||[];g[f.category].push(f.name);n++;}"
    + "console.log(JSON.stringify({total:n,groups:Object.keys(g).length,"
    + "SL:g['供应商税率']||[],JSQ:g['结算周期']||[],KW:g['库位类型']||[]}));")
r2 = subprocess.run(['node', '-e', node_code], capture_output=True, text=True, shell=False)
assert r2.returncode == 0, r2.stderr
info = json.loads(r2.stdout.strip())
print('dictItems 项数=%d（期望 141） 组数=%d（期望 28）' % (info['total'], info['groups']))
assert info['total'] == 141 and info['groups'] == 28
print('SL 供应商税率 %d 值: %s' % (len(info['SL']), '/'.join(info['SL'])))
print('JSQ 结算周期 %d 值: %s' % (len(info['JSQ']), '/'.join(info['JSQ'])))
print('KW 库位类型 %d 值: %s' % (len(info['KW']), '/'.join(info['KW'])))
assert info['SL'] == ['0%', '1%', '3%', '6%', '9%', '13%']
assert info['JSQ'] == ['预付', '货到付款', '周结', '半月结', '月结', '发票后 30 天', '发票后 60 天', '发票后 90 天', '发票后 120 天']

print()
print('=== 判定5：组件改造断言 ===')
tp, tt = load(F['page_prod']), load(F['tpl_prod'])
for name, t in [('产品档案', tp), ('新建产品', tt)]:
    a = t.count('<textarea id="prodRemarkTa"')
    b = t.count("g34TaCount")
    c = len(re.findall(r'SL\.map\(function\(o\)', t))
    d = len(re.findall(r'JSQ\.map\(function\(o\)', t))
    w = t.count('width:220px;flex:none;')
    e = t.count("maxlength=\"200\"")
    print('%s：物料备注textarea=%d(期望1) maxlength200=%d(期望1) 计数函数=%d 税率select=%d(期望1) 结算周期JSQ=%d(期望1) 220px短占位=%d(期望4)' % (name, a, e, b, c, d, w))
    assert a == 1 and e == 1 and c == 1 and d == 1 and w == 4
tl, tk = load(F['page_loc']), load(F['tpl_loc'])
for name, t in [('库位档案', tl), ('新建库位', tk)]:
    a = len(re.findall(r'<textarea placeholder="选填" style="flex:1', t))
    b = t.count('id="locTypeSel"')
    c = t.count('仓库名称')
    d = t.count('平面库位') + t.count('待定选项')
    print('%s：库位备注textarea=%d(期望1) 类型字典select=%d(期望1) 仓库名称标签=%d(期望1) 脏占位残留=%d(期望0)' % (name, a, b, c, d))
    assert a == 1 and b == 1 and c == 1 and d == 0
assert tk.count('原料区 RA') == 0 and tl.count('原料区 RA') == 0, '库区残留未清'
print('库区残留（原料区 RA 等）=0 PASS')
ti, tkk = load(F['tpl_inv']), load(F['page_kst'])
for name, t in [('客商开票资料', ti), ('客商管理', tkk)]:
    a = t.count('id="invSettleSel"')
    b = t.count("f.category === '结算周期'")
    c = t.count('月结')  # 静态兜底存在
    print('%s：结算周期select id=%d(期望1) JSQ渲染脚本=%d(期望1) 静态兜底(月结)=%d' % (name, a, b, c))
    assert a == 1 and b == 1
td = load(F['dict_page'])
a = td.count('<div class="dic-item')  # 含 active 态行
b = td.count('<option>供应商税率</option>')
print('数据字典：dic-item 左列表=%d 行(期望28·含active) select新组option=%d(期望1)' % (a, b))
assert a == 28 and b == 1

print()
print('=== 判定5b：productTaxes 税率值落在 SL/JSQ 值域内 ===')
node_code2 = ("const fs=require('fs');const src=fs.readFileSync(%r,'utf8');" % F['demo_data'].replace('\\', '/')
    + "const window={};eval(src);const T=window.DEMO_DATA.productTaxes||{};"
    + "const SL=['0%','1%','3%','6%','9%','13%'];const JSQ=['预付','货到付款','周结','半月结','月结','发票后 30 天','发票后 60 天','发票后 90 天','发票后 120 天'];"
    + "let bad=[];for(const k of Object.keys(T)){const f=(T[k].row||{}).fields||{};if(SL.indexOf(f.taxRate)<0)bad.push(k+':'+f.taxRate);if(JSQ.indexOf(f.settleCycle)<0)bad.push(k+':'+f.settleCycle);}"
    + "console.log(JSON.stringify({rows:Object.keys(T).length,bad:bad}));")
r3 = subprocess.run(['node', '-e', node_code2], capture_output=True, text=True)
assert r3.returncode == 0, r3.stderr
info2 = json.loads(r3.stdout.strip())
print('productTaxes %d 行·值域外=%s（期望 []）' % (info2['rows'], info2['bad']))
assert info2['bad'] == []

print()
print('ALL G34 VERIFY-1..5 PASS')
