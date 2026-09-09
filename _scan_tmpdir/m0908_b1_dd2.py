# -*- coding: utf-8 -*-
"""批1 Stage7b：demo-data 残留收尾——链尾退租申请节点替换 + 财务实体内联 url 剥离"""
from pathlib import Path
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
DD = ROOT / "P3-R01-包装租赁管理后台原型" / "_data" / "demo-data.js"
src = DD.read_bytes().decode('utf-8')

# 1. leaseOrders 链尾退租申请节点（url 已被前轮剥除）→ 退租入库节点
old_node = ("        {\n          'role': '退租申请',\n          'name': 'TZSQ-20260902-008',\n        }")
new_node = ("        {\n          'role': '退租入库',\n          'name': 'TZRK-20260902-010',\n          'url': '租赁管理/退租入库列表.html'\n        }")
c = src.count(old_node)
assert c == 1, f'链尾申请节点 {c}'
src = src.replace(old_node, new_node)
print(' ✓ leaseOrders 链尾节点→退租入库 1')

# 2. 财务实体内联 url 剥离（refs/fees/chain 单行式）
REMOVED = r"(?:租赁管理/退租申请列表|仓储作业/组装列表|仓储作业/组装录单|仓储作业/拆卸管理列表|租赁管理/丢损赔偿单)\.html"
src, k1 = re.subn(r", url: '" + REMOVED + r"'", '', src)
src, k2 = re.subn(r"url: '" + REMOVED + r"', ", '', src)
print(f' ✓ 内联 url 剥 {k1}+{k2}')
assert k1 + k2 == 8, f'内联 url {k1}+{k2}≠8'

DD.write_bytes(src.encode('utf-8'))

# 3. 校验
assert not re.search(REMOVED, src), '被移除页路径残留'
import subprocess
r = subprocess.run(['node', '--check', str(DD)], capture_output=True, text=True)
assert r.returncode == 0, f'node --check 失败: {r.stderr[:500]}'
# 退租申请 角色节点残留检查（应仅剩有意保留的丢损赔偿类纯文本节点）
leftover_roles = re.findall(r"'role': '(退租申请[^']*)'", src)
print('PASS: 残留清零 + node --check 通过；退租申请 role 残留:', leftover_roles)
