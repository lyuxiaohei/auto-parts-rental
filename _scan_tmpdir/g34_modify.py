# -*- coding: utf-8 -*-
"""G34 主改造脚本 v2（T1-T7）：EOL 自适应（HTML=纯 CRLF）+ 幂等（已应用自动跳过）。
"""
import io

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
F = {
    'page_prod':  ROOT + r'\基础数据\产品档案.html',
    'tpl_prod':   ROOT + r'\基础数据\弹窗\新建产品.html',
    'page_kst':   ROOT + r'\基础数据\客商管理.html',
    'tpl_inv':    ROOT + r'\基础数据\弹窗\客商开票资料.html',
    'page_loc':   ROOT + r'\基础数据\库位档案.html',
    'tpl_loc':    ROOT + r'\基础数据\弹窗\新建库位.html',
    'dict_page':  ROOT + r'\系统管理\数据字典.html',
    'demo_data':  ROOT + r'\_data\demo-data.js',
}

def load(p):
    with io.open(p, encoding='utf-8', newline='') as f:
        return f.read()

def save(p, t):
    with io.open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(t)

LOG = []
def log(m):
    LOG.append(m); print(m)

class Ctx:
    """按文件 EOL 自适应的替换器（幂等：新串已存在且旧串不存在 → 跳过）"""
    def __init__(self, path):
        self.path = path
        self.t = load(path)
        mixed = self.t.count('\n') - self.t.count('\r\n')
        self.eol = '\r\n' if self.t.count('\r\n') >= (self.t.count('\n') - mixed) and self.t.count('\r\n') > 0 else '\n'
        assert mixed == 0, '%s 混合行尾 LF-only=%d（先归一）' % (path, mixed)
    def A(self, s):
        return s.replace('\n', self.eol)
    def rep(self, old, new, tag, n=1):
        old = self.A(old); new = self.A(new)
        no, nn = self.t.count(old), self.t.count(new)
        if no == 0 and nn == n:
            log('  [skip 已应用] %s' % tag); return
        assert no == n, '[%s] anchor x%d (expect %d)' % (tag, no, n)
        self.t = self.t.replace(old, new)
    def save(self):
        save(self.path, self.t)
        log('%s: 落盘（<div=%d </div>=%d）' % (self.path.split('\\')[-1], self.t.count('<div'), self.t.count('</div>')))

# ============================================================
# 1) demo-data.js：dictItems 追加 SL（6）+ JSQ（9）——含幂等护栏
# ============================================================
c = Ctx(F['demo_data'])
if "'SL-01'" in c.t and "'JSQ-09'" in c.t:
    log('  [skip 已应用] demo-data SL/JSQ 追加')
else:
    anchor_tkl2 = ("'TKL-02': { 'row': {\"fields\": {\"category\": \"退款类型\", \"abbr\": \"应收退款\", \"name\": \"应收退款\", \"status\": \"启用\"}, "
                   "\"cells\": [\"应收退款\", \"应收退款\", \"<span class=\\\"td-num\\\">2</span>\", \"对客户·源自销售退货·资金方向=付款\", \"<span class=\\\"tag tag-green\\\">启用</span>\"], "
                   "\"ops\": [{\"t\": \"编辑\"}, {\"t\": \"停用\", \"act\": \"openModal('stopModal')\"}]} },")
    def item(code, cat, val, seq, note):
        return ("    '%s': { 'row': {\"fields\": {\"category\": \"%s\", \"abbr\": \"%s\", \"name\": \"%s\", \"status\": \"启用\"}, "
                "\"cells\": [\"%s\", \"%s\", \"<span class=\\\"td-num\\\">%d</span>\", \"%s\", \"<span class=\\\"tag tag-green\\\">启用</span>\"], "
                "\"ops\": [{\"t\": \"编辑\"}, {\"t\": \"停用\", \"act\": \"openModal('stopModal')\"}]} },") % (code, cat, code, val, code, val, seq, note)
    SL = ['0%', '1%', '3%', '6%', '9%', '13%']
    JSQ = ['预付', '货到付款', '周结', '半月结', '月结', '发票后 30 天', '发票后 60 天', '发票后 90 天', '发票后 120 天']
    add = [item('SL-%02d' % (i + 1), '供应商税率', v, i + 1, '供应商默认税率下拉值源（D-127）') for i, v in enumerate(SL)]
    add += [item('JSQ-%02d' % (i + 1), '结算周期', v, i + 1, '结算周期统一值源·客商开票资料+物料供应商税率区共用（D-127）') for i, v in enumerate(JSQ)]
    c.rep(anchor_tkl2, anchor_tkl2 + '\n\n' + '\n'.join(add), 'dict-append')
    c.save()

