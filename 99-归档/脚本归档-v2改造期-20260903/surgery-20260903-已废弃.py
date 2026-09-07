# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已废弃（一次性修复，已完成使命）
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
"""步骤6b：4 个重点页面手术式改造"""
import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v2lib import read_page, write_page

def must_replace(html, old, new, tag):
    if old not in html:
        raise RuntimeError(f'[{tag}] 未找到目标片段: {old[:60]}...')
    return html.replace(old, new, 1)

# ============================================================
# A. 订单协同/客户订单.html —— 增加「下单方式」列（改造#3）
# ============================================================
rel = '订单协同/客户订单.html'
h = read_page(rel)
h = must_replace(h, '<th>下单人</th>', '<th>下单人</th>\n          <th>下单方式</th>', rel)
# 两笔改为项目经理代下单，其余客户自助
h = must_replace(h, '<td>袁明（客户账号）</td>\n          <td>2026-08-30 16:40</td>',
                 '<td>王强（项目经理）</td>\n          <td><span class="tag tag-blue">代下单</span></td>\n          <td>2026-08-30 16:40</td>', rel)
h = must_replace(h, '<td>何静（客户账号）</td>\n          <td>2026-08-29 08:45</td>',
                 '<td>王强（项目经理）</td>\n          <td><span class="tag tag-blue">代下单</span></td>\n          <td>2026-08-29 08:45</td>', rel)
# 其余 6 行的下单人 td 后插入 客户自助 标签
for who, when in [('袁明（客户账号）', '2026-08-31 08:12'), ('何静（客户账号）', '2026-08-30 10:05'),
                  ('林芳（客户账号）', '2026-08-29 09:22'), ('袁明（客户账号）', '2026-08-28 15:30'),
                  ('袁明（客户账号）', '2026-08-27 14:10'), ('赵磊（客户账号）', '2026-08-26 11:20')]:
    h = must_replace(h, f'<td>{who}</td>\n          <td>{when}</td>',
                     f'<td>{who}</td>\n          <td><span class="tag tag-gray">客户自助</span></td>\n          <td>{when}</td>', rel)
write_page(rel, h)
print(f'A 完成: {rel}')

# ============================================================
# B. 包装管理/丢损赔偿单.html —— 按 5.11 重构表格列
# ============================================================
rel = '包装管理/丢损赔偿单.html'
h = read_page(rel)
old_thead = '''          <th></th>
          <th>赔偿单号</th>
          <th>关联退租单</th>
          <th>所属项目</th>
          <th>客户</th>
          <th>缺损内容</th>
          <th>赔偿金额(元)</th>
          <th>状态</th>
          <th>生成时间</th>
          <th>操作</th>'''
new_thead = '''          <th></th>
          <th>赔偿单号</th>
          <th>关联退租申请单号</th>
          <th>客户名称</th>
          <th>所属项目</th>
          <th>赔偿器具</th>
          <th>缺损数量</th>
          <th>丢失数量</th>
          <th>赔偿单价(元)</th>
          <th>赔偿金额(元)</th>
          <th>状态</th>
          <th>操作</th>'''
h = must_replace(h, old_thead, new_thead, rel)

