# -*- coding: utf-8 -*-
"""批2 Script D：客商去运营商 + 用户权限六角色 + 审核人（主管角色）行 + 客户虚拟仓 + 全站运营方→供应商（F01 除外）"""
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
# 1. demo-data：partners DW-0201 运营方→供应商
# ============================================================
DD = PROTO / "_data" / "demo-data.js"
src = DD.read_bytes().decode('utf-8')
src = rep(src, '"type": "运营方"', '"type": "供应商"', 1, 'DW-0201 type')
src = rep(src, '<span class=\\"tag tag-orange\\">运营方</span>', '<span class=\\"tag tag-blue\\">供应商</span>', 1, 'DW-0201 cell')
src = rep(src, "'label': '客商类型',\n          'text': '运营方'", "'label': '客商类型',\n          'text': '供应商'", 1, 'DW-0201 info')

# ============================================================
# 2. demo-data：locations 加客户虚拟仓（安吉智行）
# ============================================================
VROW = ("    'XNC-AJZX': {\n"
        "      'row': {\"fields\": {\"wh\": \"华东中心仓（WH-01）\", \"area\": \"客户虚拟仓\", \"ltype\": \"虚拟仓\", \"spec\": \"按客户归集\", \"usage\": \"on-hire 640 只\", \"status\": \"启用\"}, \"cells\": [\"客户虚拟仓（安吉智行）\", \"<span class=\\\"lk\\\">XNC-AJZX</span>\", \"虚拟仓\", \"按客户归集\", \"on-hire 640 只\", \"<span class=\\\"tag tag-blue\\\">启用</span>\"], \"ops\": [{\"t\": \"详情\", \"detail\": true}, {\"t\": \"编辑\", \"act\": \"openModal('createModal')\"}]},\n"
        "      'title': '库位详情',\n"
        "      'info': [\n"
        "        {\n          'label': '仓库',\n          'text': '华东中心仓（WH-01）· 虚拟',\n          'full': true\n        },\n"
        "        {\n          'label': '库区',\n          'text': '客户虚拟仓'\n        },\n"
        "        {\n          'label': '库位编码',\n          'text': 'XNC-AJZX'\n        },\n"
        "        {\n          'label': '库位类型',\n          'text': '虚拟仓'\n        },\n"
        "        {\n          'label': '归集口径',\n          'text': '在客户处的租赁资产按客户归集（on-hire）；客户转租为其子状态',\n          'full': true\n        },\n"
        "        {\n          'label': '容量占用',\n          'text': 'on-hire 640 只（围板箱）'\n        },\n"
        "        {\n          'label': '状态',\n          'tag': '启用'\n        }\n"
        "      ],\n"
        "      'chain': [\n"
        "        {\n          'role': '租赁单',\n          'name': 'ZL-20260823-033',\n          'url': '租赁管理/租赁单列表.html'\n        },\n"
        "        {\n          'role': '组合出库',\n          'name': 'CK-20260824-009',\n          'url': '租赁管理/组合出库列表.html'\n        },\n"
        "        {\n          'role': '客户虚拟仓（本仓）',\n          'name': 'XNC-AJZX · 安吉智行',\n          'self': true\n        }\n"
        "      ],\n"
        "      'timeline': [\n"
        "        {\n          't': '09-02',\n          'text': '组合出库 640 只至安吉智行 · 记客户虚拟仓（on-hire）',\n          'who': '张伟'\n        },\n"
        "        {\n          't': '当前',\n          'text': '虚拟仓在库 640 只 · 支撑按客户对账/盘点核对'\n        }\n"
        "      ]\n"
        "    },\n")
ps, pe = None, None
m = re.search(r'^  locations: \{', src, re.M)
assert m
first_rec = re.search(r"^    '", src[m.end():], re.M)
ins = m.end() + 1 + first_rec.start()
src = src[:ins] + VROW + src[ins:]
LOG.append('locations +XNC-AJZX 客户虚拟仓')

