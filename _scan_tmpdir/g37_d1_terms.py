# -*- coding: utf-8 -*-
"""G37 D1：页面内术语三条统一（D-142）——原型目录全站替换
水单→银行回单（银行水单→银行回单 先行防叠词）｜盈亏→损益｜回款→收款
保护：5 个含术语文件名的 href/go() 引用（文件名不改）＋F01 SRC_DATA 会议原文句＋A05 G25 保留句
白名单文件：P3-R01-F01-业务流程导航图-开发规则.md（沿革文档）整文件不动。"""
import io, os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
PROTECT = ['银行水单核销.html', '水单核销详情.html', '回款登记.html', '回款详情.html', '盈亏报表.html']
PH = ['\x00P%d\x00' % i for i in range(len(PROTECT))]
SKIP_FILES = {os.path.join('P3-R01-F01-业务流程导航图-开发规则.md')}
# 沿革句白名单（逐文件）
HERITAGE = {
    'P3-R01-F01-业务流程导航图.html': ['再是客户回款、水单核销、收款核销'],
    'P3-R01-A05-字段字典.md': ['水单号（待拍板）'],
}

def apply(s):
    for i, fn in enumerate(PROTECT):
        s = s.replace(fn, PH[i])
    hph = []
    for i, sent in enumerate(HERITAGE.get(cur, [])):
        if sent in s:
            hph.append(('\x00H%d\x00' % i, sent))
            s = s.replace(sent, '\x00H%d\x00' % i)
    n0 = (s.count('水单'), s.count('盈亏'), s.count('回款'))
    s = s.replace('银行水单', '银行回单')
    s = s.replace('水单', '银行回单')
    s = s.replace('盈亏', '损益')
    s = s.replace('回款', '收款')
    for ph, sent in hph:
        s = s.replace(ph, sent)
    for i, fn in enumerate(PROTECT):
        s = s.replace(PH[i], fn)
    return s, n0

tot = [0, 0, 0]
nfiles = 0
for dp, dn, fn in os.walk(ROOT):
    if 'backup' in dp or os.sep + 'mobile' in dp:
        continue
    for f in fn:
        if not (f.endswith('.html') or f.endswith('.js') or f.endswith('.md') or f.endswith('.json')):
            continue
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, ROOT)
        if rel in SKIP_FILES:
            continue
        s = io.open(p, encoding='utf-8', newline='').read()
        cur = rel
        n0 = (s.count('水单'), s.count('盈亏'), s.count('回款'))
        if not any(n0):
            continue
        s2, _ = apply(s)
        # 文件名引用必须原样保留
        for fnm in PROTECT:
            assert s2.count(fnm) == s.count(fnm), rel + ' 文件名引用被改: ' + fnm
        io.open(p, 'w', encoding='utf-8', newline='').write(s2)
        tot[0] += n0[0]; tot[1] += n0[1]; tot[2] += n0[2]
        nfiles += 1

print('D1 替换完成：%d 文件｜水单 %d→0｜盈亏 %d→0｜回款 %d→0' % (nfiles, tot[0], tot[1], tot[2]))

# ---- 残留统计（白名单外应为 0）----
res = {'水单': [], '盈亏': [], '回款': []}
for dp, dn, fn in os.walk(ROOT):
    if 'backup' in dp or os.sep + 'mobile' in dp:
        continue
    for f in fn:
        if not (f.endswith('.html') or f.endswith('.js') or f.endswith('.md') or f.endswith('.json')):
            continue
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, ROOT)
        if rel in SKIP_FILES:
            continue
        s = io.open(p, encoding='utf-8', errors='replace').read()
        # 还原句/文件名单独剔除后统计
        s2 = s
        for sent in HERITAGE.get(rel, []):
            s2 = s2.replace(sent, '')
        for fnm in PROTECT:
            s2 = s2.replace(fnm, '')
        for w in res:
            c = s2.count(w)
            if c:
                res[w].append((rel, c))
for w in res:
    print('残留 %s：%s' % (w, res[w] if res[w] else '0（白名单外清零）'))
