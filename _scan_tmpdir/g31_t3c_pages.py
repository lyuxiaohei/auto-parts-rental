# -*- coding: utf-8 -*-
"""G31 T3c：三页面落地（库位档案/新建库位弹窗/库存查询）。demo-data 已终态，不再触碰。"""
import io, re, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
Q = chr(39)
CRLF = chr(13) + chr(10)
WH_OPTS = '<option selected>正品仓</option><option>次品仓</option><option>客户虚拟仓（安吉智行）</option>'
CARET = '<span class="caret"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>'
SELSTYLE = 'style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"'

def rd(p):
    return io.open(os.path.join(ROOT, p), encoding='utf-8', newline='').read()

def wr(p, s):
    io.open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='').write(s)

def location_page():
    p = '基础数据/库位档案.html'
    s = rd(p)
    if '<th>仓库</th>' in s and s.count('仓库：') > 0:
        print('库位档案 已是 v4 终态（幂等跳过）'); return
    # 1) 筛选卡：库房+库区 → 仓库
    m = re.search(r'<div class="ff"><span class="ff-label">库房：</span>.*?</div>\s*<div class="ff"><span class="ff-label">库区：</span>.*?</div>', s, re.S)
    assert m, 'filter ff'
    NEWFF = ('<div class="ff"><span class="ff-label">仓库：</span>' + CRLF +
             '      <select><option selected>全部</option><option>正品仓</option><option>次品仓</option><option>客户虚拟仓（安吉智行）</option></select>' + CRLF +
             '      <svg class="ff-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>' + CRLF +
             '    </div>')
    s = s.replace(m.group(0), NEWFF, 1)
    # 2) thead
    old_th = '<th></th>' + CRLF + '          <th>库房</th>' + CRLF + '          <th>库区</th>' + CRLF + '          <th>库位编码</th>'
    if old_th not in s:
        old_th = old_th.replace(CRLF, '\n')
    assert s.count(old_th) == 1, 'thead'
    s = s.replace(old_th, old_th.replace('<th>库房</th>' + CRLF[0], '<th>仓库</th>' + CRLF[0]).replace(CRLF + '          <th>库区</th>', ''), 1)
    # 3) renderListPage filters
    old_f = "{ label: '库房', field: 'wh' }," + CRLF + "    { label: '库区', field: 'area' },"
    if old_f not in s:
        old_f = old_f.replace(CRLF, '\n')
    assert old_f in s, 'filters'
    s = s.replace(old_f, "{ label: '仓库', field: 'wh' },", 1)
    # 4) createModal 两行→一行
    m2 = re.search(r'<div class="form-row">\s*<span class="form-label"><span class="req">\*</span>库房</span>.*?<div class="form-row">\s*<span class="form-label">库区</span>.*?</div>\s*</div>', s, re.S)
    assert m2, 'createModal rows'
    NEWROW = ('<div class="form-row">' + CRLF +
              '    <span class="form-label"><span class="req">*</span>仓库</span>' + CRLF +
              '    <div class="input-box select-box"><select ' + SELSTYLE + '>' + WH_OPTS + '</select>' + CARET + '</div>' + CRLF +
              '  </div>')
    s = s.replace(m2.group(0), NEWROW, 1)
    # 5) stopModal dlabel
    s = s.replace('<div class="dlabel">库区</div><div class="dval">原料区 RA · 华东中心仓</div>',
                  '<div class="dlabel">仓库</div><div class="dval">正品仓 · 华东中心仓（WH-01）</div>', 1)
    # 6) 静态 tbody 11 行重写（[cb] 仓库|编码|类型|规格|占用|状态|操作）
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
    TR = ('<tr>' + CRLF + '          <td><input type="checkbox" class="cb"></td>' + CRLF +
          '          <td>%s</td>' + CRLF + '          <td><span class="lk">%s</span></td>' + CRLF +
          '          <td>%s</td>' + CRLF + '          <td>%s</td>' + CRLF + '          <td>%s</td>' + CRLF +
          '          <td><span class="%s">%s</span></td>' + CRLF +
          '          <td class="sticky-op"><span class="ops"><a onclick="openModal(' + Q + 'detailModal' + Q + ')">详情</a><a onclick="openModal(' + Q + 'createModal' + Q + ')">编辑</a><a onclick="openModal(' + Q + 'stopModal' + Q + ')">停用</a></span></td>' + CRLF + '        </tr>')
    trs = [TR % r for r in rows]
    s = s.replace(m3.group(0), '<tbody>' + CRLF + CRLF.join(trs) + CRLF + '      </tbody>', 1)
    assert len(re.findall(r'<th[>\s]', s)) == len(re.findall(r'</th>', s))
    wr(p, s)
    print('库位档案.html: 筛选/表头/表单/详情注记/静态行 仓库层收敛 OK')

