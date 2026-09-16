# -*- coding: utf-8 -*-
"""G40 T1 术语三条文本替换 + T2 路径引用同步（精确串·assert 计数·幂等）
范围：P3-R01-包装租赁管理后台原型/ 下 .html/.js/.json/.md/.css，跳过 .prompts/（工具日志·非交付物）
红线：白名单（F01 SRC_DATA 会议原文句 / A05 禁用写法列·沿革注记）先行掩码保护，替换后原样还原
"""
import io, os, sys, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(BASE, 'P3-R01-包装租赁管理后台原型')
EXTS = ('.html', '.js', '.json', '.md', '.css')

MASK = '\x00G40W%d\x00'
WHITELIST = [
    '客户回款、水单核销、收款核销',   # F01 SRC_DATA 第2次沟通音频转写原文（会议材料·禁改）
    '水单（D-142 已清）',             # A05 概念索引「禁用写法」列
    '水单号（待拍板）',               # A05 G17 标签同步沿革注记
    '水单→银行回单／盈亏→损益／回款→收款',  # A05 G37 D1 术语沿革注记（自述句）
]

# 顺序敏感：先长串路径（避免 银行水单→银行银行回单），再裸串，最后自由文本
REPL = [
    ('银行水单核销.html', '银行回单核销.html'),
    ('水单核销详情.html', '银行回单核销详情.html'),
    ('回款登记.html', '收款登记.html'),
    ('回款详情.html', '收款详情.html'),
    ('盈亏报表.html', '损益报表.html'),
    ('银行水单核销', '银行回单核销'),
    ('水单核销', '银行回单核销'),
    ('水单', '银行回单'),
    ('盈亏', '损益'),
    ('回款', '收款'),
]


def collect():
    out = []
    for dp, dn, fn in os.walk(ROOT):
        if '.prompts' in dp.replace(os.sep, '/'):
            continue
        for f in fn:
            if f.lower().endswith(EXTS):
                out.append(os.path.join(dp, f))
    return sorted(out)


def main():
    files = collect()
    print('扫描文件数 %d' % len(files))
    changed = []
    agg = collections.Counter()
    for p in files:
        s = io.open(p, encoding='utf-8', newline='').read()
        orig = s
        # 1) 掩码白名单
        masks = {}
        for i, lit in enumerate(WHITELIST):
            n = s.count(lit)
            if n:
                key = MASK % i
                masks[key] = lit
                s = s.replace(lit, key)
        # 2) 替换
        for a, b in REPL:
            c = s.count(a)
            if c:
                s = s.replace(a, b)
                agg[a + ' -> ' + b] += c
        # 3) 还原
        for key, lit in masks.items():
            s = s.replace(key, lit)
        if s != orig:
            io.open(p, 'w', encoding='utf-8', newline='').write(s)
            changed.append((os.path.relpath(p, ROOT), len(orig), len(s)))
    print('改动文件 %d' % len(changed))
    for r, a, b in changed[:200]:
        print('   %s   (%d -> %d)' % (r, a, b))
    print('--- 替换计数 ---')
    for k in sorted(agg):
        print('   %-40s %d' % (k, agg[k]))

    # 4) 终检：白名单外残留必须 0
    print('--- 终检（白名单外残留）---')
    bad = 0
    tot = collections.Counter()
    for p in files:
        s = io.open(p, encoding='utf-8', newline='').read()
        for i, lit in enumerate(WHITELIST):
            s = s.replace(lit, '')
        for t in ['水单', '盈亏', '回款']:
            c = s.count(t)
            if c:
                tot[t] += c
                bad += c
                print('   [残留] %s  %s x%d' % (t, os.path.relpath(p, ROOT), c))
    print('白名单外残留合计 = %d  %s' % (bad, dict(tot)))

    # 5) 白名单自身计数（应保持不变）
    print('--- 白名单内计数（应保留）---')
    for lit in WHITELIST:
        n = sum(io.open(p, encoding='utf-8', newline='').read().count(lit) for p in files)
        print('   %r x%d' % (lit, n))
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