# ============================================================
# 2) 物料弹窗双层
# ============================================================
SELECT_LINE_TYPE = ('    <div class="input-box select-box"><select style="flex:1;min-width:0;border:none;outline:none;'
    'background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;">'
    '<option selected>围板箱</option><option>塑料托盘</option><option>木托盘</option><option>料箱</option><option>料架</option><option>组件</option>'
    '</select><span class="caret"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>')

def block_head(ph):
    return ('<div class="form-row">\n    <span class="form-label"><span class="req">*</span>物料编码</span>\n'
            '    <div class="input-box"><input placeholder="' + ph + '"></div>\n'
            '  </div><div class="form-row">\n    <span class="form-label">型号</span>\n'
            '    <div class="input-box"><input placeholder="选填"></div>\n'
            '  </div><div class="form-row">\n    <span class="form-label">内部编码</span>\n'
            '    <div class="input-box"><input placeholder="选填 · 供应商/客户方产品编码"></div>\n'
            '  </div><div class="form-row">\n    <span class="form-label"><span class="req">*</span>物料名称</span>\n'
            '    <div class="input-box"><input placeholder="如 围板箱 1200×1000×970"></div>\n'
            '  </div><div class="form-row">\n    <span class="form-label"><span class="req">*</span>物料类型</span>\n'
            + SELECT_LINE_TYPE + '\n  </div>\n  </div>')

def block_new(ph):
    return ('<div class="form-row">\n    <span class="form-label"><span class="req">*</span>物料编码</span>\n'
            '    <div class="input-box"><input placeholder="' + ph + '"></div>\n'
            '  </div><div class="form-row">\n    <span class="form-label"><span class="req">*</span>物料名称</span>\n'
            '    <div class="input-box"><input placeholder="如 围板箱 1200×1000×970"></div>\n'
            '  </div><div class="form-row">\n    <span class="form-label"><span class="req">*</span>物料类型</span>\n'
            + SELECT_LINE_TYPE + '\n  </div><div class="form-row">\n    <span class="form-label">供应商内部编码</span>\n'
            '    <div class="input-box"><input placeholder="选填 · 供应商/客户方产品编码"></div>\n'
            '  </div><div class="form-row">\n    <span class="form-label">物料型号</span>\n'
            '    <div class="input-box"><input placeholder="选填"></div>\n  </div>')

W220 = ' style="width:220px;flex:none;"'
TEXTAREA_REMARK = ('</div><div class="form-row g2">\n    <span class="form-label">备注</span>\n'
    '    <div class="input-box" style="height:72px;align-items:stretch;padding:6px 11px;position:relative;">\n'
    '      <textarea id="prodRemarkTa" maxlength="200" placeholder="选填" oninput="g34TaCount(this,\'prodRemarkCnt\',200)" '
    'style="flex:1;min-width:0;height:100%;border:none;outline:none;background:transparent;font:inherit;color:inherit;resize:none;padding:0;line-height:1.6;"></textarea>\n'
    '      <span class="char-count" id="prodRemarkCnt" style="position:absolute;right:10px;bottom:6px;font-size:12px;color:#8c8c8c;background:rgba(255,255,255,.92);">0/200</span>\n'
    '    </div>\n  </div>')
OLD_REMARK = ('</div><div class="form-row g2">\n    <span class="form-label">备注</span>\n'
    '    <div class="input-box"><input placeholder="选填"></div>\n  </div>')
