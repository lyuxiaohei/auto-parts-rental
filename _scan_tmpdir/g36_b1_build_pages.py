# -*- coding: utf-8 -*-
"""G36 B1 建页脚本：基础数据 9 页 + 项目管理 3 页（新建页面允许生成；宿主页改动走 rewire 脚本）"""
import io, os, re, sys

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
SKEL_PATH = os.path.join(ROOT, '采购管理', '采购订单新建.html')
SKEL = io.open(SKEL_PATH, encoding='utf-8').read()

# ---------- 从样板与宿主页提取可复用脚本 ----------
def grab_script(src, anchor):
    i = src.index(anchor)
    j = src.index('</script>', i) + len('</script>')
    blk = src[i:j]
    if not blk.lstrip().startswith('<script'):
        blk = '<script>\n' + blk  # 锚点位于 script 体内时补开标签
    return blk

def cut_script(src, anchor):
    """整块删除：锚点所在 script 的 <script 起点到 </script> 止"""
    i = src.index(anchor)
    a = src.rfind('<script', 0, i)
    j = src.index('</script>', i) + len('</script>')
    return src[:a] + src[j:]

TAX_EDITOR = grab_script(SKEL_PATH and io.open(os.path.join(ROOT, '基础数据', '产品档案.html'), encoding='utf-8').read(), '/* 供应商税率行编辑器')
TPL_NEWPROD = io.open(os.path.join(ROOT, '基础数据', '弹窗', '新建产品.html'), encoding='utf-8').read()
G21 = grab_script(TPL_NEWPROD, '/* G21 租价三段式联动')
G21 = G21.replace("u.disabled=(m==='按次');", "/* 按次→周期单位隐藏（G21 口径不变；去除 disabled 以免只读控件被审计判死） */")
G34 = grab_script(TPL_NEWPROD, '/* G34 T4（D-127）：物料备注字数计数')

DETAIL_CSS = '''<style id="detail-modal-css">
/* 详情页（四段式）专用样式：段落标题 / 关联链 / 流转时间线 */
.dt-sec{font-size:13px;font-weight:600;color:#262626;margin:0 0 10px;padding-left:8px;border-left:3px solid #1677ff;line-height:1.3}
.dt-sec:not(:first-child){margin-top:18px}
.chain{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.chain .node{border:1px solid #f0f0f0;border-radius:6px;padding:8px 12px;background:#fafafa;min-width:126px}
.chain .node .n-role{font-size:11px;color:#8c8c8c}
.chain .node .n-name{font-size:12.5px;font-weight:600;margin-top:2px;word-break:break-all}
.chain .link-arrow{color:#8c8c8c}
.tl{position:relative;padding-left:16px}
.tl::before{content:'';position:absolute;left:4px;top:6px;bottom:6px;width:2px;background:#e6f4ff}
.tl-i{position:relative;padding:0 0 12px 6px;font-size:12.5px;color:#262626}
.tl-i:last-child{padding-bottom:0}
.tl-i::before{content:'';position:absolute;left:-16px;top:5px;width:7px;height:7px;border-radius:50%;background:#fff;border:2px solid #1677ff}
.tl-i.off::before{border-color:#d9d9d9}
.tl-i .tl-t{color:#8c8c8c;font-size:12px;margin-right:8px;font-variant-numeric:tabular-nums}
.tl-i .tl-who{color:#8c8c8c;font-size:12px;margin-left:8px}
</style>'''