new_rows = [
    ('BS-20260902-010', 'TZSQ-20260829-004', '小鹏汽车科技有限公司', 'PRJ-2603', 'ZH-2603-C 电池托盘护角套件', '2 套', '1 套', '310.00', '930.00',
     '<span class="tag tag-orange">待审核</span>', '<a>审核</a><a>详情</a>'),
    ('BS-20260901-009', 'TZSQ-20260818-001', '一汽解放汽车有限公司', 'PRJ-2601', 'ZH-2601-A 驾驶室围板箱整箱套件', '3 套', '0', '1,230.00', '3,690.00',
     '<span class="tag tag-orange">赔偿中</span>', '<a>详情</a><a onclick="go(\'../财务协同/应收账单.html\')">转应收</a>'),
    ('BS-20260828-004', 'TZSQ-20260826-002', '一汽解放汽车有限公司', 'PRJ-2601', 'WBX-1210L 围板箱', '2 只', '2 只', '380.00', '1,520.00',
     '<span class="tag tag-blue">已转应收</span>', '<a>详情</a><a onclick="go(\'../财务协同/应收账单.html\')">查看应收</a>'),
    ('BS-20260827-003', 'TZSQ-20260823-005', '小鹏汽车科技有限公司', 'PRJ-2603', '护角（散件）', '2 件', '0', '310.00', '620.00',
     '<span class="tag tag-green">已赔偿</span>', '<a>详情</a>'),
    ('BS-20260815-002', 'TZSQ-20260812-004', '上汽大众宁波分公司', 'PRJ-2602', 'BTC-6040 料箱盖', '6 件', '0', '78.00', '468.00',
     '<span class="tag tag-green">已赔偿</span>', '<a>详情</a>'),
]
rows_html = ''
for r in new_rows:
    cells = ('<td><input type="checkbox" class="cb"></td>\n'
             f'          <td><span class="lk">{r[0]}</span></td>\n'
             f'          <td><span class="lk">{r[1]}</span></td>\n'
             f'          <td>{r[2]}</td>\n'
             f'          <td>{r[3]}</td>\n'
             f'          <td>{r[4]}</td>\n'
             f'          <td><span class="td-num">{r[5]}</span></td>\n'
             f'          <td><span class="td-num">{r[6]}</span></td>\n'
             f'          <td><span class="td-num">{r[7]}</span></td>\n'
             f'          <td><span class="td-num" style="color:var(--danger)">{r[8]}</span></td>\n'
             f'          <td>{r[9]}</td>\n'
             f'          <td><span class="ops">{r[10]}</span></td>')
    rows_html += f'        <tr>\n          {cells}\n        </tr>\n'
h, n = re.subn(r'<tbody>.*?</tbody>', lambda m: '<tbody>\n' + rows_html.rstrip('\n') + '\n      </tbody>', h, flags=re.S)
if n != 1:
    raise RuntimeError(f'[{rel}] tbody 替换失败')
# 补充说明：赔偿单来源
h = must_replace(h, '<div class="head-btns"><button class="btn btn-default btn-sm">批量导出</button></div>',
                 '<div class="head-btns"><button class="btn btn-default btn-sm">批量导出</button><button class="btn btn-sm" onclick="go(\'../财务协同/应收账单.html\')">查看应收账单</button></div>', rel)
write_page(rel, h)
print(f'B 完成: {rel}')

# ============================================================
# C. 包装管理/在租台账.html —— 增加四态统计卡片（改造#8）+ 租出台账入口
# ============================================================
rel = '包装管理/在租台账.html'
h = read_page(rel)
four_state = '''<div class="stat-grid">
  <div class="stat">
    <div class="st-label"><span>在库（仓库内可用）</span></div>
    <div class="st-num">42,860<span class="unit">件/套</span></div>
    <div class="st-foot">含已组装组合单元 1,610 套</div>
  </div>
  <div class="stat">
    <div class="st-label"><span>在途（退租未审核）</span></div>
    <div class="st-num">240<span class="unit">件/套</span></div>
    <div class="st-foot">退租申请待审核 3 单</div>
  </div>
  <div class="stat">
    <div class="st-label"><span>客户端（租出在外）</span></div>
    <div class="st-num">12,480<span class="unit">只/套</span></div>
    <div class="st-foot">较上月 <em>+3.2%</em></div>
  </div>
  <div class="stat">
    <div class="st-label"><span>退租库存（待入库）</span></div>
    <div class="st-num">260<span class="unit">件/套</span></div>
    <div class="st-foot">验收通过待入库 4 单</div>
  </div>
</div>

'''
h = must_replace(h, '<div class="stat-grid">\n  <div class="stat">\n    <div class="st-label"><span>在租资产总量</span></div>', four_state + '<div class="stat-grid">\n  <div class="stat">\n    <div class="st-label"><span>在租资产总量</span></div>', rel)
h = must_replace(h, '<div class="head-btns"><button class="btn btn-default btn-sm">批量导出</button></div>',
                 '<div class="head-btns"><button class="btn btn-default btn-sm" onclick="go(\'../包装管理/租出台账.html\')">租出台账</button><button class="btn btn-default btn-sm">批量导出</button></div>', rel)
