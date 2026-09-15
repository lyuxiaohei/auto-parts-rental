# -*- coding: utf-8 -*-
"""G35 T2：分级落盘勘察清单 _scan_tmpdir/g35_筛选区补充建议.md
数据源：g35_t1_raw.json（T1 勘察产物）＋ 本脚本内编码的逐页判定（判据八条）
分级口径（任务书第七节）：P0 必备（状态/主体/单号）/ P1 常用（类型/日期/库房/人员）/ P2 可选（金额·只登记）
"""
import io, json, os

RAW = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\g35_t1_raw.json'
OUT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\g35_筛选区补充建议.md'
PROTO = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

raw = json.load(io.open(RAW, encoding='utf-8'))

# 逐页判定：(页名, 建议列表[(动作, 项, 优先级, 理由)], 页级备注)
# 动作: ADD=新增筛选 / FIX=修复既有失效 / WIRE=接线cfg / DATA=补fields / P2REG=登记
A = [
 ('其他入库列表', [('NONE', '无需补充', '-', '判据1/2/3/4/6/7 全覆盖：单据编号/入库类型/物料名称/状态/入库日期(range)/入库库房 六项齐备且 cfg 一一接线；无人员/金额列')], ''),
 ('其他出库列表', [('NONE', '无需补充', '-', '判据1/2/3/4/6/7 全覆盖：单据编号/出库类型/物料名称/状态/出库日期(range)/出库库房 六项齐备且接线；无人员/金额列')], ''),
 ('库存查询', [('ADD', '物料类型（select·值域=dictItems WL 6 值）', 'P1', '判据2：表格有「物料类型」列（th 第3列），筛选区无类型筛选；stockFlows 行带 fields.cls')], ''),
 ('库存调拨列表', [('NONE', '无需补充', '-', '判据1/3/4/6/7 全覆盖：调拨单号/物料名称/调出库房/调入库房/调拨日期(range)/状态 六项齐备；无类型/人员/金额列')], ''),
 ('盘点列表', [('P2REG', '盈亏合计金额区间', 'P2', '判据8：表格有「盈亏合计」金额列——按任务书 P2 只登记不补')], '盘点单号/范围/口径/状态/日期/盘点人 六项齐备'),
 ('BOM', [('ADD', '更新人（select·值域=bomList fields.updater 去重）', 'P1', '判据5：表格有「更新人」列，筛选区无人员筛选')], ''),
 ('产品档案', [('NONE', '无需补充', '-', '判据1/2/6 全覆盖：物料编码/物料名称/物料类型(select)/状态/建档时间(range) 五项齐备；四参考价列属档案属性非单据金额（见不建议项）')], ''),
 ('客商管理', [('FIX', 'cfg label「客商」→「客商名称」（与 HTML 控件 label 对齐）', 'P0', '判据3 主体：HTML 控件 label=客商名称、cfg label=客商，readFilters 按 label 全等匹配→主体筛选真过滤失效（控制台报「筛控件未找到」）')], ''),
 ('库位档案', [('NONE', '无需补充', '-', '判据1/2/7 全覆盖：仓库/库位编码/库位类型(select)/状态 四项齐备（G34 已字典化 KW）；无日期/人员列')], ''),
 ('租入入库列表', [('ADD', '制单人（select·值域=rentInbounds fields.maker 去重）', 'P1', '判据5：表格有「制单人」列（李国栋/陈金），筛选区无人员筛选'),
                  ('ADD', '入库库房（select·值域=rentInbounds fields.area 去重）', 'P1', '判据7：表格有「入库库区」列，筛选区无库房筛选')], ''),
 ('租入单列表', [('P2REG', '租金/押金/累计租金应付 金额区间', 'P2', '判据8：表格有三个金额列——P2 只登记不补')], '租入单号/供应商/物料/状态/租期开始(range)/经办人 六项齐备'),
 ('租入归还列表', [('ADD', '制单人（select·值域=rentInReturns fields.maker 去重）', 'P1', '判据5：表格有「制单人」列，筛选区无人员筛选')], ''),
 ('租赁出库列表', [('NONE', '无需补充', '-', '判据1/3/4/6 全覆盖：出库单号/所属项目/客户/出库状态/出库时间(range)/组合件编码 六项齐备；无类型/库房列（出库走组合件）')], ''),
 ('租赁单列表', [('FIX', 'cfg label「客户」→「客户名称」', 'P0', '判据3 主体：HTML label=客户名称、cfg label=客户→客户筛选真过滤失效')], '其余判据全覆盖（状态/项目/日期/单号）'),
 ('退租入库列表', [('FIX', 'cfg label「客户」→「客户名称」', 'P0', '判据3 主体：label 不匹配→客户筛选失效'),
                  ('ADD', '入库库房（select·值域=returnInbounds fields.warehouse 去重）', 'P1', '判据7：表格有「入库库房」列，筛选区无库房筛选')], ''),
 ('操作日志', [('ADD', '操作结果（select·值域=opLogs cells 第7列值域 成功/失败）＋DATA 补 fields.result×10 行', 'P0', '判据1 状态类：表格有「操作结果」列（成功/失败），属日志常见状态维度；行数据缺 fields.result 需随筛选补齐（值取自本行 cells，不改口径）')], ''),
 ('用户权限', [('WIRE', 'cfg filters 补 {label:\'状态\', field:\'status\'}（HTML 已有 状态 select）', 'P0', '判据1 状态：HTML 状态筛选控件存在但 cfg 未配置→点查询不生效')], ''),
 ('角色管理', [('NONE', '无需补充', '-', '表列仅 角色/备注/数据权限/账号数：现有 角色名称(input)+数据权限(select) 两项已覆盖可筛维度；备注/账号数非筛选维度（判据八条无对应列）')], '仅 2 项但表无可筛余量'),
 ('付款登记', [('FIX', 'cfg label「供应商」→「供应商名称」', 'P0', '判据3 主体：label 不匹配→供应商筛选失效'),
              ('P2REG', '付款金额区间', 'P2', '判据8：表格有「付款金额(元)」列——P2 只登记')], ''),
 ('回款登记', [('P2REG', '收款金额区间', 'P2', '判据8：表格有「收款金额(元)」列——P2 只登记')], '收款编号/客户/收款日期(range)/核销状态/银行账户 五项齐备且接线'),
 ('应付账单', [('FIX', 'cfg label「供应商」→「供应商名称」', 'P0', '判据3 主体：label 不匹配→供应商筛选失效'),
             ('ADD', '所属项目（select·值域=projects 实体）', 'P0', '判据3 主体：表格有「所属项目」列（th 第4列），筛选区无项目筛选；payableBills 行带 fields.project'),
             ('ADD', '账期（select·值域=payableBills fields.period 去重·ZQ 字典对齐）', 'P1', '判据2 分类变体：表格有「账期」列且同域应收账单已有账期筛选——跨页一致性')], '补后 8 项'),
 ('应收账单', [('P2REG', '账单金额区间', 'P2', '判据8——P2 只登记')], '账单编号/客户/所属项目/账单类型/账单状态/账期/生成日期 七项齐备且接线（已达查漏线：状态/主体/日期三项齐）'),
 ('开票登记', [('P2REG', '开票金额区间', 'P2', '判据8：表格有「开票金额(元)」列——P2 只登记')], '发票登记号/发票号码/购方名称/发票类型/开票日期(range)/开票状态 六项齐备'),
 ('盈亏报表', [('NONE', '无需补充', '-', '账期/所属项目(cfg field=code·行键即项目编码) 已接线可用；金额列全为数值列→判据8 全部 P2 登记（见不建议项·报表金额列不入筛选）；「统计口径」不建议接线（见不建议项）')], '仅 3 项但属报表页'),
 ('退款登记', [('P2REG', '退款金额区间', 'P2', '判据8——P2 只登记')], '退款编号/退款类型/关联退货单号/往来单位/状态/退款日期 六项齐备且接线'),
 ('采购入库列表', [('ADD', '制单人（select·值域=purchaseInbounds cells 制单人列）＋DATA 补 fields.maker×8 行', 'P1', '判据5：表格有「制单人」列，筛选区无人员筛选；行数据缺 fields.maker 需补（值取自本行 cells）'),
                 ('ADD', '入库库房（select·值域=cells 入库库区列）＋DATA 补 fields.area×8 行', 'P1', '判据7：表格有「入库库区」列，筛选区无库房筛选；行数据缺 fields.area 需补')], ''),
 ('采购订单列表', [('NONE', '无需补充', '-', '判据1/2/3/4/6 全覆盖（订单状态/物料类型/供应商/下单日期(range)/采购订单号）；HTML 既有「所属项目」select 无表列支撑且行数据无 project 字段——不建议接线（见不建议项）')], ''),
 ('采购退货单列表', [('P2REG', '金额区间', 'P2', '判据8：表格有「金额(元)」列——P2 只登记')], '退货单号/供应商/退货类型/关联原单号/退货状态/退货日期 六项齐备且接线'),
 ('销售出库列表', [('FIX', 'cfg label「客户」→「客户名称」', 'P0', '判据3 主体：label 不匹配→客户筛选失效'),
                 ('ADD', '出库库房（select·值域=salesOutbounds fields.warehouse 去重）', 'P1', '判据7：表格有「出库库房」列，筛选区无库房筛选')], ''),
 ('销售订单列表', [('FIX', 'cfg label「客户」→「客户名称」', 'P0', '判据3 主体：label 不匹配→客户筛选失效'),
                 ('ADD', '下单人（select·值域=salesOrders fields.agent 去重）', 'P1', '判据5：表格有「下单人」列（D-19 拍板唯一来源=项目经理代下），筛选区无人员筛选'),
                 ('P2REG', '金额区间', 'P2', '判据8：表格有「金额(元)」列——P2 只登记')], ''),
 ('销售退货单列表', [('P2REG', '金额区间', 'P2', '判据8——P2 只登记')], '退货单号/客户名称/退货类型/关联出库单号/退货状态/退货日期 六项齐备且接线（该页 label 本就一致）'),
 ('项目档案', [('FIX', 'cfg label「客户」→「客户名称」', 'P0', '判据3 主体：label 不匹配→客户筛选失效')], '七项已达查漏线（默认决策表：≥7 项只核对状态/主体/日期——三项均已齐，仅修 P0）'),
 ('我的待办', [('ADD', '所属项目（select·值域=todoItems fields.project 去重·自定义 filterTodo 页加 data-project 属性）', 'P0', '判据3 主体：表格有「所属项目」列，筛选区无项目筛选；单号检索已由「关键词」input 覆盖（innerText 含单号）'),
             ('ADD', '提交人（select·值域=fields.submitter 去重·data-submitter 属性）', 'P1', '判据5 人员：表格有「提交人」列，筛选区无人员筛选')], '静态自定义页（filterTodo），非 renderListPage'),
]

