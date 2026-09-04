# -*- coding: utf-8 -*-
"""
详情落地页补齐 · 共享库（2026-09-04 任务书第十节 A/B/C/D 组）
- 四段式详情弹窗构建器（单据头字段网格/物料明细表/关联单据互溯链/流转时间线）
- 页面注入引擎：锚点=最早出现的绑定脚本（菜单折叠/弹窗开关/overlay forEach）之前 → 满足 R4 位次纪律
- 独立模板生成器：抄 弹窗/采购入库审核.html 包壳惯例，默认打开，go 路径 ../ → ../../ 改写
纪律：全部精确替换 + assert 计数；禁止整页生成覆盖业务页。
"""
import re
from pathlib import Path

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")

# ==================== 样式块（注入业务页与独立模板共用） ====================
DETAIL_CSS = '''<style id="detail-modal-css">
/* 详情弹窗（四段式）专用样式：段落标题 / 关联链 / 流转时间线 */
.dt-sec{font-size:13px;font-weight:600;color:#262626;margin:0 0 10px;padding-left:8px;border-left:3px solid #1677ff;line-height:1.3}
.modal-body .dt-sec:not(:first-child){margin-top:18px}
.chain{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.chain .node{border:1px solid #f0f0f0;border-radius:6px;padding:8px 12px;background:#fafafa;min-width:126px}
.chain .node .n-role{font-size:11px;color:#8c8c8c}
.chain .node .n-name{font-size:12.5px;font-weight:600;margin-top:2px;word-break:break-all}
.chain .link-arrow{color:#8c8c8c}
.tl{position:relative;padding-left:16px}
.tl::before{content:'';position:absolute;left:4px;top:6px;bottom:6px;width:2px;background:#e6f4ff}
.tl-i{position:relative;padding:0 0 12px 6px;font-size:12.5px;color:#262626}
.tl-i:last-child{padding-bottom:0}
.tl-i::before{content:'';position:absolute;left:-16px;top:5px;width:7px;height:7px;border-radius:50%;background:#fff;border:2px solid #1677ff}
.tl-i.off::before{border-color:#d9d9d9}
.tl-i .tl-t{color:#8c8c8c;font-size:12px;margin-right:8px;font-variant-numeric:tabular-nums}
.tl-i .tl-who{color:#8c8c8c;font-size:12px;margin-left:8px}
</style>'''

# ==================== markup 构件 ====================

def drow(label, value):
    return '<div class="drow"><div class="dlabel">%s</div><div class="dval">%s</div></div>' % (label, value)

def node(role, name, link=None, cur=False):
    inner = '<span class="lk" onclick="go(\'%s\')">%s</span>' % (link, name) if link else name
    style = ' style="border-color:#1677ff;background:#e6f4ff;"' if cur else ''
    return '<div class="node"%s><div class="n-role">%s</div><div class="n-name">%s</div></div>' % (style, role, inner)

ARROW = '<span class="link-arrow">→</span>'

def tl(t, text, who=''):
    return '<div class="tl-i"><span class="tl-t">%s</span>%s%s</div>' % (t, text, ('<span class="tl-who">%s</span>' % who) if who else '')

def tl_off(t, text, who=''):
    return '<div class="tl-i off"><span class="tl-t">%s</span>%s%s</div>' % (t, text, ('<span class="tl-who">%s</span>' % who) if who else '')

def mat_table(thead, rows):
    ths = ''.join('<th%s>%s</th>' % (' class="td-num"' if h.startswith('~') else '', h.lstrip('~')) for h in thead)
    trs = ''
    for r in rows:
        tds = ''
        for c in r:
            if isinstance(c, str) and c.startswith('~'):
                tds += '<td class="td-num">%s</td>' % c.lstrip('~')
            else:
                tds += '<td>%s</td>' % c
        trs += '<tr>' + tds + '</tr>\n'
    return ('<div class="table-wrap"><table><thead><tr>%s</tr></thead>\n<tbody>\n%s</tbody></table></div>' % (ths, trs))

