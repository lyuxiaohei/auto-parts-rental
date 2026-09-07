# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已完成（一次性校验）
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
import os, re, glob, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2lib
PROTO = v2lib.PROTO
pages = [os.path.relpath(p, PROTO).replace(os.sep, '/') for p in glob.glob(os.path.join(PROTO, '*', '*.html'))]
print('现有页面数:', len(pages))

for rel in sorted(pages):
    html = v2lib.read_page(rel)
    m = re.search(r'<div class="sm-link selected">(?:<span class="sm-ico">.*?</span>)?([^<]*)</div>', html)
    opens = re.findall(r'<li class="sm-item has-sub open">\s*<div class="sm-link">.*?</span>([^<]+)<span class="sm-arrow">', html, re.S)
    switcher = 'sysSwitchBtn' in html or 'sys-pop' in html
    print(f'{rel} | selected={m.group(1) if m else "无"} | open={opens} | 切换器残留={switcher}')

print()
print('=== 误替换扫描 ===')
hit = False
for rel in sorted(pages):
    html = v2lib.read_page(rel)
    for bad in ['电子项', '零件项', '部项', '组项', '器材料', '包装包装', '租赁管理</', '>租赁管理<']:
        if bad in html:
            print(f'{rel}: 发现可疑词 {bad}')
            hit = True
if not hit:
    print('无可疑替换')
