# -*- coding: utf-8 -*-
"""物料合并落账：A05（cls 行+记录数+D-96 注记）+ P2-R01（F-06+D-96 行）+ 基线追记 + 记忆。"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'

# ---------- A05（CRLF） ----------
P = ROOT + r'\P3-R01-包装租赁管理后台原型\P3-R01-A05-字段字典.md'
t = io.open(P, encoding='utf-8', newline='').read()
A1 = '| `cls` | 物料分类 ¹ | 枚举 | 围板箱 / 托盘 / 料箱 / 组件 | 12/12 |'
assert t.count(A1) == 1, 'A05 cls 锚 %d' % t.count(A1)
t = t.replace(A1, '| `cls` | 物料类型 ¹（D-96 合并·原物料分类） | 枚举 | 围板箱 / 塑料托盘 / 木托盘 / 料箱 / 料架 / 组件（托盘拆分·数据 2+1+1+2+0+6） | 12/12 |')
A2 = ('记录数 117（G16 +WL-01/02 物料类型·G21 +BF-04 按年/BF-05 按日·**G30** +13 组 65 项'
      '[RK→RKU 前缀避撞]+DW-07 托+ZF-03/04·49→117）')
assert t.count(A2) == 1, '记录数锚 %d' % t.count(A2)
t = t.replace(A2, '记录数 115（49→117 见 G30·**D-96 合并**：物料类型 WL 与物料分类 FL 二组合一——WL-01~06=分类 6 值[器具/零部件退役]、FL 组删除·117→115 项 24→23 组）')
# G30 注记尾部追加 D-96 注记
A3 = '主数据引用型 20 组不进字典（值源=各实体·登记 '
i3 = t.find(A3)
assert i3 > 0
# 找 G30 注记 blockquote 的行尾（该行以 117 项 24 组。 结尾）
m = re.search(r'分配表实辖 13 组 65 项、终态 117 项 24 组。\r\n', t)
assert m, 'G30 注记尾锚'
INS = ('\r\n> **D-96 物料类型×物料分类合并（2026-09-14·道远拍板「名称取物料类型·值取物料分类」）**：'
       'WL-01~06（物料类型）=原 FL 6 值（围板箱/塑料托盘/木托盘/料箱/料架/组件·abbr=code·G30 体例）；'
       'WL-01 器具/WL-02 零部件 退役；products.cls 值域 6 值（原「托盘」2 行按 name 拆 塑料托盘/木托盘）；'
       'info「分类」行标签→物料类型×12。**单据/派生域旧值域零改动**：purchaseOrders.mtype（零部件/器具·7 行·'
       'poQjRow 器具行联动依赖）、stockFlows.cls（租赁器具/零部件）、productTaxes.cls（标签仍物料分类·值域 '
       '6 值子集）——同名两层待接线任务统一。\r\n')
t = t.replace(m.group(0), m.group(0) + INS)
io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('PASS A05：cls 行+记录数 115+D-96 注记')

# ---------- P2-R01（CRLF） ----------
P2 = ROOT + r'\P2-R01-产品需求文档.md'
t = io.open(P2, encoding='utf-8', newline='').read()
A4 = '物料档案（物料类型×物料分类两级＋供应商税率维护区＋四参考价三段式租价）'
assert t.count(A4) == 1, 'F-06 锚 %d' % t.count(A4)
t = t.replace(A4, '物料档案（物料类型一级[原类型×分类两级合并·D-96·值域=围板箱/塑料托盘/木托盘/料箱/料架/组件]＋供应商税率维护区＋四参考价三段式租价）')
m = re.search(r'^\| D-95 \|.*?\| ✅ \|', t, re.M)
assert m, 'D-95 行未定位'
d95 = m.group(0)
A5 = '### A.5 维护规则'
anchor = d95 + '\r\n' + A5
assert t.count(anchor) == 1, 'D-95→A.5 锚 %d' % t.count(anchor)
D96 = ('| D-96 | 物料类型与物料分类合并（道远「两组重复·名称取物料类型·值取物料分类」）：字典 WL/FL 二组合一'
       '——WL-01~06=分类 6 值[器具/零部件退役·FL 删除]·dictItems 117→115 项 24→23 组；产品档案筛选/列头/cfg/'
       '新建弹窗双层两级→一级「物料类型」6 值（筛选原 5 值「托盘」口径一并统一）；products.cls「托盘」2 行按 '
       'name 拆 塑料托盘/木托盘·info「分类」→物料类型×12；单据/派生域旧二元值域零改动挂注记'
       '（purchaseOrders.mtype/stockFlows.cls/productTaxes.cls·接线任务统一） | 道远 09-14 对话拍板 | ✅ |')
t = t.replace(anchor, d95 + '\r\n' + D96 + '\r\n' + A5)
from collections import Counter
rows = re.findall(r'\| D-(\d+) \|', t)
cnt = Counter(int(x) for x in rows)
dup = [k for k, v in cnt.items() if v > 1]
missing = [i for i in range(1, 97) if i not in cnt]
assert not dup and not missing, 'dup=%s missing=%s' % (dup, missing)
io.open(P2, 'w', encoding='utf-8', newline='').write(t)
print('PASS P2-R01：F-06 一级化注记+D-96 落行（D-01~96 逐号恰一次）')

# ---------- 基线（LF） ----------
P3 = ROOT + r'\agent-handoff\_AGENT基线.md'
t = io.open(P3, encoding='utf-8', newline='').read()
marker = '- **追记（09-14 会话·客商收货信息独立维护·D-95）**：'
lines = t.split('\n')
hit = [i for i, l in enumerate(lines) if l.startswith(marker)]
assert len(hit) == 1, '收货信息追记行 %d' % len(hit)
assert 'D-96 物料合并' not in t
NEW = ('- **追记（09-14 会话·物料类型×物料分类合并·D-96）**：道远「两组重复·名称取物料类型·值取物料分类」——'
       'dictItems WL/FL 合并：WL-01~06=分类 6 值（围板箱/塑料托盘/木托盘/料箱/料架/组件·器具/零部件退役·'
       'FL 删除）·**117→115 项 24→23 组**；产品档案筛选（原 5 值「托盘」口径）/列头/cfg/新建弹窗双层两级→一级 '
       '6 值；products.cls「托盘」2 行按 name 拆塑料/木托盘·info「分类」→物料类型×12；数据字典页 dic-item 23；'
       '单据/派生域旧二元值零改动挂注记（PO.mtype 器具联动/SF.cls/ Taxes.cls·接线统一）；验证：PW 13 断言'
       '+listfull batch3 43 项+audit 产品档案零新增+node 0+截图×2')
lines.insert(hit[0] + 1, NEW)
t = '\n'.join(lines)
io.open(P3, 'w', encoding='utf-8', newline='').write(t)
print('PASS 基线追记')

# ---------- 记忆 ----------
MP = r'C:\Users\Administrator\.zcode\cli\memories\projects\5--active-22f97eac6e89b0ca\memory'
t = io.open(MP + r'\p3r01-prototype-baseline.md', encoding='utf-8', newline='').read()
A6 = '**下一任务**：'
assert A6 in t
NEW2 = ('**物料类型×物料分类合并（2026-09-14·D-96·交互任务）**：dictItems 117→**115 项 23 组**'
        '（WL=分类 6 值·器具/零部件退役·FL 删）；产品档案筛选/列头/cfg/弹窗双层一级化；products.cls 托盘拆 '
        '塑料/木；**单据/派生域旧二元值零改动**（PO.mtype 器具行联动/SF.cls/Taxes.cls——接线任务统一）。\n\n')
t = t.replace(A6, NEW2 + A6)
t = t.replace('（dictItems 49→117 项 24 组·13 组 65 项+双源统一 3 处·RKU 避撞·差集档留接线底稿）',
              '（dictItems 49→117 项 24 组·后 D-96 合并→115 项 23 组）')
io.open(MP + r'\p3r01-prototype-baseline.md', 'w', encoding='utf-8', newline='').write(t)
t2 = io.open(MP + r'\MEMORY.md', encoding='utf-8', newline='').read()
A7 = 'dictItems 49→117 项 24 组·13 组 65 项+双源统一 3 处·RKU 避撞·差集档留接线底稿'
assert t2.count(A7) == 1
t2 = t2.replace(A7, 'dictItems 49→117 项 24 组·后 D-96 物料合并→115 项 23 组')
io.open(MP + r'\MEMORY.md', 'w', encoding='utf-8', newline='').write(t2)
print('PASS 记忆双写')
