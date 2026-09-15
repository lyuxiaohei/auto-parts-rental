# -*- coding: utf-8 -*-
"""G35 T4 第二轮：表外复合真名派生替换（勘察 Phase3 残留处置）"""
import io, os

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
PAIRS2 = [
    ('一汽大众汽车有限公司', '北方商用汽车有限公司'),
    ('一汽大众', '北方商用'),
    ('东风锂电', '长丰锂电'),                      # 映射表只含「东风锂电科技」全形·数据用短形·同族派生
    ('小鹏', '星途'),                              # 小鹏汽车短形·同族派生
    ('一汽解…', '华骏重卡…'),                       # A05 截断残片
    ('中国工商银行长春第一汽车厂支行', '中国工商银行长春汽车城支行'),  # 真实支行名→派生
]
PAIRS2.sort(key=lambda x: len(x[0]), reverse=True)

def iter_files():
    for dp, dn, fn in os.walk(ROOT):
        for f in fn:
            if f.endswith(('.html', '.js', '.md', '.json', '.css')):
                yield os.path.join(dp, f)

print('== T4 round2 ==')
totals = {}
touched = 0
for p in iter_files():
    t = io.open(p, encoding='utf-8', newline='').read()
    orig = t
    for old, new in PAIRS2:
        if old in t:
            n = t.count(old)
            t = t.replace(old, new)
            totals[old] = totals.get(old, 0) + n
    if t != orig:
        io.open(p, 'w', encoding='utf-8', newline='').write(t)
        touched += 1
print('touched files:', touched)
for old, new in PAIRS2:
    print('  %s -> %s : %d' % (old, new, totals.get(old, 0)))

# 终扫：碎片词（东风大街=街名·地名保留·白名单）
print('== 终扫 ==')
bad = 0
for w in ['一汽', '上汽', '东风', '本田', '小鹏', '吉利', '五菱', '大众', 'FAW']:
    n = 0
    where = []
    for p in iter_files():
        t = io.open(p, encoding='utf-8', newline='').read()
        c = t.count(w)
        if c:
            n += c
            i = t.find(w)
            where.append((os.path.relpath(p, ROOT), t[max(0,i-12):i+14].replace('\r','').replace('\n','⏎')))
    if n:
        bad += 1
        print('  [%s] %d' % (w, n))
        for rel, ctx in where[:5]:
            print('     %s …%s…' % (rel, ctx))
    else:
        print('  [%s] OK(0)' % w)
print('RESIDUE:', bad)
