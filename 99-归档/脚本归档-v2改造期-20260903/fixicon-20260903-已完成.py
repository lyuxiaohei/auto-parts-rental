# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已完成（图标修复期工具）
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
import re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
html = open('P3-R01-包装租赁管理后台原型/仓储作业/采购入库列表.html', encoding='utf-8').read()
m = re.search(r'系统管理<span class="sm-arrow">', html)
# 找到系统管理菜单项的 svg
seg = html[m.start()-3000:m.start()]
svg = re.findall(r'<svg width="14" height="14"[^>]*>(.*?)</svg>', seg, re.S)
print(repr(svg[-1]))
