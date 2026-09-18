# -*- coding: utf-8 -*-
"""G51 T2: A05 追加登记节「G51 登记节 · 0917 交互批次归档」"""
import io

p = 'P3-R01-包装租赁管理后台原型/P3-R01-A05-字段字典.md'
t = io.open(p, encoding='utf-8', newline='').read()
CRLF = '\r\n'

anchor = '- 库位档案页内 pin 口径同步（D-102 沿革＋0917 收口注记）；库存查询库房筛选 append 值改「次品区 RC」。'
assert t.count(anchor) == 1, 'A05 tail anchor fail: %d' % t.count(anchor)
assert 'G51 登记节' not in t, 'A05 G51 section already present (idempotent guard)'

section = anchor + CRLF + CRLF + '''### G51 登记节 · 0917 交互批次归档（2026-09-17 · D-154~D-156 · 任务档=agent-handoff/20260917-G51-施工后文档落后修正.md）

- **共享件 `_data/mat-search.js`（D-155）**：表单搜索下拉组件——两种形态（明细表格带框／表单头部 bare 保箭头）；原生 select 隐藏保留为取值载体，选中派发 change 触发既有联动；输入过滤（编码/名称或单号/摘要双向匹配）；Esc 恢复／点外/滚动关闭；幂等重绑＋自动包装明细重建钩子。全站约 43 处（含样板页）：物料明细 10 页＋物料名称列 4＋销售出库新建 1＋关联单据号 12＋主数据 15＋样板 1（采购订单新建）。
- **出入库单据库位字段名刷齐（D-154）**：8 族 15 页——采购入库列表/录单、销售出库列表/新建、租赁出库录单、租入入库列表、退租入库列表/新建、其他入库列表/新建、其他出库列表/新建、库存调拨列表/新建/审核；旧用词页面域实测清零（grep 0）。单据明细库位列值显仓库名称（fees 26 处编码→区名·列头保「库位」·库位编码为独立字段）＋采购入库录单明细「批量设置库位」。
- **BOM 字段定名（D-154）**：bomList `_key`/`name` 已改 **BOM物料编码／BOM物料名称**（本表 159/160 行·改称沿革注记在行内）；BOM维护页编码字段输入框化。
- **退租入库新建字段补齐（D-154）**：客户/所属项目/入库库位/拆散方式/退回日期五字段＋明细「去向」列（P3-R05 表单缺口收口）。
- **附件上传列表（D-156）**：销售/采购订单新建「附件」卡＋两列表行级上传弹窗——页面级演示组件，**不新增 demo-data 实体字段**（真实文件选择器演示上传·按扩展名配图标·不做真传输·G13 口径）。
- **实体/记录数复核**：node 实读 `window.DEMO_DATA`＝**43 实体 485 记录**（2026-09-18 G51 复核·逐实体键计数：locations=10〔客户虚拟仓主数据行删除后〕·dictItems=150 项 28 组·todoItems=20·stockEvents=23）。'''
section = section.replace('\n', CRLF)

t = t.replace(anchor, section)
for trial in range(3):
    try:
        with io.open(p, 'w', encoding='utf-8', newline='') as f:
            f.write(t)
        break
    except OSError:
        if trial == 2: raise
chk = io.open(p, encoding='utf-8', newline='').read()
for kw in ['G51 登记节 · 0917 交互批次归档', 'mat-search.js`（D-155）', '8 族 15 页', '43 实体 485 记录', '不新增 demo-data 实体字段']:
    assert kw in chk, 'VERIFY FAIL: ' + kw
assert chk.count('\r\n') == chk.count('\n'), 'CRLF broken'
print('T2 OK: A05 G51 section appended')
