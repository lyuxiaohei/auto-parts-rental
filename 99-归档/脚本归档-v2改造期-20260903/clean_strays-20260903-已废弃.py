# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已废弃（一次性清理，已完成使命）
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
"""修复4补完：清理所有 modal 块之外的游离片段（form-row 残尾 + modal-footer 残尾 + 多余闭合 div）"""
import os, re, glob, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PROTO = 'P3-R01-包装租赁管理后台原型'

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

# 残尾模式 A：审核弹窗后半截（以「审核结论」form-row 起头为特征，避免误伤表单页正文）
PAT_A = re.compile(
    r'\n?[ \t]*<div class="form-row">\s*<span class="form-label"><span class="req">\*</span>审核结论</span>'
    r'[\s\S]*?<div class="modal-footer">[\s\S]*?</div>\s*</div>\s*</div>')
# 残尾模式 B：单独的 modal-footer + 闭合 div（createModal 残尾）
PAT_B = re.compile(
    r'\n?[ \t]*<div class="modal-footer">[\s\S]*?</div>\s*</div>\s*</div>')

total = 0
for p in sorted(glob.glob(os.path.join(PROTO, '*', '*.html'))):
    if os.sep + '弹窗' + os.sep in p:
        continue
    html = open(p, encoding='utf-8').read()
    removed = 0
    for _ in range(6):  # 迭代收敛（残尾可能多段/叠置）
        spans = modal_spans(html)
        def stray(m):
            return not any(s <= m.start() < e for s, e in spans)
        hits = [m for m in PAT_A.finditer(html) if stray(m)]
        hits += [m for m in PAT_B.finditer(html) if stray(m)]
        # 去掉互相包含的（A 含 B）
        hits = sorted(hits, key=lambda m: m.start())
        dedup = []
        for m in hits:
            if not any(m.start() >= d.start() and m.end() <= d.end() for d in dedup):
                dedup.append(m)
        if not dedup:
            break
        for m in reversed(dedup):
            html = html[:m.start()] + html[m.end():]
        removed += len(dedup)
    if removed:
        html = re.sub(r'\n{3,}', '\n\n', html)
        open(p, 'w', encoding='utf-8', newline='\n').write(html)
        rel = os.path.relpath(p, PROTO).replace(os.sep, '/')
        o = len(re.findall(r'<div\b', html)); c = len(re.findall(r'</div>', html))
        print(f'清理 {rel}: 删 {removed} 段 | 残存div差 {c - o}')
        total += removed
print(f'\n共删除 {total} 段残尾')

# 最终平衡报告
print('\n=== div 平衡终查 ===')
bad = 0
for p in sorted(glob.glob(os.path.join(PROTO, '*', '*.html'))):
    if os.sep + '弹窗' + os.sep in p:
        continue
    html = open(p, encoding='utf-8').read()
    o = len(re.findall(r'<div\b', html)); c = len(re.findall(r'</div>', html))
    if o != c:
        print(f'仍不平衡: {os.path.relpath(p, PROTO)} <div>={o} </div>={c}（差{c-o}）')
        bad += 1
print('全部平衡 ✅' if bad == 0 else f'{bad} 页待查')
