# -*- coding: utf-8 -*-
"""G51 T10a: 任务书执行记录回写"""
import io

p = 'agent-handoff/20260917-G51-施工后文档落后修正.md'
t = io.open(p, encoding='utf-8', newline='').read()

old = '## 执行记录（收尾回写）\r\n\r\n（待执行）'
if t.count(old) != 1:
    old = '## 执行记录（收尾回写）\n\n（待执行）'
assert t.count(old) == 1, 'exec-record anchor fail: %d' % t.count(old)

new = old.replace('（待执行）', '''**✅ 2026-09-18 执行完毕（无人值守 goal·ZCode 主机 Win）**

- **T-1 前置批次**：`e27ed9e`（89 文件·+58461/−2691）——0917 交互施工全量清混树（原型 47 页＋_data/demo-data.js＋mat-search.js〔新〕＋A03 重注入＋A05 0917 两节＋P2-R01/A02/基线 0917 最小同步＋P3-R05＋P1-R01/P1-R08/拍板登记＋立项三件＋留档 28 件）；归属核对法=mtime 分窗＋逐文件 diff 抽查；**11 个清单外页面内容相符并入**（库存查询/付款登记/收款登记/租入入库列表/采购入库列表/开票登记/应收账单/用户权限/项目档案/转移出库列表/我的待办·库位详情 DEL 随批）；并行残留 22 项登记 g51_failures（mobile 七件/银行回单核销/xlsx/不合理清单双版/zip 8 件/截图 3 张）。
- **T0**：取证 16 项全落 g51_survey（预查全部复现：A02/A05/P1-R08 mat-search=0·基线/A02 件数落后·P1-R04 旧词 2·拍板 19·台账 D-153·132 页）；g51_failures 建。
- **T1**：P2-R01 **V1.8**——D-154/D-155/D-156 三行落 A.5 台账（19 条拍板按默认决策表 #1 分组归并）＋正文最小增量（SAL/PUR/LEA/WHS/BAS 五模块概述句各追加一句＋范围边界节加全局 mat-search 句·FP/UC/表格零触碰）。
- **T2**：A05 追加「G51 登记节 · 0917 交互批次归档」六条（mat-search 共享件/库位刷齐 **8 族 15 页**实算/BOM 定名/退租入库五字段/附件口径=不增 demo-data 字段/**43 实体 485 记录** node 实算）。
- **T3**：A02 **v6.8**——_data 件数**勘误为九件**（任务书「八件」系沿用 G43 漏更基数·git ls-tree 实算：G43 前 7→G43 后 8→0917 后 9）＋L16 断尾清单补全（G43 旧伤）＋mat-search 登记。
- **T4**：P1-R04 **V0.8**——新词 2 条（BOM物料编码/BOM物料名称）＋BOM/组合件词条改称沿革注记＋库位档案词条补单据字段语义。
- **T5**：P1-R08 第三节 _data 行登记 mat-search.js（九件口径）。
- **T6**：基线滚动——快照标题 G41→**G51 后**·原型现状 109→**132 HTML（PC127+mobile5·库位详情退场后口径）**·数据驱动 37→**43 实体 485 记录/_data 九件**·追加「0917 交互批次·G51 归档·D-154~156」追记行·上一任务行刷新 G51（前值 G43）。
- **T7**：A03 token 失配 **0**（88 pin 遍历·与预查一致）；**新发现**：5 个陈旧键指向已删弹窗页面＋BOM维护 pin3 note「次品仓」漏刷 ×1——均登记不修（零写入红线）。
- **T8**：A06 概念行文保留（T8 拍板）/P3-R04 已删页 0 引用/P1-R01 附录 10.2 在案/菜单 v6 未动——四项全过。
- **T9**：①node --check=0；②全量审计 **132 页 问题 0/死链 0/JS 错 0**（net::ERR_ 噪音亦 0）；③术语门三组**白名单外均 0**（全量 20/32/56·白名单口径扩展四类依据见 g51_survey）；④文档断言全过（P2-R01 三 D 号+V1.8·A02/P1-R08 mat-search·P1-R04 BOM物料编码·基线 九件〔实算改验·见口径出入〕+132）；⑤台账 153→156 连续无重（全表唯一重复 D-132=G41 在案历史撞号·无缺号）。
- **口径出入三处**（默认决策表 #3/#9 处置·详见 g51_survey「任务书口径出入」节）：_data 八件→实算九件；库位 9 族→实算 8 族 15 页；mat-search 37+ 处→实算 43 处。
- **失败清单**：无失败项（登记性条目=并行残留 22＋A03 陈旧 5＋note 残留 1＋P2-R02 落后 2＋截图 3）。
- **独立验收**：只读子 agent 复验验证门 1-5 全 PASS（g51_accept_verify.md·结论贴对话）。
- **收尾**：G51 本体提交（精确路径）＋哈希回填本任务书与索引 G51 行——不 push。''')

t = t.replace(old, new)
for trial in range(3):
    try:
        with io.open(p, 'w', encoding='utf-8', newline='') as f:
            f.write(t)
        break
    except OSError:
        if trial == 2: raise
chk = io.open(p, encoding='utf-8', newline='').read()
assert '执行完毕（无人值守 goal' in chk and '（待执行）' not in chk
print('T10a OK: exec record written')
