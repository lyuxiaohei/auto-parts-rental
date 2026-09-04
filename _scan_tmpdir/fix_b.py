# -*- coding: utf-8 -*-
"""B组：停用确认（6页×40钮）/ 重置密码确认 ×9 / 权限配置已绑定核对 / 在租台账退租跳转 ×9 + 报废确认 ×9。"""
import sys
sys.path.insert(0, r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir")
from detail_modal_lib import *

STOP = '<a>停用</a>'
STOPN = '<a onclick="openModal(\'stopModal\')">停用</a>'

def deploy_stop(page, rows_html, warn, expect, tpl=None, with_js=False, extra_css=True):
    _t = read_page(page)
    if 'id="stopModal"' in _t and STOPN in _t:  # 幂等：已完成则跳过
        assert _t.count(STOPN) == expect, page + ': stopModal 已存在但绑定数不符'
        print('SKIP(已完成)', page)
        return
    modal = confirm_modal('stopModal', '停用确认', warn, header_html=rows_html, ok='确认停用')
    t, t2 = inject_block(page, modal, with_js=with_js, extra_css=extra_css)
    t2 = bind_buttons(t2, STOP, STOPN, expect)
    assert_unique_id(t2, 'stopModal')
    write_page(page, t2)
    if tpl:
        standalone(tpl, '停用确认', page, modal)
    print('OK 停用确认', page, '×%d' % expect)

# ---- BOM 配方停用 ×4（页面无既有弹窗 → 带脚本）----
deploy_stop('基础数据/BOM.html',
    drow('父项编码', 'ZH-2601-A') + drow('父项名称', '驾驶室围板箱整箱套件')
    + drow('当前状态', '<span class="tag tag-green">启用</span>') + drow('子项数', '5'),
    '确认停用该 BOM 配方（ZH-2601-A）？<br>停用后不可再用于新组装，历史单据与在用配方版本不受影响。',
    4, tpl='基础数据/弹窗/停用确认.html', with_js=True)

# ---- 器具停用 ×6 ----
deploy_stop('基础数据/器具档案.html',
    drow('器具编码', 'WBX-1210L') + drow('名称', '围板箱 1200×1000×970')
    + drow('资产来源', '自有') + drow('当前状态', '<span class="tag tag-green">启用</span>'),
    '确认停用该器具（WBX-1210L）？<br>停用后不可再出租、不可新增租赁单；在租与库存数据不受影响。',
    6, extra_css=False)

# ---- 零部件停用 ×6 ----
deploy_stop('基础数据/零部件档案.html',
    drow('零件号', 'LJ-A100') + drow('名称', '锁扣组件')
    + drow('规格', '不锈钢 304 · M8') + drow('当前状态', '<span class="tag tag-green">启用</span>'),
    '确认停用该零部件（LJ-A100）？<br>停用后不可再用于新 BOM 配方与新采购订单；历史单据不受影响。',
    6, extra_css=False)

# ---- 库位停用 ×10 ----
deploy_stop('基础数据/库位档案.html',
    drow('库位编码', 'RA-A-01-01') + drow('库区', '原料区 RA · 华东中心仓')
    + drow('容量占用', '68%') + drow('当前状态', '<span class="tag tag-green">启用</span>'),
    '确认停用该库位（RA-A-01-01）？<br>停用后不可再存放物料；在库物料请先调拨至其他库位。',
    10, extra_css=False)

# ---- 数据字典停用 ×5 ----
deploy_stop('系统管理/数据字典.html',
    drow('字典项编码', 'DT-01') + drow('简码 / 名称', 'PS · 破损')
    + drow('备注', '外观或结构损坏，可维修') + drow('当前状态', '<span class="tag tag-green">启用</span>'),
    '确认停用该字典项（破损 PS）？<br>停用后丢损赔偿单不可再选用该原因，历史数据不受影响。',
    5)

# ---- 用户停用 ×9 + 重置密码 ×9（用户权限，独立模板各一）----
modal = confirm_modal('stopModal', '停用确认',
    '确认停用该用户（admin · 系统管理员）？<br>停用后该用户无法登录系统，历史操作日志保留。',
    header_html=drow('用户账号', 'admin') + drow('姓名 / 角色', '系统管理员 · 系统管理员')
        + drow('所属方', '我方') + drow('当前状态', '<span class="tag tag-green">启用</span>'),
    ok='确认停用')
t, t2 = inject_block('系统管理/用户权限.html', modal, with_js=False)
t2 = bind_buttons(t2, STOP, STOPN, 9)
assert_unique_id(t2, 'stopModal')
write_page('系统管理/用户权限.html', t2)
standalone('系统管理/弹窗/停用确认.html', '停用确认', '系统管理/用户权限.html', modal)
print('OK 停用确认 系统管理/用户权限.html ×9')

modal = confirm_modal('resetModal', '重置密码确认',
    '确认将该用户（admin）的密码重置为初始密码？<br>重置后该用户首次登录时须修改密码。',
    header_html=drow('用户账号', 'admin') + drow('姓名', '系统管理员')
        + drow('手机号', '138****0001') + drow('当前状态', '<span class="tag tag-green">启用</span>'),
    ok='确认重置', ok_style='')
t, t2 = inject_block('系统管理/用户权限.html', modal, with_js=False, extra_css=False)
t2 = bind_buttons(t2, '<a>重置密码</a>', '<a onclick="openModal(\'resetModal\')">重置密码</a>', 9)
assert_unique_id(t2, 'resetModal')
write_page('系统管理/用户权限.html', t2)
standalone('系统管理/弹窗/重置密码确认.html', '重置密码确认', '系统管理/用户权限.html', modal)
print('OK 重置密码确认 系统管理/用户权限.html ×9')

# ---- 在租台账：退租跳转 ×9 + 报废确认 ×9（trackModal/开关脚本 A 组已注入 → with_js=False）----
t = read_page('包装管理/在租台账.html')
t2 = bind_buttons(t, '<a>退租</a>', '<a onclick="go(\'../包装管理/退租申请列表.html\')">退租</a>', 9)
write_page('包装管理/在租台账.html', t2)
print('OK 在租台账 退租跳转 ×9')

modal = confirm_modal('scrapModal', '报废确认',
    '确认报废该器具（WBX-1210L 围板箱）？<br>报废后资产出库、不可再出租；如器具仍在租，请先办理退租。',
    header_html=drow('器具编码', 'WBX-1210L') + drow('名称', '围板箱 1200×1000×970')
        + drow('在租数量', '3,120 只') + drow('循环状态', '<span class="tag tag-green">在租</span>'),
    ok='确认报废')
t, t2 = inject_block('包装管理/在租台账.html', modal, with_js=False, extra_css=False)
t2 = bind_buttons(t2, '<a>报废</a>', '<a onclick="openModal(\'scrapModal\')">报废</a>', 9)
assert_unique_id(t2, 'scrapModal')
write_page('包装管理/在租台账.html', t2)
standalone('包装管理/弹窗/报废确认.html', '报废确认', '包装管理/在租台账.html', modal)
print('OK 在租台账 报废确认 ×9')

# ---- 权限配置核对：应已全部绑定 roleModal（既有） ----
t = read_page('系统管理/用户权限.html')
n_bound = t.count("onclick=\"openModal('roleModal')\"")
n_bare = len([1 for _ in [0]])
import re
bare = len(re.findall(r'<a[^>]*>权限配置</a>', t))
assert n_bound == 14 and bare == 0, '权限配置绑定异常: bound=%d bare=%d' % (n_bound, bare)
print('OK 权限配置核对：14 处已绑定 roleModal，无需改动')
print('B 组完成')
