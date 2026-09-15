# -*- coding: utf-8 -*-
"""以 采购管理/采购订单新建.html 为样板，扫描 G36 改造页的样式一致性偏差（只读分析）"""
import io, os, re, json
from collections import Counter

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
SAMPLE = '采购管理/采购订单新建.html'
SAMPLE_DETAIL = '项目管理/项目详情.html'

PAGES = [
    # B1
    '基础数据/物料新建.html', '基础数据/客商新建.html', '基础数据/库位新建.html', '基础数据/客商开票资料.html',
    '基础数据/客商收货信息.html', '基础数据/物料详情.html', '基础数据/客商详情.html', '基础数据/库位详情.html',
    '基础数据/BOM版本查看.html', '项目管理/项目新建.html', '项目管理/上下游绑定.html', '项目管理/编码规则.html',
    # B2
    '采购管理/采购订单详情.html', '采购管理/采购订单审核.html', '采购管理/采购入库详情.html', '采购管理/采购入库审核.html',
    '采购管理/采购退货详情.html', '采购管理/采购退货审核.html', '采购管理/采购退货新建.html',
    '销售管理/销售订单详情.html', '销售管理/销售订单审核.html', '销售管理/销售订单新建.html',
    '销售管理/销售出库详情.html', '销售管理/销售出库审核.html', '销售管理/销售出库新建.html',
    '销售管理/销售退货详情.html', '销售管理/销售退货审核.html', '销售管理/销售退货新建.html',
    # B3
    '租赁管理/租赁单详情.html', '租赁管理/租赁单审核.html', '租赁管理/租赁单新建.html',
    '租赁管理/租赁出库详情.html', '租赁管理/租赁出库确认.html', '租赁管理/退租入库详情.html',
    '租赁管理/退租入库审核.html', '租赁管理/退租入库新建.html', '租赁管理/器具出租履历.html',
    '租入管理/租入单详情.html', '租入管理/租入单审核.html', '租入管理/租入单新建.html',
    '租入管理/租入入库详情.html', '租入管理/租入入库确认.html', '租入管理/租入归还详情.html',
    '租入管理/租入归还审核.html', '租入管理/租入归还新建.html',
    # B4
    '仓储作业/其他入库详情.html', '仓储作业/其他入库审核.html', '仓储作业/其他入库新建.html',
    '仓储作业/其他出库详情.html', '仓储作业/其他出库审核.html', '仓储作业/其他出库新建.html',
    '仓储作业/库存流水.html', '仓储作业/盘点详情.html', '仓储作业/盘点审核.html',
    '仓储作业/调拨详情.html', '仓储作业/调拨审核.html', '仓储作业/调拨新建.html',
    # B5
    '财务协同/付款新建.html', '财务协同/付款详情.html', '财务协同/付款确认.html', '财务协同/回款详情.html',
    '财务协同/应付新建.html', '财务协同/应付详情.html', '财务协同/应收生成.html', '财务协同/应收详情.html',
    '财务协同/开票新建.html', '财务协同/开票详情.html', '财务协同/收款新建.html', '财务协同/水单核销详情.html',
    '财务协同/退款新建.html', '财务协同/退款详情.html',
    '系统管理/字典项新建.html', '系统管理/用户新建.html', '系统管理/角色新建.html', '系统管理/权限配置.html',
]

def rd(p):
    return io.open(os.path.join(ROOT, p), encoding='utf-8', errors='ignore').read()

s = rd(SAMPLE)
print('==== 样板 %s 指纹 ====' % SAMPLE)
print('form-label 形态: div=%d  span=%d' % (s.count('<div class="form-label"'), s.count('<span class="form-label"')))
print('caret 形态: 字符▾=%d  svg=%d' % (s.count('<span class="caret">▾</span>'), len(re.findall(r'<span class="caret"><svg', s))))
print('input-box 宽度分布:', Counter(re.findall(r'class="input-box[^"]*"[^>]*style="width:(\d+)px', s)))
print('submit-bar:', s.count('class="submit-bar"'), '| card:', s.count('class="card"'), '| card-head:', s.count('class="card-head"'))
print('返回列表按钮:', s.count('返回列表'))
print('textarea:', len(re.findall(r'<textarea[^>]*>', s)), '| resize 值:', Counter(re.findall(r'<textarea[^>]*style="([^"]*)"', s)))
print('页内额外 style 块:', len(re.findall(r'<style[^>]*>', s)), '个；含 style id=', re.findall(r'<style id="([^"]+)"', s))
print()