G21_OLD = "document.getElementById(p+'Hint').textContent='元/'+unit+'·'+(m==='按次'?'次':u.value);}</script>"
G21_NEW = ("document.getElementById(p+'Hint').textContent='元/'+unit+'·'+(m==='按次'?'次':u.value);};\n"
    "/* G34 T4（D-127）：物料备注字数计数（maxlength=200·满额标红） */\n"
    "window.g34TaCount=function(ta,cid,mx){var el=document.getElementById(cid);if(!el)return;var n=ta.value.length;"
    "el.textContent=n+'/'+mx;el.classList.toggle('over',n>=mx);};</script>")
ESC_ANCHOR = "  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }\n  window.addTaxRow = function (sup, rate, cyc) {"
ESC_NEW = ("  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }\n"
    "  /* G34 T5/T6（D-127）：默认税率/结算周期下拉=数据字典 SL/JSQ 渲染，字典缺失回退硬编码 */\n"
    "  var SL = [], JSQ = [];\n"
    "  try {\n"
    "    var DICT = (window.DEMO_DATA || {}).dictItems || {};\n"
    "    Object.keys(DICT).forEach(function (k) {\n"
    "      var df = (DICT[k].row || {}).fields || {};\n"
    "      if (df.category === '供应商税率') SL.push(df.name);\n"
    "      else if (df.category === '结算周期') JSQ.push(df.name);\n"
    "    });\n"
    "  } catch (e) {}\n"
    "  if (!SL.length) SL = ['0%','1%','3%','6%','9%','13%'];\n"
    "  if (!JSQ.length) JSQ = ['月结','发票后 30 天','发票后 60 天','发票后 90 天','发票后 120 天'];\n"
    "  window.addTaxRow = function (sup, rate, cyc) {")
RATE_OLD = "      + '<span class=\"tax-cell\"><input class=\"tax-in\" value=\"' + esc(rate || '13%') + '\"></span>'"
RATE_NEW = ("      + '<span class=\"tax-cell\"><select class=\"tax-sel\">' + SL.map(function(o){return '<option'"
    "+(o===(rate||'13%')?' selected':'')+'>'+o+'</option>';}).join('') + '</select></span>'")
CYC_OLD = "      + '<span class=\"tax-cell\"><select class=\"tax-sel\">' + ['月结','发票后 30 天','发票后 60 天','发票后 90 天','发票后 120 天'].map(function(o){return '<option'+(o===(cyc||'月结')?' selected':'')+'>'+o+'</option>';}).join('') + '</select></span>'"
CYC_NEW = "      + '<span class=\"tax-cell\"><select class=\"tax-sel\">' + JSQ.map(function(o){return '<option'+(o===(cyc||'月结')?' selected':'')+'>'+o+'</option>';}).join('') + '</select></span>'"

for key, ph in [('page_prod', '如 WBX-1210L'), ('tpl_prod', '如 WBX-1210L / LJ-A100')]:
    c = Ctx(F[key])
    c.rep(block_head(ph), block_new(ph), key + ':T1+T2 头块(顺序+改名+去游离闭合)')
    c.rep('<span class="form-label">规格</span>\n    <div class="input-box"><input value="1200×1000×970mm"',
          '<span class="form-label">规格</span>\n    <div class="input-box"' + W220 + '><input value="1200×1000×970mm"', key + ':T3 规格')
    c.rep('<span class="form-label">单位</span>\n    <div class="input-box select-box"><select id="unitSel"',
          '<span class="form-label">单位</span>\n    <div class="input-box select-box"' + W220 + '><select id="unitSel"', key + ':T3 单位')
    c.rep('<span class="form-label">参考未税采购价(元)</span>\n    <div class="input-box"><input value="380.00"',
          '<span class="form-label">参考未税采购价(元)</span>\n    <div class="input-box"' + W220 + '><input value="380.00"', key + ':T3 采购价')
    c.rep('<span class="form-label">参考未税销售价(元)</span>\n    <div class="input-box"><input placeholder="可售物料填写，不适用留空">',
          '<span class="form-label">参考未税销售价(元)</span>\n    <div class="input-box"' + W220 + '><input placeholder="可售物料填写，不适用留空">', key + ':T3 销售价')
    c.rep(OLD_REMARK, TEXTAREA_REMARK, key + ':T4 备注textarea')
    c.rep(G21_OLD, G21_NEW, key + ':T4 计数函数')
    c.rep(ESC_ANCHOR, ESC_NEW, key + ':T5/T6 字典装载')
    c.rep(RATE_OLD, RATE_NEW, key + ':T5 税率select')
    c.rep(CYC_OLD, CYC_NEW, key + ':T6 结算周期JSQ')
    c.save()