# ---------- 样板模板化 ----------
def build_template():
    t = SKEL
    # title
    assert t.count('<title>新建采购订单 - 包装租赁管理后台</title>') == 1
    t = t.replace('<title>新建采购订单 - 包装租赁管理后台</title>', '<title>{{TITLE}} - 包装租赁管理后台</title>')
    # tabs（首个 .tabs 块）
    m = re.search(r'<div class="tabs">.*?</div>\n', t, re.S)
    assert m, 'tabs block not found'
    t = t.replace(m.group(0), '<div class="tabs">\n{{TABS}}\n</div>\n')
    # sidebar：取消采购管理 open
    assert t.count('<li class="sm-item has-sub open">') == 1
    t = t.replace('<li class="sm-item has-sub open">', '<li class="sm-item has-sub">', 1)
    # selected 项还原为可点击
    assert t.count('<li><div class="sm-link selected">采购订单</div></li>') == 1
    t = t.replace('<li><div class="sm-link selected">采购订单</div></li>',
                  '<li><div class="sm-link" onclick="go(\'../采购管理/采购订单列表.html\')">采购订单</div></li>')
    # content + submit-bar → 占位
    i = t.index('    <div class="content submit-pad">')
    j = t.index('<script>\nfunction addDetailRow')
    t = t[:i] + '    <div class="content submit-pad">\n{{CONTENT}}\n{{SUBMITBAR}}\n    </div>\n  </div>\n</div>\n' + t[j:]
    # 采购专属脚本段（addDetailRow/PO_SO/dict/prod/PRJ_SUPPLIERS）→ 占位；保留 demo-data 引入
    a0 = t.index('<script>\nfunction addDetailRow')
    mb = t.index('/* ===== 菜单折叠')
    b0 = t.rfind('<script', a0, mb)  # 菜单折叠脚本的开标签不计入删除段
    seg = t[a0:b0]
    keep = '<script src="../_data/demo-data.js"></script>'
    assert keep in seg
    t = t.replace(seg, keep + '\n{{PAGE_SCRIPTS}}\n')  # demo-data 先于页脚本（依赖 DEMO_DATA）
    # F-A 税率脚本删除（采购专属）
    t = cut_script(t, '/*F-A 税率三件套双向换算')
    assert 'F-A 税率' not in t
    # detail css 注入口
    assert t.count('</head>') == 1
    t = t.replace('</head>', '{{DETAIL_CSS}}</head>')
    return t

TEMPLATE = build_template()

# ---------- 组件助手 ----------
def frow(label, ctrl, req=False, colon='：'):
    star = '<span class="req">*</span>' if req else ''
    return ('  <div class="form-row">\n    <div class="form-label">%s%s</div>\n    <div>%s</div>\n  </div>\n' % (star, label, colon and label and (label + colon) or label, ctrl)) if False else (
        '  <div class="form-row">\n    <div class="form-label">%s%s%s</div>\n    <div>\n      %s\n    </div>\n  </div>\n' % (star, label, colon, ctrl))

def inp(pid, placeholder='', value='', width=380, extra=''):
    v = ' value="%s"' % value if value else ''
    style = ' style="width:%dpx;%s"' % (width, extra) if extra or width != 350 else ''
    return '<div class="input-box"%s><input id="%s" placeholder="%s"%s></div>' % (style, pid, placeholder, v)

def sel(pid, options, width=380, onchange=''):
    oc = ' onchange="%s"' % onchange if onchange else ''
    inner = ('style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"')
    opts = ''.join('<option%s>%s</option>' % (' selected' if i == 0 else '', o) for i, o in enumerate(options))
    return '<div class="input-box select-box" style="width:%dpx;"><select id="%s"%s %s>%s</select><span class="caret">▾</span></div>' % (width, pid, oc, inner, opts)

def ta(pid, placeholder='选填', width=380, minh=72, extra=''):
    return ('<div class="input-box" style="width:%dpx;height:auto;padding:6px 11px;%s"><textarea id="%s" placeholder="%s" style="width:100%%;border:none;outline:none;background:transparent;font:inherit;color:inherit;resize:vertical;min-height:%dpx;line-height:1.6;"></textarea></div>' % (width, extra, pid, placeholder, minh))

def trow_wrap(label, inner, req=False):
    star = '<span class="req">*</span>' if req else ''
    return '  <div class="form-row">\n    <div class="form-label">%s%s：</div>\n    <div>\n      %s\n    </div>\n  </div>\n' % (star, label, inner)

DICT_JS = '''function dictOpts(cat) {
  var D = (window.DEMO_DATA || {}).dictItems || {};
  return Object.keys(D).filter(function (k) {
    var f = (D[k].row || {}).fields || {};
    return f.category === cat && f.status !== '停用';
  }).sort().map(function (k) { return ((D[k].row || {}).fields || {}).name; }).filter(Boolean);
}
function fillSel(id, opts, keepCur) {
  var s = document.getElementById(id); if (!s) return;
  if (!opts || !opts.length) return;
  var cur = keepCur ? s.value : null;
  s.innerHTML = opts.map(function (o) { return '<option>' + o + '</option>'; }).join('');
  if (cur && opts.indexOf(cur) > -1) s.value = cur;
}'''

