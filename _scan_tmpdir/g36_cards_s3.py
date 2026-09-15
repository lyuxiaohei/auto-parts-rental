# -*- coding: utf-8 -*-
"""卡片化改造 · 阶段 3：带标签的明细表单行 → 独立成卡（备注上移到表单卡末尾）"""
import io, os, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

CFG = [
    # 页, 明细标签, 卡标题, 备注标签, 行 id（可选）
    ('租赁管理/退租入库新建.html', '退回明细', '退回明细', '验收备注', None),
    ('租入管理/租入归还新建.html', '归还明细', '归还明细', '备注', 'riDetailRow'),
]


def rd(p):
    return io.open(os.path.join(ROOT, p.replace('/', os.sep)), encoding='utf-8', newline='').read()


def wr(p, s):
    io.open(os.path.join(ROOT, p.replace('/', os.sep)), 'w', encoding='utf-8', newline='').write(s)


def block_span(s, start_idx):
    """从 start_idx 的 <div …> 起做深度扫描，返回 (start, end)"""
    i = s.index('>', start_idx) + 1
    depth = 1
    while i < len(s):
        m = re.compile(r'<div\b|</div>').search(s, i)
        if not m:
            raise AssertionError('未闭合')
        if m.group(0) == '</div>':
            depth -= 1
            if depth == 0:
                return start_idx, m.end()
        else:
            depth += 1
        i = m.end()
    raise AssertionError('扫描越界')


for p, dlabel, ctitle, nlabel, rid in CFG:
    s = rd(p)
    log = []
    # 1) 取出备注行
    mi = s.index(nlabel + '：')
    ns = s.rfind('<div class="form-row"', 0, mi)
    nb = s[ns:s.index('>', ns) + 1]
    a, b = block_span(s, ns)
    note_block = s[a:b]
    assert nlabel in note_block
    s = s[:a] + s[b:]
    log.append('备注行取出（%s）' % nlabel)

    # 2) 明细行 → 卡
    di = s.index(dlabel + '：')
    ds = s.rfind('<div class="form-row"', 0, di)
    dtag_end = s.index('>', ds) + 1
    dtag = s[ds:dtag_end]                      # <div class="form-row" …>
    inner_start = s.index('<div class="form-label"', dtag_end)
    wrapper_start = s.index('<div style="flex:1;min-width:0;">', inner_start)
    old_open = s[ds:wrapper_start]
    assert dlabel in old_open and dtag in old_open
    card_open = ('</div>\r\n'
                 '<div class="card"' + ((' id="%s"' % rid) if rid else '') + '>\r\n'
                 '  <div class="card-head">\r\n'
                 '    <h3 class="card-title">' + ctitle + '</h3>\r\n'
                 '  </div>\r\n'
                 '  ')
    s = s[:ds] + card_open + s[wrapper_start:]
    log.append('明细行 → 卡片「%s」' % ctitle)

    # 3) 备注行插到表单卡末尾（新卡边界之前）
    marker = '</div>\r\n<div class="card"' + ((' id="%s"' % rid) if rid else '') + '>'
    assert s.count(marker) == 1, '卡边界锚 %d' % s.count(marker)
    s = s.replace(marker, note_block + '\r\n' + marker)
    log.append('备注行 → 表单卡末尾')
    wr(p, s)
    print('%-28s %s' % (p.split('/')[-1], ' | '.join(log)))
