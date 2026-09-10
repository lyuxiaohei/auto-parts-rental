# -*- coding: utf-8 -*-
"""G10-B5: 台账对齐 demo-data/A02/P3-R04/P1-R01⑱"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def patch(path, pairs):
    s = open(path, encoding='utf-8').read()
    for old, new in pairs:
        n = s.count(old)
        assert n == 1, f'{path}: 期望 1 处，实际 {n} 处: {old[:60]}'
        s = s.replace(old, new)
    open(path, 'w', encoding='utf-8', newline='').write(s)
    print('OK', path, f'({len(pairs)} edits)')

# 1) demo-data.js：角色管理行菜单入口语境（desc+cells 两处同串）
p = r'P3-R01-包装租赁管理后台原型/_data/demo-data.js'
s = open(p, encoding='utf-8').read()
n = s.count('财务应收/应付/项目损益')
assert n == 2, f'demo-data 期望 2 处，实际 {n}'
open(p, 'w', encoding='utf-8', newline='').write(s.replace('财务应收/应付/项目损益', '财务应收/应付/财务看板'))
print('OK demo-data 2 处入口语境')

# 2) A02
A02 = r'P3-R01-包装租赁管理后台原型/P3-R01-A02-页面类型与入口对照表.md'
s = open(A02, encoding='utf-8').read()
edits = []
# 2a 版本号
old = '## 二、菜单树（v3.4 · 九组序 · 38 页侧边栏统一）'
assert s.count(old) == 1
s = s.replace(old, '## 二、菜单树（v3.5 · 九组序 · 38 页侧边栏统一）')
# 2b 财务管理组行：财务看板置首、去组尾项
old = '| 8 | 财务管理（目录仍 `财务协同/`） | 应收 ｜ 应付（2 标签） | 应收账单 → `财务协同/应收账单.html`；开票登记 → `财务协同/开票登记.html`；收款登记 → `财务协同/回款登记.html`；收款核销 → `财务协同/银行水单核销.html`；应付账单 → `财务协同/应付账单.html`；付款登记 → `财务协同/付款登记.html`；**项目损益（组尾普通项，v3.2 损益归财务）** → `财务协同/盈亏报表.html` |'
assert s.count(old) == 1, 'A02 组行形态不符'
new = '| 8 | 财务管理（目录仍 `财务协同/`） | 应收 ｜ 应付（2 标签） | **财务看板（组首普通项·v3.5 移位改名，原「项目损益」）** → `财务协同/盈亏报表.html`；应收账单 → `财务协同/应收账单.html`；开票登记 → `财务协同/开票登记.html`；收款登记 → `财务协同/回款登记.html`；收款核销 → `财务协同/银行水单核销.html`；应付账单 → `财务协同/应付账单.html`；付款登记 → `财务协同/付款登记.html` |'
s = s.replace(old, new)
# 2c 盈亏报表行菜单格
old = '菜单「财务管理 → 项目损益」（v3.2 归财务管理组尾）'
assert s.count(old) == 1
s = s.replace(old, '菜单「财务管理 → 财务看板」（v3.5 组首·页面名仍「项目损益」）')
# 2d 注记行 菜单项合计
old = '菜单项合计 33 个（含我的待办一级项与项目损益）'
assert s.count(old) == 1
s = s.replace(old, '菜单项合计 33 个（含我的待办一级项与财务看板）')
# 2e 注记⑨ 追加在注记⑧之后
old = '8. **退租入库移入租赁小标签（2026-09-10 G09·道远拍板）**：菜单 v3.4——退租入库自「退租」小标签移入「租赁」小标签（租赁出库之下），退租小标签取消（租赁管理组 3→2 标签：租赁 3 项/租入 3 项）；38 页侧边栏统一调整，本表行数与入口零变更（108 HTML 不变）'
assert s.count(old) == 1
new = old + '\n9. **财务看板移位置首改名（2026-09-10 G10·道远拍板）**：菜单 v3.5——「项目损益」自财务管理组尾移至组首（应收小标签之前·无小标签）并改名「财务看板」（href/文件/页面名零改动，页面标题仍「项目损益」）；38 页侧边栏统一调整，v32_menu_verify 断言④⑤⑤b⑥/banner v3.5 更新（菜单门 14/14）；本表行数与入口零变更（108 HTML 不变）'
s = s.replace(old, new)
open(A02, 'w', encoding='utf-8', newline='').write(s)
print('OK A02 5 edits')

# 3) P3-R04 菜单入口语境
patch(r'P3-R04-演示场景覆盖梳理.md', [
    ('5. **项目损益**：财务管理组尾「项目损益」→ 盈亏报表.html（v3.2 损益归财务管理组，项目管理组仅 看板/列表 两项）',
     '5. **财务看板**：财务管理组首「财务看板」→ 盈亏报表.html（v3.5 移位改名·原菜单名「项目损益」；v3.2 损益归财务管理组，项目管理组仅 看板/列表 两项）'),
])

# 4) P1-R01 变更记录⑱
P1 = r'P1-R01-需求梳理与功能框架.md'
s = open(P1, encoding='utf-8').read()
anchor = '；38 页侧边栏统一调整+v32_menu_verify 断言⑧更新（菜单门 14/14）；页面/文件零移动。'
assert s.count(anchor) == 1, 'P1-R01 ⑰ 锚不符'
s = s.replace(anchor, anchor + '\n⑱ 2026-09-10：**菜单 v3.5·财务看板移位置首改名（G10·道远拍板）**——「项目损益」自财务管理组尾移至组首（应收小标签之前·无小标签）并改名「财务看板」（→财务协同/盈亏报表.html，href/文件/页面名零改动，页面标题仍「项目损益」）；38 页侧边栏统一调整+v32_menu_verify 断言④⑤⑤b⑥/banner v3.5（菜单门 14/14）；F01 S2 支线节点标签同步改名（副标/href 不动）；demo-data 角色管理行入口语境同步。')
open(P1, 'w', encoding='utf-8', newline='').write(s)
print('OK P1-R01 ⑱')
print('==== G10-B5 台账对齐 全部通过 ====')
