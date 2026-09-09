# -*- coding: utf-8 -*-
"""批2 Script D 续：用户权限六角色 + 审核人行 + 虚拟仓行 + 全站运营方→供应商（F01 除外）
前置状态：demo-data（partners/locations/stockFlows/全局换词）与客商管理.html 已完成。
"""
from pathlib import Path
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁")
PROTO = ROOT / "P3-R01-包装租赁管理后台原型"
LOG = []

def rep(txt, old, new, exp, tag):
    c = txt.count(old)
    assert c == exp, f'[{tag}] 「{old[:50]}」{c}≠{exp}'
    return txt.replace(old, new)

# ============================================================
# 6. 用户权限.html：六角色重排
# ============================================================
UP = PROTO / "系统管理" / "用户权限.html"
txt = UP.read_bytes().decode('utf-8')
nl = '\r\n' if '\r\n' in txt else '\n'

txt = rep(txt, '<select><option selected>全部</option><option>系统管理员</option><option>项目经理</option><option>仓储主管</option><option>财务</option><option>客户账号</option></select>',
          '<select><option selected>全部</option><option>系统管理员</option><option>财务</option><option>商务</option><option>物流</option><option>财务主管</option><option>商务主管</option><option>物流主管</option><option>客户账号</option><option>供应商账号</option></select>', 1, '角色筛选')
n_all = txt.count('<option>我方</option><option>客户</option><option>运营方</option>')
assert n_all == 2, n_all
txt = txt.replace('<option>我方</option><option>客户</option><option>运营方</option>', '<option>我方</option><option>客户</option><option>供应商</option>')

txt = rep(txt, '<span class="stab active">全部用户<span class="stab-count">24</span></span>',
          '<span class="stab active">全部用户<span class="stab-count">18</span></span>', 1, '页签1')
txt = rep(txt, '<span class="stab">我方<span class="stab-count">14</span></span>',
          '<span class="stab">我方<span class="stab-count">8</span></span>', 1, '页签2')
txt = rep(txt, '<span class="stab">运营方<span class="stab-count">3</span></span>',
          '<span class="stab">供应商<span class="stab-count">3</span></span>', 1, '页签4')

def urow(acct, name, role, role_cls, side, side_cls, perm, phone, login):
    ops = "<td class=\"sticky-op\"><span class=\"ops\"><a onclick=\"openModal('createModal')\">编辑</a><a onclick=\"openModal('roleModal')\">权限配置</a><a onclick=\"openModal('resetModal')\">重置密码</a><a onclick=\"openModal('stopModal')\">停用</a></span></td>"
    return (f'        <tr>{nl}'
            f'          <td><input type="checkbox" class="cb"></td>{nl}'
            f'          <td><span class="lk">{acct}</span></td>{nl}'
            f'          <td>{name}</td>{nl}'
            f'          <td><span class="tag {role_cls}">{role}</span></td>{nl}'
            f'          <td><span class="tag {side_cls}">{side}</span></td>{nl}'
            f'          <td>{perm}</td>{nl}'
            f'          <td>{phone}</td>{nl}'
            f'          <td><span class="tag tag-green">启用</span></td>{nl}'
            f'          <td>{login}</td>{nl}'
            f'          {ops}{nl}'
            f'        </tr>{nl}')