# ---------- 12 页配置 ----------
PAGES = []

def add_page(path, title, tab_host, tab_self, group, menu_label, menu_target, host_url, content, scripts, submitbar, detail=False, detail_cfg=None):
    PAGES.append(dict(path=path, title=title, tab_host=tab_host, tab_self=tab_self, group=group,
                      menu_label=menu_label, menu_target=menu_target, host_url=host_url,
                      content=content, scripts=scripts, submitbar=submitbar, detail=detail, detail_cfg=detail_cfg))

def submitbar(host, cancel='取 消', saves=('<button class="btn">保 存</button>',)):
    btns = '<button class="btn btn-default" onclick="go(\'%s\')">%s</button>' % (host, cancel)
    for s in saves:
        btns += s
    return '<div class="submit-bar">%s</div>' % btns

def card(title, body):
    return '<div class="card">\n  <div class="card-head">\n    <h3 class="card-title">%s</h3>\n  </div>\n%s</div>\n' % (title, body)

HOST_CK = '../基础数据/客商管理.html'
HOST_WL = '../基础数据/产品档案.html'
HOST_KW = '../基础数据/库位档案.html'
HOST_BOM = '../基础数据/BOM维护.html'
HOST_PRJ = '../项目管理/项目档案.html'

SEL = 'style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"'

# ===== 1. 物料新建 =====
tax_sec = '''<div class="tax-sec">
    <div class="tax-sec-title">供应商税率<span class="tax-sec-sub">同一物料可按供应商维护不同税率；单据明细税率默认带出、可手动覆盖</span></div>
    <div class="tax-edit">
      <div class="tax-edit-hd"><span>供应商</span><span>默认税率</span><span>结算周期</span><span style="flex:0 0 44px;">操作</span></div>
      <div id="taxEditRows"></div>
      <button class="btn btn-default btn-sm" type="button" onclick="addTaxRow()">+ 添加一行</button>
    </div>
  </div>'''
TAX_CSS = open(os.path.join(ROOT, '基础数据', '弹窗', '新建产品.html'), encoding='utf-8').read()
m = re.search(r'<style>\s*\n\s*\.tax-sec\{.*?</style>', TAX_CSS, re.S)
assert m, 'tax css not found'
TAX_CSS = m.group(0)

body_wl = ''
body_wl += frow('物料编码', inp('wlCode', '如 WBX-1210L / LJ-A100'), req=True)
body_wl += frow('物料名称', inp('wlName', '如 围板箱 1200×1000×970'), req=True)
body_wl += frow('物料类型', sel('wlTypeSel', ['围板箱', '塑料托盘', '木托盘', '料箱', '料架', '组件']), req=True)
body_wl += frow('供应商内部编码', inp('wlInner', '选填 · 供应商/客户方产品编码'))
body_wl += frow('物料型号', inp('wlModel', '选填'))
body_wl += frow('规格', inp('wlSpec', '', value='1200×1000×970mm'))
body_wl += frow('单位', sel('unitSel', ['只', '套', '个', '托', '件'], onchange="g21RentHint('rentIn');g21RentHint('rental');"))
body_wl += frow('参考未税采购价(元)', inp('wlBuyPrice', '', value='380.00'))
body_wl += frow('参考未税销售价(元)', inp('wlSalePrice', '可售物料填写，不适用留空'))
tri = lambda p, hint: ('<div style="display:flex;gap:6px;align-items:center;width:380px;">'
    '<div class="input-box select-box" style="width:116px;flex:none;"><select id="%sModeSel" onchange="g21RentHint(\'%s\')" %s><option selected>按时间周期</option><option>按次</option></select></div>'
    '<div class="input-box select-box" id="%sUnitBox" style="width:72px;flex:none;"><select id="%sUnitSel" onchange="g21RentHint(\'%s\')" %s><option selected>月</option><option>年</option><option>日</option></select></div>'
    '<div class="input-box" style="flex:1;min-width:0;"><input placeholder="%s"></div>'
    '<span id="%sHint" style="font-size:12px;color:#8c8c8c;white-space:nowrap;">%s</span></div>')