def detail_modal(mid, title, header_html, sec2_title, mat_html, chain_html, timeline_html, width=780):
    """四段式详情弹窗。sec2_title/mat_html 传 None 则跳过物料明细段（档案类用其它段名仍可传）。"""
    parts = ['<div class="dt-sec">单据信息</div>', '<div class="dgrid c3">%s</div>' % header_html]
    if mat_html:
        parts.append('<div class="dt-sec">%s</div>' % (sec2_title or '物料明细'))
        parts.append(mat_html)
    if chain_html:
        parts.append('<div class="dt-sec">关联单据</div>')
        parts.append('<div class="chain">%s</div>' % chain_html)
    if timeline_html:
        parts.append('<div class="dt-sec">流转时间线</div>')
        parts.append('<div class="tl">%s</div>' % timeline_html)
    return ('<!-- 详情弹窗（四段式：单据头/明细/关联单据互溯链/流转时间线）· 详情落地页补齐 2026-09-04 -->\n'
            '<div class="modal-overlay" id="%s">\n'
            '  <div class="modal modal-lg" style="width:%dpx;">\n'
            '    <div class="modal-header">\n'
            '      <h3 class="modal-title">%s</h3>\n'
            '      <span class="modal-close" onclick="closeModal(\'%s\')">×</span>\n'
            '    </div>\n'
            '    <div class="modal-body">\n      %s\n    </div>\n'
            '    <div class="modal-footer">\n'
            '      <button class="btn btn-default" onclick="closeModal(\'%s\')">关 闭</button>\n'
            '    </div>\n'
            '  </div>\n'
            '</div>') % (mid, width, title, mid, '\n      '.join(parts), mid)

def confirm_modal(mid, title, warn, header_html=None, ok='确认停用', ok_style='background:#ff4d4f;'):
    """B 组操作确认弹窗（单段：对象信息 + 警示文案 + 取消/确认）。"""
    body = ''
    if header_html:
        body += '<div class="dgrid">%s</div>\n      <div style="height:14px;"></div>\n      ' % header_html
    body += '<p style="font-size:13px;color:#262626;line-height:1.7;">%s</p>' % warn
    return ('<!-- 操作确认弹窗 · 详情落地页补齐 2026-09-04 -->\n'
            '<div class="modal-overlay" id="%s">\n'
            '  <div class="modal">\n'
            '    <div class="modal-header">\n'
            '      <h3 class="modal-title">%s</h3>\n'
            '      <span class="modal-close" onclick="closeModal(\'%s\')">×</span>\n'
            '    </div>\n'
            '    <div class="modal-body">\n      %s</div>\n'
            '    <div class="modal-footer">\n'
            '      <button class="btn btn-default" onclick="closeModal(\'%s\')">取 消</button>\n'
            '      <button class="btn" style="%s" onclick="closeModal(\'%s\')">%s</button>\n'
            '    </div>\n'
            '  </div>\n'
            '</div>') % (mid, title, mid, body, mid, ok_style, mid, ok)

# 弹窗开关脚本（注入无弹窗页面用；有弹窗页面已有同款脚本则跳过）
MODAL_JS = '''<script>
/* ===== 详情弹窗开关（详情落地页补齐注入） ===== */
function openModal(id) { document.getElementById(id).classList.add('show'); }
function closeModal(id) { document.getElementById(id).classList.remove('show'); }
document.querySelectorAll('.modal-overlay').forEach(function (ov) {
  ov.addEventListener('click', function (e) { if (e.target === ov) ov.classList.remove('show'); });
});
</script>'''

# ==================== 业务页注入引擎 ====================

ANCHOR_MARKERS = ['/* ===== 菜单折叠', '/* ===== 弹窗开关', "querySelectorAll('.modal-overlay')"]

def read_page(rel):
    with open(ROOT / rel, 'r', encoding='utf-8', newline='') as f:
        return f.read()

def write_page(rel, text):
    with open(ROOT / rel, 'w', encoding='utf-8', newline='') as f:
        f.write(text)

def tag_balance(block):
    """标签配平检查（R4 同源教训：注入块不得破坏结构）。"""
    for a, b in [('<div', '</div'), ('<table', '</table'), ('<thead', '</thead'), ('<tbody', '</tbody'),
                 ('<tr', '</tr'), ('<td', '</td'), ('<th', '</th'), ('<span', '</span'), ('<p', '</p'),
                 ('<button', '</button'), ('<script', '</script'), ('<style', '</style'), ('<h3', '</h3')]:
        if block.count(a) != block.count(b):
            raise AssertionError('tag unbalance %s vs %s: %d/%d' % (a, b, block.count(a), block.count(b)))

def inject_block(rel, modal_html, with_js, extra_css=True):
    """在绑定脚本之前注入 modal（+样式+开关脚本）。锚点=绑定脚本所在 <script> 开标签之前 → 满足 R4。"""
    t = read_page(rel)
    assert 'id="detail-modal-css"' not in t or not extra_css, rel + ': detail css 已存在，防重复注入'
    cands = []
    for m in ANCHOR_MARKERS:
        p = t.find(m)
        if p > 0:
            s = t.rfind('<script', 0, p)  # 回退到包含该标记的 <script> 开标签
            assert s > 0, rel + ': 标记 %r 前找不到 <script' % m
            cands.append(s)
    assert cands, rel + ': 找不到注入锚点（菜单折叠/弹窗开关/overlay 绑定脚本）'
    pos = min(cands)
    # R4 断言：注入点必须早于所有 radio/overlay 绑定执行点
    rb = t.find("querySelectorAll('.radio')")
    if 0 < rb < pos:
        raise AssertionError(rel + ': 注入点晚于 radio 绑定脚本，违反 R4')
    block = (DETAIL_CSS + '\n' if extra_css else '') + modal_html + ('\n' + MODAL_JS + '\n' if with_js else '')
    tag_balance(block)
    t2 = t[:pos] + block + '\n' + t[pos:]
    # 全文件配平差不变量（原文件可能有历史遗留未闭合标签，只要求注入不改变差值）+ 无重复 modal id
    tag_balance_delta(t, t2)
    return t, t2