ROWS = [
    ('admin', '系统管理员', '系统管理员', 'tag-blue', '我方', 'tag-blue', '全部数据', '138****0001', '2026-08-31 08:00'),
    ('chenjin', '陈金', '系统管理员', 'tag-blue', '我方', 'tag-blue', '全部数据', '139****2266', '2026-08-31 09:12'),
    ('zhangwei', '张伟', '物流', 'tag-green', '我方', 'tag-blue', '全部项目 · 仓储作业', '137****4455', '2026-08-31 07:45'),
    ('liguodong', '李国栋', '物流主管', 'tag-green', '我方', 'tag-blue', '全部项目 · 仓储作业 + 出/入库审核', '136****7789', '2026-08-30 19:20'),
    ('lijing', '李静', '财务', 'tag-orange', '我方', 'tag-blue', '全部项目 · 财务应收', '135****9911', '2026-08-31 08:30'),
    ('zhoumin', '周敏', '财务主管', 'tag-orange', '我方', 'tag-blue', '全部项目 · 财务 + 付款/回款确认', '135****8024', '2026-08-30 16:40'),
    ('wangqiang', '王强', '商务', 'tag-green', '我方', 'tag-blue', '全部项目 · 订单/项目', '133****6678', '2026-08-30 17:05'),
    ('wanglin', '王琳', '商务主管', 'tag-green', '我方', 'tag-blue', '全部项目 · 订单 + 租赁单审核', '137****2950', '2026-08-31 08:55'),
    ('yuanming', '袁明', '客户用户', 'tag-gray', '客户', 'tag-gray', '仅 PRJ-2601 · 客户下单', '138****6621', '2026-08-31 08:12'),
    ('hejing', '何静', '客户用户', 'tag-gray', '客户', 'tag-gray', '仅 PRJ-2602 · 客户下单', '139****0233', '2026-08-30 10:02'),
    ('zhoumin_lk', '周敏（路凯）', '供应商账号', 'tag-orange', '供应商', 'tag-orange', 'PRJ-2601/02/04 · 下发回执', '021-66****', '2026-08-31 08:40'),
]
tb_s = txt.find('      <tbody>')
tb_e = txt.find('      </tbody>', tb_s) + len('      </tbody>')
assert tb_s > -1 and tb_e > tb_s
new_tb = '      <tbody>' + nl + ''.join(urow(*r) for r in ROWS) + '      </tbody>'
txt = txt[:tb_s] + new_tb + txt[tb_e:]
txt = rep(txt, '<span class="pg-info">第 1-10 条/总共 24 条</span>', '<span class="pg-info">第 1-11 条/总共 18 条</span>', 1, 'pager')

role_rows = [
    ('系统管理员', '全部功能 + 系统管理', '全部项目', '2'),
    ('财务', '财务应收/应付/项目损益', '全部项目', '1'),
    ('财务主管', '财务全模块 + 付款/回款确认审核', '全部项目', '1'),
    ('商务', '订单/租赁全流程', '全部项目', '2'),
    ('商务主管', '订单/租赁全流程 + 单据审核', '全部项目', '1'),
    ('物流', '仓储作业 + 库存查询', '全部项目', '1'),
    ('物流主管', '仓储作业 + 库存查询 + 出/入库审核', '全部项目', '1'),
    ('客户账号', '仅查看与下单申请', '所属客户', '7'),
    ('供应商账号', '下发回执与对账', '所属供应商', '3'),
]
rr = nl.join(
    f'            <tr><td><b>{r[0]}</b></td><td>{r[1]}</td><td>{r[2]}</td><td><span class="td-num">{r[3]}</span></td><td class="sticky-op"><span class="ops"><a onclick="openModal(\'roleModal\')">权限配置</a></span></td></tr>'
    for r in role_rows) + nl
rm_pos = txt.find("openModal('roleModal')\">角色管理")
assert rm_pos > -1
old_rr_s = txt.find('<tr><td><b>系统管理员</b></td>', rm_pos)
old_rr_e = txt.find('</tbody>', old_rr_s)
assert old_rr_s > -1 and old_rr_e > old_rr_s
txt = txt[:old_rr_s] + rr.rstrip('\r\n ') + txt[old_rr_e:]

txt = rep(txt, '我方/客户/运营方三类账号体系——客户账号由项目经理代下单时使用',
          '我方（财务/商务/物流三线 + 各主管）+ 客户 + 供应商账号；审核按角色配置（主管角色审核，2026-09-08 会议 D4）', 1, '权限pin')