body_wl += trow_wrap('参考未税租入价', tri('rentIn', '元/只·月') % ('rentIn', 'rentIn', SEL, 'rentIn', 'rentIn', 'rentIn', SEL, '数值，如 45.00（无租入来源留空）', 'rentIn', '元/只·月'))
body_wl += trow_wrap('参考未税租赁价', tri('rental', '元/只·月') % ('rental', 'rental', SEL, 'rental', 'rental', 'rental', SEL, '数值，如 60.00', 'rental', '元/只·月'))
body_wl += ('  <div class="form-row" style="align-items:flex-start;">\n    <div class="form-label" style="padding-top:6px;">备注：</div>\n    <div>\n      '
    '<div class="input-box" style="width:380px;height:auto;padding:6px 11px;position:relative;"><textarea id="prodRemarkTa" maxlength="200" placeholder="选填" oninput="g34TaCount(this,\'prodRemarkCnt\',200)" style="width:100%;border:none;outline:none;background:transparent;font:inherit;color:inherit;resize:vertical;min-height:72px;line-height:1.6;"></textarea>'
    '<span class="char-count" id="prodRemarkCnt" style="position:absolute;right:10px;bottom:6px;font-size:12px;color:#8c8c8c;background:rgba(255,255,255,.92);">0/200</span></div>\n    </div>\n  </div>\n')
scripts_wl = '\n'.join([G21, G34, '<script>' + DICT_JS + '''
(function(){ fillSel('wlTypeSel', dictOpts('物料类型')); fillSel('unitSel', dictOpts('计量单位'), true); })();
</script>''', TAX_EDITOR, '<script>if(document.readyState!=="loading"){initTaxEdit()}else{document.addEventListener("DOMContentLoaded",function(){initTaxEdit()})}</script>'])
add_page('基础数据/物料新建.html', '新建物料', '物料档案', '新建物料', '基础资料', '物料档案', '../基础数据/产品档案.html', HOST_WL,
         card('基础信息', body_wl) + TAX_CSS + '\n' + card('供应商税率', tax_sec),
         scripts_wl, submitbar(HOST_WL, '取 消', ['<button class="btn">保 存</button>']))

# ===== 2. 客商新建 =====
body_ks = ''
body_ks += frow('客商名称', inp('ksName', '企业全称'), req=True)
body_ks += frow('客商类型', sel('ksTypeSel', ['客户', '供应商', '客户兼供应商']), req=True)
body_ks += frow('联系人', inp('ksContact', '请输入', value='张三'))
body_ks += frow('联系电话', inp('ksPhone', '请输入', value='138****0000'))
body_ks += ('  <div class="form-row" style="align-items:flex-start;">\n    <div class="form-label" style="padding-top:6px;">备注：</div>\n    <div>\n      ' + ta('ksRemark') + '\n    </div>\n  </div>\n')
scripts_ks = '<script>' + DICT_JS + '''\n(function(){ fillSel('ksTypeSel', dictOpts('客商类型'), true); })();</script>'''
add_page('基础数据/客商新建.html', '新建客商', '客商管理', '新建客商', '基础资料', '客商管理', HOST_CK, HOST_CK,
         card('基础信息', body_ks), scripts_ks, submitbar(HOST_CK, '取消', ['<button class="btn">保存</button>']))

# ===== 3. 库位新建 =====
body_kw = ''
body_kw += frow('仓库名称', inp('kwWh', '自定义输入，如 上海一号仓 / 正品仓'))
body_kw += frow('库位编码', inp('kwCode', '如 RA-A01'), req=True)
body_kw += frow('库位类型', sel('locTypeSel', ['存储位', '拣选位', '暂存位', '不合格品位']))
body_kw += frow('规格 / 承载', inp('kwSpec', '请输入', value='1200×1000 · ≤800kg'))
body_kw += ('  <div class="form-row" style="align-items:flex-start;">\n    <div class="form-label" style="padding-top:6px;">备注：</div>\n    <div>\n      ' + ta('kwRemark') + '\n    </div>\n  </div>\n')
scripts_kw = '<script>' + DICT_JS + '''\n(function(){ fillSel('locTypeSel', dictOpts('库位类型'), true); })();</script>'''
add_page('基础数据/库位新建.html', '新建库位', '库位档案', '新建库位', '基础资料', '库位档案', '../基础数据/库位档案.html', HOST_KW,
         card('基础信息', body_kw), scripts_kw, submitbar(HOST_KW, '取消', ['<button class="btn">保存</button>']))