NOT_RECOMMEND = [
 ('采购订单列表·所属项目 select 接线', '表格无「所属项目」列、purchaseOrders 行数据无 project 字段（采购为全局行为不挂项目）——接线需造行级数据，属改业务口径风险，不接线（HTML 控件保留现状）'),
 ('盈亏报表·统计口径 select 接线', '统计口径属报表层维度（切换口径=换数据版本），profitRows 行级无口径字段，接线会把整表滤空——不接线（控件保留现状）'),
 ('产品档案·四参考价区间', '参考价为档案属性非交易单据金额（判据8 门槛建立在单据金额上），数值区间筛选用例少——不入 P2 清单'),
 ('各页·银行账户/币种/IP地址/关联单号类追加', '非判据八条维度：银行账户已有页面（回款登记）保留现状不推广；币种单一（人民币）无筛选价值；IP 属日志明细非筛选项；关联单号检索已由单号 input 或关键词覆盖'),
 ('角色管理·补项', '表列无可筛余量（见逐页行），强加筛选=为凑数而加'),
 ('页签(stabs)与筛选区的关系', '状态页签已承担状态快捷筛选（点击切换视觉态），与筛选区状态 select 并存为既有设计——本任务不动页签'),
]

def ff_summary(e):
    return '；'.join('%s(%s%s)' % (f['label'], f['type'], '·extra' if f['extra'] else '') for f in e['filters']) or '（无）'

