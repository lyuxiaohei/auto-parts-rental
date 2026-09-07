# -*- coding: utf-8 -*-
"""任务二：预收/预付静态表达（6 文件）。
应收账单：首行前加预收行 + 详情时间线（内嵌+独立模板双层）加预收节点
应付账单：首行前加预付行 + 详情时间线（双层）加预付冲抵节点
银行水单核销：②卡头加类型筛选 select（含预收款/预付款）+ dzTable 加预收款示例行
F01：押金注记下方加同款灰字预收/预付注记（纯 SVG text 追加，不碰节点/连线/坐标）
纪律：二进制精确替换 + assert 计数 + 标签配平；新行不加 A04 pin。"""
import pathlib

ROOT = pathlib.Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型')

def patch(rel, old, new, tagset=('div', 'span', 'tr', 'td')):
    p = ROOT / rel
    b = p.read_bytes()
    ob, nb = old.encode(), new.encode()
    n = b.count(ob)
    assert n == 1, '%s 锚点计数 %d != 1' % (rel, n)
    bal0 = {t: b.count(('<' + t + '>').encode()) + b.count(('<' + t + ' ').encode()) - b.count(('</' + t + '>').encode()) for t in tagset}
    out = b.replace(ob, nb, 1)
    bal1 = {t: out.count(('<' + t + '>').encode()) + out.count(('<' + t + ' ').encode()) - out.count(('</' + t + '>').encode()) for t in tagset}
    assert bal0 == bal1, '%s 标签配平被破坏 %s -> %s' % (rel, bal0, bal1)
    p.write_bytes(out)
    print('OK %-40s +%d 字节' % (rel, len(out) - len(b)))

C = '\r\n'

# ---------- 1. 应收账单：预收行（首行前） ----------
ar_row = (
    '<tr>' + C +
    '          <td><input type="checkbox" class="cb"></td>' + C +
    '          <td><span class="lk">AR-2026-09-PRJ2601-YS</span></td>' + C +
    '          <td>2026-09</td>' + C +
    '          <td>PRJ-2601</td>' + C +
    '          <td>安吉智行物流</td>' + C +
    '          <td><span class="tag tag-blue">预收</span><div style="color:#8c8c8c;font-size:11px;">客户预付 9-10 月租金，后续按月冲抵</div></td>' + C +
    '          <td>—</td>' + C +
    '          <td><span class="td-num"><b>50,000.00</b></span></td>' + C +
    '          <td><span class="td-num">0.00</span></td>' + C +
    '          <td><span class="tag tag-green">已收</span></td>' + C +
    '          <td><span class="tag tag-blue">手动登记</span></td>' + C +
    '          <td>2026-09-05 10:20</td>' + C +
    '          <td class="sticky-op"><span class="ops"><a onclick="openModal(\'detailModal\')">详情</a></span></td>' + C +
    '        </tr>' + C + '        '
)
patch('财务协同/应收账单.html',
      '<tbody>' + C + '        <tr>' + C + '          <td><input type="checkbox" class="cb"></td>' + C + '          <td data-note="1">',
      '<tbody>' + C + '        ' + ar_row + '<tr>' + C + '          <td><input type="checkbox" class="cb"></td>' + C + '          <td data-note="1">')

# ---------- 2. 应收详情时间线：预收节点（双层） ----------
ar_tl_old = '账单自动生成 · 销售费汇总<span class="tl-who">系统</span></div>'
ar_tl_new = ar_tl_old + ('<div class="tl-i"><span class="tl-t">09-05</span>预收款到账 · 记预收（安吉智行 ¥50,000）<span class="tl-who">财务</span></div>'
                         '<div class="tl-i"><span class="tl-t">每月</span>租金自预收冲抵 · 月度账单生成后自动冲抵<span class="tl-who">系统</span></div>')
patch('财务协同/应收账单.html', ar_tl_old, ar_tl_new)
patch('财务协同/弹窗/应收账单详情.html', ar_tl_old, ar_tl_new)