# ===== 4. 客商开票资料 =====
body_inv = ''
body_inv += frow('单位名称', inp('invName', '请输入', value='华骏重卡汽车有限公司'))
body_inv += frow('发票类型', sel('invTypeSel', ['增值税专用发票（13%）', '增值税普通发票']))
body_inv += frow('纳税人识别号', inp('invTaxNo', '请输入', value='91220100MA100000XX'))
body_inv += frow('开户银行', inp('invBank', '请输入', value='中国工商银行长春汽车城支行'))
body_inv += frow('银行账号', inp('invAcct', '请输入', value='4200 6710 0987 6543 210'))
body_inv += frow('收款账号', inp('invRecvAcct', '选填 · 收付款账号可与开票账号不一致'))
body_inv += frow('结算周期', sel('invSettleSel', ['月结', '发票后 30 天', '发票后 60 天', '发票后 90 天', '发票后 120 天']), req=True)
body_inv += ('  <div class="form-row" style="align-items:flex-start;">\n    <div class="form-label" style="padding-top:6px;">备注：</div>\n    <div>\n      ' + ta('invRemark') + '\n    </div>\n  </div>\n')
scripts_inv = '<script>' + DICT_JS + '''\n(function(){ fillSel('invTypeSel', dictOpts('发票类型'), true); fillSel('invSettleSel', dictOpts('结算周期'), true); })();</script>'''
add_page('基础数据/客商开票资料.html', '开票资料', '客商管理', '开票资料', '基础资料', '客商管理', HOST_CK, HOST_CK,
         card('开票资料', body_inv), scripts_inv, submitbar(HOST_CK, '取消', ['<button class="btn">保存</button>']))

# ===== 5. 客商收货信息 =====
body_recv = ''
body_recv += frow('收货人', inp('recvName', '请输入', value='严明'))
body_recv += frow('收货电话', inp('recvPhone', '请输入', value='138****6621'))
body_recv += frow('收货地址', inp('recvAddr', '请输入', value='吉林省长春市汽开区开拓大街 2222 号 · 1 号收货口'))
add_page('基础数据/客商收货信息.html', '收货信息', '客商管理', '收货信息', '基础资料', '客商管理', HOST_CK, HOST_CK,
         card('收货信息', body_recv), '', submitbar(HOST_CK, '取消', ['<button class="btn">保存</button>']))

# ===== 6-8. 详情页（物料/客商/库位） =====
def detail_page(path, title, tab_host, tab_self, entity, def_key, menu_label, menu_target, host_url):
    content = ('<div class="card">\n  <div class="card-head">\n'
               '    <h3 class="card-title" id="dtTitle">%s</h3>\n'
               '    <div class="head-btns"><button class="btn btn-default btn-sm" onclick="go(\'%s\')">返回列表</button></div>\n'
               '  </div>\n  <div id="detailBody"><!-- 内容由 _data/detail-generic.js 按单号渲染 --></div>\n</div>\n' % (title, host_url))
    scripts = ('<script src="../_data/detail-generic.js"></script>\n<script>\n'
               '(function () {\n'
               '  var ENT = %s, DEF = %s;\n'
               '  var k = null;\n'
               '  try { k = new URLSearchParams(location.search).get("id"); } catch (e) {}\n'
               '  var D = (window.DEMO_DATA || {})[ENT] || {};\n'
               '  if (!D[k]) k = Object.keys(D).filter(function (x) { return D[x] && (D[x].info || D[x].title); })[0] || DEF;\n'
               '  var rec = D[k] || {};\n'
               '  var t = document.getElementById("dtTitle");\n'
               '  if (t) t.textContent = (rec.title || %s) + " · " + (rec.titleNo || k);\n'
               '  var el = document.getElementById("detailBody");\n'
               '  if (el && window.renderGenericDetailHTML) el.innerHTML = window.renderGenericDetailHTML(rec, "../");\n'
               '})();\n</script>' % (repr(entity), repr(def_key), repr(title)))
    add_page(path, title, tab_host, tab_self, '基础资料', menu_label, menu_target, host_url,
             content, scripts, '', detail=True)

