# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已完成（一次性校验）
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
    titles = re.findall(r'<h3 class="card-title"[^>]*>([^<]*)</h3>', html)
    h2 = re.findall(r'<h2[^>]*>([^<]*)</h2>', html)
    ths = re.findall(r'<th[^>]*>([^<]*)</th>', html)
    has_status = any('状态' in t for t in ths)
    print(f'{rel}\n  card-titles={titles} h2={h2}\n  状态列={has_status} 列数={len(ths)}')