# ---------- 3. 应付账单：预付行（首行前） ----------
ap_row = (
    '<tr>' + C +
    '          <td><input type="checkbox" class="cb"></td>' + C +
    '          <td><span class="lk">AP-20260905-012</span></td>' + C +
    '          <td>路凯包装运营</td>' + C +
    '          <td><span class="tag tag-blue">预付</span><div style="color:#8c8c8c;font-size:11px;">预付运营方大箱租金（9 月度）</div></td>' + C +
    '          <td>PRJ-2604</td>' + C +
    '          <td>2026-09</td>' + C +
    '          <td><span class="lk">RZD-20260815-005</span></td>' + C +
    '          <td>—</td>' + C +
    '          <td><span class="td-num">30,000.00</span></td>' + C +
    '          <td><span class="td-num">0.00</span></td>' + C +
    '          <td><span class="td-num">30,000.00</span></td>' + C +
    '          <td>2026-09-05</td>' + C +
    '          <td>2026-09-30</td>' + C +
    '          <td><span class="tag tag-green">已付款</span></td>' + C +
    '          <td class="sticky-op"><span class="ops"><a onclick="openModal(\'detailModal\')">详情</a></span></td>' + C +
    '        </tr>' + C + '        '
)
patch('财务协同/应付账单.html',
      '<tbody>' + C + '        <tr>' + C + '          <td><input type="checkbox" class="cb"></td>' + C + '          <td data-note="3">',
      '<tbody>' + C + '        ' + ap_row + '<tr>' + C + '          <td><input type="checkbox" class="cb"></td>' + C + '          <td data-note="3">')

# ---------- 4. 应付详情时间线：预付冲抵节点（双层） ----------
ap_tl_old = '应付账单自动生成<span class="tl-who">系统</span></div>'
ap_tl_new = ap_tl_old + ('<div class="tl-i"><span class="tl-t">09-05</span>预付款支付 · 记预付（路凯 ¥30,000）<span class="tl-who">财务</span></div>'
                         '<div class="tl-i"><span class="tl-t">每月</span>预付冲抵 · 租金应付生成后自预付冲抵<span class="tl-who">系统</span></div>')
patch('财务协同/应付账单.html', ap_tl_old, ap_tl_new)
patch('财务协同/弹窗/应付账单详情.html', ap_tl_old, ap_tl_new)

# ---------- 5. 银行水单核销：类型筛选 select + 预收款示例行 ----------
sd_sel_old = '<div class="head-btns"><button class="btn btn-default btn-sm" onclick="go(\'../财务协同/应收账单.html\')">应收台账</button></div>'
sd_sel_new = ('<div class="head-btns"><select title="类型筛选" style="height:28px;border:1px solid var(--border);border-radius:4px;padding:0 8px;font-size:12px;color:var(--text-2);background:#fff;outline:none;">'
              '<option selected>类型：全部</option><option>应收账单</option><option>丢损赔偿单</option><option>预收款</option><option>预付款</option></select>'
              '<button class="btn btn-default btn-sm" onclick="go(\'../财务协同/应收账单.html\')">应收台账</button></div>')
patch('财务协同/银行水单核销.html', sd_sel_old, sd_sel_new)

sd_row_old = '<td><span class="td-num"><b>38,000.00</b></span></td>' + C + '        </tr>' + C + '      </tbody>'
sd_row_new = ('<td><span class="td-num"><b>38,000.00</b></span></td>' + C + '        </tr>' + C + '        <tr>' + C +
              '          <td><input type="checkbox" class="cb" data-amt="50000.0"></td>' + C +
              '          <td><span class="lk">AR-2026-09-PRJ2601-YS</span></td>' + C +
              '          <td><span class="tag tag-blue">预收款</span></td>' + C +
              '          <td>安吉智行物流</td>' + C +
              '          <td><span class="td-num">50,000.00</span></td>' + C +
              '          <td><span class="td-num">0.00</span></td>' + C +
              '          <td><span class="td-num"><b>50,000.00</b></span></td>' + C +
              '        </tr>' + C + '      </tbody>')
patch('财务协同/银行水单核销.html', sd_row_old, sd_row_new)

# ---------- 6. F01：押金注记下方加预收/预付同款灰字 ----------
f01_old = '<text x="40" y="1594" fill="#9ca3af" font-size="8.5" font-family="\'Geist\',sans-serif">押金：租赁单现有押金字段（原型自带）；收退规则属商务口径待客户确认（计费单价/押金/缺损标准，见 P1-R01 待确认项）——非会议提出的需求</text>'
f01_new = f01_old + '\n    <text x="40" y="1610" fill="#9ca3af" font-size="8.5" font-family="\'Geist\',sans-serif">预收/预付：客户预付租金记预收按月冲抵；预付运营方租金记预付（09-06 补充）</text>'
patch('P3-R01-F01-业务流程导航图.html', f01_old, f01_new, tagset=('text',))

print('任务二全部完成')
