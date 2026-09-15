# -*- coding: utf-8 -*-
import io, os
ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def iter_files():
    for dp, dn, fn in os.walk(ROOT):
        for f in fn:
            if f.endswith(('.html', '.js', '.md', '.json', '.css')):
                yield os.path.join(dp, f)

def scan(terms, show=4):
    for term in terms:
        total = 0
        where = {}
        for p in iter_files():
            t = io.open(p, encoding='utf-8', newline='').read()
            n = t.count(term)
            if n:
                total += n
                rel = os.path.relpath(p, ROOT)
                i = t.find(term)
                where[rel] = t[max(0, i-20):i+len(term)+25].replace('\r', '').replace('\n', '⏎')
        print('[%s] total=%d files=%d' % (term, total, len(where)))
        for k, v in list(where.items())[:show]:
            print('   %s: …%s…' % (k, v))

print('=== 吕道远 定位 ===')
scan(['吕道远'], show=5)
print()
print('=== 表外疑似人名 ===')
scan(['林芳', '孙建军', '吴海涛', '郑卫东'], show=3)
print()
print('=== 道远 单独引用（成语风险） ===')
scan(['道远'], show=8)
print()
print('=== 英文缩写/第三方 ===')
scan(['FAW', '吉客云', '瑞迅凯', '五菱', '大众', '本田', '小鹏', '吉利', '蔚山'], show=3)
