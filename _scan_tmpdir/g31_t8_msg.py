# -*- coding: utf-8 -*-
"""G31 T8 D-126：站内信类型筛选下拉 + 消息类型进 dictItems（双源同步）
① pc-msg.js 消息面板加类型筛选（选项优先读 DEMO_DATA.dictItems MSG 组，静态兜底）
② demo-data dictItems +MSG-01~04（消息类型 4 值）
③ 数据字典页：分类 nav +消息类型 item + createModal 分组 select +option
"""
import io, re, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
Q = chr(39)

def rd(p):
    return io.open(os.path.join(ROOT, p), encoding='utf-8', newline='').read()

def wr(p, s):
    io.open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='').write(s)

TAGS = ['账单到期', '分期付款', '押金应退', '续租跟进']

def pc_msg():
    p = '_data/pc-msg.js'
    s = rd(p)
    if 'pcMsgTag' in s:
        print('pc-msg.js 已加筛选（幂等）'); return
    NL = chr(13) + chr(10) if chr(13) + chr(10) in s else chr(10)
    # 1) 类型值源：dictItems 优先（双源同步·D-126），静态兜底
    src_fn = ('function tagSource() {' + NL +
              '  var D = window.DEMO_DATA && window.DEMO_DATA.dictItems;' + NL +
              '  if (D) {' + NL +
              "    var ks = Object.keys(D).filter(function (k) { return D[k].row && D[k].row.fields.category === '消息类型'; });" + NL +
              '    var arr = ks.map(function (k) { return D[k].row.fields.abbr; }).filter(Boolean);' + NL +
              '    if (arr.length) return arr;' + NL +
              '  }' + NL +
              "  return ['账单到期', '分期付款', '押金应退', '续租跟进'];" + NL +
              '}' + NL +
              'var curTag = ' + Q + '全部' + Q + ';' + NL)
    # 2) renderPanel：加筛选下拉行+按 curTag 过滤
    old_hd = "'<div class=\"pc-msg-hd\">站内信<span data-act=\"all\">全部标为已读</span></div>' + rows.join('')"
    assert old_hd in s, 'renderPanel anchor'
    new_loop = ('function renderPanel() {' + NL +
                '      var tags = tagSource();' + NL +
                '      var rows = [];' + NL +
                '      for (var i = 0; i < MSGS.length; i++) {' + NL +
                '        var m = MSGS[i];' + NL +
                "        if (curTag !== '全部' && m.tag !== curTag) continue;" + NL +
                '        rows.push(...)' + NL)
    # 原循环体保留：直接改两处——循环内加过滤行；面板头加下拉
    s = s.replace('function renderPanel() {',
                  'function renderPanel() {' + NL + "      if (curTag !== '全部') MSGS = MSGS.filter(function (m) { return m.tag === curTag || MSGS.indexOf(m) < 0; }) ? MSGS : MSGS;" if False else
                  'function renderPanel() {', 1)
    # 循环内加 continue
    old_for = "for (var i = 0; i < MSGS.length; i++) {" + NL + "        var m = MSGS[i];" + NL + "        rows.push("
    assert old_for in s, 'loop anchor'
    new_for = ("for (var i = 0; i < MSGS.length; i++) {" + NL +
               "        var m = MSGS[i];" + NL +
               "        if (curTag !== '全部' && m.tag !== curTag) continue;" + NL +
               "        rows.push(")
    s = s.replace(old_for, new_for, 1)
    # 空态文案区分「无消息/无该类型」
    s = s.replace("if (!rows.length) rows.push('<div class=\"pc-msg-empty\">暂无消息</div>');",
                  "if (!rows.length) rows.push('<div class=\"pc-msg-empty\">' + (curTag === '全部' ? '暂无消息' : '该类型暂无消息') + '</div>');", 1)
    # 面板头加下拉
    sel_html = ("'<div class=\"pc-msg-hd\">站内信<span data-act=\"all\">全部标为已读</span></div>'" + NL +
                "        + '<div class=\"pc-msg-flt\"><span>类型：</span><select id=\"pcMsgTag\">'" + NL +
                "        + ['全部'].concat(tagSource()).map(function (t) { return '<option' + (t === curTag ? ' selected' : '') + '>' + t + '</option>'; }).join('')" + NL +
                "        + '</select></div>' + rows.join('')")
    s = s.replace(old_hd, sel_html, 1)
    # 下拉 change 事件（面板委托里加 data-act 之外的处理：select change）
    anchor_click = "panel.addEventListener('click', function (ev) {"
    assert anchor_click in s
    change_js = ('panel.addEventListener(' + Q + 'change' + Q + ', function (ev) {' + NL +
                 "      if (ev.target && ev.target.id === 'pcMsgTag') { curTag = ev.target.value; renderPanel(); }" + NL +
                 '    });' + NL + '    ')
    s = s.replace(anchor_click, change_js + anchor_click, 1)
    # tagSource + curTag 定义插在 KEY 定义后
    anchor_key = "var KEY = 'pc-msg-read';"
    assert anchor_key in s
    s = s.replace(anchor_key, anchor_key + NL + src_fn, 1)
    # 样式：筛选行样式挂在面板（脚本内注入 style 已有？加最小行内式——用现有结构 .pc-msg-flt 需样式）
    anchor_css = '.pc-msg-hd'
    if anchor_css in s:
        s = s.replace('.pc-msg-hd {', '.pc-msg-flt{display:flex;align-items:center;gap:6px;padding:6px 14px;border-bottom:1px solid #f0f0f0;font-size:12px;color:#4b5563;}' + NL + '    .pc-msg-flt select{border:1px solid #d9d9d9;border-radius:4px;height:24px;font-size:12px;padding:0 4px;outline:none;}' + NL + '    .pc-msg-hd {', 1)
    wr(p, s)
    print('pc-msg.js: 类型筛选下拉（dictItems 双源+静态兜底）OK')

