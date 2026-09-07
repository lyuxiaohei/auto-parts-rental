# -*- coding: utf-8 -*-
"""任务〇：标注层 style 块缺失修复（8 页）。
根因：09-03 "空 script 坏块" 时代存量损伤，style 块整体丢失、pins/js/data-note 完好
→ 便签无 display:none 裸露页底、角标无 ::after、开关无视觉效果。
修复：以技能库 annotate.py 的 STYLE 常量为唯一基准，插入在 <div id="proto-pins"> 前
（标准注入三连块顺序 STYLE→pins→JS，仅位置随历史锚点，不改动其余任何内容）。
幂等：已有 style 块的页跳过。"""
import pathlib, sys

sys.path.insert(0, r'C:\Users\Administrator\.claude\skills\原型标注\scripts')
import annotate  # 技能库，STYLE 为标准块唯一基准

ROOT = pathlib.Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型')
PAGES = [
    '基础数据/客商管理.html', '基础数据/器具档案.html', '基础数据/库位档案.html',
    '基础数据/零部件档案.html', '系统管理/数据字典.html', '系统管理/用户权限.html',
    '项目管理/项目档案.html', '仓储作业/盘点列表.html',
]
ANCHOR = '<div id="proto-pins">'

def balance(h, tag):
    return h.count('<' + tag) - h.count('</' + tag + '>')

for rel in PAGES:
    p = ROOT / rel
    b = p.read_bytes()
    html = b.decode('utf-8')
    # --- 改前 assert ---
    assert html.count('id="proto-notes-style"') == 0, rel + ' 已有 style 块（幂等跳过判断失败）'
    assert html.count(ANCHOR) == 1, rel + ' pins 锚点不唯一'
    assert html.count('id="proto-notes-js"') == 1, rel + ' js 块数异常'
    assert html.count('protoNotesFab') == 2, rel + ' fab 计数异常'
    pre = {t: balance(html, t) for t in ('style', 'div', 'script')}
    assert all(v == 0 for v in pre.values()), rel + ' 改前标签不配平 ' + str(pre)
    # --- 构造插入块（随页面主导行尾） ---
    crlf = b.count(b'\r\n'); lf = b.count(b'\n') - crlf
    style = annotate.STYLE + '\n'
    if crlf > lf:
        style = style.replace('\n', '\r\n')
    # --- 精确插入（bytes 层面，锚点唯一） ---
    i = html.find(ANCHOR)
    new = html[:i] + style + html[i:]
    # --- 改后 assert ---
    assert new.count('id="proto-notes-style"') == 1, rel + ' 注入后 style 计数!=1'
    assert new.count(ANCHOR) == 1 and new.count('id="proto-notes-js"') == 1, rel + ' 注入后 pins/js 受扰'
    post = {t: balance(new, t) for t in ('style', 'div', 'script')}
    assert post == {'style': 0, 'div': 0, 'script': 0}, rel + ' 改后标签不配平 ' + str(post)
    assert len(new) - len(html) == len(style), rel + ' 长度差与插入块不符'
    assert style.rstrip('\r\n').endswith('</style>'), rel + ' STYLE 块未闭合'
    p.write_bytes(new.encode('utf-8'))
    print('OK %s  插入 %d 字节（%s）' % (rel, len(style), 'CRLF' if crlf > lf else 'LF'))

print('任务〇修复完成：8/8')
