# -*- coding: utf-8 -*-
"""G30 T4.1：P2-R01 D-93 落行+F-08 数据字典注记+拍板登记 G30 条目标已归并。"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'

# ---------- P2-R01 ----------
P = ROOT + r'\P2-R01-产品需求文档.md'
t = io.open(P, encoding='utf-8', newline='').read()
crlf = t.count('\r\n'); lf_only = t.count('\n') - crlf
NL = '\r\n' if crlf > lf_only else '\n'
print('P2-R01 EOL: CRLF=%d LF=%d → %s' % (crlf, lf_only, repr(NL)))

# ① F-08 行：数据字典（49 项）→ 24 组 49→117
A_F8 = '角色管理（权限配置矩阵+可审单据矩阵+数据权限）、数据字典（49 项）、操作日志'
N_F8 = '角色管理（权限配置矩阵+可审单据矩阵+数据权限）、数据字典（24 组业务字典 49→117 项·G30 枚举字典化）、操作日志'
assert t.count(A_F8) == 1, 'F-08 锚点 %d（任务书误写 F-06·实际数据字典描述在 F-08）' % t.count(A_F8)
t = t.replace(A_F8, N_F8)

# ② D-93 落行（编号按届時 D 行数顺延=93；锚=D-92 行 + A.5 节头）
import re
m = re.search(r'^\| D-92 \|[^\r\n]*\|', t, re.M)
assert m, 'D-92 行未定位'
d92 = m.group(0)
a5 = '### A.5 维护规则'
assert t.count(a5) == 1
D93 = ('| D-93 | 枚举值字典化收敛（道远「写死枚举值收录数据字典管理」）：13 组 65 项收录 dictItems'
       '（库存状态 KC-01~05/入库类型 RKU-01~03[RK 前缀避采购入库单号撞加长 1 位]/出库类型 CKU-01~04/'
       '应收账单类型 ARB-01~06/应付账单类型 APB-01~05/费用分类 FY-01~07/发票类型 FP-01~02/客商类型 KST-01~03/'
       '数据权限范围 SJQ-01~03/盘点口径 PDK-01~02/周期单位 ZQ-01~03/物料分类 FL-01~06/'
       '待办单据类型 DJ-01~16=todoItems 实读序·审核矩阵同值源）；双源统一 3 处（计量单位+DW-07 托 6→7/'
       '支付方式 ZF-02 银行承兑→承兑+ZF-03 现金+ZF-04 票据 2→4/库位档案「平面库位·立体库位·待定选项」占位'
       '→KW 4 值）；主数据引用型 20 组不进字典（差集档 _scan_tmpdir/g30_接线差集.md·留后续「下拉随实体渲染」'
       '立项）；计费方式两层口径（表单分组 vs BF 5 项值源）注记零改动；dictItems 49→117 项 24 组 '
       '| 道远 09-14 对话拍板（全站 135 组枚举盘点 g29_enum_scan.json 结论·G30 执行） | ✅ |')
anchor = d92 + NL + a5
assert t.count(anchor) == 1, 'D-92→A.5 毗邻锚 %d' % t.count(anchor)
t = t.replace(anchor, d92 + NL + D93 + NL + a5)

# ③ 头部最后更新日校验（G27 规则：不落后于最近拍板——今日 09-14，无需变）
assert 'V1.1' in t[:400] and '2026-09-14' in t[:400], '头部版本/日期异常'
io.open(P, 'w', encoding='utf-8', newline='').write(t)

rows = re.findall(r'\| D-(\d+) \|', t)
nums = sorted(set(int(x) for x in rows))
assert nums == list(range(1, 94)), 'D 行连续性异常：max=%d n=%d' % (nums[-1], len(nums))
print('PASS P2-R01：F-08 注记+D-93 落行·台账 D-01~D-93 连续 %d 行' % len(nums))

# ---------- 拍板登记 ----------
P2 = ROOT + r'\agent-handoff\拍板登记.md'
t2 = io.open(P2, encoding='utf-8', newline='').read()
A_MK = '- **2026-09-14（道远对话拍板·待执行 G30）**：写死枚举值收敛数据字典管理'
N_MK = '- **2026-09-14（道远对话拍板·已归并 D-93·G30 已执行 2026-09-14）**：写死枚举值收敛数据字典管理'
assert t2.count(A_MK) == 1, '拍板登记 G30 条目锚 %d' % t2.count(A_MK)
t2 = t2.replace(A_MK, N_MK)
# 条目尾部补归并注记
A_TAIL = '归并：G30 收尾落台账行'
assert t2.count(A_TAIL) == 1
t2 = t2.replace(A_TAIL, '归并：✅ 已归并 P2-R01 附录 A D-93（2026-09-14 G30 执行·13 组 65 项+双源统一 3 处+差集档留档）')
io.open(P2, 'w', encoding='utf-8', newline='').write(t2)
print('PASS 拍板登记：G30 条目已标「已归并 D-93」+归并注记')
