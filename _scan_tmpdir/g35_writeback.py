# -*- coding: utf-8 -*-
"""G35 回写三件：任务档执行记录 + _索引.md G35 行 + _AGENT基线.md 追记（哈希占位待回填）"""
import io

BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'

# ---------- 1. 任务档执行记录 ----------
p1 = BASE + r'\agent-handoff\20260915-G35-筛选区补充与真名脱敏.md'
t = io.open(p1, encoding='utf-8', newline='').read()
rec = '''
## 执行记录（2026-09-15 · 主机 Win · ZCode /goal 会话）

> **状态**：✅ 完成（A 组 P0×12＋P1×12 全部落地·P2×10 登记；B 组真名清零 0 残留）。commit：{{HASH}}

- **T1 勘察**：33/33 页（g35_t1_survey.py → g35_t1_raw.json）；关键发现=label 脱钩族 8 页（HTML 控件 label 与 cfg label 不一致→主体筛选真过滤失效）、用户权限状态未接线、采购订单/盈亏报表既有未接线 select 判不建议（无行级字段支撑）。
- **T2 分级**：_scan_tmpdir/g35_筛选区补充建议.md（409 行·五节+执行后记；FIX 声称 8 处程序化 assert 复核通过）。
- **T3 实施**：①8 页 cfg label 对齐（客户名称/供应商名称/客商名称）；②11 页新增筛选（HTML .ff + cfg entry + 值域动态渲染脚本·select id g35*）；③用户权限状态接线+options 动态化；④我的待办所属项目/提交人（自定义 filterTodo 扩展）；⑤demo-data +opLogs.result×10/+purchaseInbounds.maker·area×8（node --check 0）。**执行中并行会话 84b3212 同窗覆写库存查询/采购入库/demo-data→按 D-128/D-129 新版重适配（PI cells 索引 4/6）**；执行期两轮自愈返工（CRLF 锚点/幂等守卫）详见失败清单 F-01/F-02。
- **T4 脱敏**：36 映射词全替换（长词优先·精确字符串）；表外派生 16 组（一汽大众→北方商用/林芳→林岚等·见失败清单 F-03）；终扫 36 词+派生词+碎片词（一汽/上汽/东风/本田/小鹏/吉利/五菱/FAW）**全 0**；.prompts 会话存档路径串一并替换（非功能文本）。
- **T5 验证**：audit 全量 128 页 **死链 0／JS 0／diff 新增 0**（g35_audit_diff.py·基线键过脱敏归一映射；新基线 audit_results_g35baseline.json 落盘）；node --check 0；页面数 128 不变；PW 抽验 g35_pw_verify.py **A 落位 11/11（option≥2）·B 筛选可用 3/3（应付账单 18→10·操作日志 10→9·采购入库 8→5）·B2 label 修复页 16→11·C 待办联动 19→9→2·D 脱敏落位 PASS·pageerror 0**；A05 追加 G35 登记节（+opLogs.result/purchaseInbounds.maker·area）；BOM维护 addBomRow 占位符补丁（并行会话引入·复审归零）。
- **收尾**：失败清单 goal-failures-g35.md（6 条登记性记录·结论无失败项）；_索引.md G35 行 ✅ 挂哈希；_AGENT基线.md 追记。
- **默认决策执行注记**：①库存查询物料类型值域取实体 cls（租赁器具/零部件）而非 WL 字典 6 值（两套口径并存·值域与行数据同源优先防滤空）；②新增筛选 label 对齐各页 th（租入/采购入库用「入库库区」）；③插入位置=人员/库房类挂筛选区末位（filter-actions 前）、主体/类型类插在既有类型/日期项前；④我的待办顺序=单据类型·审核人·所属项目·提交人·关键词（工作台页类型优先）。
'''
assert '{{' not in t
io.open(p1, 'w', encoding='utf-8', newline='').write(t.rstrip('\n') + '\n' + rec.replace('{{HASH}}', '（待回填）'))
print('任务档执行记录 appended')

# ---------- 2. _索引.md G35 行 ----------
p2 = BASE + r'\agent-handoff\_索引.md'
t2 = io.open(p2, encoding='utf-8', newline='').read()
lines = t2.split('\n')
hit = 0
for i, l in enumerate(lines):
    if l.startswith('| G35 |'):
        assert '| ⏳ |' in l, 'G35 行状态异常: ' + l[:80]
        lines[i] = l.replace('| ⏳ | （待执行） |', '| ✅ | {{HASH}} |')
        hit += 1
assert hit == 1, hit
io.open(p2, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
print('索引 G35 行 -> ✅（哈希待回填）')

# ---------- 3. _AGENT基线.md 追记 ----------
p3 = BASE + r'\agent-handoff\_AGENT基线.md'
t3 = io.open(p3, encoding='utf-8', newline='').read()
anchor = '- **追记（09-15 G34·D-127）**'
i = t3.find(anchor)
assert i > -1
# 找 G34 追记行的行尾
j = t3.find('\n- **上一任务**', i)
if j < 0:
    j = t3.find('\n## 二、', i)
add = '''- **追记（09-15 G35）**：列表筛选区补充＋真名脱敏——A 组 33 页勘察（判据八条·_scan_tmpdir/g35_筛选区补充建议.md 409 行）→ **P0×12＋P1×12 全落地**（8 页 cfg label 脱钩修复〔客户名称/供应商名称/客商名称〕＋11 页新筛选 select 值域动态取实体〔select id g35*·fill 脚本挂 renderListPage 块后〕＋用户权限状态接线+options 动态化＋我的待办+项目/提交人）＋P2×10 金额区间只登记；demo-data +opLogs.result×10·purchaseInbounds.maker/area×8；B 组 **36 映射词＋表外派生 16 组全量替换·残留全 0**（一汽大众→北方商用/东风锂电→长丰锂电/小鹏→星途/林芳→林岚/FAW-BX→HJ-BX/吉客云→捷科云/拼音账号派生/.prompts 路径串·详见 goal-failures-g35.md F-03）；**同窗并行会话 84b3212（D-128/D-129）覆写库存查询/采购入库/demo-data→按新版重适配（PI cells 索引 4/6·BOM维护 addBomRow 占位符顺手补）**；验证=audit 128 页 0/0/0（diff 键过脱敏归一·g35baseline 落盘）+node 0+PW 全绿（落位 11/11·筛选可用 3+1 页行数变化·待办联动）+真名终扫全 0；A05 +G35 登记节；失败清单 6 条登记·结论无失败项——不 push'''
io.open(p3, 'w', encoding='utf-8', newline='').write(t3[:j] + '\n' + add + t3[j:])
print('基线追记 appended')