def dict_items():
    p = '_data/demo-data.js'
    s = rd(p)
    if 'MSG-01' in s:
        print('dictItems MSG 已加（幂等）'); return
    i = s.find('  dictItems: {')
    NL = chr(13) + chr(10)
    # 在 dictItems 段首插 4 行（键 MSG-01~04）
    ins = []
    for n, t in enumerate(TAGS, 1):
        row = ("    'MSG-0%d': { 'row': {\"fields\": {\"category\": \"消息类型\", \"abbr\": \"%s\", \"name\": \"站内信·%s\", \"status\": \"启用\"}, "
               "\"cells\": [\"%s\", \"站内信·%s\", \"<span class=\\\"td-num\\\">%d</span>\", \"pc-msg.js 消息面板类型筛选值源（D-126·双源同步）\", \"<span class=\\\"tag tag-green\\\">启用</span>\"], "
               "\"ops\": [{\"t\": \"编辑\"}, {\"t\": \"停用\", \"act\": \"openModal('stopModal')\"}]}}," % (n, t, t, t, t, n))
        ins.append(row + NL)
    s = s[:i + len('  dictItems: {') + len(NL)] + NL.join(ins) + s[i + len('  dictItems: {') + len(NL):]
    wr(p, s)
    print('dictItems: +MSG-01~04（消息类型 4 值·115→119 项）OK')

def dict_page():
    p = '系统管理/数据字典.html'
    s = rd(p)
    if '消息类型' in s:
        print('字典页已加（幂等）'); return
    NL = chr(13) + chr(10) if chr(13) + chr(10) in s else chr(10)
    # 分类 nav 追加（待办单据类型 后）
    anchor = '<div class="dic-item"><span>待办单据类型</span><span class="cnt">16</span></div>'
    assert anchor in s, 'dic-item anchor'
    s = s.replace(anchor, anchor + NL + '          <div class="dic-item"><span>消息类型</span><span class="cnt">4</span></div>', 1)
    # createModal 分组 select 追加 option
    m = re.search(r'<option>待办单据类型</option>', s)
    assert m, 'option anchor'
    s = s.replace('<option>待办单据类型</option>', '<option>待办单据类型</option><option>消息类型</option>', 1)
    wr(p, s)
    print('数据字典页: 分类 nav +消息类型(4) + createModal 组选项 OK')

if __name__ == '__main__':
    pc_msg()
    dict_items()
    dict_page()