# ============================================================
# 3) 客商侧 T6 + 客商开票资料.html T2 配平
# ============================================================
INV_ANCHOR = '<span class="form-label"><span class="req">*</span>结算周期</span>\n    <div class="input-box select-box"><select style='
INV_NEW = '<span class="form-label"><span class="req">*</span>结算周期</span>\n    <div class="input-box select-box"><select id="invSettleSel" style='
INV_RENDER = ('<script>/* G34 T6（D-127）：结算周期=字典 JSQ 渲染（客商开票资料与物料供应商税率区共用同一字典组）；渲染失败保留静态兜底 */\n'
    '(function () {\n'
    '  var J = [];\n'
    '  try {\n'
    "    var D = (window.DEMO_DATA || {}).dictItems || {};\n"
    "    Object.keys(D).forEach(function (k) { var f = (D[k].row || {}).fields || {}; if (f.category === '结算周期') J.push(f.name); });\n"
    '  } catch (e) {}\n'
    '  if (!J.length) return;\n'
    "  var s = document.getElementById('invSettleSel');\n"
    '  if (!s) return;\n'
    '  var cur = s.value;\n'
    "  s.innerHTML = J.map(function (o) { return '<option' + (o === cur ? ' selected' : '') + '>' + o + '</option>'; }).join('');\n"
    '})();\n'
    '</script>\n</body>')

c = Ctx(F['page_kst'])
c.rep(INV_ANCHOR, INV_NEW, 'page_kst:T6 select id')
c.rep('</body>', INV_RENDER, 'page_kst:T6 渲染脚本')
c.save()

c = Ctx(F['tpl_inv'])
c.rep('  </div>    <div class="modal-footer">', '  </div>\n    </div>\n    <div class="modal-footer">', 'tpl_inv:T2 modal-body 闭合')
c.rep(INV_ANCHOR, INV_NEW, 'tpl_inv:T6 select id')
c.rep('</body>', '<script src="../../_data/demo-data.js"></script>\n' + INV_RENDER, 'tpl_inv:T6 渲染脚本+数据引用')
c.save()

# ============================================================
# 4) 库位档案 T7（页内嵌 + 模板）
# ============================================================
SEL_STYLE = 'flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;'
CARET = '<span class="caret"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>'
LOC_TA = ('</div><div class="form-row">\n    <span class="form-label">备注</span>\n'
    '    <div class="input-box" style="height:72px;align-items:stretch;padding:6px 11px;">\n'
    '      <textarea placeholder="选填" style="flex:1;min-width:0;height:100%;border:none;outline:none;background:transparent;font:inherit;color:inherit;resize:none;padding:0;line-height:1.6;"></textarea>\n'
    '    </div>\n  </div>')
LOC_TA_OLD = ('</div><div class="form-row">\n    <span class="form-label">备注</span>\n'
    '    <div class="input-box"><input placeholder="选填"></div>\n  </div>')
LOC_RENDER = ('<script>/* G34 T7（D-127）：库位类型=字典 KW 渲染（新建弹窗+筛选区）；渲染失败保留静态兜底 */\n'
    '(function () {\n'
    '  var KW = [];\n'
    '  try {\n'
    "    var D = (window.DEMO_DATA || {}).dictItems || {};\n"
    "    Object.keys(D).forEach(function (k) { var f = (D[k].row || {}).fields || {}; if (f.category === '库位类型') KW.push(f.name); });\n"
    '  } catch (e) {}\n'
    '  if (!KW.length) return;\n'
    "  var s1 = document.getElementById('locTypeSel');\n"
    "  if (s1) s1.innerHTML = KW.map(function (o) { return '<option>' + o + '</option>'; }).join('');\n"
    "  var s2 = document.getElementById('locTypeFilterSel');\n"
    "  if (s2) s2.innerHTML = '<option selected>全部</option>' + KW.map(function (o) { return '<option>' + o + '</option>'; }).join('');\n"
    '})();\n'
    '</script>\n</body>')

