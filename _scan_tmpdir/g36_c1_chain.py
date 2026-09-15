# -*- coding: utf-8 -*-
"""G36 C1 背靠背转租数据链（D-105）：RZD-20260902-008 ↔ RZRK-20260903-023 ↔ CK-20260914-023 三向互溯"""
import io, os

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
FP = os.path.join(ROOT, '_data', 'demo-data.js')
s = io.open(FP, encoding='utf-8', newline='').read()

def rec_start(key):
    return s.index('\n    ' + chr(39) + key + chr(39) + ': {')

def insert_after_block(anchor_pos, entry_text):
    """在 anchor_pos 起的 {...} 条目的收尾 ',' 后插入 entry_text（多行格式与既有条目一致）"""
    i = s.index('{', anchor_pos)
    depth = 0
    while True:
        if s[i] == '{':
            depth += 1
        elif s[i] == '}':
            depth -= 1
            if depth == 0:
                break
        i += 1
    # i = '}'；其后应为 ',' + 换行
    j = i + 1
    assert s[j] == ',', 'expect comma after block at %d: %r' % (j, s[j:j+20])
    return j + 1  # 插入点：逗号后

def make_entry(role, name, url=None, self_=False):
    t = '\n        {\n'
    t += "          'role': '%s',\n" % role
    t += "          'name': '%s'" % name
    if url:
        t += ",\n          'url': '%s'" % url
    if self_:
        t += ",\n          'self': true"
    t += '\n        },'
    return t

# ---- 1. RZD-20260902-008 链尾补「租赁出库（立即转租）」 ----
i = rec_start('RZD-20260902-008')
a = s.index("'role': '租入入库',", i)
p = insert_after_block(a, None)
entry = make_entry('租赁出库（立即转租·供应商直发）', 'CK-20260914-023 · 待审核', '租赁管理/租赁出库列表.html')
s = s[:p] + entry + s[p:]
print('1. RZD-008 chain + CK-023 前向链 ✓')

# ---- 2. RZRK-20260903-023 链尾补「立即转租生成 · 租赁出库」 ----
i = rec_start('RZRK-20260903-023')
a = s.index("'role': '租入入库（本单）',", i)
p = insert_after_block(a, None)
entry = make_entry('立即转租生成 · 租赁出库', 'CK-20260914-023 · 待审核', '租赁管理/租赁出库列表.html')
s = s[:p] + entry + s[p:]
print('2. RZRK-023 chain + CK-023 前向链 ✓')

# ---- 3. CK-20260914-023 info 补「关联租入单」回链 ----
i = rec_start('CK-20260914-023')
a = s.index("'label': '关联租入入库',", i)
p = insert_after_block(a, None)
entry = ('\n        {\n'
         "          'label': '关联租入单',\n"
         "          'text': 'RZD-20260902-008',\n"
         "          'url': '租入管理/租入单列表.html'\n"
         '        },')
s = s[:p] + entry + s[p:]
print('3. CK-023 info + RZD-008 回链 ✓')

io.open(FP, 'w', encoding='utf-8', newline='').write(s)

# ---- 4. 租入入库列表 确认弹窗「立即转租」勾选态与链路一致（默认勾选） ----
FP2 = os.path.join(ROOT, '租入管理', '租入入库列表.html')
t = io.open(FP2, encoding='utf-8', newline='').read()
old = '<input type="checkbox" class="cb"><span>供应商直发终端客户——登记同时自动生成租赁出库单（自动带物料 · 免重复填单）</span>'
new = '<input type="checkbox" class="cb" checked><span>供应商直发终端客户——登记同时自动生成租赁出库单（自动带物料 · 免重复填单）</span>'
assert t.count(old) == 1, 'checkbox anchor x%d' % t.count(old)
t = t.replace(old, new)
io.open(FP2, 'w', encoding='utf-8', newline='').write(t)
print('4. 租入入库确认弹窗 立即转租 默认勾选 ✓（与 CK-023 链路一致）')
print('C1 DONE')