UP.write_bytes(txt.encode('utf-8'))
LOG.append('用户权限.html 六角色重排（11 行示例 + 角色表 9 行）')

# ============================================================
# 7. 审核类弹窗加「审核人（按角色配置）」行
# ============================================================
ROLE_BY_FILE = {
    '商务主管 · 王琳': ['租赁管理/租赁单列表.html', '销售管理/销售订单列表.html', '采购管理/采购订单列表.html',
                  '租赁管理/租入单列表.html', '租赁管理/弹窗/租赁单审核.html', '销售管理/弹窗/销售订单审核.html',
                  '采购管理/弹窗/采购订单审核.html', '租赁管理/弹窗/租入单审核.html'],
    '物流主管 · 李国栋': ['采购管理/采购入库列表.html', '仓储作业/其他入库列表.html', '仓储作业/其他出库列表.html',
                    '仓储作业/盘点列表.html', '仓储作业/库存调拨列表.html', '租赁管理/租入入库列表.html',
                    '租赁管理/租入归还列表.html', '租赁管理/退租入库列表.html', '租赁管理/组合出库列表.html',
                    '销售管理/销售出库列表.html', '采购管理/弹窗/采购入库审核.html', '仓储作业/弹窗/其他入库审核.html',
                    '仓储作业/弹窗/其他出库审核.html', '仓储作业/弹窗/盘点审核.html', '仓储作业/弹窗/调拨审核.html',
                    '租赁管理/弹窗/租入入库确认.html', '租赁管理/弹窗/租入归还审核.html', '租赁管理/弹窗/退租入库审核.html',
                    '租赁管理/弹窗/组合出库确认.html', '销售管理/弹窗/销售出库审核.html'],
    '财务主管 · 周敏': ['财务协同/付款登记.html', '财务协同/弹窗/付款确认.html'],
}
pat_ins = re.compile(r'([ \t]*)<div class="drow"><div class="dlabel">提交人 / 时间</div><div class="dval">([^<]*)</div></div>\n')
tot = 0
for role, files in ROLE_BY_FILE.items():
    for rel in files:
        f = PROTO / rel
        txt = f.read_bytes().decode('utf-8')
        nl = '\r\n' if '\r\n' in txt else '\n'
        norm = txt.replace('\r\n', '\n')
        matches = pat_ins.findall(norm)
        assert len(matches) == 1, f'{rel} 提交人行 {len(matches)}'
        m = pat_ins.search(norm)
        ins_line = m.group(1) + '<div class="drow"><div class="dlabel">审核人（按角色配置）</div><div class="dval">' + role + '</div></div>\n'
        norm = norm[:m.end()] + ins_line + norm[m.end():]
        if nl == '\r\n':
            norm = norm.replace('\n', '\r\n')
        f.write_bytes(norm.encode('utf-8'))
        tot += 1
LOG.append(f'审核弹窗加审核人行 {tot} 文件')