def tag_balance_delta(t_old, t_new):
    for a, b in [('<script', '</script'), ('<style', '</style'), ('<div', '</div'), ('<table', '</table'),
                 ('<tbody', '</tbody'), ('<thead', '</thead')]:
        d_old = t_old.count(a) - t_old.count(b)
        d_new = t_new.count(a) - t_new.count(b)
        if d_old != d_new:
            raise AssertionError('tag balance delta changed %s: %d -> %d' % (a, d_old, d_new))

def bind_buttons(t, old, new, expect):
    n = t.count(old)
    assert n == expect, '按钮绑定计数不符: %r 期望 %d 实际 %d' % (old, expect, n)
    return t.replace(old, new)

def assert_unique_id(t, mid):
    n = len(re.findall('id="%s"' % mid, t))
    assert n == 1, 'modal id %s 出现 %d 次（R5）' % (mid, n)

# ==================== 独立模板生成器（包壳默认开） ====================

_SHELL = None
def _shell():
    global _SHELL
    if _SHELL is None:
        with open(ROOT / '仓储作业/弹窗/采购入库审核.html', 'r', encoding='utf-8', newline='') as f:
            _SHELL = f.read()
    return _SHELL

IA_FIX = None
def _ia_fix():
    global IA_FIX
    if IA_FIX is None:
        s = _shell()
        i = s.find('<script>/*ia-fix: tab-switch + btn-feedback (2026-09-04)*/')
        j = s.find('</script>', i) + len('</script>')
        IA_FIX = s[i:j]
    return IA_FIX

def standalone(rel_out, title, inject_marker, modal_html):
    """生成 弹窗/xxx.html 独立模板：完整壳 CSS + modal（go 路径改写）+ 绑定 + 默认打开 + ia-fix。"""
    shell = _shell()
    head = shell[:shell.find('</head>') + len('</head>')]
    head = head.replace('<title>采购入库审核 - 包装租赁管理后台</title>',
                        '<title>%s - 包装租赁管理后台</title>' % title, 1)
    assert '<title>%s - 包装租赁管理后台</title>' % title in head
    head = head.replace('</head>', DETAIL_CSS + '\n</head>', 1)
    m = modal_html.replace("go('../", "go('../../")
    body = ('<body style="background:#f5f6f8;min-height:100vh;font-family:-apple-system,\'Segoe UI\',\'Microsoft YaHei\',sans-serif">\n'
            '<!-- 弹窗模板：%s（详情落地页补齐 2026-09-04） -->\n'
            '<!-- 注入标记：%s -->\n'
            '%s\n'
            '<script>\n'
            'function go(url) { location.href = url; }\n'
            'function openModal(id) { document.getElementById(id).classList.add(\'show\'); }\n'
            'function closeModal(id) { document.getElementById(id).classList.remove(\'show\'); }\n'
            'document.querySelectorAll(\'.modal-overlay\').forEach(function (ov) {\n'
            '  ov.addEventListener(\'click\', function (e) { if (e.target === ov) closeModal(ov.id); });\n'
            '});\n'
            'document.querySelectorAll(\'.radio\').forEach(function (r) {\n'
            '  r.addEventListener(\'click\', function () {\n'
            '    var box = r.parentElement;\n'
            '    box.querySelectorAll(\'.radio\').forEach(function (x) { x.classList.remove(\'checked\'); });\n'
            '    r.classList.add(\'checked\');\n'
            '  });\n'
            '});\n'
            'document.querySelectorAll(\'.checkbox\').forEach(function (c) {\n'
            '  c.addEventListener(\'click\', function () { c.classList.toggle(\'checked\'); });\n'
            '});\n'
            'document.querySelector(\'.modal-overlay\').classList.add(\'show\');\n'
            '</script>\n'
            '%s\n'
            '</body>\n'
            '</html>\n') % (title, inject_marker, m, _ia_fix())
    html = head + '\n' + body
    tag_balance(html)  # 独立模板全新生成，要求绝对配平
    out = ROOT / rel_out
    assert not out.exists(), '独立模板已存在，禁止覆盖: ' + rel_out
    with open(out, 'w', encoding='utf-8', newline='') as f:
        f.write(html)
    return rel_out
