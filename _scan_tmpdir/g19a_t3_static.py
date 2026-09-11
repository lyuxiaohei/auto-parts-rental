# -*- coding: utf-8 -*-
"""G19a T3 静态断言：css 色板/骨架件/结构/_m.js 零变化"""
import pathlib, re, subprocess, sys

MOB = pathlib.Path(r'P3-R01-包装租赁管理后台原型/mobile')
css = (MOB / '_m.css').read_text(encoding='utf-8')
ok = True

# 1a 主色变量
c1 = '--primary: #1677ff' in css
print('[1a] _m.css has --primary: #1677ff :', c1); ok &= c1
# 1b 电商红零混入（css+五页全查）
red = 0
for f in list(MOB.glob('*.css')) + list(MOB.glob('*.html')):
    red += len(re.findall(r'#ff6034|#ee0a24', f.read_text(encoding='utf-8')))
print('[1b] grep #ff6034|#ee0a24 in mobile/* =', red); ok &= (red == 0)

# 2 骨架件 grep 五页合计=0
sk = 0
pages = ['登录.html', '待办审批.html', '审批详情.html', '库存查询.html', '我的.html']
for pg in pages:
    sk += len(re.findall(r'status-bar|capsule-btn|phone-frame', (MOB / pg).read_text(encoding='utf-8')))
print('[2a] skeleton grep 5 pages total =', sk); ok &= (sk == 0)

# 2b 每页含内容区组件（卡片容器类 m-card/m-item/m-stat/m-cell 任一）+ m-header（登录页豁免·记偏差）
DEV = []
for pg in pages:
    s = (MOB / pg).read_text(encoding='utf-8')
    card = bool(re.search(r'class="m-card|class="m-item |id="m-list"|class="m-stat', s))
    hdr = 'm-header' in s
    if pg == '登录.html':
        print(f'[2b] {pg}: card-ish={card}, m-header=EXEMPT(登录页无导航·G14既定设计·偏差D-b1)')
        DEV.append('D-b1 登录页无 m-header（登录前无导航为既定设计，断言豁免）')
        ok &= card
    else:
        print(f'[2b] {pg}: card={card}, m-header={hdr}')
        ok &= (card and hdr)

# 2c _m.js 与 git HEAD 零变化
r = subprocess.run(['git', 'diff', '--stat', '--', 'P3-R01-包装租赁管理后台原型/mobile/_m.js'],
                   capture_output=True, text=True, encoding='utf-8')
c = (r.stdout.strip() == '')
print('[2c] git diff _m.js empty :', c); ok &= c
# 双保险：与备份 MD5 一致
import hashlib
m1 = hashlib.md5((MOB / '_m.js').read_bytes()).hexdigest()
m2 = hashlib.md5(pathlib.Path(r'_scan_tmpdir/backup-g19a-20260911/mobile/_m.js').read_bytes()).hexdigest()
print('[2c2] _m.js md5 == backup :', m1 == m2); ok &= (m1 == m2)

# 2d Emoji 残留检查（tabbar/cell 纪律）
emoji_re = re.compile(r'[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF]')
for pg in pages:
    s = (MOB / pg).read_text(encoding='utf-8')
    hits = emoji_re.findall(s)
    if hits:
        print(f'[2d] {pg} emoji residue: {hits}'); ok = False
print('[2d] emoji residue 5 pages : 0 (if no lines above)')

print('STATIC ALL PASS:', ok)
