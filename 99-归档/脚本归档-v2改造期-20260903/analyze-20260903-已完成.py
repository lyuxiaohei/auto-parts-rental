# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已完成（v2改造期只读分析）
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
"""分析所有页面侧边栏结构是否一致（忽略 selected/open/onclick 差异）"""
import os, re, hashlib, glob, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROTO = os.path.join(ROOT, 'P3-R01-包装租赁管理后台原型')

pages = sorted(glob.glob(os.path.join(PROTO, '*', '*.html')))
print(f'共 {len(pages)} 个页面\n')

def extract_sidebar(html):
    m = re.search(r'<ul class="side-menu">.*?</aside>', html, re.S)
    return m.group(0) if m else None

def normalize(sb):
    sb = re.sub(r'\s+', '', sb)
    sb = sb.replace('selected', '').replace('open', '')
    sb = re.sub(r'onclick="[^"]*"', '', sb)
    return sb

groups = {}
for p in pages:
    html = open(p, encoding='utf-8').read()
    sb = extract_sidebar(html)
    rel = os.path.relpath(p, PROTO)
    if sb is None:
        print(f'[无侧边栏] {rel}')
        continue
    h = hashlib.md5(normalize(sb).encode('utf-8')).hexdigest()[:8]
    groups.setdefault(h, []).append(rel)

print(f'归一化后侧边栏版本数: {len(groups)}')
for h, files in groups.items():
    print(f'\n== 版本 {h} ({len(files)} 页) ==')
    for f in files:
        print('   ', f)

# 检查 go() 中引用的所有文件是否存在
print('\n===== 死链检查（v1 基线） =====')
dead = 0
for p in pages:
    html = open(p, encoding='utf-8').read()
    for m in re.finditer(r'''go\(\s*['"]([^'"]+)['"]''', html):
        url = m.group(1)
        if url.startswith('http') or url.startswith('#'):
            continue
        target = os.path.normpath(os.path.join(os.path.dirname(p), url))
        if not os.path.exists(target):
            print(f'死链: {os.path.relpath(p, PROTO)} -> {url}')
            dead += 1
print(f'v1 死链数: {dead}')

# 检查 side-foot / sys-switch 是否每页都有
print('\n===== 系统切换器分布 =====')
for p in pages:
    html = open(p, encoding='utf-8').read()
    rel = os.path.relpath(p, PROTO)
    has_switch = 'sysSwitchBtn' in html
    has_foot = 'side-foot' in html
    if not (has_switch and has_foot):
        print(f'{rel}: switch={has_switch} foot={has_foot}')
print('检查完毕（无输出=全部页面都有切换器）')
