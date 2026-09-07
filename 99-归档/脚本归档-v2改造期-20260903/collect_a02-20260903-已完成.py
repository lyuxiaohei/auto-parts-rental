# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已完成（A02收集）
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
"""A02 数据采集（v2 终态）：每页按钮/链接/弹窗统计，输出供文档使用"""
import os, re, glob, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
PROTO = 'P3-R01-包装租赁管理后台原型'
pages = sorted(glob.glob(os.path.join(PROTO, '*', '*.html')))

# 全站通用 JS 交互（统一脚本/按 id 绑定），不算"无交互"：
UNIVERSAL = {'展开', '收起'}
# 全站通用视觉元素（统一说明，不逐页列）
COMMON_VISUAL = {'重置', '查询', '批量导出'}

total_btn_dead = {}
total_link_dead = {}
modal_rows = []
for p in pages:
    rel = os.path.relpath(p, PROTO).replace(os.sep, '/')
    html = open(p, encoding='utf-8').read()
    body = re.sub(r'<aside class="sidebar">.*?</aside>', '', html, flags=re.S)

    modal_defs = re.findall(r'<div class="modal-overlay" id="([^"]+)"', body)
    for mid in modal_defs:
        mt = re.search(r'id="' + mid + r'">.*?<h3 class="modal-title">([^<]*)</h3>', body, re.S)
        modal_rows.append((rel, mid, mt.group(1) if mt else '?'))

    btn_els = re.findall(r'(<button[^>]*>)(.*?)</button>', body, re.S)
    dead_b = []
    for attrs, text in btn_els:
        t = re.sub(r'<[^>]+>', '', text).strip()
        if 'onclick' in attrs or t in UNIVERSAL:
            continue
        dead_b.append(t)
    a_all = re.findall(r'<a([^>]*)>(.*?)</a>', body, re.S)
    dead_a = sorted(set(re.sub(r'<[^>]+>', '', t).strip() for at, t in a_all if 'onclick' not in at))
    total_btn_dead[rel] = dead_b
    total_link_dead[rel] = dead_a
    print(f'{rel} | 弹窗{len(modal_defs)} | 死按钮{len(dead_b)} | 死链接{len(dead_a)}')

print()
print('=== 弹窗清单 ===')
for rel, mid, t in modal_rows:
    print(f'{rel} | {mid} | {t}')
print(f'弹窗总数: {len(modal_rows)}')

# 统计汇总
db = sum(len(v) for v in total_btn_dead.values())
da = sum(len(v) for v in total_link_dead.values())
print(f'\n死按钮合计(含通用): {db}；死链接合计(去重/页): {da}')

# openModal 悬空引用复查
bad = []
for p in pages:
    html = open(p, encoding='utf-8').read()
    defs = set(re.findall(r'<div class="modal-overlay" id="([^"]+)"', html))
    refs = set(re.findall(r"openModal\('([^']+)'\)", html))
    if refs - defs:
        bad.append((p, refs - defs))
print('悬空弹窗引用:', bad if bad else '无')
