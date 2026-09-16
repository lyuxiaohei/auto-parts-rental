# -*- coding: utf-8 -*-
"""_AGENT基线.md 追记转移出库加审条目（插在 G41 追记行之后）+ 拍板登记销账"""
import io, os

H = u'D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/agent-handoff'
base = os.path.join(H, u'_AGENT基线.md')
reg = os.path.join(H, u'拍板登记.md')

NEW = u'- **追记（09-16 会话·转移出库加审·D-151）**：道远对闭环核查报告三.1 拍板「转移出库需要加上审核」＋三.2「加一下入口」——**①新页** `租赁管理/转移出库审核.html`（克隆租入归还审核样板·侧边栏换租赁管理组·transferOutbounds ?id= 渲染·通过/驳回＋提交条·**HTML 132→133**）；**②三方矩阵 19→20 类**：todoItems +`ZY-20260915-005` 待审核行（审核人赵磊·link 审核页?id=）＋权限配置可审矩阵 +转移出库（租赁出库后）＋dictItems +DJ-20＋数据字典页静态 cnt 19→20；**③状态流改审核驱动**：待转移→**待审核**→（审核通过）已转移·驳回退回·终止转移保留——transferOutbounds ZY-005 行 status/ops/info/chain/timeline 全改·已转移/已终止 4 行 timeline「确认转移」→「审核通过 · 转移生效」·列表 zyConfirm 函数撤除＋静态行/筛选项/页签 同步·详情页待审核单头部条件显「审核」钮（zyAuditBtn·已转移态不显）；**④库存查询客户在租弹窗五行补「转移出库」行内入口**（?mat=&cust= 带参·弹窗导语注记成真·转租行不加）＋**ZY-20260914-002 行补 note:1 修复列表页运行时标注角标 0**（list-generic 按 r.note 重挂 data-note·G37 遗留缺口）；**⑤口径同步**：F01 S7 三处（节点副标「行内审核/终止转移」·状态流行·Mermaid「待审核→已转移→已终止」）＋A03 列表 pin 文案＋A04 我的待办 16 类→20 类（顺带修 ?audit=1 过时表述）＋A02 v6.5（133 页口径·功能页 122）＋A05 status 枚举＋P2-R01 V1.6+D-151；**验证**：node --check 0＋**定向审计 12 页（7 改动页+4 数据消费抽样+F01）problems/死链/JS 全 0**＋截图 7 张（zy_shots/：列表待审核行·审核页·待办 20 单·弹窗入口·矩阵 20 项·详情两态按钮显隐）＋运行时标注 1；全量 audit 中途砍单（道远「搞快点」·改动面定向覆盖）·脚本 zy_audit_targeted.py 留档；拍板登记同日销账——不 push'

s = io.open(base, encoding='utf-8').read()
anchor = u'- **追记（09-16 G41·D-150）**'
i = s.index(anchor)
j = s.index(u'\n', i) + 1
s2 = s[:j] + NEW + u'\n' + s[j:]
assert s2.count(NEW) == 1 and u'G41·D-150' in s2
io.open(base + u'.tmp', 'w', encoding='utf-8', newline='').write(s2)
os.replace(base + u'.tmp', base)
print('基线追记 OK（G41 行后插入）')

# ---- 拍板登记销账 ----
r = io.open(reg, encoding='utf-8').read()
old = u'归并建议：P2-R01 附录 A 立行＋转移出库流程正文同步；执行载体待道远定（本会话直接改或立 G 任务）。'
new = u'✅ **已执行（2026-09-16 本会话直接改·道远选「现在就改」＋「审核页参考现有样板」＋「入口直接加上」）**：五项全落地（详见 _AGENT基线 09-16 会话追记）·定向审计 12 页 0/0/0＋截图 7 张；P2-R01 附录 A **D-151** 立行＋头部 V1.6；A02 v6.5（133 页口径）。'
assert r.count(old) == 1
r2 = r.replace(old, new)
io.open(reg + u'.tmp', 'w', encoding='utf-8', newline='').write(r2)
os.replace(reg + u'.tmp', reg)
print('拍板登记销账 OK')