# ============================================================
# 3. demo-data：stockFlows 加客户虚拟仓维度行
# ============================================================
SROW_KEY = "    'XNC-AJZX-WBX': {\n"
SROW = (SROW_KEY +
        "      'row': {\"fields\": {\"name\": \"围板箱 1200×1000×970（安吉智行·客户虚拟仓）\", \"cls\": \"租赁器具\", \"project\": \"PRJ-2605\", \"area\": \"安吉智行·客户虚拟仓\"}, \"cells\": [\"围板箱 1200×1000×970（安吉智行·客户虚拟仓）\", \"<span class=\\\"tag tag-blue\\\">租赁器具</span>\", \"PRJ-2605\", \"<span class=\\\"td-num\\\">0</span>\", \"<span class=\\\"td-num\\\">0</span>\", \"<span class=\\\"td-num\\\">640</span>\", \"<span class=\\\"td-num\\\">0</span>\", \"<span class=\\\"td-num\\\"><b>640</b></span>\", \"只\", \"安吉智行·客户虚拟仓\"], \"ops\": [{\"t\": \"库存流水\", \"detail\": true}]},\n"
        "      'title': '库存流水',\n"
        "      'titleNo': 'XNC-AJZX-WBX 围板箱（安吉智行·客户虚拟仓）',\n"
        "      'info': [\n"
        "        {\n          'label': '物料编码',\n          'text': 'XNC-AJZX-WBX'\n        },\n"
        "        {\n          'label': '名称规格',\n          'text': '围板箱 1200×1000×970（安吉智行·客户虚拟仓）',\n          'full': true\n        },\n"
        "        {\n          'label': '物料类别',\n          'text': '租赁器具'\n        },\n"
        "        {\n          'label': '适用项目',\n          'text': 'PRJ-2605',\n          'full': true\n        },\n"
        "        {\n          'label': '在库',\n          'text': '0（虚拟仓不占实体库）'\n        },\n"
        "        {\n          'label': '客户端（on-hire）',\n          'text': '640 只'\n        },\n"
        "        {\n          'label': '口径',\n          'text': '客户虚拟仓＝在客户处的租赁资产按客户归集（on-hire）；客户转租为其子状态',\n          'full': true\n        },\n"
        "        {\n          'label': '库区',\n          'text': '安吉智行·客户虚拟仓'\n        }\n"
        "      ],\n"
        "      'feeSecTitle': '进出流水（时间倒序）',\n"
        "      'feeCols': ['日期', '类型', '单据号', '方向数量', '结存'],\n"
        "      'fees': [\n"
        "        {\n          'cells': ['09-02', '组合出库', 'CK-20260824-009', '+640', '640'],\n          'links': {\n            2: '租赁管理/组合出库列表.html'\n          }\n        }\n"
        "      ],\n"
        "      'chain': [\n"
        "        {\n          'role': '租赁单',\n          'name': 'ZL-20260823-033',\n          'url': '租赁管理/租赁单列表.html'\n        },\n"
        "        {\n          'role': '组合出库',\n          'name': 'CK-20260824-009 · 出库至客户',\n          'url': '租赁管理/组合出库列表.html'\n        },\n"
        "        {\n          'role': '客户虚拟仓（本仓）',\n          'name': 'XNC-AJZX · on-hire 640 只',\n          'self': true\n        }\n"
        "      ],\n"
        "      'timeline': [\n"
        "        {\n          't': '09-02',\n          'text': '组合出库 640 只至安吉智行 · 按客户归集记客户虚拟仓（on-hire）',\n          'who': '张伟'\n"
        "        }\n"
        "      ]\n"
        "    },\n")
m2 = re.search(r'^  stockFlows: \{', src, re.M)
assert m2
first_rec2 = re.search(r"^    '", src[m2.end():], re.M)
ins2 = m2.end() + 1 + first_rec2.start()
src = src[:ins2] + SROW + src[ins2:]
LOG.append('stockFlows +XNC-AJZX-WBX 客户虚拟仓维度行')

# ============================================================
# 4. demo-data：全局 运营方→供应商（L6）
# ============================================================
n_op = src.count('运营方')
src = src.replace('运营方', '供应商')
LOG.append(f'demo-data 运营方→供应商 {n_op} 处')

