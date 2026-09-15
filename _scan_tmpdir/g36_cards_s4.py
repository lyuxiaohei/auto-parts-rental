# -*- coding: utf-8 -*-
"""付款/应付/应收生成：分期计划独立成卡（含 #createModal 编辑器根的搬迁）"""
import io, os, re, shutil

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
BAK = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-g36-cards-20260915'

CFG = [
    ('财务协同/付款新建.html', '分期付款计划（比例⇄金额互算 · 笔数不限直至付清）', '付款信息'),
    ('财务协同/应付新建.html', '分期付款计划（比例⇄金额互算 · 笔数不限直至付清）', '账单信息'),
    ('财务协同/应收生成.html', '分期收款计划（比例⇄金额互算 · 笔数不限直至收清）', '生成口径'),
]

for p, heading, _ in CFG:
    fp = os.path.join(ROOT, p.replace('/', os.sep))
    # 1) 从备份还原（去掉上一轮的错误拆卡）
    shutil.copy2(os.path.join(BAK, p.replace('/', os.sep)), fp)
    s = io.open(fp, encoding='utf-8', newline='').read()

    # 2) 取出 #createModal 开启标签（位于 card-head 之后）
    m_open = re.search(r'([ \t]*)<div id="createModal">\r?\n', s)
    assert m_open, p + ' 未找到 #createModal'
    s = s[:m_open.start()] + s[m_open.end():]

    # 3) 标题位置拆卡
    clean, hint = re.match(r'^(.+?)（(.+)）$', heading).groups()
    m_h = re.search(r'<div style="margin:\d+px 0 \d+px;font-size:13px;font-weight:600;">' + re.escape(heading) + r'</div>', s)
    assert m_h, p + ' 标题锚失配'
    repl = ('</div>\r\n'
            '<div class="card">\r\n'
            '  <div class="card-head">\r\n'
            '    <h3 class="card-title">' + clean + '</h3>\r\n'
            '  </div>\r\n'
            '  <div class="pn-hint">' + hint + '</div>\r\n'
            '  <div id="createModal">')
    s = s[:m_h.start()] + repl + s[m_h.end():]
    io.open(fp, 'w', encoding='utf-8', newline='').write(s)
    o = len(re.findall(r'<div(?:\s[^>]*)?>', s)); c = len(re.findall(r'</div>', s))
    print('  %-24s 拆卡 ✓ div %d/%d（差 %d）' % (p.split('/')[-1], o, c, o - c))
