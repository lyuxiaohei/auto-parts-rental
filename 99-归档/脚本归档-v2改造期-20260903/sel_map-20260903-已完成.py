# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已完成（选择器映射）
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
import os, re, glob, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROTO = os.path.join(ROOT, 'P3-R01-包装租赁管理后台原型')
for p in sorted(glob.glob(os.path.join(PROTO, '*', '*.html'))):
    html = open(p, encoding='utf-8').read()
    rel = os.path.relpath(p, PROTO)
    sel = re.search(r'<div class="sm-link selected"[^>]*>([^<]*)</div>', html)
    seltop = re.search(r'<div class="sm-link selected"[^>]*>.*?</div>', html, re.S)
    opened = re.findall(r'<li class="sm-item has-sub open">.*?</span>([^<]+)<span class="sm-arrow">', html, re.S)
    title = re.search(r'<title>([^<]*)</title>', html)
    print(f'{rel} | selected={sel.group(1).strip() if sel else "(top?)"} | open={opened} | title={title.group(1) if title else ""}')