DD.write_bytes(src.encode('utf-8'))
import subprocess
r = subprocess.run(['node', '--check', str(DD)], capture_output=True, text=True)
assert r.returncode == 0, 'node --check: ' + r.stderr[:300]
LOG.append('node --check OK')

# ============================================================
# 5. 客商管理.html：筛选选项/页签删运营方、示例行改供应商、pin 文案
# ============================================================
KM = PROTO / "基础数据" / "客商管理.html"
txt = KM.read_bytes().decode('utf-8')
nl = '\r\n' if '\r\n' in txt else '\n'
txt = rep(txt, '<option>供应商</option><option>运营方</option>', '<option>供应商</option>', 2, '客商筛选选项')
txt = rep(txt, '  <span class="stab">供应商<span class="stab-count">21</span></span>' + nl +
              '  <span class="stab">运营方<span class="stab-count">5</span></span>' + nl,
          '  <span class="stab">供应商<span class="stab-count">22</span></span>' + nl, 1, '客商页签')
txt = rep(txt, '<td><span class="tag tag-orange">运营方</span></td>', '<td><span class="tag tag-blue">供应商</span></td>', 1, '客商静态行')
txt = rep(txt, '客户/供应商/运营方三类主体，含开票资料（开票主体信息待确认）', '客户/供应商两类主体（运营方角色已去掉，2026-09-08 会议 L6），含开票资料', 1, '客商pin')
txt = rep(txt, '<b>FP1-02 客商管理</b>：客户/供应商/运营方三类，联系人、开票资料', '<b>FP1-02 客商管理</b>：客户/供应商两类（原三类·运营方去掉），联系人、开票资料', 1, '客商pin src')
txt = rep(txt, '客商角色仅 2 种：客户、供应商', '客商角色仅 2 种：客户、供应商', 0, 'noop')
KM.write_bytes(txt.encode('utf-8'))
LOG.append('客商管理.html 去运营方完成')

# ============================================================
# 6. 用户权限.html：六角色重排
# ============================================================
UP = PROTO / "系统管理" / "用户权限.html"
txt = UP.read_bytes().decode('utf-8')
nl = '\r\n' if '\r\n' in txt else '\n'

# 6.1 筛选下拉
txt = rep(txt, '<select><option selected>全部</option><option>系统管理员</option><option>项目经理</option><option>仓储主管</option><option>财务</option><option>客户账号</option></select>',
          '<select><option selected>全部</option><option>系统管理员</option><option>财务</option><option>商务</option><option>物流</option><option>财务主管</option><option>商务主管</option><option>物流主管</option><option>客户账号</option><option>供应商账号</option></select>', 1, '角色筛选')
txt = rep(txt, '<option>我方</option><option>客户</option><option>运营方</option>', '<option>我方</option><option>客户</option><option>供应商</option>', 2, '所属方筛选')
txt = rep(txt, '<option>全部用户</option><option>我方</option><option>客户</option><option>运营方</option>', '<option>全部用户</option><option>我方</option><option>客户</option><option>供应商</option>', 1, '状态筛选')

# 6.2 页签
txt = rep(txt, '<span class="stab active">全部用户<span class="stab-count">24</span></span>' + nl +
              '  <span class="stab">我方<span class="stab-count">14</span></span>' + nl +
              '  <span class="stab">客户<span class="stab-count">7</span></span>' + nl +
              '  <span class="stab">运营方<span class="stab-count">3</span></span>',
          '<span class="stab active">全部用户<span class="stab-count">18</span></span>' + nl +
          '  <span class="stab">我方<span class="stab-count">8</span></span>' + nl +
          '  <span class="stab">客户<span class="stab-count">7</span></span>' + nl +
          '  <span class="stab">供应商<span class="stab-count">3</span></span>', 1, '页签')

# 6.3 表体重写（11 行：2 管理员 + 六角色 + 2 客户 + 1 供应商）
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

# 6.4 角色管理弹窗表
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
old_rr_s = txt.find('            <tr><td><b>系统管理员</b></td>')
old_rr_e = txt.find('            </tbody>', old_rr_s)
assert old_rr_s > -1 and old_rr_e > old_rr_s
txt = txt[:old_rr_s] + rr + txt[old_rr_e:]

