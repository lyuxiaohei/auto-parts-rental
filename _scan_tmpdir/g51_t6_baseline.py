# -*- coding: utf-8 -*-
"""G51 T6: 基线滚动——现状数字刷新（132/九件/D-156）＋0917 交互批次追记＋上一任务行刷新"""
import io

p = 'agent-handoff/_AGENT基线.md'
t = io.open(p, encoding='utf-8', newline='').read()
CRLF = '\r\n'

def sub1(old, new):
    global t
    n = t.count(old)
    assert n == 1, 'ANCHOR FAIL count=%d: %s' % (n, old[:60])
    t = t.replace(old, new)

# 1. 快照标题滚动
sub1('### 当前基线快照（滚动更新 · 2026-09-16 G41 后）',
     '### 当前基线快照（滚动更新 · 2026-09-18 G51 后）')

# 2. 原型现状数字刷新（历史注记原文保留）
sub1('- **原型**：109 页（38 业务页 + 独立弹窗模板 70 + F01·09-14 收货信息弹窗模板 +1）——',
     '- **原型**：**132 HTML**（PC 127＝功能页 121〔菜单内 37＋菜单外 84〕＋3 独立弹窗模板＋F01 导航图＋登录页＋A06 渲染页·＋mobile H5 5 页·**09-17 库位详情退场后口径**·菜单 v6 37 项）——（历史：109 页〔38 业务页＋独立弹窗模板 70＋F01〕）')

# 3. 数据驱动现状数字刷新
sub1('- **数据驱动**：`_data/demo-data.js` **37 实体**（',
     '- **数据驱动**：`_data/demo-data.js` **43 实体 485 记录**（G51 node 逐实体键实算 2026-09-18；`_data/` 共享件 **九件**——+select-source.js〔G43〕＋mat-search.js〔0917·D-155〕·G43 行「七件」计数漏更已由 A02 v6.8 勘误）；（历史：')

# 4. 追记两行（G43 追记行后）
anchor = '值域变化类登记）——不 push'
assert t.count(anchor) == 1, 'G43 tail anchor fail'
notes = anchor + CRLF + '''- **追记（09-17 交互批次·G51 归档·D-154~D-156）**：0917 交互施工约 25 项（拍板登记 19 条归并三 D 号·P2-R01 V1.8 台账落账）——**D-154 字段口径与值域收口**（库房值域=库区命名四区〔原料区 RA/成品区 RB/外购区 RW/次品区 RC〕·出入库单据库位字段刷齐 8 族 15 页·BOM物料编码/名称定名·退租入库新建五字段·表单缺口 3 页·起租日期控件修复·BOM 按钮口径·库位详情退场 HTML 133→132·返回列表去重 3 页）；**D-155 搜索下拉组件全站化**（共享件 `_data/mat-search.js`·全站 43 处〔物料明细 10 页＋名称列 4＋销售出库 1＋关联单据号 12＋主数据 15＋样板 1·实算口径〕·两种形态/原生 select 隐藏取值/选中派发 change/幂等重绑）；**D-156 附件上传与订单列表操作栏**（销售/采购订单新建「附件」卡＋列表「上传附件/打印」〔打印模板待开发〕·页面级演示组件不增 demo-data 字段）；文档同步=A02 v6.8（_data 九件勘误）＋A05 G51 登记节＋P1-R04 V0.8（BOM 新词+沿革）＋P1-R08＋P2-R01 正文五模块增量；**台账至 D-156**；T-1 前置批次提交 e27ed9e（0917 施工 89 文件清混树·并行会话残留 22 项登记 g51_failures〔mobile 七件/银行回单核销/xlsx/不合理清单双版/zip 8 件/截图 3 张〕）——不 push'''.replace('\n', CRLF)
t = t.replace(anchor, notes)

# 5. 上一任务行刷新（G27 旧值 → G51·前值 G43）
sub1('- **上一任务**：✅ **G27 需求真值源收敛（2026-09-14·ZCode 交互会话·主机 Win·commit 见索引）**——',
     '- **上一任务**：✅ **G51 施工后文档落后修正（2026-09-18·无人值守 goal·哈希见索引）**——09-16/17 两日批次归档（T-1 前置提交 e27ed9e＋D-154~156 台账落账＋五文档同步＋基线滚动）；前值 G43 ✅ c5028b9；更早：G27 需求真值源收敛（2026-09-14·ZCode 交互会话·主机 Win·commit 见索引）——')

for trial in range(3):
    try:
        with io.open(p, 'w', encoding='utf-8', newline='') as f:
            f.write(t)
        break
    except OSError:
        if trial == 2: raise
chk = io.open(p, encoding='utf-8', newline='').read()
for kw in ['2026-09-18 G51 后', '**132 HTML**', '43 实体 485 记录', '九件', '追记（09-17 交互批次·G51 归档·D-154~D-156）', '台账至 D-156', 'G51 施工后文档落后修正（2026-09-18']:
    assert kw in chk, 'VERIFY FAIL: ' + kw
assert chk.count('\r\n') >= chk.count('\n') - 0, 'CRLF regression'
print('T6 OK: baseline rolled to G51 (132/nine-files/D-156)')