detail_page('基础数据/物料详情.html', '物料详情', '物料档案', '物料详情', 'products', 'WBX-1210L', '物料档案', HOST_WL, HOST_WL)
detail_page('基础数据/客商详情.html', '客商详情', '客商管理', '客商详情', 'partners', 'DW-0001', '客商管理', HOST_CK, HOST_CK)
detail_page('基础数据/库位详情.html', '库位详情', '库位档案', '库位详情', 'locations', 'RA-A01', '库位档案', HOST_KW, HOST_KW)

# ===== 9. BOM版本查看 =====
content_bom = ('<div class="card">\n  <div class="card-head">\n'
               '    <h3 class="card-title" id="dtTitle">BOM 版本查看</h3>\n'
               '    <div class="head-btns"><button class="btn btn-default btn-sm" onclick="go(\'%s\')">返回列表</button></div>\n'
               '  </div>\n  <div id="detailBody"><!-- 内容由 _data/detail-generic.js 按单号渲染 --></div>\n</div>\n' % HOST_BOM)
scripts_bom = ('<script src="../_data/detail-generic.js"></script>\n<script>\n'
               '(function () {\n'
               '  var ENT = "bomVersions", DEF = "V2.1";\n'
               '  var k = null;\n'
               '  try { k = new URLSearchParams(location.search).get("id"); } catch (e) {}\n'
               '  var D = (window.DEMO_DATA || {})[ENT] || {};\n'
               '  if (!D[k]) k = Object.keys(D).filter(function (x) { return D[x] && (D[x].info || D[x].title); })[0] || DEF;\n'
               '  var rec = D[k] || {};\n'
               '  var t = document.getElementById("dtTitle");\n'
               '  if (t) t.textContent = "BOM 版本查看 · " + (rec.titleNo || k);\n'
               '  var el = document.getElementById("detailBody");\n'
               '  if (el && window.renderGenericDetailHTML) el.innerHTML = window.renderGenericDetailHTML(rec, "../");\n'
               '})();\n</script>')
add_page('基础数据/BOM版本查看.html', 'BOM 版本查看', 'BOM', 'BOM 版本查看', '基础资料', 'BOM', '../基础数据/BOM.html', HOST_BOM,
         content_bom, scripts_bom, '', detail=True)

# ===== 10. 上下游绑定 =====
sup_checks = ''.join(['<label style="display:flex;align-items:center;gap:8px;padding:4px 0;cursor:pointer;font-size:13px;color:#262626"><input type="checkbox"%s style="accent-color:#1677ff;width:16px;height:16px"> %s</label>\n      ' % (ck, n) for ck, n in [(' checked', '环通循环包装运营（上海）有限公司（租入）'), (' checked', '甬城塑业包装制品有限公司（采购）'), ('', '吴越联合五金制品有限公司（采购）'), ('', '延陵塑料托盘厂（采购）'), ('', '上海喜悦智行科技股份有限公司（采购）')]])
body_bind = ''
body_bind += frow('项目', sel('bindPrj', ['PRJ-2601 华骏重卡·长春基地 驾驶室围板箱租赁']), req=True)
body_bind += frow('客户', sel('bindCust', ['华骏重卡汽车有限公司']), req=True)
body_bind += trow_wrap('供应商（多选）', '<div id="bindSups" style="width:380px;border:1px solid #d9d9d9;border-radius:4px;padding:8px 12px;background:#fff;max-height:180px;overflow-y:auto">\n      ' + sup_checks + '</div>')
body_bind += frow('默认库房', sel('bindWh', ['华东中心仓（WH-01）', '华南仓（WH-02）', '西南仓（WH-03）']))
scripts_bind = '<script>' + DICT_JS + '''
(function () {
  var P = (window.DEMO_DATA || {}).partners || {};
  var cands = [], sups = [];
  Object.keys(P).forEach(function (k) {
    var f = (P[k].row || {}).fields || {};
    if (!f.name) return;
    if (f.type === '客户' || f.type === '客户兼供应商') cands.push(f.name);
    if (f.type === '供应商' || f.type === '客户兼供应商') sups.push(f.name);
  });
  fillSel('bindCust', cands);
  var box = document.getElementById('bindSups');
  if (box && sups.length) {
    box.innerHTML = sups.map(function (n, i) {
      return '<label style="display:flex;align-items:center;gap:8px;padding:4px 0;cursor:pointer;font-size:13px;color:#262626"><input type="checkbox"' + (i < 2 ? ' checked' : '') + ' style="accent-color:#1677ff;width:16px;height:16px"> ' + n + '</label>';
    }).join('');
  }
  var J = (window.DEMO_DATA || {}).projects || {};
  var prjs = Object.keys(J).filter(function (k) { return (J[k].row || {}).fields; }).map(function (k) {
    var f = J[k].row.fields; return k + ' ' + (f.name || '');
  });
  fillSel('bindPrj', prjs);
})();
</script>'''
add_page('项目管理/上下游绑定.html', '项目上下游绑定', '项目列表', '上下游绑定', '项目管理', '项目列表', HOST_PRJ, HOST_PRJ,
         card('项目上下游绑定', body_bind), scripts_bind, submitbar(HOST_PRJ, '取 消', ['<button class="btn">保存绑定</button>']))