# ============================================================
# 8. 库存查询：静态示例行 + 口径注记
# ============================================================
SQ = PROTO / "仓储作业" / "库存查询.html"
txt = SQ.read_bytes().decode('utf-8')
nl = '\r\n' if '\r\n' in txt else '\n'
hint_row = nl.join([
'        <tr>',
'          <td><input type="checkbox" class="cb"></td>',
'          <td>XNC-AJZX-WBX</td>',
'          <td>围板箱 1200×1000×970（安吉智行·客户虚拟仓）</td>',
'          <td><span class="tag tag-blue">租赁器具</span></td>',
'          <td>PRJ-2605</td>',
'          <td><span class="td-num">0</span></td>',
'          <td><span class="td-num">0</span></td>',
'          <td><span class="td-num">640</span></td>',
'          <td><span class="td-num">0</span></td>',
'          <td><span class="td-num"><b>640</b></span></td>',
'          <td>只</td>',
'          <td>安吉智行·客户虚拟仓</td>',
'          <td class="sticky-op"><span class="ops"><a onclick="openModal(\'flowModal\')">库存流水</a></span></td>',
'        </tr>',
''])
anchor = '      <tbody>'
assert txt.count(anchor) >= 1
txt = txt.replace(anchor, anchor + nl + hint_row, 1)
XN_HINT = '<div class="pn-hint">客户虚拟仓＝在客户处的租赁资产按客户归集（on-hire）；客户转租为其子状态（2026-09-08 会议 T1 方向）。</div>'
if txt.count('class="pn-hint"') > 0:
    # 已有注记：在最后一条 pn-hint 后追加
    last = txt.rfind('</div>', 0, txt.find('id="pins_') if 'id="pins_' in txt else len(txt))
    idxs = [m.end() for m in re.finditer(r'<div class="pn-hint"[^>]*>.*?</div>', txt)]
    assert idxs, 'pn-hint 未找到'
    pos = idxs[-1]
    txt = txt[:pos] + nl + XN_HINT + txt[pos:]
    LOG.append('库存查询 虚拟仓口径注记 追加')
else:
    grid_end = txt.find('class="stat-grid"')
    ins = txt.find('</div>', txt.find('</div>', grid_end))
    txt = txt[:ins + 6] + nl + XN_HINT + txt[ins + 6:]
    LOG.append('库存查询 虚拟仓口径注记 新建')
SQ.write_bytes(txt.encode('utf-8'))
LOG.append('库存查询 静态虚拟仓行 1')

# ============================================================
# 9. 库位档案：客户虚拟仓静态行
# ============================================================
LQ = PROTO / "基础数据" / "库位档案.html"
txt = LQ.read_bytes().decode('utf-8')
nl = '\r\n' if '\r\n' in txt else '\n'
loc_row = nl.join([
'        <tr>',
'          <td><input type="checkbox" class="cb"></td>',
'          <td>华东中心仓（WH-01）</td>',
'          <td>客户虚拟仓</td>',
'          <td><span class="lk">XNC-AJZX</span></td>',
'          <td>虚拟仓</td>',
'          <td>按客户归集 · on-hire</td>',
'          <td>安吉智行 640 只</td>',
'          <td><span class="tag tag-blue">启用</span></td>',
'          <td class="sticky-op"><span class="ops"><a onclick="openModal(\'detailModal\')">详情</a><a onclick="openModal(\'createModal\')">编辑</a></span></td>',
'        </tr>',
''])
anchor = '      <tbody>'
txt = txt.replace(anchor, anchor + nl + loc_row, 1)
LQ.write_bytes(txt.encode('utf-8'))
LOG.append('库位档案 客户虚拟仓静态行 1')

# ============================================================
# 10. 全站 HTML 运营方→供应商（F01 除外；客商管理口径注记除外）
# ============================================================
n_html = 0
skip_files = {'P3-R01-F01-业务流程导航图.html'}
for f in sorted(PROTO.rglob('*.html')):
    if f.name in skip_files:
        continue
    raw = f.read_bytes()
    t = raw.decode('utf-8')
    c = t.count('运营方')
    if f.name == '客商管理.html':
        # 仅剩 2 处口径说明（有意保留）
        continue
    if c:
        t = t.replace('运营方', '供应商')
        f.write_bytes(t.encode('utf-8'))
        n_html += c
LOG.append(f'HTML 运营方→供应商 {n_html} 处（F01/客商管理注记除外）')

print('== 批2 Script D 续 ==')
for l in LOG:
    print(' ✓', l)

left = []
for f in sorted(PROTO.rglob('*.html')):
    if f.name in {'P3-R01-F01-业务流程导航图.html', '客商管理.html'}:
        continue
    if '运营方' in f.read_bytes().decode('utf-8'):
        left.append(str(f.relative_to(PROTO)))
assert not left, left
print('PASS: 运营方清零（F01 批4 / 客商管理口径注记保留）')
