# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已完成（一次性校验）
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2lib

targets = ['基础数据/客商管理.html', '基础数据/BOM.html', '基础数据/BOM维护.html', '基础数据/器具档案.html',
           '仓储作业/组装列表.html', '仓储作业/组装录单.html', '包装管理/在租台账.html', '包装管理/丢损赔偿单.html',
           '包装管理/租出台账.html', '财务协同/回款登记.html', '财务协同/银行水单核销.html', '财务协同/盈亏报表.html',
           '订单协同/客户订单.html', '订单协同/路凯下发.html', '仓储作业/库存查询.html', '首页/项目看板.html',
           '项目管理/项目详情.html', '项目管理/项目档案.html']
for rel in targets:
    html = v2lib.read_page(rel)
    t = re.search(r'<title>([^<]*)</title>', html).group(1)
    cards = re.findall(r'<h3 class="card-title"[^>]*>([^<]*)</h3>', html)
    tabs = re.findall(r'<span class="tab(?: active)?">([^<]+?)\s*<span class="close">', html)
    print(f'{rel}\n  title={t}\n  cards={cards}\n  tabs={tabs}')
