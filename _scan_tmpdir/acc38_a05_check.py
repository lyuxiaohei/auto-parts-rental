# -*- coding: utf-8 -*-
# acc38 独立验收·第4项 概念层复验（只读）
import io, re, collections
A05 = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\P3-R01-A05-字段字典.md'
t = io.open(A05, encoding='utf-8').read()
lines = t.splitlines()

# 1) 「## 字段概念索引」节内概念行数
start = end = None
for i, ln in enumerate(lines):
    if ln.startswith('## 字段概念索引') and start is None:
        start = i
    elif start is not None and ln.startswith('## ') and i > start:
        end = i
        break
sec = lines[start+1:end] if end else lines[start+1:]
concept_rows = [ln for ln in sec if ln.startswith('| `')]
print('「## 字段概念索引」节范围: 行%d-%d' % (start+1, end if end else len(lines)))
print('概念行数（| ` 开头）=', len(concept_rows))
doms = collections.Counter()
for ln in concept_rows:
    m = re.match(r'\| `([\w.]+)`', ln)
    if m:
        doms[m.group(1).split('.')[0]] += 1
print('域分布:', dict(doms))

# 2) 全文件 | ` 开头行数（实体字段行）
allrows = [ln for ln in lines if ln.startswith('| `')]
print('全文件 | ` 开头行数 =', len(allrows))

# 3) 字段行中含〔待核〕
taihe = [ln for ln in allrows if '〔待核〕' in ln]
print('字段行含〔待核〕数 =', len(taihe))
print('全文件〔待核〕出现总次数 =', t.count('〔待核〕'))
for i, ln in enumerate(lines):
    if '〔待核〕' in ln:
        print('  行%d: %s' % (i+1, ln[:120]))
print('== done ==')
