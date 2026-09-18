# -*- coding: utf-8 -*-
"""G51 T3: A02 v6.8 —— _data 计数实算勘误（九件）＋mat-search 登记＋L16 断尾补全"""
import io

p = 'P3-R01-包装租赁管理后台原型/P3-R01-A02-页面类型与入口对照表.md'
t = io.open(p, encoding='utf-8', newline='').read()

def sub1(old, new):
    global t
    n = t.count(old)
    assert n == 1, 'ANCHOR FAIL count=%d: %s' % (n, old[:60])
    t = t.replace(old, new)

# 1. 标题版本 v6.7 -> v6.8
sub1('# P3-R01-A02 页面类型与入口对照表（v6.7）', '# P3-R01-A02 页面类型与入口对照表（v6.8）')

# 2. 日期行追加 v6.8 增订（挂在 v6.7 增订之后）
sub1('BOM 列表行内「维护」→「编辑」＋删同跳重复「查看」·BOM维护页「暂存」→「保存」＋删头部「返回列表」——第五节行 7/8/9 与行 112 同步）',
     'BOM 列表行内「维护」→「编辑」＋删同跳重复「查看」·BOM维护页「暂存」→「保存」＋删头部「返回列表」——第五节行 7/8/9 与行 112 同步）｜ 2026-09-18 v6.8 增订（**G51 施工后文档落后修正·D-154~D-156**：`_data/` 共享件＋**mat-search.js** 表单搜索下拉〔全站约 43 处·D-155〕；计数勘误——原「七件」系 G43 增 select-source.js 时漏更，＋mat-search.js 后**实为九件**〔本版 git ls-tree 实算〕；§一行 16 断尾清单补全〔G43 旧伤〕）')

# 3. 范围行：七件 -> 九件（含勘误注记）
sub1('数据驱动页另挂 `_data/` 七件（G43 +select-source.js 下拉数据源化共享件·dictOpts/fillDict/fillEntity/fillPeriods）',
     '数据驱动页另挂 `_data/` 九件（G41 时七件→G43 +select-source.js 下拉数据源化共享件〔dictOpts/fillDict/fillEntity/fillPeriods·计数彼时漏更〕→0917 +mat-search.js 表单搜索下拉共享件〔D-155·约 43 处接线〕＝九件·git 实算）')

# 4. L16 断尾补全 + mat-search 一行
sub1('+ list-generic.js / detail-generic.js / receivable-bill-',
     "+ list-generic.js / detail-generic.js / receivable-bill-detail.js / payable-bill-detail.js / pc-auth.js / pc-msg.js / select-source.js（G43 下拉数据源化）/ **mat-search.js（0917 新增共享件·搜索下拉——两种形态：明细表格带框/表单头部 bare；原生 select 隐藏保留为取值载体·选中派发 change 触发既有联动·幂等重绑；全站约 43 处：物料明细 10 页＋名称列 4＋销售出库 1＋关联单据号 12＋主数据 15＋样板 1·D-155）**")

for trial in range(3):
    try:
        with io.open(p, 'w', encoding='utf-8', newline='') as f:
            f.write(t)
        break
    except OSError:
        if trial == 2: raise
chk = io.open(p, encoding='utf-8', newline='').read()
for kw in ['（v6.8）', '九件', 'mat-search.js（0917 新增共享件·搜索下拉', 'receivable-bill-detail.js / payable-bill-detail.js / pc-auth.js / pc-msg.js / select-source.js']:
    assert kw in chk, 'VERIFY FAIL: ' + kw
assert chk.count('\r\n') == chk.count('\n'), 'CRLF broken'
assert chk.count('九件') >= 2, '九件 should appear in both L5/L6'
print('T3 OK: A02 v6.8, _data 九件(勘误注记), mat-search row, L16 fixed')