def location_modal():
    p = '基础数据/弹窗/新建库位.html'
    s = rd(p)
    if '仓库</span>' in s and '库区' not in s:
        print('新建库位 已是终态（幂等跳过）'); return
    m = re.search(r'<div class="form-row">\s*<span class="form-label">(?:<span class="req">\*</span>)?库[房区]</span>.*?</div>\s*</div>', s, re.S)
    assert m, '新建库位 form row'
    NEWROW = ('<div class="form-row">' + CRLF +
              '    <span class="form-label">仓库</span>' + CRLF +
              '    <div class="input-box select-box"><select ' + SELSTYLE + '>' + WH_OPTS + '</select>' + CARET + '</div>' + CRLF +
              '  </div>')
    s = s.replace(m.group(0), NEWROW, 1)
    s = re.sub(r'(<span class="req">\*</span>)?库[房区]</span>', r'\1仓库</span>', s)
    assert '库区' not in s and '库房' not in s
    wr(p, s)
    print('弹窗/新建库位.html: 表单仓库层收敛 OK')

def stock_page():
    p = '仓储作业/库存查询.html'
    s = rd(p)
    if s.count('comboBomSel') > 0:
        print('库存查询 已是终态（幂等跳过）'); return
    # 1) 散件 thead 库区→仓库
    assert s.count('<th>库区</th>') == 1, 'thead 库区'
    s = s.replace('<th>库区</th>', '<th>仓库</th>', 1)
    # 2) 筛选卡追加 4 ff
    m = re.search(r'(<div class="ff"><span class="ff-label">库存状态：</span>.*?</div>)\s*(<div class="filter-actions">)', s, re.S)
    assert m, 'ff anchor'
    FF = (m.group(1) + CRLF + '    ' +
          '<div class="ff"><span class="ff-label">仓库：</span>' + CRLF +
          '      <select><option selected>全部</option><option>正品仓</option><option>次品仓</option><option>客户虚拟仓</option><option>转租终端仓</option><option>上海一号库</option></select>' + CRLF +
          '      <svg class="ff-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>' + CRLF +
          '    </div>' + CRLF + '    ' +
          '<div class="ff"><span class="ff-label">库位：</span>' + CRLF +
          '      <select><option selected>全部</option><option>RA-A-01-01</option><option>RA-A-01-02</option><option>RB-A-01-01</option><option>RB-A-01-02</option><option>XNC-AJZX</option></select>' + CRLF +
          '      <svg class="ff-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>' + CRLF +
          '    </div>' + CRLF + '    ' +
          '<div class="ff"><span class="ff-label">物料名称：</span><input placeholder="请输入物料名称"></div>' + CRLF + '    ' +
          '<div class="ff"><span class="ff-label">项目：</span>' + CRLF +
          '      <select><option selected>全部</option><option>PRJ-2601</option><option>PRJ-2602</option><option>PRJ-2603</option><option>PRJ-2604</option><option>PRJ-2605</option></select>' + CRLF +
          '      <svg class="ff-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>' + CRLF +
          '    </div>' + CRLF + '    ')
    s = s.replace(m.group(0), FF + m.group(2), 1)
    # 3) renderListPage filters
    for NL in (CRLF, '\n'):
        old_f = ("filters: [" + NL + "    { label: '物料编码', field: '_key' }," + NL + "    { label: '库存状态', field: 'status' }" + NL + "  ],")
        if old_f in s:
            new_f = old_f.replace("    { label: '库存状态', field: 'status' }" + NL + "  ],",
                                  "    { label: '库存状态', field: 'status' }," + NL + "    { label: '仓库', field: 'area' }," + NL + "    { label: '库位', field: 'loc' }," + NL + "    { label: '物料名称', field: 'name' }," + NL + "    { label: '项目', field: 'project', match: 'contains' }" + NL + "  ],")
            s = s.replace(old_f, new_f, 1)
            break
    else:
        raise AssertionError('stock filters anchor')
    # 4) comboView → BOM 套数
    i = s.find('<div id="comboView">')
    pstart = s.find('<div class="pager">', i)
    pend = s.find('</div>', s.find('跳转页码', pstart)) + len('</div>')
    assert i > 0 and pstart > i and pend > pstart, 'comboView bounds'
    NEWCOMBO = (
        '<div id="comboView">' + CRLF +
        '  <div style="display:flex;align-items:center;gap:12px;margin:0 0 12px;flex-wrap:wrap;">' + CRLF +
        '    <span style="font-size:13px;color:#4b5563;">选用 BOM：</span>' + CRLF +
        '    <div class="input-box select-box" style="width:360px"><select id="comboBomSel" onchange="renderComboBom(this.value)" ' + SELSTYLE + '><option value="ZH-2601-A">ZH-2601-A 驾驶室围板箱整箱套件 · V2.1</option><option value="ZH-2602-B">ZH-2602-B 保险杠料架套件 · V1.3</option><option value="ZH-2603-C">ZH-2603-C 电池托盘护角套件 · V1.0</option></select>' + CARET + '</div>' + CRLF +
        '    <span id="comboBomSum" style="font-size:13px;font-weight:600;color:#1677ff;"></span>' + CRLF +
        '  </div>' + CRLF +
        '  <div class="table-wrap">' + CRLF +
        '    <table>' + CRLF +
        '      <thead>' + CRLF +
        '        <tr><th>BOM 编码</th><th>子件</th><th>来源</th><th>单位用量</th><th>在库可用</th><th>可组成（该子件计）</th></tr>' + CRLF +
        '      </thead>' + CRLF +
        '      <tbody id="comboBomBody"></tbody>' + CRLF +
        '    </table>' + CRLF +
        '  </div>' + CRLF +
        '  <div style="font-size:12px;color:#8c8c8c;margin-top:8px;">可组成套数 = 各子件「在库可用 ÷ 单位用量」取最小值（按在库量测算 · D-111）；跨 BOM 并行汇总不做（D-45 挂起）。</div>' + CRLF +
        '  ')
    s = s[:i] + NEWCOMBO + s[pend:]
    # 5) BOM 数据+渲染 JS 挂 switchView 脚本块尾
    js_anchor = 'function switchView(v) {'
    assert js_anchor in s
    JS = ('/* G31 T3 组合视角：按选 BOM 显示可组成套数（D-111） */' + CRLF +
          'var BOM_COMBOS = {' + CRLF +
          "  'ZH-2601-A': [ ['围板箱 1200×1000×970','租入',1,320], ['围板 LJ-C300','自购',4,1860], ['箱盖','自购',1,900], ['锁扣组件 LJ-A100','自购',4,5260], ['铰链 LJ-B200','自购',2,2640] ]," + CRLF +
          "  'ZH-2602-B': [ ['料架 1300×600','租入',1,180], ['支撑臂','自购',2,640], ['锁扣组件 LJ-A100','自购',2,5260] ]," + CRLF +
          "  'ZH-2603-C': [ ['周转箱 600×400','租入',1,410], ['内衬','自购',4,2200], ['绑带','自购',2,1580], ['锁扣组件 LJ-A100','自购',4,5260], ['铰链 LJ-B200','自购',2,2640], ['标签','自购',1,99999] ]" + CRLF +
          '};' + CRLF +
          'function renderComboBom(key) {' + CRLF +
          '  var rows = BOM_COMBOS[key] || [];' + CRLF +
          '  var minSets = null;' + CRLF +
          '  var html = rows.map(function (r) {' + CRLF +
          '    var sets = Math.floor(r[3] / r[2]);' + CRLF +
          "    if (minSets === null || sets < minSets) minSets = sets;" + CRLF +
          "    return '<tr><td>' + key + '</td><td>' + r[0] + '</td><td><span class=\"tag ' + (r[1] === '租入' ? 'tag-orange' : 'tag-gray') + '\">' + r[1] + '</span></td><td><span class=\"td-num\">' + r[2] + '</span></td><td><span class=\"td-num\">' + r[3].toLocaleString() + '</span></td><td><span class=\"td-num\"><b>' + sets + ' 套</b></span></td></tr>';" + CRLF +
          "  }).join('\\n');" + CRLF +
          "  document.getElementById('comboBomBody').innerHTML = html;" + CRLF +
          "  document.getElementById('comboBomSum').textContent = key + ' 可组成 ' + (minSets || 0) + ' 套';" + CRLF +
          '}' + CRLF +
          "renderComboBom('ZH-2601-A');" + CRLF)
    k = s.find('</script>', s.find(js_anchor))
    s = s[:k] + JS + s[k:]
    assert len(re.findall(r'<th[>\s]', s)) == len(re.findall(r'</th>', s))
    assert s.count('<tbody') == s.count('</tbody>')
    wr(p, s)
    print('库存查询.html: thead 仓库 + 筛选×4 + 组合视角 BOM 套数 OK')

if __name__ == '__main__':
    location_page()
    location_modal()
    stock_page()
    print('T3c 三页面完成')
