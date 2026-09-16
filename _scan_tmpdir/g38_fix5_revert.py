# -*- coding: utf-8 -*-
"""G38：混合粒度列标签回滚（cells 含时分→「时间」）＋A05 两行同步"""
import io, os

BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

for rel, old, new, exp in [
    (r'\租入管理\租入入库列表.html', '入库日期', '入库时间', 3),
    (r'\租入管理\租入归还列表.html', '归还日期', '归还时间', 3),
]:
    p = BASE + rel
    t = io.open(p, encoding='utf-8', newline='').read()
    n = t.count(old)
    if n == 0 and new in t:
        print('[SKIP] 已回滚', os.path.basename(p))
    else:
        assert n == exp, '%s x%d != %d' % (rel, n, exp)
        io.open(p, 'w', encoding='utf-8', newline='').write(t.replace(old, new))
        print('[OK] revert', os.path.basename(p))

p = BASE + r'\P3-R01-A05-字段字典.md'
t = io.open(p, encoding='utf-8', newline='').read()

def revert_in_section(text, section, old, new):
    import re
    m = re.search(r'^### %s ' % section, text, re.M)
    assert m, section
    start = m.start()
    nxt = re.search(r'^#{2,4} ', text[m.end():], re.M)
    end = m.end() + (nxt.start() if nxt else len(text))
    seg = text[start:end]
    assert seg.count(old) == 1, '%s x%d' % (section, seg.count(old))
    return text[:start] + seg.replace(old, new) + text[end:]

t = revert_in_section(t, 'rentInbounds', '| `date` | 入库日期 ¹ | date.biz |', '| `date` | 入库时间 ¹ | date.min |')
t = revert_in_section(t, 'rentInReturns', '| `date` | 归还日期 ¹ | date.biz |', '| `date` | 归还时间 ¹ | date.min |')
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('[OK] A05 rentInbounds/rentInReturns date 行回滚 时间/date.min（节内定界）')