write_page(rel, h)
print(f'C 完成: {rel}')

# ============================================================
# D. 仓储作业/库存查询.html —— 四态视图改造（改造#2 / 验收#6）
# ============================================================
rel = '仓储作业/库存查询.html'
h = read_page(rel)

# D1. 统计卡片 → 四态
old_stats = re.search(r'<div class="stat-grid">.*?</div>\s*</div>\s*</div>\s*</div>', h, re.S)
new_stats = '''<div class="stat-grid">
  <div class="stat">
    <div class="st-label"><span>在库（仓库内可用）</span></div>
    <div class="st-num">42,860<span class="unit">件/套</span></div>
    <div class="st-foot">其中组装占用 <em>3,920</em> 件</div>
  </div>
  <div class="stat">
    <div class="st-label"><span>在途（退租未审核）</span></div>
    <div class="st-num">240<span class="unit">件/套</span></div>
    <div class="st-foot">退租申请待审核 3 单</div>
  </div>
  <div class="stat">
    <div class="st-label"><span>客户端（租出在外）</span></div>
    <div class="st-num">12,480<span class="unit">只/套</span></div>
    <div class="st-foot">对应在租租赁单 40 张</div>
  </div>
  <div class="stat">
    <div class="st-label"><span>退租库存（待入库）</span></div>
    <div class="st-num">260<span class="unit">件/套</span></div>
    <div class="st-foot">验收通过待入库 4 单</div>
  </div>
</div>'''
h = h[:old_stats.start()] + new_stats + h[old_stats.end():]

# D2. 视角切换命名 + 卡片标题
h = must_replace(h, "switchView('part')\">零件视角", "switchView('part')\">散件视角", rel)
h = must_replace(h, '<h3 class="card-title" data-note="1">库存双视角查询</h3>', '<h3 class="card-title" data-note="1">库存四态查询</h3>', rel)

# D3. 散件视角表头
old_ph = '''          <th>编码</th>
          <th>名称</th>
          <th>类别</th>
          <th>适用项目</th>
          <th>可用库存</th>
          <th>已分配(待出库)</th>
          <th data-note="2">组装占用</th>
          <th>采购在途</th>
          <th>总库存</th>'''
new_ph = '''          <th>编码</th>
          <th>名称</th>
          <th>物料类别</th>
          <th>适用项目</th>
          <th>在库</th>
          <th>在途(退租未审核)</th>
          <th data-note="2">客户端(租出)</th>
          <th>退租待入库</th>
          <th>总量</th>'''
h = must_replace(h, old_ph, new_ph, rel)

# D4. 散件视角行：类别标签改 零部件/租赁器具；租赁器具行客户端列给非零值
h = h.replace('<td><span class="tag tag-green">正常</span></td>', '<td><span class="tag tag-blue">零部件</span></td>')
h = h.replace('<td><span class="tag tag-blue">在租</span></td>', '<td><span class="tag tag-green">租赁器具</span></td>')
# WBX-1210L 行: 在库2,120 / 在途360 / 客户端0→3,120 / 退租待入库500
h = must_replace(h, '''<td><span class="td-num">2,120</span></td>
          <td><span class="td-num">360</span></td>
          <td><span class="td-num">0</span></td>
          <td><span class="td-num">500</span></td>''',
                 '''<td><span class="td-num">2,120</span></td>
          <td><span class="td-num">160</span></td>
          <td><span class="td-num">3,120</span></td>
          <td><span class="td-num">80</span></td>''', rel)