rows = []
for p in PAGES:
    if not os.path.exists(os.path.join(ROOT, p)):
        rows.append((p, 'MISSING', []))
        continue
    t = rd(p)
    isdetail = ('详情' in p) or ('履历' in p) or ('流水' in p) or ('确认' in p) or ('审核' in p) or ('BOM版本查看' in p)
    isform = not isdetail
    issues = []
    # 1) form-label 标签形态
    nd, ns = t.count('<div class="form-label"'), t.count('<span class="form-label"')
    if ns > 0:
        issues.append('form-label 用 <span>（样板用 <div>）×%d' % ns)
    # 2) caret 形态
    nsvg = len(re.findall(r'<span class="caret"><svg', t))
    if nsvg > 0:
        issues.append('下拉箭头用 svg（样板用字符 ▾）×%d' % nsvg)
    # 3) 控件宽
    ws = Counter(re.findall(r'class="input-box[^"]*"[^>]*style="width:(\d+)px', t))
    badw = sorted(w for w in ws if w not in ('380', '220'))
    if badw:
        issues.append('控件宽非 380/220: %s' % badw)
    if '380' not in ws and isform:
        issues.append('表单页无 380px 控件（宽度集合=%s）' % dict(ws))
    # 4) 提交条
    has_bar = 'class="submit-bar"' in t
    if isform and not has_bar:
        issues.append('表单页缺 .submit-bar')
    if has_bar:
        m = re.search(r'\.submit-bar\s*\{[^}]*\}', t)
        if not m:
            issues.append('有 submit-bar 但缺 .submit-bar CSS 定义')
        elif 'justify-content:center' not in m.group(0).replace(' ', ''):
            issues.append('submit-bar 未居中')
    # 5) 表单页顶部冗余「返回列表」
    if isform and '返回列表' in t:
        issues.append('表单页含「返回列表」（样板无·取消已承担返回）')
    # 6) 备注 textarea 规范
    for ta in re.findall(r'<textarea[^>]*style="([^"]*)"', t):
        style = ta.replace(' ', '')
        if 'min-height:72px' not in style and 'min-height:72' not in style and 'maxlength' not in t[:0]:
            if 'height:100%' in style or 'resize:none' in style:
                issues.append('备注 textarea 非样板式（%s）' % ta[:60])
                break
    # 7) 页内额外 style 覆盖
    extra = re.findall(r'<style(?![^>]*id="(?:modal-css|proto-notes-style|detail-modal-css|f01-fab-style)")[^>]*>', t)
    # 只统计重复定义核心类的覆盖块
    for st in re.findall(r'<style[^>]*>(.*?)</style>', t, re.S):
        if re.search(r'\.form-row\s*(?:\.input-box|\{)|\.input-box\s*\{', st) and 'width:380px' in st.replace(' ', ''):
            issues.append('页内 style 覆盖 .form-row .input-box 宽度')
            break
    # 8) 残留 modal 结构（content 区内）
    if re.search(r'<div class="modal-header"', t) or re.search(r'<div class="modal-footer"', t):
        if '<div class="modal-overlay"' not in t:
            issues.append('残留 modal-header/footer 但无 overlay 容器')
    # 9) 核心 CSS 是否齐全
    need = ['.form-row{', '.form-label{', '.input-box{', '.select-box{', '.btn{', '.card{']
    miss = [c for c in need if c.replace(' ', '') not in t.replace(' ', '').replace('\n', '')]
    if miss:
        issues.append('缺核心 CSS: %s' % miss)
    # 10) 详情/审核页结构
    if isdetail:
        if '.dt-sec{' not in t and 'detail-generic' not in t and 'bill-detail' not in t:
            issues.append('详情类页缺 .dt-sec/渲染器引入')
    rows.append((p, 'OK' if not issues else 'ISSUE', issues))

print('==== 逐页偏差 ====')
iss_cnt = 0
for p, st, issues in rows:
    if st == 'ISSUE':
        iss_cnt += 1
        print('%s' % p)
        for i in issues:
            print('    - %s' % i)
print()
print('总页数 %d ｜ 有偏差 %d ｜ 一致 %d' % (len(rows), iss_cnt, len(rows) - iss_cnt))
# 汇总偏差类型
cnt = Counter()
for p, st, issues in rows:
    for i in issues:
        key = i.split('（')[0].split(':')[0].split('×')[0]
        cnt[key] += 1
print()
print('==== 偏差类型汇总 ====')
for k, v in cnt.most_common():
    print('%3d 次  %s' % (v, k))
