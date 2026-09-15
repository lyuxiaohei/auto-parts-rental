# -*- coding: utf-8 -*-
"""把本次插入的卡片块行尾归一为宿主主导行尾（LF 主导页 → LF）"""
import io, os, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
# LF 主导页（本次插入 CRLF 的）
PAGES = ['采购管理/采购退货新建.html', '销售管理/销售退货新建.html', '租赁管理/租赁单新建.html',
         '租入管理/租入单新建.html', '财务协同/应付新建.html', '财务协同/应收生成.html',
         '租赁管理/退租入库新建.html', '租入管理/租入归还新建.html']

# 阶段 2 插入块的 LF 化（标题 + 可选 head-btns + card-head 收尾 + 可选 hint）
PAT2 = re.compile(
    r'</div>\r\n<div class="card">\r\n  <div class="card-head">\r\n'
    r'    <h3 class="card-title">([^<]*)</h3>\r\n'
    r'((?:    <div class="head-btns">.*?</div>\r\n)?)'
    r'  </div>\r\n'
    r'((?:  <div class="pn-hint">.*?</div>\r\n)?)'
)


def lf2(m):
    return ('</div>\n<div class="card">\n  <div class="card-head">\n'
            '    <h3 class="card-title">' + m.group(1) + '</h3>\n'
            + m.group(2).replace('\r\n', '\n')
            + '  </div>\n'
            + m.group(3).replace('\r\n', '\n'))


# 阶段 3 插入块
PAT3 = re.compile(
    r'</div>\r\n<div class="card"( id="[^"]*")?>\r\n  <div class="card-head">\r\n'
    r'    <h3 class="card-title">([^<]*)</h3>\r\n  </div>\r\n  '
)


def lf3(m):
    return ('</div>\n<div class="card"%s>\n  <div class="card-head">\n'
            '    <h3 class="card-title">%s</h3>\n  </div>\n  ' % (m.group(1) or '', m.group(2)))


for p in PAGES:
    fp = os.path.join(ROOT, p.replace('/', os.sep))
    s = io.open(fp, encoding='utf-8', newline='').read()
    n2 = len(PAT2.findall(s))
    n3 = len(PAT3.findall(s))
    s = PAT2.sub(lf2, s)
    s = PAT3.sub(lf3, s)
    # 阶段 3 的备注插入：note_block 后的 '\r\n' → '\n'
    s = s.replace('</div>\r\n<div class="card" id="riDetailRow">', '</div>\n<div class="card" id="riDetailRow">')
    io.open(fp, 'w', encoding='utf-8', newline='').write(s)
    fc = s.count('\r\n'); lc = s.count('\n') - fc
    print('  %-24s 归一 %d(阶段2)/%d(阶段3) 块 → CRLF=%d LF=%d' % (p.split('/')[-1], n2, n3, fc, lc))
