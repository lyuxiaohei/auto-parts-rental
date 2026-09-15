# -*- coding: utf-8 -*-
"""G36 共享工厂：页面模板化（样板=采购订单新建）＋表单移植＋详情/审核页生成＋宿主接线＋demo-data ops 重定向"""
import io, os, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
SKEL = io.open(os.path.join(ROOT, '采购管理', '采购订单新建.html'), encoding='utf-8').read()

DETAIL_CSS = '''<style id="detail-modal-css">
.dt-sec{font-size:13px;font-weight:600;color:#262626;margin:0 0 10px;padding-left:8px;border-left:3px solid #1677ff;line-height:1.3}
.dt-sec:not(:first-child){margin-top:18px}
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

def _grab(src, anchor):
    i = src.index(anchor)
    j = src.index('</script>', i) + len('</script>')
    blk = src[i:j]
    if not blk.lstrip().startswith('<script'):
        blk = '<script>\n' + blk
    return blk

def _cut(src, anchor):
    i = src.index(anchor)
    a = src.rfind('<script', 0, i)
    j = src.index('</script>', i) + len('</script>')
    return src[:a] + src[j:]

def build_template():
    t = SKEL
    t = t.replace('<title>新建采购订单 - 包装租赁管理后台</title>', '<title>{{TITLE}} - 包装租赁管理后台</title>')
    m = re.search(r'<div class="tabs">.*?</div>\n', t, re.S)
    t = t.replace(m.group(0), '<div class="tabs">\n{{TABS}}\n</div>\n')
    t = t.replace('<li class="sm-item has-sub open">', '<li class="sm-item has-sub">', 1)
    t = t.replace('<li><div class="sm-link selected">采购订单</div></li>',
                  '<li><div class="sm-link" onclick="go(\'../采购管理/采购订单列表.html\')">采购订单</div></li>')
    i = t.index('    <div class="content submit-pad">')
    j = t.index('<script>\nfunction addDetailRow')
    t = t[:i] + '    <div class="content submit-pad">\n{{CONTENT}}\n{{SUBMITBAR}}\n    </div>\n  </div>\n</div>\n' + t[j:]
    a0 = t.index('<script>\nfunction addDetailRow')
    mb = t.index('/* ===== 菜单折叠')
    b0 = t.rfind('<script', a0, mb)
    seg = t[a0:b0]
    keep = '<script src="../_data/demo-data.js"></script>'
    assert keep in seg
    t = t.replace(seg, keep + '\n{{PAGE_SCRIPTS}}\n')
    t = _cut(t, '/*F-A 税率三件套双向换算')
    assert 'F-A 税率' not in t
    t = t.replace('</head>', '{{DETAIL_CSS}}</head>')
    return t

TEMPLATE = build_template()

def sidebar_select(t, group, menu_label, menu_target):
    gi = t.index(group + '<span class="sm-arrow">')
    li = t.rfind('<li class="sm-item has-sub">', 0, gi)
    t = t[:li] + '<li class="sm-item has-sub open">' + t[li + len('<li class="sm-item has-sub">'):]
    old = '<li><div class="sm-link" onclick="go(\'%s\')">%s</div></li>' % (menu_target, menu_label)
    assert t.count(old) == 1, 'menu not found: ' + menu_label + ' ' + menu_target
    return t.replace(old, '<li><div class="sm-link selected">%s</div></li>' % menu_label)

def assemble(path, title, tab_host, tab_self, group, menu_label, menu_target, content, scripts, submitbar, detail=False):
    t = TEMPLATE
    t = t.replace('{{TITLE}}', title)
    t = t.replace('{{TABS}}', '  <span class="tab">%s <span class="close">×</span></span>\n  <span class="tab active">%s <span class="close">×</span></span>' % (tab_host, tab_self))
    t = sidebar_select(t, group, menu_label, menu_target)
    t = t.replace('{{CONTENT}}', content)
    t = t.replace('{{SUBMITBAR}}', submitbar or '')
    t = t.replace('{{PAGE_SCRIPTS}}', scripts or '')
    t = t.replace('{{DETAIL_CSS}}', DETAIL_CSS if detail else '')
    for ph in ('{{TITLE}}', '{{TABS}}', '{{CONTENT}}', '{{SUBMITBAR}}', '{{PAGE_SCRIPTS}}', '{{DETAIL_CSS}}'):
        assert ph not in t, ph + ' left in ' + path
    if '\r\n' not in t:
        t = t.replace('\n', '\r\n')
    fp = os.path.join(ROOT, path)
    io.open(fp, 'w', encoding='utf-8', newline='').write(t)
    return path

# ---------------- 详情页 ----------------
def dpage(path, entity, def_key, host_url, tab_host, tab_self, title, group, menu_label, menu_target):
    content = ('<div class="card">\n  <div class="card-head">\n'
               '    <h3 class="card-title" id="dtTitle">%s</h3>\n'
               '    <div class="head-btns"><button class="btn btn-default btn-sm" onclick="go(\'%s\')">返回列表</button></div>\n'
               '  </div>\n  <div id="detailBody"><!-- 内容由 _data/detail-generic.js 按单号渲染 --></div>\n</div>\n' % (title, host_url))
    scripts = ('<script src="../_data/detail-generic.js"></script>\n<script>\n'
               '(function () {\n'
               '  var ENT = %s, DEF = %s;\n'
               '  var k = null;\n'
               '  try { k = new URLSearchParams(location.search).get("id"); } catch (e) {}\n'
               '  var D = (window.DEMO_DATA || {})[ENT] || {};\n'
               '  if (!D[k]) k = Object.keys(D).filter(function (x) { return D[x] && JSON.stringify(D[x]).replace(/\\s/g, "").indexOf(\'"tag":"待\') > -1; })[0]'

               '    || Object.keys(D).filter(function (x) { return D[x] && (D[x].info || D[x].title); })[0] || DEF;\n'
               '  var rec = D[k] || {};\n'
               '  var t = document.getElementById("dtTitle");\n'
               '  if (t) t.textContent = (rec.title || %s) + " · " + (rec.titleNo || k);\n'
               '  var el = document.getElementById("detailBody");\n'
               '  if (el && window.renderGenericDetailHTML) el.innerHTML = window.renderGenericDetailHTML(rec, "../");\n'
               '})();\n</script>' % (repr(entity), repr(def_key), repr(title)))
    return assemble(path, title, tab_host, tab_self, group, menu_label, menu_target, content, scripts, '', detail=True)

# ---------------- 审核页 ----------------
def apage(path, entity, def_key, host_url, tab_host, tab_self, title, group, menu_label, menu_target, hint='通过后单据生效并流转下一环节；驳回退回提交人修改。'):
    ta_style = 'style="width:100%;border:none;outline:none;background:transparent;font:inherit;color:inherit;resize:vertical;min-height:72px;line-height:1.6;"'
    content = (
        '<div class="card">\n  <div class="card-head">\n'
        '    <h3 class="card-title" id="dtTitle">' + title + '</h3>\n'
        '    <div class="head-btns"><button class="btn btn-default btn-sm" onclick="go(\'' + host_url + '\')">返回列表</button></div>\n'
        '  </div>\n  <div id="detailBody"><!-- 单据明细（detail-generic 按单号渲染） --></div>\n</div>\n'
        '<div class="card">\n  <div class="card-head">\n    <h3 class="card-title">审核决策</h3>\n  </div>\n'
        '  <div class="form-row">\n    <div class="form-label"><span class="req">*</span>审核结论：</div>\n    <div>\n'
        '      <span class="radio checked"><span class="dot"></span>通过</span>\n'
        '      <span class="radio"><span class="dot"></span>驳回</span>\n    </div>\n  </div>\n'
        '  <div class="form-row" style="align-items:flex-start;">\n    <div class="form-label" style="padding-top:6px;">审核意见：</div>\n    <div>\n'
        '      <div class="input-box" style="width:380px;height:auto;padding:6px 11px;"><textarea placeholder="选填，驳回时建议填写原因" ' + ta_style + '></textarea></div>\n'
        '      <div class="pn-hint">' + hint + '</div>\n    </div>\n  </div>\n</div>\n')
    scripts = ('<script src="../_data/detail-generic.js"></script>\n<script>\n'
               '(function () {\n'
               '  var ENT = %s, DEF = %s;\n'
               '  var k = null;\n'
               '  try { k = new URLSearchParams(location.search).get("id"); } catch (e) {}\n'
               '  var D = (window.DEMO_DATA || {})[ENT] || {};\n'
               '  if (!D[k]) k = Object.keys(D).filter(function (x) { return D[x] && JSON.stringify(D[x]).replace(/\\s/g, "").indexOf(\'"tag":"待\') > -1; })[0]'

               '    || Object.keys(D).filter(function (x) { return D[x] && (D[x].info || D[x].title); })[0] || DEF;\n'
               '  var rec = D[k] || {};\n'
               '  var t = document.getElementById("dtTitle");\n'
               '  if (t) t.textContent = (rec.title || %s) + " · " + (rec.titleNo || k);\n'
               '  var el = document.getElementById("detailBody");\n'
               '  if (el && window.renderGenericDetailHTML) el.innerHTML = window.renderGenericDetailHTML(rec, "../");\n'
               '})();\n</script>' % (repr(entity), repr(def_key), repr(title)))
    bar = ('<div class="submit-bar"><button class="btn btn-default" onclick="go(\'%s\')">取 消</button>'
           '<button class="btn">确认提交</button></div>' % host_url)
    return assemble(path, title, tab_host, tab_self, group, menu_label, menu_target, content, scripts, bar, detail=True)

# ---------------- 表单页（弹窗模板移植） ----------------
BOILER_MARKERS = ['function openModal', 'function closeModal', 'modal-overlay\'', "modal-overlay\")", 'ia-fix', 'proto-notes', 'function go(url)', 'tab-switch', '===== 菜单折叠']

def fpage(path, tpl_rel, host_url, tab_host, tab_self, title, group, menu_label, menu_target, card_title=None):
    """tpl_rel: 弹窗模板相对原型根路径；移植 modal-body + 业务脚本 + footer→提交条"""
    _fp = os.path.join(ROOT, tpl_rel)
    if not os.path.exists(_fp):
        _fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backup-g36-b2-20260915', tpl_rel)
    s = io.open(_fp, encoding='utf-8', newline='').read()
    i = s.index('<div class="modal-body">') + len('<div class="modal-body">')
    j = s.index('<div class="modal-footer"', i)
    span = s[i:j]
    _embedded = re.findall(r'<script(?![^>]*src=)[^>]*>.*?</script>', span, re.S)
    for _e in _embedded:
        span = span.replace(_e, chr(10))
    body = span
    b2 = body.rstrip()
    assert b2.endswith('</div>'), 'modal-body close not found in ' + tpl_rel
    body = b2[:-len('</div>')]
    # footer 按钮
    ftr = re.search(r'<div class="modal-footer">(.*?)</div>', s[j:], re.S)
    btns = []
    if ftr:
        for t2 in re.findall(r'<button[^>]*>([^<]+)</button>', ftr.group(1)):
            btns.append(t2.strip())
    # 业务脚本
    keep_scripts = []
    for _e in _embedded:
        keep_scripts.append(_e)
    for sc in re.findall(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', s, re.S):
        t2 = sc.strip()
        if not t2:
            continue
        if any(mk in t2 for mk in BOILER_MARKERS):
            continue
        keep_scripts.append('<script>' + t2 + '</script>')
    # 规范化：宽 350→380；body 内 closeModal→go(host)
    body = body.replace('width:350px', 'width:380px')
    body = re.sub(r"closeModal\('[a-zA-Z]+Modal'\)", "go('%s')" % host_url, body)
    # 备注行 input → textarea（标签为「备注」的裸 input 行）
    def _tx(m2):
        return ('<div class="form-row" style="align-items:flex-start;">\n    <div class="form-label" style="padding-top:6px;">%s</div>\n    <div>\n'
                '      <div class="input-box" style="width:380px;height:auto;padding:6px 11px;"><textarea placeholder="%s" style="width:100%%;border:none;outline:none;background:transparent;font:inherit;color:inherit;resize:vertical;min-height:72px;line-height:1.6;"></textarea></div>\n'
                '    </div>\n  </div>') % (m2.group(1), m2.group(2) or '选填')
    body = re.sub(r'<div class="form-row">\s*(?:<div|<span) class="form-label"[^>]*>((?:<span class="req"[^>]*>\*</span>)?\s*备注\s*[：:]?)</(?:div|span)>\s*<div>\s*<div class="input-box"(?![^>]*height:auto)><input[^>]*?placeholder="([^"]*)"[^>]*/?>\s*</div>\s*</div>\s*</div>',
                  _tx, body, count=1)
    # 日期行 input 加 type=date（值形如 2026-09-14）
    def _dt(m2):
        row = m2.group(0)
        return re.sub(r'<input((?![^>]*type=)[^>]*value="(\d{4}-\d{2}-\d{2})")', r'<input type="date"\1', row)
    body = re.sub(r'<div class="form-row">(?:(?!</div>\s*</div>\s*</div>|<div class="form-row">).)*?日期(?:(?!</div>\s*</div>\s*</div>|<div class="form-row">).)*?</div>\s*</div>\s*</div>', _dt, body, flags=re.S)
    # 组装
    ct = card_title or title
    content = '<div class="card">\n  <div class="card-head">\n    <h3 class="card-title">%s</h3>\n  </div>\n%s\n</div>\n<style>.form-row .input-box{width:380px;}</style>\n' % (ct, body)
    bar_btns = ''
    for i2, b2 in enumerate(btns or ['取 消', '保 存']):
        if b2.replace(' ', '') in ('取消', '取 消'):
            bar_btns += '<button class="btn btn-default" onclick="go(\'%s\')">%s</button>' % (host_url, b2)
        else:
            bar_btns += '<button class="btn">%s</button>' % b2
    bar = '<div class="submit-bar">%s</div>' % bar_btns
    return assemble(path, title, tab_host, tab_self, group, menu_label, menu_target, content, '\n'.join(keep_scripts), bar)

# ---------------- 宿主页接线 ----------------
def cut_overlay(s, mid):
    a = s.index('<div class="modal-overlay" id="%s"' % mid)
    i = a; depth = 0; n = len(s)
    while i < n:
        mo = re.compile(r'<div\b|</div>').search(s, i)
        if not mo:
            raise AssertionError('unbalanced ' + mid)
        if mo.group(0) == '</div>':
            depth -= 1
            if depth == 0:
                end = mo.end()
                while end < n and s[end] in '\r\n ':
                    end += 1
                return s[:a] + s[end:]
        else:
            depth += 1
        i = mo.end()
    raise AssertionError('no close ' + mid)

def cut_script_containing(s, marker):
    i = s.index(marker)
    a = s.rfind('<script', 0, i)
    j = s.index('</script>', i) + len('</script>')
    while j < len(s) and s[j] in '\r\n':
        j += 1
    return s[:a] + s[j:]

# ---------------- demo-data ops 重定向 ----------------
def rd(p):
    return io.open(os.path.join(ROOT, p), encoding='utf-8', newline='').read()

def wr(p, s):
    io.open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='').write(s)

def entity_span(s, ent):
    a = s.index(ent + ': {')
    a = s.rfind('\n', 0, a) + 1
    b = s.index('\n  },', a)
    return a, b

def rew_detail_audit(s, ent, detail_url, audit_url=None, det_label='详情'):
    """detail:true→go(detail_url?id=KEY)；openModal('auditModal')→go(audit_url?id=KEY)"""
    a, b = entity_span(s, ent)
    blk = s[a:b]
    lines = blk.split('\n')
    key = None; nd = 0; na = 0
    for i, ln in enumerate(lines):
        mk = re.search(r"^\s*'([A-Za-z0-9\-\.]+)': \{", ln)
        if mk and mk.group(1) != 'row':
            key = mk.group(1)
        det = '{"t": "%s", "detail": true}' % det_label
        if det in ln:
            assert key, 'no key in ' + ent
            ln = ln.replace(det, '{"t": "%s", "act": "go(\'%s?id=%s\')"}' % (det_label, detail_url, key))
            nd += 1
        if audit_url and "openModal('auditModal')" in ln:
            assert key, 'no key in ' + ent
            ln = ln.replace("openModal('auditModal')", "go('%s?id=%s')" % (audit_url, key))
            na += 1
        lines[i] = ln
    return s[:a] + '\n'.join(lines) + s[b:], nd, na

def rew_act(s, ent, old, new):
    """实体内 act 字符串精确替换"""
    a, b = entity_span(s, ent)
    blk = s[a:b]
    n = blk.count(old)
    blk = blk.replace(old, new)
    return s[:a] + blk + s[b:], n

def rew_regex(s, ent, pat, repl):
    """实体内正则替换（如 openRetDetail('x','KEY')→go('..?id=KEY')）"""
    a, b = entity_span(s, ent)
    blk = s[a:b]
    blk2, n = re.subn(pat, repl, blk)
    return s[:a] + blk2 + s[b:], n


def rew_todo_links(s, mapping):
    """todoItems 记录 link: '列表?audit=1' → '审核页?id=KEY'（mapping: 列表路径→审核页路径）"""
    a, b = entity_span(s, 'todoItems')
    blk = s[a:b]
    lines = blk.split('\n')
    key = None; n = 0
    for i, ln in enumerate(lines):
        mk = re.search(r"^\s*'([A-Za-z0-9\-\.]+)': \{", ln)
        if mk and mk.group(1) != 'row':
            key = mk.group(1)
        for lst, ap in mapping.items():
            old = "'link': '%s?audit=1'" % lst
            if old in ln:
                assert key, 'todo no key'
                ln = ln.replace(old, "'link': '%s?id=%s'" % (ap, key))
                n += 1
        lines[i] = ln
    return s[:a] + '\n'.join(lines) + s[b:], n