# WBX-1210M 行
h = must_replace(h, '''<td><span class="td-num">860</span></td>
          <td><span class="td-num">140</span></td>
          <td><span class="td-num">0</span></td>
          <td><span class="td-num">0</span></td>''',
                 '''<td><span class="td-num">860</span></td>
          <td><span class="td-num">40</span></td>
          <td><span class="td-num">1,020</span></td>
          <td><span class="td-num">0</span></td>''', rel)
# PLT-1210P 行
h = must_replace(h, '''<td><span class="td-num">1,410</span></td>
          <td><span class="td-num">290</span></td>
          <td><span class="td-num">0</span></td>
          <td><span class="td-num">0</span></td>''',
                 '''<td><span class="td-num">1,410</span></td>
          <td><span class="td-num">0</span></td>
          <td><span class="td-num">1,860</span></td>
          <td><span class="td-num">60</span></td>''', rel)
# BTC-6040 行
h = must_replace(h, '''<td><span class="td-num">3,300</span></td>
          <td><span class="td-num">640</span></td>
          <td><span class="td-num">0</span></td>
          <td><span class="td-num">0</span></td>''',
                 '''<td><span class="td-num">3,300</span></td>
          <td><span class="td-num">40</span></td>
          <td><span class="td-num">2,480</span></td>
          <td><span class="td-num">120</span></td>''', rel)

# D5. 组合视角表头
old_ch = '''          <th>父项编码</th>
          <th>组合件名称</th>
          <th>BOM版本</th>
          <th>所属项目</th>
          <th>已组装成品</th>
          <th>已分配(待出库)</th>
          <th>可用组合</th>
          <th>在租/在外</th>
          <th>累计出库</th>'''
new_ch = '''          <th>父项编码</th>
          <th>组合单元名称</th>
          <th>BOM版本</th>
          <th>所属项目</th>
          <th>在库(已组装)</th>
          <th>在途(退租未审核)</th>
          <th>客户端(在租)</th>
          <th>退租待入库</th>
          <th>累计出库</th>'''
h = must_replace(h, old_ch, new_ch, rel)

# D6. 组合视角数据行（3 行，数值与四态口径对齐）
combo_rows = {
    'ZH-2601-A': ('640', '60', '3,120', '80', '18,420'),
    'ZH-2602-B': ('820', '45', '4,120', '0', '22,650'),
    'ZH-2603-C': ('150', '0', '1,020', '20', '6,830'),
}
for code, vals in combo_rows.items():
    pat = re.compile(r'(<td><span class="lk">' + code + r'</span></td>\s*<td>[^<]*</td>\s*<td>[^<]*</td>\s*<td>[^<]*</td>)\s*<td><span class="td-num">[\d,]+</span></td>\s*<td><span class="td-num">[\d,]+</span></td>\s*<td><span class="td-num"><b>[\d,]+</b></span></td>\s*<td><span class="td-num">[\d,]+</span></td>\s*<td><span class="td-num">[\d,]+</span></td>')
    repl = (r'\1\n          <td><span class="td-num">' + vals[0] + '</span></td>\n'
            r'          <td><span class="td-num">' + vals[1] + '</span></td>\n'
            r'          <td><span class="td-num"><b>' + vals[2] + '</b></span></td>\n'
            r'          <td><span class="td-num">' + vals[3] + '</span></td>\n'
            r'          <td><span class="td-num">' + vals[4] + '</span></td>')
    h, n = pat.subn(repl, h)
    if n != 1:
        raise RuntimeError(f'[{rel}] 组合行 {code} 替换失败 n={n}')

# D7. 标注文案更新
h = h.replace('库存双视角查询</div><div class="pnp-d">零件视角 / 组合视角切换——本次新增能力',
              '库存四态查询</div><div class="pnp-d">在库/在途/客户端/退租库存四态 + 散件/组合双视角切换')
h = h.replace('库存四项状态</div><div class="pnp-d">可用、已分配、组装占用、采购在途——「组装占用」正是组装改进的体现',
              '库存四态说明</div><div class="pnp-d">在库（仓库内可用）、在途（退租未审核）、客户端（租出在外）、退租库存（待入库）')
write_page(rel, h)
print(f'D 完成: {rel}')
print('全部完成')
