# -*- coding: utf-8 -*-
"""G31 T6 压轴（D-105/117·D-122 红线内）：
① 租入入库确认弹窗（双层）+「立即转租」勾选（登记同时生成租赁出库单·自动带物料）
② 租入单新建（双层）租期两层：起租日期（单输入·去结束日期）+ 合同起止（框架）
③ comboOutbounds +1 溯源行（立即转租生成·供应商直发）
红线核对：不动计费方式/单价/租金字段（含 demo-data 计费键）。"""
import io, re, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
Q = chr(39)

def rd(p):
    return io.open(os.path.join(ROOT, p), encoding='utf-8', newline='').read()

def wr(p, s):
    io.open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='').write(s)

ZZROW = ('<div class="form-row">' + chr(13) + chr(10) +
         '    <span class="form-label">立即转租</span>' + chr(13) + chr(10) +
         '    <div><label style="display:flex;align-items:center;gap:8px;cursor:pointer;"><input type="checkbox" class="cb"><span>供应商直发终端客户——登记同时自动生成租赁出库单（自动带物料 · 免重复填单）</span></label>' + chr(13) + chr(10) +
         '      <div style="font-size:12px;color:#8c8c8c;margin-top:4px;">背靠背转租（D-105）：租赁出库列表可查该单；库存侧「转租登记」入口保留不变（D-78）；计费口径不受影响（D-122 梳理中）。</div></div>' + chr(13) + chr(10) +
         '  </div>')

def add_zz(p):
    s = rd(p)
    if '立即转租' in s:
        print(p, '已加（幂等）'); return
    NL = chr(13) + chr(10) if chr(13) + chr(10) in s else chr(10)
    row = ZZROW.replace(chr(13) + chr(10), NL)
    # 锚：审核结论 form-row 前
    m = re.search(r'<div class="form-row">\s*<span class="form-label"><span class="req">\*</span>审核结论</span>', s)
    assert m, '审核结论 anchor ' + p
    s = s[:m.start()] + row + NL + '  ' + s[m.start():]
    wr(p, s)
    print(p, ': +立即转租勾选 OK')

LEASE_NEW = ('<div class="form-row">' + chr(13) + chr(10) +
             '    <span class="form-label"><span class="req">*</span>起租日期</span>' + chr(13) + chr(10) +
             '    <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;"><div class="input-box" style="width:170px"><input placeholder="开始日期"></div><span style="font-size:12px;color:#8c8c8c;">单据起止只填开始时间，结束日期不填（D-117 两层租期）</span></div>' + chr(13) + chr(10) +
             '  </div><div class="form-row">' + chr(13) + chr(10) +
             '    <span class="form-label">合同起止（框架）</span>' + chr(13) + chr(10) +
             '    <div style="display:flex;gap:10px"><div class="input-box" style="width:170px"><input placeholder="框架合同开始"></div><div class="input-box" style="width:170px"><input placeholder="框架合同结束"></div></div>' + chr(13) + chr(10) +
             '  </div>')

def two_layer(p):
    s = rd(p)
    if '起租日期' in s:
        print(p, '已改（幂等）'); return
    NL = chr(13) + chr(10) if chr(13) + chr(10) in s else chr(10)
    pat = re.compile(r'<div class="form-row">\s*<span class="form-label"><span class="req">\*</span>租期起止</span>.*?</div>\s*</div>\s*</div>', re.S)
    m = pat.search(s)
    assert m, '租期起止 row ' + p
    new = LEASE_NEW.replace(chr(13) + chr(10), NL)
    s = s.replace(m.group(0), new, 1)
    assert s.count('租期起止</span>') == 0 or p.endswith('列表.html'), '残留'
    wr(p, s)
    print(p, ': 租期两层（起租日期+合同起止框架）OK')

def combo_row():
    p = '_data/demo-data.js'
    s = rd(p)
    if 'CK-20260914-023' in s:
        print('comboOutbounds 溯源行已加（幂等）'); return
    NL = chr(13) + chr(10)
    m = re.search(r"'CK-20260910-022': \{[\s\S]*?\n    \},", s)
    assert m, 'CK-022 block'
    Q1 = chr(39)
    NEW = (NL + NL + "    'CK-20260914-023': {  /* G31 T6 立即转租溯源行（D-105·供应商直发） */" + NL +
           "      'row': {\"fields\": {\"project\": \"PRJ-2603\", \"customer\": \"上汽大众宁波分公司\", \"zl\": \"—（立即转租生成）\", \"combo\": \"塑料托盘 1200×1000 × 50 只\", \"so\": \"—（租赁出库·租入直发）\", \"addr\": \"宁波杭州湾基地\", \"status\": \"待审核\", \"date\": \"2026-09-14\"}, " +
           "\"cells\": [\"PRJ-2603\", \"上汽大众宁波分公司\", \"<span class=\\\"tag tag-orange\\\">租入直发（立即转租）</span>\", \"塑料托盘 1200×1000 × 50 只\", \"—（租赁出库·租入直发）\", \"宁波杭州湾基地\", \"<span class=\\\"tag tag-orange\\\">待审核</span>\", \"2026-09-14 10:05\"], " +
           "\"ops\": [{\"t\": \"详情\", \"detail\": true}, {\"t\": \"审核\", \"act\": \"openModal('exitConfirmModal')\"}]}," + NL +
           "      'title': '租赁出库单详情'," + NL +
           "      'info': [" + NL +
           "        {'label': '出库单号', 'text': 'CK-20260914-023', 'full': true}," + NL +
           "        {'label': '状态', 'tag': '待审核'}," + NL +
           "        {'label': '来源', 'text': '立即转租（租入入库登记时勾选·自动生成）', 'full': true}," + NL +
           "        {'label': '关联租入入库', 'text': 'RZRK-20260903-023', 'url': '租入管理/租入入库列表.html'}," + NL +
           "        {'label': '客户', 'text': '上汽大众宁波分公司', 'full': true}," + NL +
           "        {'label': '所属项目', 'text': 'PRJ-2603'}," + NL +
           "        {'label': '出库内容', 'text': '塑料托盘 1200×1000 × 50 只', 'full': true}," + NL +
           "        {'label': '出库仓库', 'text': '—（供应商直发·不经实物入库）'}," + NL +
           "        {'label': '送达地点', 'text': '宁波杭州湾基地'}," + NL +
           "        {'label': '出库日期', 'text': '2026-09-14'}" + NL +
           "      ]," + NL +
           "    },")
    s = s[:m.end()] + NEW + s[m.end():]
    wr(p, s)
    print('comboOutbounds: +CK-20260914-023 立即转租溯源行 OK')

if __name__ == '__main__':
    add_zz('租入管理/弹窗/租入入库确认.html')
    add_zz('租入管理/租入入库列表.html')
    two_layer('租入管理/弹窗/租入单新建.html')
    two_layer('租入管理/租入单列表.html')
    combo_row()
