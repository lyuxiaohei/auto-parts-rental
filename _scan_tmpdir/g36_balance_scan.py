# -*- coding: utf-8 -*-
"""全 75 个 G36 页标签配平扫描 + 定位多余闭合标签"""
import io, os, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
PAGES = [
    '基础数据/物料新建.html', '基础数据/客商新建.html', '基础数据/库位新建.html', '基础数据/客商开票资料.html',
    '基础数据/客商收货信息.html', '基础数据/物料详情.html', '基础数据/客商详情.html', '基础数据/库位详情.html',
    '基础数据/BOM版本查看.html', '项目管理/项目新建.html', '项目管理/上下游绑定.html', '项目管理/编码规则.html',
    '采购管理/采购订单详情.html', '采购管理/采购订单审核.html', '采购管理/采购入库详情.html', '采购管理/采购入库审核.html',
    '采购管理/采购退货详情.html', '采购管理/采购退货审核.html', '采购管理/采购退货新建.html',
    '销售管理/销售订单详情.html', '销售管理/销售订单审核.html', '销售管理/销售订单新建.html',
    '销售管理/销售出库详情.html', '销售管理/销售出库审核.html', '销售管理/销售出库新建.html',
    '销售管理/销售退货详情.html', '销售管理/销售退货审核.html', '销售管理/销售退货新建.html',
    '租赁管理/租赁单详情.html', '租赁管理/租赁单审核.html', '租赁管理/租赁单新建.html',
    '租赁管理/租赁出库详情.html', '租赁管理/租赁出库确认.html', '租赁管理/退租入库详情.html',
    '租赁管理/退租入库审核.html', '租赁管理/退租入库新建.html', '租赁管理/器具出租履历.html',
    '租入管理/租入单详情.html', '租入管理/租入单审核.html', '租入管理/租入单新建.html',
    '租入管理/租入入库详情.html', '租入管理/租入入库确认.html', '租入管理/租入归还详情.html',
    '租入管理/租入归还审核.html', '租入管理/租入归还新建.html',
    '仓储作业/其他入库详情.html', '仓储作业/其他入库审核.html', '仓储作业/其他入库新建.html',
    '仓储作业/其他出库详情.html', '仓储作业/其他出库审核.html', '仓储作业/其他出库新建.html',
    '仓储作业/库存流水.html', '仓储作业/盘点详情.html', '仓储作业/盘点审核.html',
    '仓储作业/调拨详情.html', '仓储作业/调拨审核.html', '仓储作业/调拨新建.html',
    '财务协同/付款新建.html', '财务协同/付款详情.html', '财务协同/付款确认.html', '财务协同/回款详情.html',
    '财务协同/应付新建.html', '财务协同/应付详情.html', '财务协同/应收生成.html', '财务协同/应收详情.html',
    '财务协同/开票新建.html', '财务协同/开票详情.html', '财务协同/收款新建.html', '财务协同/水单核销详情.html',
    '财务协同/退款新建.html', '财务协同/退款详情.html',
    '系统管理/字典项新建.html', '系统管理/用户新建.html', '系统管理/角色新建.html', '系统管理/权限配置.html',
]
TAGS = ['div', 'section', 'table', 'thead', 'tbody', 'tr', 'td', 'th', 'select', 'ul', 'li', 'button', 'label', 'textarea']

def rd(p):
    return io.open(os.path.join(ROOT, p), encoding='utf-8', errors='ignore').read()

bad = []
for p in PAGES:
    s = rd(p)
    issues = []
    for t in TAGS:
        o = len(re.findall(r'<' + t + r'(?:\s[^>]*)?>', s))
        c = len(re.findall(r'</' + t + r'>', s))
        if o != c:
            issues.append('%s %d/%d' % (t, o, c))
    if issues:
        bad.append((p, issues))
print('==== 标签不平衡页 ====')
for p, iss in bad:
    print('  %-30s %s' % (p.split('/')[-1], ', '.join(iss)))
print('  合计 %d / %d 页' % (len(bad), len(PAGES)))

# 定位多余闭合：逐行追踪 div 深度，找深度异常归零处
print()
print('==== 多余 </div> 定位 ====')
for p, iss in bad:
    if not any('div' in i for i in iss):
        continue
    s = rd(p)
    depth = 0; line = 1; marks = []
    for m in re.finditer(r'<div(?:\s[^>]*)?>|</div>|\n', s):
        g = m.group(0)
        if g == '\n':
            line += 1
        elif g.startswith('</'):
            depth -= 1
            if depth == 0:
                marks.append((line, depth))
        else:
            depth += 1
    print('  %s 结束 depth=%d；深度归零行样本=%s' % (p.split('/')[-1], depth, marks[-4:]))
