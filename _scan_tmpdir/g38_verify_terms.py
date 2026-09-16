# -*- coding: utf-8 -*-
"""G38 完成判定 2/4 证据：7 组异名逐词 str.count＋概念层计数"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
os.chdir(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型')

print('=== 7 组异名逐词 str.count（全站 HTML＋_data js·backup 除外）===')
files = []
for root, ds, fs in os.walk('.'):
    if 'backup' in root or 'node_modules' in root:
        continue
    for f in fs:
        if f.endswith(('.html', '.js')):
            files.append(os.path.join(root, f))
terms = ['货品', '入库库区', '出库库区', '调出库区', '调入库区', '零件号', '托数', '每托数量', '入库总数', '到货托数', '以托为单位', '租赁器具']
for term in terms:
    hits = []
    for p in files:
        t = io.open(p, encoding='utf-8', errors='ignore').read()
        n = t.count(term)
        if n:
            hits.append((p[2:], n))
    tot = sum(n for _, n in hits)
    print('%-8s 合计 %-4d %s' % (term, tot, hits[:5] if hits else ''))

print()
t = io.open(r'_data\demo-data.js', encoding='utf-8').read()
print('=== demo-data 直查 ===')
print('货品(扣供货品类) = %d' % (t.count('货品') - t.count('供货品类')))
for term in ['入库库区', '出库库区', '调出库区', '调入库区', '零件号', '托数', '每托数量', '入库总数', '以托为单位', '租赁器具', '多货品']:
    print('%s = %d' % (term, t.count(term)))

print()
a05 = io.open(r'P3-R01-A05-字段字典.md', encoding='utf-8').read()
i = a05.find('## 字段概念索引')
j = a05.find('## 基础资料')
ct = [l for l in a05[i:j].splitlines() if l.startswith('| `')]
rows = [l for l in a05.splitlines() if re.match(r'^\|\s*`[\w.]+`\s*\|', l) and not any(l.startswith('| `' + c) for c in ('price.', 'qty.', 'date.', 'wh.', 'material.', 'doc.', 'status.', 'partner.', 'project.', 'amount.'))]
print('=== 概念层 ===')
print('概念表行数 = %d（60 概念＋表头行外）' % (len(ct) - 1))
print('A05 字段行（实体节·六列）= %d' % len(rows))
print('A05 行级〔待核〕残留 = %d' % len([l for l in rows if '〔待核〕' in l]))