def main():
    # 验证：33 页判定行数
    assert len(A) == 33, '判定行数 != 33: %d' % len(A)
    # 验证 label 脱钩声称（FIX 项）在页面中两侧 label 确实不一致
    checked = 0
    for name, items, _note in A:
        for act, item, pri, reason in items:
            if act == 'FIX':
                e = raw[name]
                html_labels = [f['label'] for f in e['filters']]
                cfg_labels = e['cfg']['cfgFilters'] if e['cfg'] else []
                # 从 item 提取 from→to
                import re
                m = re.search(r'「(.+?)」→「(.+?)」', item)
                frm, to = m.group(1), m.group(2)
                assert to in html_labels, '%s: HTML 无 label %s' % (name, to)
                assert frm in cfg_labels, '%s: cfg 无 label %s' % (name, frm)
                checked += 1
    # 生成文档
    L = []
    L.append('# G35 列表筛选区补充建议（勘察清单）')
    L.append('')
    L.append('> 生成：2026-09-15 G35 T2（勘察脚本 g35_t1_survey.py ＋ 分级脚本 g35_t2_grade.py）')
    L.append('> 范围：33 个标准列表页（任务书第二节）；判据八条（任务书第三节）；分级口径=任务书第七节默认决策表')
    L.append('> FIX 项已程序化复核：HTML label 与 cfg label 确实不一致（assert 通过 %d 处）' % checked)
    L.append('')
    # 统计
    p0 = sum(1 for _, items, _ in A for act, item, pri, _ in items if pri == 'P0' and act != 'P2REG' and act != 'NONE')
    p1 = sum(1 for _, items, _ in A for act, item, pri, _ in items if pri == 'P1' and act != 'P2REG' and act != 'NONE')
    p2 = sum(1 for _, items, _ in A for act, item, pri, _ in items if act == 'P2REG')
    L.append('## 一、概览')
    L.append('')
    L.append('- 勘察页数：33/33（每页有结论行）')
    L.append('- 实施项：**P0 %d 项 / P1 %d 项**（T3 落地）' % (p0, p1))
    L.append('- 登记项：P2 %d 项（只登记不补）' % p2)
    L.append('- 无需补充页：见明细（「无需补充」也含理由）')
    L.append('')
    L.append('| # | 页面 | 现有筛选数 | 结论 |')
    L.append('|---|---|---|---|')
    for i, (name, items, _note) in enumerate(A, 1):
        e = raw[name]
        parts = []
        for act, item, pri, _r in items:
            if act == 'NONE':
                parts.append('无需补充')
            elif act == 'P2REG':
                parts.append('P2 登记：%s' % item)
            else:
                tag = {'ADD': '补', 'FIX': '修', 'WIRE': '接线', 'DATA': '数据'}[act]
                parts.append('%s[%s] %s' % (pri, tag, item.split('（')[0].split('＋')[0]))
        L.append('| %d | %s | %d | %s |' % (i, name, len(e['filters']), '；'.join(parts) if parts else '-'))
    L.append('')
    L.append('## 二、逐页明细表')
    L.append('')
    for name, items, note in A:
        e = raw[name]
        L.append('### %s（%s）' % (name, e['path']))
        L.append('')
        L.append('- **页面类型**：%s（entity=%s）%s' % ('数据驱动 renderListPage' if e['cfg'] else '静态自定义（filterTodo）', (e['cfg'] or {}).get('entity') or '-', '；状态页签 %d 个' % len(e['stabs']) if e['stabs'] else ''))
        L.append('- **现有筛选（HTML）**：%s' % ff_summary(e))
        cfgl = '；'.join(e['cfg']['cfgFilters']) if e['cfg'] else '（无 renderListPage cfg）'
        L.append('- **cfg filters**：%s' % cfgl)
        L.append('- **表格列（th）**：%s' % ' / '.join(e['ths']))
        if note:
            L.append('- **页级备注**：%s' % note)
        L.append('- **判定**：')
        for act, item, pri, reason in items:
            L.append('  - [%s·%s] %s —— 理由：%s' % (pri if act != 'NONE' else '结论', {'ADD':'新增','FIX':'修复','WIRE':'接线','DATA':'补数据','P2REG':'登记','NONE':'-'}[act], item, reason))
        L.append('')
    L.append('## 三、共性问题')
    L.append('')
    L.append('1. **label 脱钩族（8 页·P0）**：HTML 控件 label 与 renderListPage cfg label 不一致（客商名称≠客商、客户名称≠客户、供应商名称≠供应商），readFilters 按 label 全等匹配→这些主体筛选控件点「查询」不生效（控制台 warn 筛控件未找到）。涉及：客商管理/租赁单列表/退租入库列表/付款登记/应付账单/销售出库列表/销售订单列表/项目档案。修复=cfg label 对齐 HTML（改脚本侧一处字符串，不动控件）。')
    L.append('2. **cfg 漏配族（1 页·P0）**：用户权限 HTML 有「状态」select 但 cfg filters 未列该项。')
    L.append('3. **行数据缺 fields 族（2 实体）**：操作日志缺 fields.result（操作结果）、采购入库缺 fields.maker/fields.area——新增对应筛选须同步补 fields（值取自本行 cells，不改口径）。')
    L.append('4. **主体/库房/人员覆盖缺口**：应付账单缺所属项目（判据3）；退租入库/销售出库缺库房（判据7）；BOM/租入入库/租入归还/采购入库/销售订单/我的待办缺人员（判据5）；库存查询缺物料类型（判据2）。')
    L.append('5. **静态 option 未动态化（既有·不在本任务范围）**：各页既有 select 的 option 多为静态写死（如客户名单）——本任务只要求**新增项**值域动态取（任务书第七节），既有项不动（真名由 B 组统一替换）。')
    L.append('')
    L.append('## 四、不建议补充项（登记·不实施）')
    L.append('')
    for t, r in NOT_RECOMMEND:
        L.append('- **%s**：%s' % (t, r))
    L.append('')
    L.append('## 五、P2 登记汇总（判据8 金额区间·只登记不补）')
    L.append('')
    for name, items, _ in A:
        for act, item, pri, _r in items:
            if act == 'P2REG':
                L.append('- %s：%s' % (name, item))
    L.append('')
    txt = '\n'.join(L)
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(txt)
    print('written:', OUT)
    print('lines:', txt.count('\n') + 1)
    print('P0 items:', p0, '| P1 items:', p1, '| P2 reg:', p2, '| FIX verified:', checked)
    # 小节行数
    for sec in ['## 一、概览', '## 二、逐页明细表', '## 三、共性问题', '## 四、不建议补充项', '## 五、P2 登记汇总']:
        i = txt.find(sec)
        j = txt.find('\n## ', i + 1)
        print(sec, '-> lines:', txt[i:j].count('\n') if j > 0 else txt[i:].count('\n'))

if __name__ == '__main__':
    main()
