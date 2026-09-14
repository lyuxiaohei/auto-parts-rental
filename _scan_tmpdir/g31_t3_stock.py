# -*- coding: utf-8 -*-
"""G31 T3：库位档案去库区只留仓库层 + 库存查询筛选增强 + 组合视图按 BOM 套数
D-102/111/112/113。纪律：读取-精确替换+assert；io.open(newline='')；标签配平自检。
"""
import io, re, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
Q = chr(39)

def rd(p):
    return io.open(os.path.join(ROOT, p), encoding='utf-8', newline='').read()

def wr(p, s):
    io.open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='').write(s)

# 仓库层映射（旧 area → 新 仓库）
AREA2WH = {'原料区 RA': '正品仓', '成品区 RB': '正品仓', '安吉智行·转租终端仓': '转租终端仓',
           '安吉智行·客户虚拟仓': '客户虚拟仓', '上海一号库': '上海一号库'}
# 库位指派（按新仓库层 coherence；无实体库位的行 loc='—'）
LOCS = {'RA-A-01-01': ['RA-A-01-01', 'RA-A-01-02', 'RB-A-01-01', 'RB-A-01-02']}

def t3_demo_data():
    p = '_data/demo-data.js'
    s = rd(p)
    # ---- locations：逐行手术（保留 title/info/chain，只改 row 行 + info 的仓库/库区标签）----
    WHMAP = {'XNC-AJZX': '客户虚拟仓（安吉智行）', 'RC-01': '次品仓', 'RC-02': '次品仓'}
    def wh_of(key):
        return WHMAP.get(key, '正品仓')
    i = s.find('  locations: {')
    j = s.find('  bomVersions', i)
    seg = s[i:j]
    keys = [k for k in re.findall(r"^[ ]{2,6}'([^']+)': \{", seg, re.M) if k != 'row']
    assert len(keys) == 11, keys
    for key in keys:
        # 定位该键块
        ki = seg.find("'" + key + "': {")
        nk = re.search(r"^     '[^']+': \{", seg[ki + 10:], re.M)
        kend = ki + 10 + nk.start() if nk else len(seg)
        block = seg[ki:kend]
        # 1) 替换 'row': {...}, 单行（保留原 ops）
        rm = re.search(r"'row': (\{.*?\}),\r\n", block)
        assert rm, 'row line ' + key
        row_src = rm.group(1)
        om = re.search(r'"ops": \[.*\]', row_src)
        ops = om.group(0) if om else '[]'
        fm = re.search(r'"fields": \{(.*?)\}, "cells"', row_src)
        f = dict(re.findall(r'"(\w+)": "([^"]*)"', fm.group(1)))
        wh = wh_of(key)
        tag = 'tag-green' if f['status'] == '启用' else 'tag-gray'
        cells = '["%s", "%s", "%s", "%s", "<span class=\\"%s\\">%s</span>"]' % (wh, f['ltype'], f['spec'], f['usage'], tag, f['status'])
        new_row = ('{"fields": {"wh": "%s", "ltype": "%s", "spec": "%s", "usage": "%s", "status": "%s"}, '
                   '"cells": %s, %s}' % (wh, f['ltype'], f['spec'], f['usage'], f['status'], cells, ops))
        block = block.replace(rm.group(1), new_row, 1)
        # 2) info：仓库 text 换新值；库区 条目删除
        bm = re.search(r"('label': '仓库',\r\n          'text': ')[^']*'", block)
        assert bm, 'info 仓库 ' + key
        block = block[:bm.start()] + bm.group(1) + wh + "'" + block[bm.end():]
        am = re.search(r"\{\r\n          'label': '库区',\r\n          'text': '[^']*'\r\n        \},\r\n", block)
        assert am, 'info 库区 ' + key
        block = block[:am.start()] + block[am.end():]
        seg = seg[:ki] + block + seg[kend:]
    s = s[:i] + seg + s[j:]
    # ---- stockFlows：area→仓库层（fields + 末位 cell）+ 新增 loc ----
    i = s.find('  stockFlows: {')
    j = s.find('  rentTracks', i)
    seg = s[i:j]
    n_area = 0
    if seg.count('"area": "原料区 RA"') == 0 and seg.count('"loc"') == 14:
        n_area = 14  # 幂等：前次执行已完成转换
        print('stockFlows: 已是终态（幂等跳过）')
    else:
        for a, wh in AREA2WH.items():
            ca = '"area": "%s"' % a
            cw = '"area": "%s"' % wh
            n = seg.count(ca)
            assert n == {'原料区 RA': 5, '成品区 RB': 4, '安吉智行·转租终端仓': 3,
                         '安吉智行·客户虚拟仓': 1, '上海一号库': 1}[a], (a, n)
            seg = seg.replace(ca, cw)
            seg = seg.replace('"%s"' % a, '"%s"' % wh)
            n_area += n
    def add_loc(m):
        wh = m.group(1)
        pool = {'正品仓': ['RA-A-01-01', 'RA-A-01-02', 'RB-A-01-01', 'RB-A-01-02'],
                '客户虚拟仓': ['XNC-AJZX'], '转租终端仓': ['—'], '上海一号库': ['—']}
        seq = pool[wh]
        add_loc.k = getattr(add_loc, 'k', {})
        idx = add_loc.k.get(wh, 0)
        add_loc.k[wh] = idx + 1
        return '"area": "%s", "loc": "%s"' % (wh, seq[idx % len(seq)])
    seg = re.sub(r'"area": "([^"]+)"', add_loc, seg)
    s = s[:i] + seg + s[j:]
    wr(p, s)
    print('demo-data: locations 11 行仓库层收敛 + stockFlows area %d 处/loc 14 行 OK' % n_area)
    # ---- stockFlows：area→仓库层（fields + 末位 cell）+ 新增 loc ----
    i = s.find('  stockFlows: {')
    j = s.find('  rentTracks', i)
    seg = s[i:j]
    n_area = 0
    for a, wh in AREA2WH.items():
        ca = '"area": "%s"' % a
        cw = '"area": "%s"' % wh
        n = seg.count(ca)
        assert n == {'原料区 RA': 5, '成品区 RB': 4, '安吉智行·转租终端仓': 3,
                     '安吉智行·客户虚拟仓': 1, '上海一号库': 1}[a], (a, n)
        seg = seg.replace(ca, cw)
        # cells 末位（库区列文本）：'"原料区 RA"' 裸串
        seg = seg.replace('"%s"' % a, '"%s"' % wh)
        n_area += n
    # 新增 loc：按行插入 fields（wh 后）
    def add_loc(m):
        wh = m.group(1)
        pool = {'正品仓': ['RA-A-01-01', 'RA-A-01-02', 'RB-A-01-01', 'RB-A-01-02'],
                '客户虚拟仓': ['XNC-AJZX'], '转租终端仓': ['—'], '上海一号库': ['—']}
        seq = pool[wh]
        add_loc.k = getattr(add_loc, 'k', {})
        idx = add_loc.k.get(wh, 0)
        add_loc.k[wh] = idx + 1
        return '"area": "%s", "loc": "%s"' % (wh, seq[idx % len(seq)])
    seg = re.sub(r'"area": "([^"]+)"', add_loc, seg)
    s = s[:i] + seg + s[j:]
    wr(p, s)
    print('demo-data: locations 11 行仓库层收敛 + stockFlows area %d 处/loc 14 行 OK' % n_area)

