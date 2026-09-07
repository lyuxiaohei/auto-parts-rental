# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已废弃（一次性清理，已完成使命）
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
"""修复4收尾：删除 modal 之外的可见游离元素（form-row/modal-footer/dgrid），保留结构性闭合 div"""
import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v2lib import PROTO, read_page, write_page

def modal_spans(html):
    spans = []
    for m in re.finditer(r'<div class="modal-overlay"', html):
        depth = 1
        for mm in re.finditer(r'<div|</div>', html[m.end():]):
            depth += 1 if mm.group(0) == '<div' else -1
            if depth == 0:
                spans.append((m.start(), m.end() + mm.end()))
                break
    return spans

def extract_balanced(html, start):
    """从 <div 开始平衡提取一个完整元素，返回 (end)"""
    depth = 0
    for mm in re.finditer(r'<div|</div>', html[start:]):
        depth += 1 if mm.group(0) == '<div' else -1
        if depth == 0:
            return start + mm.end()
    return None

VISIBLE_CLS = ('form-row', 'modal-footer', 'dgrid')
for rel in ['订单协同/客户订单.html', '项目管理/项目档案.html']:
    h = read_page(rel)
    removed = 0
    while True:
        spans = modal_spans(h)
        # 找第一个不在弹窗内的可见游离元素
        m = None
        for mm in re.finditer(r'<div class="(form-row|modal-footer|dgrid)"', h):
            if not any(s <= mm.start() < e for s, e in spans):
                m = mm
                break
        if not m:
            break
        e = extract_balanced(h, m.start())
        if e is None:
            print(f'⚠️ {rel}: 无法平衡提取，行 {h.count(chr(10), 0, m.start())+1}')
            break
        frag = h[m.start():e]
        # 向前吃掉前导空白行，向后吃掉一个尾随换行
        s = m.start()
        while s > 0 and h[s-1] in ' \t':
            s -= 1
        if s > 0 and h[s-1] == '\n':
            s -= 1
        h = h[:s] + h[e:]
        removed += 1
    # 收敛空行
    h = re.sub(r'\n{3,}', '\n\n', h)
    write_page(rel, h)
    o = len(re.findall(r'<div\b', h)); c = len(re.findall(r'</div>', h))
    print(f'✅ {rel}: 删除可见游离元素 {removed} 个 | 剩余 div 差 {c - o}')

print('完成')
