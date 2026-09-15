# -*- coding: utf-8 -*-
"""G36 C1 修复：撤错位插入（落进了 timeline/相邻 info 后）→ 按「锚点所在块」重插"""
import io, os

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
FP = os.path.join(ROOT, '_data', 'demo-data.js')
s = io.open(FP, encoding='utf-8', newline='').read()

def rec_start(key):
    i = s.index('\n    ' + chr(39) + key + chr(39) + ': {')
    return i

def insert_after_containing_block(anchor, from_pos):
    """在 from_pos 起找 anchor，定位包含它的 {...} 块，返回 (插入点, 是否需补逗号)。
    块后随 ',' → 插入点在逗号后；块是数组末项（后随换行+]）→ 插入点在 '}' 后且需补逗号（JS 尾逗号合法）"""
    ap = s.index(anchor, from_pos)
    a = s.rfind('{', 0, ap)
    i = a; depth = 0
    while True:
        if s[i] == '{':
            depth += 1
        elif s[i] == '}':
            depth -= 1
            if depth == 0:
                break
        i += 1
    j = i + 1
    if s[j] == ',':
        return j + 1, ''
    assert s[j] in '\r\n ', 'unexpected %r' % s[j:j+12]
    return i + 1, ','

def make_entry(k, v, url=None):
    t = '\n        {\n'
    t += "          '%s': '%s',\n" % (k, v)
    if url:
        t += "          'url': '%s'\n" % url
    t += '        },'
    return t

# 1) 撤销三处错位插入
E1 = "\n        {\n          'role': '租赁出库（立即转租·供应商直发）',\n          'name': 'CK-20260914-023 · 待审核',\n          'url': '租赁管理/租赁出库列表.html'\n        },"
E2 = "\n        {\n          'role': '立即转租生成 · 租赁出库',\n          'name': 'CK-20260914-023 · 待审核',\n          'url': '租赁管理/租赁出库列表.html'\n        },"
E3 = "\n        {\n          'label': '关联租入单',\n          'text': 'RZD-20260902-008',\n          'url': '租入管理/租入单列表.html'\n        },"
for e in (E1, E2, E3):
    assert s.count(e) == 1, 'undo anchor x%d' % s.count(e)
    s = s.replace(e, '')
print('撤销 3 处错位插入 ✓')

# 2) 重插（包含块定位·限定记录范围）
i = rec_start('RZD-20260902-008')
p, c0 = insert_after_containing_block("'role': '租入入库',", i)
s = s[:p] + c0 + E1 + s[p:]
i = rec_start('RZRK-20260903-023')
p, c0 = insert_after_containing_block("'role': '租入入库（本单）',", i)
s = s[:p] + c0 + E2 + s[p:]
i = rec_start('CK-20260914-023')
p, c0 = insert_after_containing_block("'label': '关联租入入库',", i)
s = s[:p] + c0 + E3 + s[p:]
print('重插 3 处（链/信息块后） ✓')

# 3) 校验：RZD-008 的 chain 数组内含 CK；timeline 内无 'role'
i = rec_start('RZD-20260902-008')
j = s.index("'timeline'", i)
chain_sec = s[s.index("'chain'", i):j]
assert 'CK-20260914-023' in chain_sec, 'RZD-008 chain still missing CK'
tl_sec = s[j:s.index('\n    }', j)]
assert "'role'" not in tl_sec, 'timeline polluted'
i = rec_start('RZRK-20260903-023')
j2 = s.index("'timeline'", i)
chain2 = s[s.index("'chain'", i):j2]
assert 'CK-20260914-023' in chain2 and 'RZD-20260902-008' in chain2
tl2 = s[j2:s.index('\n    }', j2)]
assert "'role'" not in tl2
io.open(FP, 'w', encoding='utf-8', newline='').write(s)
print('校验通过：两链含 CK 且 timeline 无污染；已写盘')
