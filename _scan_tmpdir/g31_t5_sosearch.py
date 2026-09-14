# -*- coding: utf-8 -*-
"""G31 T5：采购订单「关联销售订单号」改搜索下拉（D-104·双层：采购订单列表.html + 弹窗/新建采购订单.html）
选中带出客户＋销售明细；不强制、留手输；未选/清空时明细恢复默认不报错。"""
import io, re, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
Q = chr(39)

def rd(p):
    return io.open(os.path.join(ROOT, p), encoding='utf-8', newline='').read()

def wr(p, s):
    io.open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='').write(s)

# 先取 3 组真实演示销售单（键/客户/明细摘要）
d = rd('_data/demo-data.js')
i = d.find('  salesOrders: {'); j = d.find('  purchaseInbounds', i)
seg = d[i:j]
DQ = chr(34)
triples = []
pat = re.compile(r"'(SO-[\d-]+)': \{[\s\S]*?'row': \{" + DQ + "fields" + DQ + r": \{([^}]*)\}")
for m in pat.finditer(seg):
    key = m.group(1)
    f = dict(re.findall(r'"(\w+)": "([^"]*)"', m.group(2)))
    if f.get('customer') and f.get('summary'):
        triples.append((key, f['customer'], f['summary']))
    if len(triples) >= 3:
        break
assert len(triples) == 3, triples
SOJS = 'var PO_SO_SRC = [' + ', '.join(
    "['%s', '%s', '%s']" % t for t in triples) + '];'

FORM_NEW = (
    '<div class="form-row">\n'
    '    <span class="form-label">关联销售订单号</span>\n'
    '    <div class="input-box" style="width:350px;position:relative;"><input id="poSoInput" placeholder="输入单号/客户搜索 · 选填 · 可直接手输" oninput="poSoSearch(this.value)" onfocus="poSoSearch(this.value)" autocomplete="off"><div id="poSoDrop" style="display:none;position:absolute;top:36px;left:0;width:100%;background:#fff;border:1px solid var(--border);border-radius:6px;box-shadow:0 4px 12px rgba(0,0,0,.08);z-index:30;max-height:220px;overflow:auto;font-size:12.5px;"></div></div>\n'
    '  </div><div class="form-row" id="poSoCustRow" style="display:none;">\n'
    '    <span class="form-label">客户（带出）</span>\n'
    '    <div class="input-box" style="width:350px;"><input id="poSoCust" readonly style="background:#f5f7fa;"></div>\n'
    '  </div>')

JS = (
    '<script>/* G31 T5 关联销售订单搜索下拉（D-104）：选中带出客户+销售明细；可手输；未选恢复默认明细 */\n'
    + SOJS + '\n'
    "var poSoDefaultRows = null;\n"
    "function poSoSearch(v) {\n"
    "  var drop = document.getElementById('poSoDrop');\n"
    "  if (!v || !v.trim()) { drop.style.display = 'none'; poSoReset(); return; }\n"
    "  var hits = PO_SO_SRC.filter(function (s) { return s[0].indexOf(v.trim()) > -1 || s[1].indexOf(v.trim()) > -1; });\n"
    "  if (!hits.length) { drop.innerHTML = '<div style=\"padding:8px 12px;color:#8c8c8c;\">无匹配销售订单（可保留手输单号）</div>'; drop.style.display = 'block'; return; }\n"
    "  drop.innerHTML = hits.map(function (s) {\n"
    "    return '<div style=\"padding:8px 12px;cursor:pointer;border-bottom:1px solid #f0f0f0;\" onmousedown=\"poSoPick(\\'' + s[0] + '\\')\"><b>' + s[0] + '</b> · ' + s[1] + '<div style=\"color:#8c8c8c;margin-top:2px;\">' + s[2] + '</div></div>';\n"
    "  }).join('');\n"
    "  drop.style.display = 'block';\n"
    "}\n"
    "function poSoPick(no) {\n"
    "  var s = PO_SO_SRC.find(function (x) { return x[0] === no; });\n"
    "  document.getElementById('poSoInput').value = no;\n"
    "  document.getElementById('poSoDrop').style.display = 'none';\n"
    "  var cr = document.getElementById('poSoCustRow');\n"
    "  if (cr) { cr.style.display = ''; document.getElementById('poSoCust').value = s ? s[1] : ''; }\n"
    "  /* 带出销售明细 → 采购明细表（可编辑，未选/清空恢复默认行） */\n"
    "  var tb = document.querySelector('.modal .edit-tbl tbody');\n"
    "  if (tb) {\n"
    "    if (!poSoDefaultRows) poSoDefaultRows = tb.innerHTML;\n"
    "    var items = s ? s[2].split('+') : [];\n"
    "    tb.innerHTML = items.map(function (it, idx) {\n"
    "      var mth = it.match(/^(.+?)[×x]\\s*([\\d,]+)元?/) || [null, it.trim(), '1'];\n"
    "      return '<tr><td>' + (idx + 1) + '</td><td><input value=\"\"></td><td><input value=\"' + mth[1] + '\"></td><td class=\"td-num\"><input value=\"' + String(mth[2]).replace(/,/g, '') + '\"></td><td class=\"td-num\"><input value=\"13%\"></td><td class=\"td-num\"><span class=\"td-num\">自动计算</span></td></tr>';\n"
    "    }).join('') || poSoDefaultRows;\n"
    "  }\n"
    "}\n"
    "function poSoReset() {\n"
    "  var cr = document.getElementById('poSoCustRow');\n"
    "  if (cr) cr.style.display = 'none';\n"
    "  var tb = document.querySelector('.modal .edit-tbl tbody');\n"
    "  if (tb && poSoDefaultRows) tb.innerHTML = poSoDefaultRows;\n"
    "}\n"
    "document.addEventListener('click', function (e) { var d = document.getElementById('poSoDrop'); if (d && !d.parentElement.contains(e.target)) d.style.display = 'none'; });\n"
    '</script>')

def apply(p):
    s = rd(p)
    if 'poSoSearch' in s:
        print(p, '已改（幂等跳过）'); return
    # 表单行替换（input→搜索复合控件＋客户带出行）
    pat = re.compile(r'<div class="form-row">\s*<span class="form-label">关联销售订单号</span>.*?</div>\s*</div>', re.S)
    m = pat.search(s)
    assert m, 'form row ' + p
    s = s.replace(m.group(0), FORM_NEW.replace('\n', '\r\n') if '\r\n' in s else FORM_NEW, 1)
    # JS 注入：createModal 弹窗结束后（modal-overlay 收口后任意 script 前）——挂到页面最后一个 </div> 后的 script 区
    k = s.find('</script>')
    # 更稳：挂在含 openModal 定义的 script 之前，即找最后一个 <script> 起点
    k2 = s.rfind('<script>')
    s = s[:k2] + (JS.replace('\n', '\r\n') if '\r\n' in s else JS) + '\n' + s[k2:]
    wr(p, s)
    print(p, ': 关联销售订单 搜索下拉 OK')

if __name__ == '__main__':
    apply('采购管理/采购订单列表.html')
    apply('采购管理/弹窗/新建采购订单.html')
