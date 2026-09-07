# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已废弃·禁止运行（内嵌12页旧快照生成器）
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
"""步骤5：生成 12 个 v2 新页面。CSS 壳从已改造的采购入库列表.html 提取，保证样式一致。"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v2lib import PROTO, render_sidebar, write_page, read_page

# 从现有页面提取 CSS 壳（已移除 sys-switch）
_shell = read_page('仓储作业/采购入库列表.html')
CSS = re.search(r'<style>(.*?)</style>', _shell, re.S).group(1)

TOPBAR = '''<header class="topbar">
  <div class="logo">包装租赁管理后台</div>
  <div class="tools">
    <span class="ico-btn" title="刷新"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-2.64-6.36"/><path d="M21 3v6h-6"/></svg></span>
    <span class="ico-btn" title="通知"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9a6 6 0 0 1 12 0c0 5 2 6 2 6H4s2-1 2-6"/><path d="M10 20a2 2 0 0 0 4 0"/></svg></span>
    <span class="manual">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M9.2 9a2.8 2.8 0 0 1 5.5.7c0 1.8-2.7 2.3-2.7 3.8"/><line x1="12" y1="17" x2="12" y2="17.01"/></svg>
      操作手册
    </span>
    <span class="avatar" title="账户"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="8" width="14" height="10" rx="3"/><circle cx="10" cy="13" r="0.6" fill="#fff"/><circle cx="14" cy="13" r="0.6" fill="#fff"/><path d="M12 8V4"/><circle cx="12" cy="3.4" r="0.8" fill="#fff"/></svg></span>
  </div>
</header>'''

SEL_CARET = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>'

JS_COMMON = '''<script>
/* ===== 筛选区 收起/展开 ===== */
(function () {
  var btn = document.getElementById('btnCollapse');
  if (!btn) return;
  var ico = document.getElementById('collapseIco');
  var txt = document.getElementById('collapseTxt');
  var rows = document.querySelectorAll('.collapse-row');
  btn.addEventListener('click', function () {
    var collapsed = txt.textContent === '展开';
    rows.forEach(function (r) { r.style.display = collapsed ? 'flex' : 'none'; });
    txt.textContent = collapsed ? '收起' : '展开';
    ico.style.transform = collapsed ? 'rotate(180deg)' : '';
  });
})();
</script>
<script>
/* ===== 菜单折叠 / 页签与表单视觉态（统一脚本） ===== */
function go(url) { location.href = url; }
document.querySelectorAll('.sm-item.has-sub > .sm-link').forEach(function (link) {
  link.addEventListener('click', function () { link.parentElement.classList.toggle('open'); });
});
/* 状态页签切换（视觉选中态） */
document.querySelectorAll('.stabs .stab').forEach(function (tab) {
  tab.addEventListener('click', function () {
    tab.parentElement.querySelectorAll('.stab').forEach(function (t) { t.classList.remove('active'); });
    tab.classList.add('active');
  });
});
/* 表单单选/复选视觉态切换 */
document.querySelectorAll('.radio').forEach(function (r) {
  r.addEventListener('click', function () {
    r.parentElement.querySelectorAll('.radio').forEach(function (x) { x.classList.remove('checked'); });
    r.classList.add('checked');
  });
});
document.querySelectorAll('.checkbox').forEach(function (c) {
  c.addEventListener('click', function (c2) { c.classList.toggle('checked'); });
});
/* ===== 弹窗 ===== */
function openModal(id) { document.getElementById(id).classList.add('show'); }
function closeModal(id) { document.getElementById(id).classList.remove('show'); }
document.querySelectorAll('.modal-overlay').forEach(function (ov) {
  ov.addEventListener('click', function (e) { if (e.target === ov) ov.classList.remove('show'); });
});
</script>'''


def fi_input(label, ph='请输入'):
    return f'<div class="fi"><label>{label}：</label><div class="ctl"><input placeholder="{ph}"></div></div>'

def fi_sel(label, val='全部'):
    return f'<div class="fi"><label>{label}：</label><div class="ctl sel"><span class="v">{val}</span>{SEL_CARET}</div></div>'

def fi_range(label):
    return f'<div class="fi"><label>{label}：</label><div class="ctl range"><input placeholder="开始日期"><span class="sep">~</span><input placeholder="结束日期"></div></div>'

def filter_card(items, collapsed=None):
    """items: 首行筛选项 HTML 列表；collapsed: 收起区筛选项"""
    cells = list(items)
    cells.append('''<div class="fi" style="justify-content:flex-end;">
      <div class="fbtns">
        <button class="link-btn" id="btnCollapse"><svg id="collapseIco" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg><span id="collapseTxt">展开</span></button>
        <button class="btn btn-default">重置</button>
        <button class="btn btn-primary">查询</button>
      </div>
    </div>''')
    for c in (collapsed or []):
        cells.append(c.replace('class="fi"', 'class="fi collapse-row"', 1))
    return '<div class="card filter">\n  <div class="fgrid">\n    ' + '\n    '.join(cells) + '\n  </div>\n</div>'

def stabs_bar(tabs):
    """tabs: [(名称, 数量)]，第一个为 active"""
    out = ['<div class="stabs">']
    for i, (name, cnt) in enumerate(tabs):
        out.append(f'  <span class="stab{" active" if i == 0 else ""}">{name}<span class="stab-count">{cnt}</span></span>')
    out.append('</div>')
    return '\n'.join(out)

def pager(total, per=10):
    pages = max(1, (total + per - 1) // per)
    btns = ['<span class="pg-btn">‹</span>', '<span class="pg-btn cur">1</span>']
    for i in range(2, min(pages, 5) + 1):
        btns.append(f'<span class="pg-btn">{i}</span>')
    if pages > 5:
        btns.append('<span class="pg-ellipsis">…</span>')
        btns.append(f'<span class="pg-btn">{pages}</span>')
    btns.append('<span class="pg-btn">›</span>')
    return f'''<div class="pager">
    <span class="pg-info">第 1-{min(per, total)} 条/总共 {total} 条</span>
    {' '.join(btns)}
    <span class="pg-size">10 条/页
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
    </span>
    <span class="pg-jump">跳至 <input value=""> 页</span>
  </div>'''

def tag(text, color):
    return f'<span class="tag tag-{color}">{text}</span>'

STATUS_COLOR = {
    '待审核': 'orange', '已审核': 'blue', '已完成': 'green', '已关闭': 'gray',
    '待发货': 'blue', '已发货': 'green', '在租': 'blue', '已退租': 'green',
    '待入库': 'orange', '已入库': 'green', '待提交': 'gray', '待验收': 'orange',
    '未付款': 'red', '部分付款': 'orange', '已付款': 'green', '已核销': 'green',
    '待确认': 'orange', '已确认': 'green', '已生效': 'green', '草稿': 'gray',
}

def st(text):
    return tag(text, STATUS_COLOR.get(text, 'blue'))

def num(v, bold=False, danger=False):
    style = ' style="color:var(--danger)"' if danger else ''
    inner = f'<b>{v}</b>' if bold else v
    return f'<span class="td-num"{style}>{inner}</span>'

def ops(*links):
    """links: (文本, url或None, modalId或None)"""
    out = []
    for text, url, mid in links:
        if url:
            out.append(f"<a onclick=\"go('{url}')\">{text}</a>")
        elif mid:
            out.append(f'<a onclick="openModal(\'{mid}\')">{text}</a>')
        else:
            out.append(f'<a>{text}</a>')
    return '<span class="ops">' + ''.join(out) + '</span>'

def table(headers, rows):
    """headers: 列名列表（'' 表示复选框列）；rows: 单元格 HTML 列表的列表"""
    ths = '\n'.join(f'          <th>{h}</th>' for h in headers)
    trs = []
    for r in rows:
        tds = '\n'.join(f'          <td>{c}</td>' for c in r)
        trs.append(f'        <tr>\n{tds}\n        </tr>')
    return f'''<div class="table-wrap">
    <table>
      <thead>
        <tr>
{ths}
        </tr>
      </thead>
      <tbody>
{chr(10).join(trs)}
      </tbody>
    </table>
  </div>'''

CB = '<input type="checkbox" class="cb">'

def tabs_bar(names):
    out = ['<div class="tabs">']
    for i, n in enumerate(names):
        out.append(f'  <span class="tab{" active" if i == 0 else ""}">{n} <span class="close">×</span></span>')
    out.append('</div>')
    return '\n'.join(out)

# ===== 弹窗构造 =====
def m_select(label, val, req=False, w='350px'):
    reqh = '<span class="req">*</span>' if req else ''
    return f'''<div class="form-row">
    <span class="form-label">{reqh}{label}</span>
    <div class="input-box select-box" style="width:{w};"><span>{val}</span><span class="caret">{SEL_CARET}</span></div>
  </div>'''

def m_input(label, val='', req=False, ph='请输入', w='350px'):
    reqh = '<span class="req">*</span>' if req else ''
    v = f' value="{val}"' if val else ''
    return f'''<div class="form-row">
    <span class="form-label">{reqh}{label}</span>
    <div class="input-box" style="width:{w};"><input{v} placeholder="{ph}"></div>
  </div>'''

def m_radio(label, options, checked=0):
    radios = ''.join(f'<span class="radio{" checked" if i == checked else ""}"><span class="dot"></span>{o}</span>' for i, o in enumerate(options))
    return f'''<div class="form-row">
    <span class="form-label">{label}</span>
    <div>{radios}</div>
  </div>'''

def m_table(title, headers, rows):
    ths = ''.join(f'<th>{h}</th>' for h in headers)
    trs = ''
    for r in rows:
        tds = ''.join(f'<td>{c}</td>' for c in r)
        trs += f'<tr>{tds}</tr>'
    return f'''<div style="margin:4px 0 8px;font-size:13px;font-weight:600;color:#1a1a1a;">{title}</div>
  <div class="table-wrap" style="border:1px solid var(--border);border-radius:6px;">
    <table class="edit-tbl">
      <thead><tr>{ths}</tr></thead>
      <tbody>{trs}</tbody>
    </table>
  </div>
  <button class="btn btn-dashed btn-sm" style="width:100%;margin-top:8px;">+ 添加一行</button>'''

def m_hint(text):
    return f'<div class="pn-hint" style="margin:4px 0 12px;">{text}</div>'

def modal(mid, title, body_html, wide=True):
    return f'''<div class="modal-overlay" id="{mid}">
  <div class="modal{' modal-lg' if wide else ''}">
    <div class="modal-header">
      <h3 class="modal-title">{title}</h3>
      <span class="modal-close" onclick="closeModal('{mid}')">×</span>
    </div>
    <div class="modal-body">
{body_html}
    </div>
    <div class="modal-footer">
      <button class="btn btn-default" onclick="closeModal('{mid}')">取消</button>
      <button class="btn btn-default" onclick="closeModal('{mid}')">保存草稿</button>
      <button class="btn" onclick="closeModal('{mid}')">提交审核</button>
    </div>
  </div>
</div>'''

def build_page(rel, title, selected, tab_names, content_html, modals_html=''):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{title} - 包装租赁管理后台</title>
<style>{CSS}</style>
</head>
<body>
{TOPBAR}
<div class="body fixed">
{render_sidebar(selected)}
  <div class="main-col">
{tabs_bar(tab_names)}
    <div class="content">
{content_html}
    </div>
  </div>
</div>

{modals_html}

{JS_COMMON}
</body>
</html>
'''

def list_card(title, head_btns, stabs_html, table_html, pager_html):
    return f'''<div class="card">
  <div class="card-head">
    <h3 class="card-title">{title}</h3>
    <div class="head-btns">{head_btns}</div>
  </div>
{stabs_html}
{table_html}
{pager_html}
</div>'''