# ===== 11. 项目新建 =====
prj_sup_checks = ''.join(['<label style="display:flex;align-items:center;gap:8px;padding:4px 0;cursor:pointer;font-size:13px;color:#262626"><input type="checkbox"%s style="accent-color:#1677ff;width:16px;height:16px"> %s</label>\n      ' % (ck, n) for ck, n in [(' checked', '环通循环包装运营（上海）有限公司（租入）'), ('', '甬城塑业包装制品有限公司（采购）'), ('', '吴越联合五金制品有限公司（采购）'), ('', '延陵塑料托盘厂（采购）'), ('', '上海喜悦智行科技股份有限公司（采购）')]])
body_prj = ''
body_prj += trow_wrap('项目编码', '<div class="input-box" style="width:380px;background:#fafafa;"><span style="color:#8c8c8c;">PRJ-2606（自动生成 · 不可编辑）</span></div>')
body_prj += frow('项目名称', inp('prjName', '请输入项目名称'), req=True)
body_prj += frow('客户', sel('prjCust', ['华骏重卡汽车有限公司', '东海商用汽车有限公司宁波分公司', '星途新能源汽车科技有限公司', '长风汽车制造有限公司']), req=True)
body_prj += trow_wrap('供应商（多选）', '<div id="prjSups" style="width:380px;border:1px solid #d9d9d9;border-radius:4px;padding:8px 12px;background:#fff;max-height:150px;overflow-y:auto">\n      ' + prj_sup_checks + '</div>', req=True)
body_prj += trow_wrap('项目起止', '<div class="input-box" style="width:380px;gap:8px;"><input type="date" style="text-align:center;"><span style="color:var(--text-3)">~</span><input type="date" style="text-align:center;"></div>', req=True)
body_prj += frow('项目负责人', sel('prjOwner', ['江强', '江强·其他']))
scripts_prj = '<script>' + DICT_JS + '''
(function () {
  var P = (window.DEMO_DATA || {}).partners || {};
  var cands = [], sups = [];
  Object.keys(P).forEach(function (k) {
    var f = (P[k].row || {}).fields || {};
    if (!f.name) return;
    if (f.type === '客户' || f.type === '客户兼供应商') cands.push(f.name);
    if (f.type === '供应商' || f.type === '客户兼供应商') sups.push(f.name);
  });
  fillSel('prjCust', cands);
  var box = document.getElementById('prjSups');
  if (box && sups.length) {
    box.innerHTML = sups.map(function (n, i) {
      return '<label style="display:flex;align-items:center;gap:8px;padding:4px 0;cursor:pointer;font-size:13px;color:#262626"><input type="checkbox"' + (i === 0 ? ' checked' : '') + ' style="accent-color:#1677ff;width:16px;height:16px"> ' + n + '</label>';
    }).join('');
  }
  var J = (window.DEMO_DATA || {}).projects || {};
  var owners = [];
  Object.keys(J).forEach(function (k) {
    var o = ((J[k].row || {}).fields || {}).owner;
    if (o && owners.indexOf(o) === -1) owners.push(o);
  });
  fillSel('prjOwner', owners.length ? owners : ['江强']);
})();
</script>'''
add_page('项目管理/项目新建.html', '新建项目', '项目列表', '新建项目', '项目管理', '项目列表', HOST_PRJ, HOST_PRJ,
         card('项目信息', body_prj), scripts_prj, submitbar(HOST_PRJ, '取 消', ['<button class="btn">保 存</button>']))

