# -*- coding: utf-8 -*-
"""收货信息落账：P2-R01（F-06 增量注记+D-94 台账行）+ P1-R08 计数同步 + 基线追记。"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'

# ---------- P2-R01（CRLF） ----------
P = ROOT + r'\P2-R01-产品需求文档.md'
t = io.open(P, encoding='utf-8', newline='').read()
assert t.count('\r\n') > 1000

A_F6 = '客商管理（客户/供应商两类）'
assert t.count(A_F6) == 1, 'F-06 锚 %d' % t.count(A_F6)
t = t.replace(A_F6, '客商管理（客户/供应商两类＋开票资料/收货信息行内维护·D-94）')

A_D93 = '| ✅ |'  # 占位防误判——实际锚用 D-93 行尾+A.5 节头
import re
m = re.search(r'^\| D-93 \|.*?\| ✅ \|', t, re.M)
assert m, 'D-93 行未定位'
d93 = m.group(0)
A5 = '### A.5 维护规则'
anchor = d93 + '\r\n' + A5
assert t.count(anchor) == 1, 'D-93→A.5 毗邻锚 %d' % t.count(anchor)
D94 = ('| D-94 | 客商收货信息独立维护：客商管理列表操作列新增「收货信息」入口（详情/编辑/开票资料/收货信息'
       '四操作·参照开票资料先例），独立弹窗维护收货人/收货电话/收货地址——与联系人/联系电话（商务联系）'
       '两套信息区分互不混用；partners ops×8+静态行×8+recvInfoModal 弹窗+弹窗/客商收货信息.html 模板（双层）'
       ' | 道远 09-14 对话拍板（区分商务联系与收货信息·列表按钮+独立弹窗维护） | ✅ |')
t = t.replace(anchor, d93 + '\r\n' + D94 + '\r\n' + A5)
nums = sorted(set(int(x) for x in re.findall(r'\| D-(\d+) \|', t)))
assert nums == list(range(1, 95)), '台账行数异常 max=%d n=%d' % (nums[-1], len(nums))
io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('PASS P2-R01：F-06 注记+D-94 落行（台账 94 行连续）')

# ---------- P1-R08（LF） ----------
P2 = ROOT + r'\P1-R08-项目文件索引.md'
t2 = io.open(P2, encoding='utf-8', newline='').read()
assert t2.count('\r\n') == 0
A1 = '### 3.1 `P3-R01-包装租赁管理后台原型/`（115 HTML = PC 110 + mobile 5）'
assert t2.count(A1) == 1, 'P1-R08 3.1 锚 %d' % t2.count(A1)
t2 = t2.replace(A1, '### 3.1 `P3-R01-包装租赁管理后台原型/`（116 HTML = PC 111 + mobile 5）')
A2 = '| 弹窗模板（69 个） |'
assert t2.count(A2) == 1, 'P1-R08 模板行锚 %d' % t2.count(A2)
t2 = t2.replace(A2, '| 弹窗模板（70 个） |')
io.open(P2, 'w', encoding='utf-8', newline='').write(t2)
print('PASS P1-R08：116 HTML=PC 111+mobile 5·模板 70')

# ---------- 基线（LF） ----------
P3 = ROOT + r'\agent-handoff\_AGENT基线.md'
t3 = io.open(P3, encoding='utf-8', newline='').read()
assert t3.count('\r\n') == 0
A_P = '- **原型**：108 页（38 业务页 + 独立弹窗模板 69 + F01）'
assert t3.count(A_P) == 1, '基线原型 bullet 头锚 %d' % t3.count(A_P)
t3 = t3.replace(A_P, '- **原型**：109 页（38 业务页 + 独立弹窗模板 70 + F01·09-14 收货信息弹窗模板 +1）')
A_115 = '**全站口径 115 HTML=PC 110+mobile 5**'
assert t3.count(A_115) == 1, '基线 115 锚 %d' % t3.count(A_115)
t3 = t3.replace(A_115, '**全站口径 116 HTML=PC 111+mobile 5（09-14 收货信息 +1）**')
# 追记块：插在 G30 追记行之后
marker = '- **追记（09-14 G30·D-93）**：'
lines = t3.split('\n')
hit = [i for i, l in enumerate(lines) if l.startswith(marker)]
assert len(hit) == 1, 'G30 追记行 %d' % len(hit)
assert '收货信息独立维护' not in t3
NEW = ('- **追记（09-14 会话·客商收货信息独立维护·D-94）**：客商管理列表操作列+「收货信息」按钮'
       '（详情/编辑/开票资料/收货信息四操作·参照开票资料先例 8dea641）——独立弹窗 recvInfoModal 维护'
       '收货人/收货电话/收货地址，与联系人/联系电话（商务联系）两套区分；partners ops×8（实体驱动按钮）'
       '+静态行×8+列表页弹窗+弹窗/客商收货信息.html 模板（双层·div 配平修正源模板缺 modal-body 闭合的'
       '坑未继承）·模板 69→70·116 HTML=PC 111+mobile 5；验证：PW 7 断言+listfull batch3 43 项全过'
       '+audit 客商域 5 页与 g17 基线逐键零新增（页存 1 问题=基线既有 detailModal 不可达·审计盲区口径）'
       '+截图×2；P2-R01 D-94+F-06 注记')
lines.insert(hit[0] + 1, NEW)
t3 = '\n'.join(lines)
io.open(P3, 'w', encoding='utf-8', newline='').write(t3)
t3b = io.open(P3, encoding='utf-8', newline='').read()
assert t3b.count('收货信息独立维护·D-94') == 1 and t3b.count('116 HTML=PC 111+mobile 5') >= 1
print('PASS 基线：原型 bullet 计数+追记块')
