# -*- coding: utf-8 -*-
"""G19a T2: 五页 HTML 精确替换（读取-替换-assert-写回，禁整页生成）"""
import pathlib

MOB = pathlib.Path(r'P3-R01-包装租赁管理后台原型/mobile')

# ---- SVG 图标（线性 24 视口 · stroke currentColor · 纯矢量无 Emoji） ----
SVG_TMPL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{p}</svg>'
ICO = {
    'todo':  SVG_TMPL.format(p='<path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/><path d="m9 14 2 2 4-4"/>'),
    'stock': SVG_TMPL.format(p='<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>'),
    'me':    SVG_TMPL.format(p='<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>'),
    'chat':  SVG_TMPL.format(p='<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'),
    'db':    SVG_TMPL.format(p='<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14a9 3 0 0 0 18 0V5"/><path d="M3 12a9 3 0 0 0 18 0"/>'),
    'pc':    SVG_TMPL.format(p='<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8"/><path d="M12 17v4"/>'),
    'info':  SVG_TMPL.format(p='<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>'),
    'back':  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>',
}

results = []

def rep(fname, old, new, expect):
    p = MOB / fname
    s = p.read_text(encoding='utf-8')
    n = s.count(old)
    assert n == expect, f'{fname}: expect {expect} got {n} for {old[:60]!r}'
    p.write_text(s.replace(old, new), encoding='utf-8')
    results.append(f'[OK] {fname}: {expect}x  {old[:44]!r}')

# ---- 1. 三页 tabbar：Emoji → SVG（保留 href/active/文字） ----
TAB = [('待办审批.html', 'todo'), ('库存查询.html', 'stock'), ('我的.html', 'me')]
for fname, _ in TAB:
    rep(fname, '<span class="m-tab-ico">☑</span>待办', f'<span class="m-tab-ico">{ICO["todo"]}</span>待办', 1)
    rep(fname, '<span class="m-tab-ico">📦</span>库存', f'<span class="m-tab-ico">{ICO["stock"]}</span>库存', 1)
    rep(fname, '<span class="m-tab-ico">👤</span>我的', f'<span class="m-tab-ico">{ICO["me"]}</span>我的', 1)

# ---- 2. 我的页 m-cell：Emoji → SVG（m-cell-key 结构） ----
ME = '我的.html'
rep(ME, '<span>📷 企业微信</span>',  f'<span class="m-cell-key">{ICO["chat"]}企业微信</span>', 1)
rep(ME, '<span>🗄 数据来源</span>',  f'<span class="m-cell-key">{ICO["db"]}数据来源</span>', 1)
rep(ME, '<span>🖥 PC 端</span>',     f'<span class="m-cell-key">{ICO["pc"]}PC 端</span>', 1)
rep(ME, '<span>ℹ️ 版本信息</span>',  f'<span class="m-cell-key">{ICO["info"]}版本信息</span>', 1)

# ---- 3. 审批详情：返回 ‹ → SVG chevron（onclick 原样保留·URL 语境不动） ----
rep('审批详情.html',
    '<span style="cursor:pointer;font-size:20px;line-height:1;padding:2px 6px 2px 0;" onclick="go(\'待办审批.html\')">‹</span>',
    f'<span class="m-hd-back" onclick="go(\'待办审批.html\')">{ICO["back"]}</span>', 1)

print('\n'.join(results))
print(f'TOTAL {len(results)} replacements OK')