# ===== 12. 编码规则 =====
body_rule = ''
body_rule += ('  <div class="form-row">\n    <div class="form-label">编码结构：</div>\n    <div>\n      <div class="form-tip" style="line-height:2;">前缀 <code>PRJ-</code> + 年份两位 <code>{YY}</code> + 连字符 + 流水四位 <code>{NNNN}</code></div>\n    </div>\n  </div>\n')
body_rule += frow('项目前缀', inp('rulePrefix', '', value='PRJ-'), req=True)
body_rule += trow_wrap('流水位数', '<div style="display:flex;">\n        <span class="radio"><span class="dot"></span>2 位</span>\n        <span class="radio"><span class="dot"></span>3 位</span>\n        <span class="radio checked"><span class="dot"></span>4 位</span>\n      </div>', req=True)
body_rule += trow_wrap('是否连续', '<div style="display:flex;">\n        <span class="radio checked"><span class="dot"></span>连续流水（推荐）</span>\n        <span class="radio"><span class="dot"></span>按年份独立</span>\n      </div>')
body_rule += ('  <div class="form-row">\n    <div class="form-label">预览示例：</div>\n    <div>\n      <div class="form-tip">下一个项目编码：<code>PRJ-2606</code>（自动生成、不可编辑，与库存/单据编码规则一致）</div>\n    </div>\n  </div>\n')
add_page('项目管理/编码规则.html', '项目编码规则', '项目列表', '编码规则', '项目管理', '项目列表', HOST_PRJ, HOST_PRJ,
         card('项目编码规则', body_rule), '', submitbar(HOST_PRJ, '取 消', ['<button class="btn">保存规则</button>']))

# ---------- 组装与写出 ----------
def sidebar_select(t, group, menu_label, menu_target):
    # 目标组 open
    gi = t.index(group + '<span class="sm-arrow">')
    li = t.rfind('<li class="sm-item has-sub">', 0, gi)
    assert li > -1, 'group li not found: ' + group
    t = t[:li] + '<li class="sm-item has-sub open">' + t[li + len('<li class="sm-item has-sub">'):]
    # 目标菜单项 selected
    old = '<li><div class="sm-link" onclick="go(\'%s\')">%s</div></li>' % (menu_target, menu_label)
    assert t.count(old) == 1, 'menu item not found: ' + menu_label
    t = t.replace(old, '<li><div class="sm-link selected">%s</div></li>' % menu_label)
    return t

written = []
for p in PAGES:
    t = TEMPLATE
    t = t.replace('{{TITLE}}', p['title'])
    tabs = '  <span class="tab">%s <span class="close">×</span></span>\n  <span class="tab active">%s <span class="close">×</span></span>' % (p['tab_host'], p['tab_self'])
    t = t.replace('{{TABS}}', tabs)
    t = sidebar_select(t, p['group'], p['menu_label'], p['menu_target'])
    t = t.replace('{{CONTENT}}', p['content'])
    t = t.replace('{{SUBMITBAR}}', p['submitbar'] if p['submitbar'] else '')
    t = t.replace('{{PAGE_SCRIPTS}}', p['scripts'] if p['scripts'] else '')
    t = t.replace('{{DETAIL_CSS}}', DETAIL_CSS if p['detail'] else '')
    for ph in ('{{TITLE}}', '{{TABS}}', '{{CONTENT}}', '{{SUBMITBAR}}', '{{PAGE_SCRIPTS}}', '{{DETAIL_CSS}}'):
        assert ph not in t, ph + ' left in ' + p['path']
    # 行尾与宿主模块一致：模块页 CRLF
    if '\r\n' not in t:
        t = t.replace('\n', '\r\n')
    fp = os.path.join(ROOT, p['path'])
    io.open(fp, 'w', encoding='utf-8', newline='').write(t)
    written.append(p['path'])

print('BUILT %d pages:' % len(written))
for w in written:
    print('  +' + w)
