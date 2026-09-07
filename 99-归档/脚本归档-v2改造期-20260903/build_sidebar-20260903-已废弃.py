# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已废弃·禁止运行（内嵌菜单快照，重跑覆盖全站侧边栏）
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
"""步骤2-4：批量重建现有 32 页侧边栏 + 移除系统切换器 + 路径重映射 + 术语清理"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v2lib import *

# 页面 -> 选中菜单项
SELECTED = {
    '首页/项目看板.html': '首页',
    '项目管理/项目档案.html': '项目管理',
    '项目管理/项目详情.html': '项目管理',
    '基础数据/客商管理.html': '客商管理',
    '基础数据/器具档案.html': '器具档案',
    '基础数据/零部件档案.html': '零部件档案',
    '基础数据/BOM.html': 'BOM',
    '基础数据/BOM维护.html': 'BOM',
    '基础数据/库位档案.html': '库位档案',
    '仓储作业/采购入库列表.html': '采购入库',
    '仓储作业/采购入库录单.html': '采购入库',
    '仓储作业/组装列表.html': '组装',
    '仓储作业/组装录单.html': '组装',
    '仓储作业/组合出库列表.html': '组合出库',
    '仓储作业/组合出库录单.html': '组合出库',
    '仓储作业/盘点列表.html': '库存盘点',
    '仓储作业/盘点录入.html': '库存盘点',
    '仓储作业/库存查询.html': '库存查询',
    '包装管理/租赁单列表.html': '租赁单',
    '包装管理/退租申请列表.html': '退租申请',
    '包装管理/在租台账.html': '在租台账',
    '包装管理/丢损赔偿单.html': '丢损赔偿单',
    '包装管理/租出台账.html': '在租台账',
    '订单协同/客户订单.html': '订单审核',
    '订单协同/路凯下发.html': '订单同步',
    '订单协同/结算导出.html': '对账结算',
    '财务协同/应收账单.html': '应收账单',
    '财务协同/开票登记.html': '开票登记',
    '财务协同/回款登记.html': '收款登记',
    '财务协同/银行水单核销.html': '收款核销',
    '财务协同/盈亏报表.html': '项目损益',
    '系统管理/用户权限.html': '用户权限',
    '系统管理/操作日志.html': '操作日志',
    '系统管理/数据字典.html': '数据字典',
}

ok, fail = 0, []
for rel, sel in SELECTED.items():
    path = os.path.join(PROTO, rel)
    if not os.path.exists(path):
        fail.append((rel, '文件不存在'))
        continue
    try:
        html = read_page(rel)
        html = apply_path_remap(html)      # 1) 先改 go() 路径
        html = rebuild_sidebar(html, sel)  # 2) 重建侧边栏（含新 side-foot，无切换器）
        html = strip_sys_switch(html)      # 3) 删切换器 CSS/JS
        html = apply_text_repl(html)       # 4) 术语清理（保护属性值）
        write_page(rel, html)
        ok += 1
    except Exception as e:
        fail.append((rel, str(e)))

print(f'成功 {ok} 页')
for rel, err in fail:
    print(f'失败: {rel} -> {err}')