WH_ROW_OLD = ('<div class="form-row">\n    <span class="form-label"><span class="req">*</span>仓库</span>\n'
    '    <div class="input-box select-box"><select style="' + SEL_STYLE + '"><option selected>正品仓</option><option>次品仓</option><option>客户虚拟仓（安吉智行）</option></select>' + CARET + '</div>\n  </div>')
WH_ROW_NEW = ('<div class="form-row">\n    <span class="form-label"><span class="req">*</span>仓库名称</span>\n'
    '    <div class="input-box"><input placeholder="自定义输入，如 上海一号仓 / 正品仓"></div>\n  </div>')

c = Ctx(F['page_loc'])
c.rep(WH_ROW_OLD, WH_ROW_NEW, 'page_loc:T7 仓库名称')
c.rep('<span class="form-label">库位类型</span>\n    <div class="input-box select-box"><select style=',
      '<span class="form-label">库位类型</span>\n    <div class="input-box select-box"><select id="locTypeSel" style=', 'page_loc:T7 弹窗类型 id')
c.rep('<select><option selected>全部</option><option>存储位</option>',
      '<select id="locTypeFilterSel"><option selected>全部</option><option>存储位</option>', 'page_loc:T7 筛选区 id')
c.rep(LOC_TA_OLD, LOC_TA, 'page_loc:T7 备注 textarea')
c.rep('</body>', LOC_RENDER, 'page_loc:T7 渲染脚本')
c.save()

c = Ctx(F['tpl_loc'])
c.rep('<div class="form-row">\n    <span class="form-label">仓库</span>\n    <div class="input-box select-box"><select style="' + SEL_STYLE + '"><option selected>原料区 RA</option><option>成品区 RB</option><option>外购区 RW</option><option>器具区 JC</option></select>' + CARET + '</div>\n  </div>', '', 'tpl_loc:T7 删库区残留行(D-102)')
n_wh = c.t.count('<span class="form-label">仓库</span>')
assert n_wh == 1, 'tpl_loc: 仓库 label x%d' % n_wh
c.rep('<div class="form-row">\n    <span class="form-label">仓库</span>\n    <div class="input-box select-box"><select style="' + SEL_STYLE + '"><option selected>正品仓</option><option>次品仓</option><option>客户虚拟仓（安吉智行）</option></select>' + CARET + '</div>\n  </div>',
      '<div class="form-row">\n    <span class="form-label">仓库名称</span>\n    <div class="input-box"><input placeholder="自定义输入，如 上海一号仓 / 正品仓"></div>\n  </div>', 'tpl_loc:T7 仓库名称')
c.rep('<span class="form-label">库位类型</span>\n    <div class="input-box select-box"><select style=',
      '<span class="form-label">库位类型</span>\n    <div class="input-box select-box"><select id="locTypeSel" style=', 'tpl_loc:T7 类型 id')
c.rep('<option selected>平面库位</option><option>全部</option><option>待定选项（演示数据）</option>',
      '<option selected>存储位</option><option>拣选位</option><option>暂存位</option><option>不合格品位</option>', 'tpl_loc:T7 清脏占位')
c.rep(LOC_TA_OLD, LOC_TA, 'tpl_loc:T7 备注 textarea')
c.rep('</body>', '<script src="../../_data/demo-data.js"></script>\n' + LOC_RENDER, 'tpl_loc:T7 渲染脚本+数据引用')
c.save()

# ============================================================
# 5) 数据字典.html
# ============================================================
c = Ctx(F['dict_page'])
c.rep('<div class="dic-item"><span>退款类型</span><span class="cnt">2</span></div>',
      '<div class="dic-item"><span>退款类型</span><span class="cnt">2</span></div>\n          <div class="dic-item"><span>供应商税率</span><span class="cnt">6</span></div>\n          <div class="dic-item"><span>结算周期</span><span class="cnt">9</span></div>', 'dict_page: 左列表+2组')
c.rep('<option>退货类型</option><option>退款类型</option>',
      '<option>退货类型</option><option>退款类型</option><option>供应商税率</option><option>结算周期</option>', 'dict_page: select+2组')
c.save()

print('\nALL G34 MODIFY STEPS DONE.')
