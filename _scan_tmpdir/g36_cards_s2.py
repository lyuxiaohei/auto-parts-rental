# -*- coding: utf-8 -*-
"""卡片化改造 · 阶段 2：卡内分段（明细/计划）独立成卡 + 卡头标题 + 添加按钮入卡头"""
import io, os, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
HEAD_RE = re.compile(r'<div style="margin:\d+px 0 \d+px;font-size:13px;font-weight:600;(?:color:#1a1a1a;)?">([^<]+)</div>')


def rd(p):
    return io.open(os.path.join(ROOT, p.replace('/', os.sep)), encoding='utf-8', newline='').read()


def wr(p, s):
    io.open(os.path.join(ROOT, p.replace('/', os.sep)), 'w', encoding='utf-8', newline='').write(s)


def split_title(t):
    m = re.match(r'^(.+?)（(.+)）$', t)
    return (m.group(1), m.group(2)) if m else (t, None)


# 页 → (期望标题列表, 需搬入卡头的按钮)
CFG = {
    '采购管理/采购退货新建.html': (['退货明细（可退上限内填写）'],
                              '<button class="btn btn-dashed btn-sm" onclick="addRetRow()">+ 添加一行</button>'),
    '销售管理/销售订单新建.html': (['订单明细', '订单附件（PDF / 邮件截图 · 演示上传）'],
                              '<button class="btn btn-dashed btn-sm" style="width:100%;margin-top:8px;">+ 添加一行</button>'),
    '销售管理/销售出库新建.html': (['出库明细'],
                              '<button class="btn btn-dashed btn-sm" style="width:100%;margin-top:8px;">+ 添加一行</button>'),
    '销售管理/销售退货新建.html': (['退货明细（可退上限内填写）'],
                              '<button class="btn btn-dashed btn-sm" onclick="addRetRow()">+ 添加一行</button>'),
    '租赁管理/租赁单新建.html': (['租赁器具明细'],
                             '<button class="btn btn-dashed btn-sm" style="width:100%;margin-top:8px;">+ 添加一行</button>'),
    '租入管理/租入单新建.html': (['租入明细（多货品 · 计费方式：按月 / 按次）'], None),
    '财务协同/付款新建.html': (['分期付款计划（比例⇄金额互算 · 笔数不限直至付清）'], None),
    '财务协同/应付新建.html': (['分期付款计划（比例⇄金额互算 · 笔数不限直至付清）'], None),
    '财务协同/应收生成.html': (['分期收款计划（比例⇄金额互算 · 笔数不限直至收清）'], None),
}

for p, (titles, btn) in CFG.items():
    s = rd(p)
    heads = HEAD_RE.findall(s)
    want = [t for t in titles if heads.count(t) == 1]
    if not want:
        print('%-28s 已为卡片式（跳过）' % p.split('/')[-1])
        continue
    titles = want
    log = []
    for t in titles:
        clean, hint = split_title(t)
        head_btns = ''
        if btn and btn in s:
            b = btn.replace(' style="width:100%;margin-top:8px;"', '').replace('+ 添加一行', '添加一行')
            head_btns = '    <div class="head-btns">' + b + '</div>\r\n'
            s = s.replace(btn, '', 1)
            log.append('按钮入卡头: %s' % clean)
        repl = ('</div>\r\n'
                '<div class="card">\r\n'
                '  <div class="card-head">\r\n'
                '    <h3 class="card-title">' + clean + '</h3>\r\n'
                + head_btns +
                '  </div>\r\n'
                + ('  <div class="pn-hint">' + hint + '</div>\r\n' if hint else ''))
        old = '<div style="margin:' + re.escape('')  # placeholder
        m = re.search(r'<div style="margin:\d+px 0 \d+px;font-size:13px;font-weight:600;(?:color:#1a1a1a;)?">' + re.escape(t) + r'</div>', s)
        assert m, '%s 标题锚失配: %s' % (p, t)
        s = s[:m.start()] + repl + s[m.end():]
        log.append('成卡: %s%s' % (clean, '（hint 保留）' if hint else ''))
    wr(p, s)
    print('%-28s %s' % (p.split('/')[-1], ' | '.join(log)))

# 全站复核：不应再有 13px/600 的内联分段标题（排除弹窗与表头）
print()
print('==== 残留内联分段标题复核 ====')
n = 0
for dp, dn, fns in os.walk(ROOT):
    if '.git' in dp:
        continue
    for f in sorted(fns):
        if not f.endswith('.html'):
            continue
        fp = os.path.join(dp, f)
        x = io.open(fp, encoding='utf-8', errors='ignore').read()
        for m in HEAD_RE.finditer(x):
            ln = x[:m.start()].count('\n') + 1
            seg = x[max(0, m.start() - 900):m.start()]
            if 'modal-body' in seg[-400:]:
                continue  # 弹窗内的分段标题不属卡片体系
            print('  %-40s L%-5d %s' % (os.path.relpath(fp, ROOT).replace(os.sep, '/'), ln, m.group(1)[:34]))
            n += 1
print('  合计', n)