def t3_location_page():
    p = '基础数据/库位档案.html'
    s = rd(p)
    # 1) 筛选卡：库房+库区 两个 ff → 一个 仓库 ff
    m = re.search(r'<div class="ff"><span class="ff-label">库房：</span>.*?</div>\s*<div class="ff"><span class="ff-label">库区：</span>.*?</div>', s, re.S)
    assert m, 'filter 库房+库区 ff not found'
    NEWFF = ('<div class="ff"><span class="ff-label">仓库：</span>\r\n'
             '      <select><option selected>全部</option><option>正品仓</option><option>次品仓</option><option>客户虚拟仓（安吉智行）</option></select>\r\n'
             '      <svg class="ff-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\r\n'
             '    </div>')
    s = s.replace(m.group(0), NEWFF, 1)
    # 2) thead：库房→仓库、删库区 th
    old_th = '<th></th>\r\n          <th>库房</th>\r\n          <th>库区</th>\r\n          <th>库位编码</th>'
    assert s.count(old_th) == 1, 'thead anchor'
    s = s.replace(old_th, '<th></th>\r\n          <th>仓库</th>\r\n          <th>库位编码</th>', 1)
    # 3) renderListPage filters
    old_f = "{ label: '库房', field: 'wh' },\r\n    { label: '库区', field: 'area' },"
    if old_f not in s:
        old_f = old_f.replace('\r\n', '\n')
    assert old_f in s, 'renderListPage filters anchor'
    s = s.replace(old_f, "{ label: '仓库', field: 'wh' },", 1)
    # 4) createModal：库房+库区 两行 → 仓库一行
    m2 = re.search(r'<div class="form-row">\s*<span class="form-label"><span class="req">\*</span>库房</span>.*?<div class="form-row">\s*<span class="form-label">库区</span>.*?</div>\s*</div>', s, re.S)
    assert m2, 'createModal 库房/库区 rows not found'
    NEWROW = ('<div class="form-row">\r\n    <span class="form-label"><span class="req">*</span>仓库</span>\r\n'
              '    <div class="input-box select-box"><select style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option selected>正品仓</option><option>次品仓</option><option>客户虚拟仓（安吉智行）</option></select><span class="caret"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>\r\n'
              '  </div>')
    s = s.replace(m2.group(0), NEWROW, 1)
    # 5) stopModal dlabel 库区→仓库
    s = s.replace('<div class="dlabel">库区</div><div class="dval">原料区 RA · 华东中心仓</div>',
                  '<div class="dlabel">仓库</div><div class="dval">正品仓 · 华东中心仓（WH-01）</div>', 1)
    # 6) 静态 tbody 11 行重写
    rows = [
        ('客户虚拟仓（安吉智行）', 'XNC-AJZX', '虚拟仓', '按客户归集', 'on-hire 640 只', 'tag-green', '启用'),
        ('正品仓', 'RA-A-01-01', '存储位', '1.2m×1.0m / 2t', '68%', 'tag-green', '启用'),
        ('正品仓', 'RA-A-01-02', '存储位', '1.2m×1.0m / 2t', '45%', 'tag-green', '启用'),
        ('正品仓', 'RA-B-02-01', '存储位', '1.2m×1.0m / 2t', '0%', 'tag-green', '启用'),
        ('正品仓', 'RB-A-01-01', '存储位', '1.2m×1.0m / 2t', '82%', 'tag-green', '启用'),
        ('正品仓', 'RB-A-01-02', '存储位', '1.2m×1.0m / 2t', '74%', 'tag-green', '启用'),
        ('正品仓', 'RB-B-01-01', '拣选位', '1.2m×1.0m / 1.5t', '60%', 'tag-green', '启用'),
        ('正品仓', 'RD-01', '组装暂存', '工位 1', '组装中', 'tag-green', '启用'),
        ('正品仓', 'RD-02', '组装暂存', '工位 2', '空闲', 'tag-green', '启用'),
        ('次品仓', 'RC-01', '退货暂存', '1.2m×1.0m / 2t', '36%', 'tag-green', '启用'),
        ('次品仓', 'RC-02', '退货暂存', '1.2m×1.0m / 2t', '0%', 'tag-gray', '停用'),
    ]
    m3 = re.search(r'<tbody>(.*?)</tbody>', s, re.S)
    assert m3 and m3.group(1).count('<tr>') == 11, 'static tbody'
    trs = []
    TR = ('<tr>
          <td><input type="checkbox" class="cb"></td>
'
          '          <td>%s</td>
          <td><span class="lk">%s</span></td>
'
          '          <td>%s</td>
          <td>%s</td>
          <td>%s</td>
'
          '          <td><span class="%s">%s</span></td>
'
          '          <td class="sticky-op"><span class="ops"><a onclick="openModal('detailModal')">详情</a><a onclick="openModal('createModal')">编辑</a><a onclick="openModal('stopModal')">停用</a></span></td>
        </tr>')
    for wh, code, lt, spec, usage, tag, st in rows:
        trs.append(TR % (wh, code, lt, spec, usage, tag, st))
        s = s.replace(m3.group(0), '<tbody>\r\n' + '\r\n'.join(trs) + '\r\n      </tbody>', 1)
    # 标签配平
    assert len(re.findall(r'<th[>\s]', s)) == len(re.findall(r'</th>', s))
    wr(p, s)
    print('库位档案.html: 筛选/表头/表单/详情注记/静态行 仓库层收敛 OK')

def t3_location_modal():
    p = '基础数据/弹窗/新建库位.html'
    s = rd(p)
    m = re.search(r'<div class="form-row">\s*<span class="form-label"><span class="req">\*</span>库房</span>.*?<div class="form-row">\s*<span class="form-label">库区</span>.*?</div>\s*</div>', s, re.S)
    if not m:
        m = re.search(r'<div class="form-row">\s*<span class="form-label">库区</span>.*?</div>\s*</div>', s, re.S)
        assert m, '新建库位 库区 row not found'
        NEWROW = ('<div class="form-row">\r\n    <span class="form-label">仓库</span>\r\n'
                  '    <div class="input-box select-box"><select style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option selected>正品仓</option><option>次品仓</option><option>客户虚拟仓（安吉智行）</option></select><span class="caret"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>\r\n  </div>')
        s = s.replace(m.group(0), NEWROW, 1)
    else:
        NEWROW = ('<div class="form-row">\r\n    <span class="form-label"><span class="req">*</span>仓库</span>\r\n'
                  '    <div class="input-box select-box"><select style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option selected>正品仓</option><option>次品仓</option><option>客户虚拟仓（安吉智行）</option></select><span class="caret"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>\r\n  </div>')
        s = s.replace(m.group(0), NEWROW, 1)
    # 库房 select 若仍独立存在（首行），改标签为仓库
    s = re.sub(r'(<span class="req">\*</span>)库房</span>', r'\1仓库</span>', s)
    wr(p, s)
    print('弹窗/新建库位.html: 表单仓库层收敛 OK')

def t3_stock_page():
    p = '仓储作业/库存查询.html'
    s = rd(p)
    # 1) 散件 thead 库区→仓库
    old = '<th>库区</th>'
    assert s.count(old) == 1, s.count(old)
    s = s.replace(old, '<th>仓库</th>', 1)
    # 2) 筛选卡：库存状态 ff 后追加 4 个 ff（仓库/库位/物料名称/项目）
    m = re.search(r'(<div class="ff"><span class="ff-label">库存状态：</span>.*?</div>)\s*(<div class="filter-actions">)', s, re.S)
    assert m, '库存状态 ff anchor'
    ADDFF = (m.group(1) + '\r\n    ' +
             '<div class="ff"><span class="ff-label">仓库：</span>\r\n'
             '      <select><option selected>全部</option><option>正品仓</option><option>次品仓</option><option>客户虚拟仓</option><option>转租终端仓</option><option>上海一号库</option></select>\r\n'
             '      <svg class="ff-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\r\n'
             '    </div>\r\n    '
             '<div class="ff"><span class="ff-label">库位：</span>\r\n'
             '      <select><option selected>全部</option><option>RA-A-01-01</option><option>RA-A-01-02</option><option>RB-A-01-01</option><option>RB-A-01-02</option><option>XNC-AJZX</option></select>\r\n'
             '      <svg class="ff-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\r\n'
             '    </div>\r\n    '
             '<div class="ff"><span class="ff-label">物料名称：</span><input placeholder="请输入物料名称"></div>\r\n    '
             '<div class="ff"><span class="ff-label">项目：</span>\r\n'
             '      <select><option selected>全部</option><option>PRJ-2601</option><option>PRJ-2602</option><option>PRJ-2603</option><option>PRJ-2604</option><option>PRJ-2605</option></select>\r\n'
             '      <svg class="ff-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\r\n'
             '    </div>\r\n    ')
    s = s.replace(m.group(0), ADDFF + m.group(2), 1)
    # 3) renderListPage filters 增 4 项
    old_f = "filters: [\r\n    { label: '物料编码', field: '_key' },\r\n    { label: '库存状态', field: 'status' }\r\n  ],"
    if old_f not in s:
        old_f = old_f.replace('\r\n', '\n')
    assert old_f in s, 'stock filters anchor'
    new_f = old_f.replace("    { label: '库存状态', field: 'status' }\r\n  ],",
                          "    { label: '库存状态', field: 'status' },\r\n    { label: '仓库', field: 'area' },\r\n    { label: '库位', field: 'loc' },\r\n    { label: '物料名称', field: 'name' },\r\n    { label: '项目', field: 'project', match: 'contains' }\r\n  ],")
    s = s.replace(old_f, new_f, 1)
    # 4) comboView → BOM 套数视图
    i = s.find('<div id="comboView">')
    pstart = s.find('<div class="pager">', i)
    pend = s.find('</div>', s.find('跳转页码', pstart)) + len('</div>')
    assert i > 0 and pstart > i and pend > pstart, 'comboView bounds'
    NEWCOMBO = '''<div id="comboView">
  <div style="display:flex;align-items:center;gap:12px;margin:0 0 12px;flex-wrap:wrap;">
    <span style="font-size:13px;color:#4b5563;">选用 BOM：</span>
    <div class="input-box select-box" style="width:360px"><select id="comboBomSel" onchange="renderComboBom(this.value)" style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option value="ZH-2601-A">ZH-2601-A 驾驶室围板箱整箱套件 · V2.1</option><option value="ZH-2602-B">ZH-2602-B 保险杠料架套件 · V1.3</option><option value="ZH-2603-C">ZH-2603-C 电池托盘护角套件 · V1.0</option></select><span class="caret"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
    <span id="comboBomSum" style="font-size:13px;font-weight:600;color:#1677ff;"></span>
  </div>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>BOM 编码</th>
          <th>子件</th>
          <th>来源</th>
          <th>单位用量</th>
          <th>在库可用</th>
          <th>可组成（该子件计）</th>
        </tr>
      </thead>
      <tbody id="comboBomBody"></tbody>
    </table>
  </div>
  <div style="font-size:12px;color:#8c8c8c;margin-top:8px;">可组成套数 = 各子件「在库可用 ÷ 单位用量」取最小值（按在库量测算 · D-111）；跨 BOM 并行汇总不做（D-45 挂起）。</div>
  '''
    s = s[:i] + NEWCOMBO + s[pend:]
    # 5) BOM 数据+渲染 JS：挂到 switchView 脚本块尾
    js_anchor = "function switchView(v) {"
    assert js_anchor in s
    JS = '''/* G31 T3 组合视角：按选 BOM 显示可组成套数（D-111） */
var BOM_COMBOS = {
  'ZH-2601-A': [ ['围板箱 1200×1000×970','租入',1,320], ['围板 LJ-C300','自购',4,1860], ['箱盖','自购',1,900], ['锁扣组件 LJ-A100','自购',4,5260], ['铰链 LJ-B200','自购',2,2640] ],
  'ZH-2602-B': [ ['料架 1300×600','租入',1,180], ['支撑臂','自购',2,640], ['锁扣组件 LJ-A100','自购',2,5260] ],
  'ZH-2603-C': [ ['周转箱 600×400','租入',1,410], ['内衬','自购',4,2200], ['绑带','自购',2,1580], ['锁扣组件 LJ-A100','自购',4,5260], ['铰链 LJ-B200','自购',2,2640], ['标签','自购',1,99999] ]
};
function renderComboBom(key) {
  var rows = BOM_COMBOS[key] || [];
  var minSets = null;
  var html = rows.map(function (r) {
    var sets = Math.floor(r[3] / r[2]);
    if (minSets === null || sets < minSets) minSets = sets;
    return '<tr><td>' + key + '</td><td>' + r[0] + '</td><td><span class="tag ' + (r[1] === '租入' ? 'tag-orange' : 'tag-gray') + '">' + r[1] + '</span></td><td><span class="td-num">' + r[2] + '</span></td><td><span class="td-num">' + r[3].toLocaleString() + '</span></td><td><span class="td-num"><b>' + sets + ' 套</b></span></td></tr>';
  }).join('\\n');
  document.getElementById('comboBomBody').innerHTML = html;
  document.getElementById('comboBomSum').textContent = key + ' 可组成 ' + (minSets || 0) + ' 套';
}
renderComboBom('ZH-2601-A');
'''
    k = s.find('</script>', s.find(js_anchor))
    s = s[:k] + JS + s[k:]
    # 配平
    assert len(re.findall(r'<th[>\s]', s)) == len(re.findall(r'</th>', s))
    assert s.count('<tbody') == s.count('</tbody>')
    wr(p, s)
    print('库存查询.html: thead 仓库 + 筛选×4 + 组合视角 BOM 套数 OK')

if __name__ == '__main__':
    t3_demo_data()
    t3_location_page()
    t3_location_modal()
    t3_stock_page()
    print('T3 全部替换完成')
