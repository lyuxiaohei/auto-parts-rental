# -*- coding: utf-8 -*-
"""G12 T4：白名单 g12-whitelist.md 生成"""
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
cls = json.load(open(r'_scan_tmpdir/g12-classify.json', encoding='utf-8'))
lines = ['# G12 · B 类白名单（数据驱动豁免登记）', '',
         '> 生成：2026-09-10 ｜ 来源：_scan_tmpdir/g12-classify.json（T1 分类判定）',
         '> 规则：纯表单（新建/审核/确认/录单主体）或表格 ≤5 行演示性质 → 豁免数据驱动；**本体零改动**（git diff 交集必须为空）。', '',
         '## B 类业务页（%d 个）' % len(cls['B_pages']), '']
for it in cls['B_pages']:
    lines.append('- `%s` — %s' % (it['path'], it['reason']))
lines += ['', '## B 类弹窗（%d 个）' % len(cls['B_modals']), '',
          '统一理由：新建/审核/确认类表单弹窗，无数据表格或表格 ≤5 行（默认决策表第 4 条静态保留）。逐文件：', '']
for it in cls['B_modals']:
    lines.append('- `%s`' % it['path'])
lines += ['', '## 附注（A 类页内的局部静态块，非白名单文件）', '',
          '- `系统管理/数据字典.html` 第二卡片「计费方式」3 行（≤5 行，静态保留；主表已驱动）',
          '- `系统管理/用户权限.html` 第二表格「角色管理」9 行（ops 引用 openRolePerm 仅角色管理页定义，驱动会产生 JS 错；本体保持静态，roles 实体在角色管理页已驱动）',
          '- `首页/项目看板.html` `财务协同/盈亏报表.html` 统计卡片区（混合页：卡片静态+主表驱动）',
          '- `财务协同/盈亏报表.html` 按月趋势/按客户汇总页签（聚合视图切换，纯视觉演示；真聚合留 G13+）',
          '- `系统管理/用户权限.html`「状态」筛选下拉（选项语义与所属方重复的演示占位，未接线；其余 4 控件已接）',
          '- `财务协同/盈亏报表.html`「统计口径」筛选下拉（含税口径演示占位，未接线；账期/所属项目已接）',
          '']
open(r'agent-handoff/g12-whitelist.md', 'w', encoding='utf-8').write('\n'.join(lines))
print('g12-whitelist.md 写入：B 页 %d + B 弹窗 %d' % (len(cls['B_pages']), len(cls['B_modals'])))
