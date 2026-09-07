# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已废弃（一次性修复，已完成使命）
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
"""步骤6a：批量精修——标题/表头/页签/残留术语/叠字 bug"""
import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v2lib import PROTO, read_page, write_page

FIX = {}

def add(rel, pairs):
    FIX.setdefault(rel, []).extend(pairs)

# ---- 全站性小修（对所有页面执行）----
GLOBAL = [
    ('丢损赔偿单单', '丢损赔偿单'),          # 叠字 bug
    ('BOM BOM', 'BOM 清单'),               # 子母件 BOM -> BOM BOM 修正
    ('水单核销 5 笔', '收款核销 5 笔'),      # 项目看板统计脚注
    ('>水单核销 <', '>收款核销 <'),          # 各页面页签
    ('<span class="tab">客户下单 <span class="close">×</span></span>', '<span class="tab">销售订单 <span class="close">×</span></span>'),
    ('<span class="tab">损益报表 <span class="close">×</span></span>', '<span class="tab">项目损益 <span class="close">×</span></span>'),
    ('<span class="tab active">损益报表 <span class="close">×</span></span>', '<span class="tab active">项目损益 <span class="close">×</span></span>'),
    ('<title>损益报表 - 包装租赁管理后台</title>', '<title>项目损益 - 包装租赁管理后台</title>'),
    ('>全部项目 · 财务协同<', '>全部项目 · 财务应收<'),   # 用户权限 数据权限列
    ('<td>财务协同</td>', '<td>财务应收</td>'),           # 操作日志 模块列
    ('生成水单核销记录', '生成收款核销记录'),             # 操作日志 内容
    ('>项目盈亏</button>', '>项目损益</button>'),          # 项目详情 按钮
]

# ---- 客商管理 ----
add('基础数据/客商管理.html', [
    ('<h3 class="card-title">企业档案</h3>', '<h3 class="card-title">客商管理</h3>'),
    ('<th>企业编码</th>', '<th>客商编码</th>'),
    ('<th>企业名称</th>', '<th>客商名称</th>'),
    ('<th>类型</th>', '<th>客商类型</th>'),
    ('<label>企业名称：</label>', '<label>客商名称：</label>'),
    ('<label>企业类型：</label>', '<label>客商类型：</label>'),
    ('新建企业', '新建客商'),
    ('<span class="tab active">企业 <span class="close">×</span></span>', '<span class="tab active">客商管理 <span class="close">×</span></span>'),
])

# ---- 银行水单核销（页面文件名保留，可见文本改收款核销/回单）----
add('财务协同/银行水单核销.html', [
    ('<span class="tab active">水单核销 <span class="close">×</span></span>', '<span class="tab active">收款核销 <span class="close">×</span></span>'),
    ('已选水单合计', '已选回单合计'),
    ('导入水单', '导入回单'),
    ('<th>水单编号</th>', '<th>回单编号</th>'),
    ('按水单未核销金额', '按回单未核销金额'),
    ('水单↔单据逐笔勾对', '回单↔单据逐笔勾对'),
])

# ---- 用户权限：客户端相关标注文案 ----
add('系统管理/用户权限.html', [
    ('我方/客户/运营方三类账号体系——客户端登录即在此配置', '我方/客户/运营方三类账号体系——客户账号由项目经理代下单时使用'),
])

# ---- 采购入库列表：补「应付账单」跳转（第八节）----
add('仓储作业/采购入库列表.html', [
    ('<a>打印</a></span>', '<a>打印</a><a onclick="go(\'../财务协同/应付账单.html\')">应付账单</a></span>'),
])

# ---- 组装列表：补新建按钮跳录单页已有；确认组装单标题已是「组装单」 ----

total_changed = 0
all_pages = []
import glob
all_pages = [os.path.relpath(p, PROTO).replace(os.sep, '/') for p in glob.glob(os.path.join(PROTO, '*', '*.html'))]

for rel in all_pages:
    html = read_page(rel)
    orig = html
    pairs = list(GLOBAL) + FIX.get(rel, [])
    for old, new in pairs:
        if old in html:
            html = html.replace(old, new)
    if html != orig:
        write_page(rel, html)
        n = sum(1 for old, new in pairs if old in orig)
        print(f'{rel}: 应用 {n} 处替换')
        total_changed += 1

print(f'\n共修改 {total_changed} 个文件')

# 叠字/残留复扫
print('\n=== 复扫 ===')
bad_patterns = ['赔偿单单', '客商客商', 'BOM BOM', '组装装', '器具器具', '水单核销', '损益报表 -', '财务协同</td>', '财务协同<']
hit = False
for rel in all_pages:
    html = read_page(rel)
    body = re.sub(r'''go\('[^']*'\)|href="[^"]*"''', '', html)
    for bp in bad_patterns:
        if bp in body:
            print(f'残留: {rel} -> {bp}')
            hit = True
if not hit:
    print('无残留')