# 6.5 pin 文案
txt = rep(txt, '我方/客户/运营方三类账号体系——客户账号由项目经理代下单时使用', '我方（财务/商务/物流三线 + 各主管）+ 客户 + 供应商账号；审核按角色配置（财务/商务/物流三类主管，2026-09-08 会议 D4）', 1, '权限pin')
UP.write_bytes(txt.encode('utf-8'))
LOG.append('用户权限.html 六角色重排完成（11 行示例 + 角色表 9 行）')

# ============================================================
# 7. 审核类弹窗加「审核人（按角色配置）」行（30 文件·双层）
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
        # 统一为 \n 处理后按原行尾写回
        norm = txt.replace('\r\n', '\n')
        matches = pat_ins.findall(norm)
        assert len(matches) == 1, f'{rel} 提交人行 {len(matches)}'
        ins_line = matches[0][0] + '<div class="drow"><div class="dlabel">审核人（按角色配置）</div><div class="dval">' + role + '</div></div>\n'
        norm = pat_ins.sub(lambda m: m.group(0) + ins_line, norm, count=1)
        if nl == '\r\n':
            norm = norm.replace('\n', '\r\n')
        f.write_bytes(norm.encode('utf-8'))
        tot += 1
LOG.append(f'审核弹窗加审核人行 {tot} 文件')

# ============================================================
# 8. 库存查询：虚拟仓口径注记 + 静态示例行
# ============================================================
SQ = PROTO / "仓储作业" / "库存查询.html"
txt = SQ.read_bytes().decode('utf-8')
nl = '\r\n' if '\r\n' in txt else '\n'
# 8.1 主表静态行（tbody 第一行前加客户虚拟仓行）
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
c = txt.count(anchor)
assert c >= 1, c
txt = txt.replace(anchor, anchor + nl + hint_row, 1)
# 8.2 口径注记（五态卡注记后追加）
pat_hint = re.compile(r'(<div class="pn-hint"[^>]*>[^<]*在途[^<]*</div>)')
m3 = pat_hint.search(txt)
if m3:
    txt = txt.replace(m3.group(1), m3.group(1) + nl +
        '<div class="pn-hint">客户虚拟仓＝在客户处的租赁资产按客户归集（on-hire）；客户转租为其子状态（2026-09-08 会议 T1 方向）。</div>', 1)
    LOG.append('库存查询 虚拟仓口径注记 追加 1')
else:
    # 无既有注记则挂在五态卡 grid 后
    grid_end = txt.find('</div>', txt.find('class="stat-grid"'))
    assert grid_end > -1
    txt = txt[:grid_end + 6] + nl + '<div class="pn-hint">客户虚拟仓＝在客户处的租赁资产按客户归集（on-hire）；客户转租为其子状态（2026-09-08 会议 T1 方向）。</div>' + txt[grid_end + 6:]
    LOG.append('库存查询 虚拟仓口径注记 新建 1')
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
# 10. 全站 HTML 运营方→供应商（F01 除外）
# ============================================================
n_html = 0
for f in sorted(PROTO.rglob('*.html')):
    if f.name.startswith('P3-R01-F01'):
        continue
    raw = f.read_bytes()
    t = raw.decode('utf-8')
    c = t.count('运营方')
    if c:
        t = t.replace('运营方', '供应商')
        f.write_bytes(t.encode('utf-8'))
        n_html += c
LOG.append(f'HTML 运营方→供应商 {n_html} 处（F01 除外，批4 处理）')

print('== 批2 Script D ==')
for l in LOG:
    print(' ✓', l)

# 校验
left = []
for f in sorted(PROTO.rglob('*.html')):
    if f.name.startswith('P3-R01-F01'):
        continue
    if '运营方' in f.read_bytes().decode('utf-8'):
        left.append(str(f.relative_to(PROTO)))
assert not left, left
dd = DD.read_bytes().decode('utf-8')
assert '运营方' not in dd
print('PASS: 运营方清零（F01 除外）')
