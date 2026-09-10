# -*- coding: utf-8 -*-
"""G12 T5 回写 3/3：_AGENT基线.md 快照滚动"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = r'agent-handoff\_AGENT基线.md'
lines = open(p, encoding='utf-8').read().split('\n')

NEW_DD = ('- **数据驱动**：`_data/demo-data.js` **37 实体**（G12 漏网收口 2026-09-10：28 存量复核+新增 9——opLogs/users/dictItems/todoItems/projects/projectDocs/boardRows/profitRows/bomList；'
          'A 类 9 页接线=renderListPage 7[操作日志 noOps/用户权限 stabField=side/项目档案/项目详情 stabField=type/BOM/盈亏报表 noOps/项目看板]+自写渲染器 2[我的待办 #todoBody 实体重建·filterTodo 原逻辑不变·统计卡联动；数据字典 dic-item 分类切换+计数重算=道远点名交互]；'
          'B 类 46 文件白名单=agent-handoff/g12-whitelist.md（3 录单页+43 弹窗，本体零改动）；list-generic.js 增 noOps 开关[无操作列页·向后兼容]；verify_listfull batch3 清单已修 G07 陈旧引用[租出台账→租赁单列表·在租台账删]）。'
          'G07 重指向存量：url/role 指针 66+8 处改指 库存查询/租赁单列表；leaseOrders 9 行列手术[退回进度·去约定归还/天数]；stockFlows 10 行 ops+客户在租；assetTracks/rentTracks 宿主注记留档；库存查询 openTrack(key) 页内渲染模式（与 flowModal 的 detailTitle/detailBody id 冲突规避方案）；'
          'F01=v3.3 唯一演示图（G08 拆 T1/T2·7 泳道 76 节点）；audit 口径=死链 0/JS 0/相对 g12baseline 逐键 diff 新增 0（G12 后基线 audit_results_g12baseline.json）')

NEW_TASK = ('- **当前任务**：✅ **G12 数据驱动查漏收口（2026-09-10 道远目检发现·d9aa5b1）**——55 漏网文件（实扫 12 业务页+43 弹窗未引 demo-data，任务书 11+43 多出「我的待办」按实扫收口）分类 A=9/B=46；'
            'A 类接线后全站 38 业务页+26 弹窗引 demo-data（漏网 A 类清零）；七道验证门全过（audit 108 页死链0/JS0/diff 新增0·grep 9=9·PW 4/4[数据字典分类切换 6→3→2 行·操作日志/用户权限/项目档案 行≥6+筛选真生效]·白名单 git diff ∅·verify 三批 100/88/43 失败0·失败清单 0 失败 5 偏差留档 _scan_tmpdir/goal-failures-g12-20260910.md）；'
            '开工前按七.0.② 存档另一会话 F01 v3.4 重写 WIP（29e4496 分股）；上一任务 G11（标注污染清查）✅ 见 _索引；**任务总账=`agent-handoff/_索引.md`**；下一任务 **G13 会议功能补全（13 项·前置=G12 已完成✅）**任务书已就绪待道远投喂（遗留：F01 旧术语清理、即将到期待客户确认、工期表重估追加范围、F01 完整截图 PNG 仍 v2.9 待重截、zip 20260910 菜单仍 v3.3 待下轮刷新）')

found_dd = found_task = False
for i, line in enumerate(lines):
    if line.startswith('- **数据驱动**：'):
        lines[i] = NEW_DD; found_dd = True
    elif line.startswith('- **当前任务**：'):
        lines[i] = NEW_TASK; found_task = True
assert found_dd and found_task, (found_dd, found_task)
head = lines[7] if len(lines) > 7 else ''
for i, line in enumerate(lines[:10]):
    if '滚动更新' in line:
        lines[i] = line.replace('2026-09-09', '2026-09-10')
open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
print('3/3 _AGENT基线 快照滚动 ✓（数据驱动行+当前任务行+快照日期）')
