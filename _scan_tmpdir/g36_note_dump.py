# -*- coding: utf-8 -*-
"""导出 20 个表单移植页的「备注行」「注入 style」「控件宽来源」原始标记"""
import io, os, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
PAGES = ['采购管理/采购退货新建.html', '销售管理/销售订单新建.html', '销售管理/销售出库新建.html', '销售管理/销售退货新建.html',
         '租赁管理/租赁单新建.html', '租赁管理/退租入库新建.html', '租入管理/租入单新建.html', '租入管理/租入归还新建.html',
         '仓储作业/其他入库新建.html', '仓储作业/其他出库新建.html', '仓储作业/调拨新建.html',
         '财务协同/付款新建.html', '财务协同/应付新建.html', '财务协同/应收生成.html', '财务协同/开票新建.html',
         '财务协同/收款新建.html', '财务协同/退款新建.html',
         '系统管理/字典项新建.html', '系统管理/用户新建.html', '系统管理/角色新建.html', '系统管理/权限配置.html']

def rd(p):
    return io.open(os.path.join(ROOT, p), encoding='utf-8', errors='ignore').read()

for p in PAGES:
    s = rd(p)
    print('=' * 78)
    print(p)
    # 注入 style
    m = re.search(r'<style>\.form-row \.input-box\{[^}]*\}</style>', s)
    print('  注入 style:', repr(m.group(0)) if m else 'NONE')
    # 备注行
    for m2 in re.finditer(r'<div class="form-row"[^>]*>\s*\r?\n?\s*<span class="form-label">[^<]*(?:<span[^>]*>[^<]*</span>)?[^<]*备注[^<]*</span>.*?\r?\n\s*</div>', s, re.S):
        print('  备注行:')
        print('    ' + m2.group(0).replace('\r', '').replace('\n', '\n    '))
        break
    else:
        print('  备注行: NONE')
    # 控件宽来源统计
    withw = len(re.findall(r'class="input-box[^"]*"[^>]*style="width:\d+px', s))
    total = len(re.findall(r'class="input-box', s))
    print('  input-box 总数=%d 其中带内联 width=%d' % (total, withw))
    print('  内联宽度值:', sorted(set(re.findall(r'style="width:(\d+)px', s))))
