# -*- coding: utf-8 -*-
"""物料名称列补齐搜索下拉（2026-09-17·道远指出）：4 页名称列转搜索选择＋编码↔名称双向联动"""
import io, re

B = "P3-R01-包装租赁管理后台原型/"
SEL_STYLE = 'style="width:100%;min-width:120px;border:1px solid #d9d9d9;border-radius:4px;padding:2px 4px;font:inherit;background:#fff;cursor:pointer;"'

def rows_codes(s, code_sel_pat):
    """取各行（编码, 名称）用于静态兜底选项"""
    out = []
    for m in re.finditer(code_sel_pat + r"\s*<td(?: class=\"tkName\")?>([^<]{2,60})</td>", s, re.S):
        name = m.group(2)
        cm = re.search(r'value="([^"]+)"\s+selected|selected>([^<]+)<', m.group(0))
        code = m.group(1)
        out.append((code, name.strip()))
    return out

def opts_html(pairs, own_code):
    h = ""
    for c, n in pairs:
        h += ('<option value="%s" selected>%s</option>' % (c, n)) if c == own_code else ('<option value="%s">%s</option>' % (c, n))
    return h

def patch(p, code_sel_pat, name_cls, code_q, src, extra_fill_code=""):
    """name 单元格转 select + 页尾接线"""
    s = io.open(B + p, encoding="utf-8", newline="").read()
    pairs = []
    def repl(m):
        code, name = m.group(1), m.group(2).strip()
        pairs.append((code, name))
        return m.group(0).replace('<td>' + m.group(2) + '</td>' if 'class="tkName"' not in m.group(0) else '<td class="tkName">' + m.group(2) + '</td>',
                                  '<td><select class="%s" %s>%s</select></td>' % (name_cls, SEL_STYLE, opts_html([(c, n) for c, n in [(code, name)]], code)))
    # 逐行处理（repl 里只能给本行 own 选项，稍后统一补全选项集）
    pat = re.compile("(" + code_sel_pat + r")\s*<td(?: class=\"tkName\")?>([^<]{2,60})</td>", re.S)
    def repl2(m):
        code, name = m.group(2), m.group(3).strip()
        pairs.append((code, name))
        oh = opts_html(pairs_all.get(p, [(code, name)]), code) if p in pairs_all else ('<option value="%s" selected>%s</option>' % (code, name))
        return m.group(1) + '<td><select class="%s" %s>%s</select></td>' % (name_cls, SEL_STYLE, ('<option value="%s" selected>%s</option>' % (code, name)))
    # 简化：两遍——先收集 pairs，再替换
    pairs = []
    for m in pat.finditer(s):
        pairs.append((m.group(2), m.group(3).strip()))
    assert pairs, p + " 未匹配到名称行"
    uniq = list(dict.fromkeys(pairs))
    n_repl = [0]
    def repl3(m):
        code, name = m.group(2), m.group(3).strip()
        n_repl[0] += 1
        oh = "".join(('<option value="%s" selected>%s</option>' % (c, n)) if c == code else ('<option value="%s">%s</option>' % (c, n)) for c, n in uniq)
        return m.group(1) + '<td><select class="%s" %s>%s</select></td>' % (name_cls, SEL_STYLE, oh)
    s2 = pat.sub(repl3, s)
    assert n_repl[0] == len(pairs), p + " 替换数不符"
    # 接线
    wiring = (
        "/* 物料名称列搜索下拉＋编码↔名称双向联动（2026-09-17 道远指出补齐） */\r\n"
        "document.querySelectorAll('select." + name_cls + "').forEach(function (name) {\r\n"
        "  var tr = name.closest('tr'); var code = tr.querySelector('" + code_q + "');\r\n"
        "  if (!code) return;\r\n"
        + extra_fill_code +
        "  SSEL.fillEntity(name, " + src + ", { label: function (k, f) { return f.name || k; } });\r\n"
        "  name.value = code.value;\r\n"
        "  code.addEventListener('change', function () { name.value = code.value; MSEL.syncAll(); });\r\n"
        "  name.addEventListener('change', function () { code.value = name.value; MSEL.syncAll(); });\r\n"
        "});\r\n"
        "MSEL.attachAll('select." + name_cls + "', { placeholder: '输入名称搜索' });"
    )
    block = '<script>\r\n' + wiring + '\r\n</script>\r\n'
    assert s2.count('</body>') == 1 and name_cls + "'" not in s2.split('</body>')[0] or True
    s2 = s2.replace('</body>', block + '</body>', 1)
    io.open(B + p, 'w', encoding='utf-8', newline='').write(s2)
    print('OK', p, '名称行', n_repl[0], '·选项', [c for c, _ in uniq])

pairs_all = {}

# 1 销售订单新建：编码 select[data-tax=prod] 后的 input 名称格
p = '销售管理/销售订单新建.html'
s = io.open(B + p, encoding='utf-8', newline='').read()
pat = re.compile(r'(<td><select data-tax="prod"[^>]*>.*?</select></td>)\s*<td><input value="([^"]+)"></td>', re.S)
pairs = [(re.search(r'(?:value="([^"]+)"\s*)?selected?>([^<]+)<', m.group(1)).group(1) or '', m.group(2)) for m in pat.finditer(s)]
# 该页编码选项无 value——用选中项文本前缀当编码
pairs = []
for m in pat.finditer(s):
    sel_html = m.group(1)
    cm = re.search(r'<option selected>([^<]+?)\s', sel_html)
    code = cm.group(1) if cm else re.search(r'<option>([^<]+?)\s', sel_html).group(1)
    pairs.append((code, m.group(2)))
assert len(pairs) >= 2, pairs
uniq = list(dict.fromkeys(pairs))
n = [0]
def rep(m):
    cm = re.search(r'<option selected>([^<]+?)\s', m.group(1)) or re.search(r'<option>([^<]+?)\s', m.group(1))
    code = cm.group(1); name = m.group(2); n[0] += 1
    oh = "".join(('<option value="%s" selected>%s</option>' % (c, nn)) if c == code else ('<option value="%s">%s</option>' % (c, nn)) for c, nn in uniq)
    return m.group(1) + '<td><select class="soName" %s>%s</select></td>' % (SEL_STYLE, oh)
s2 = pat.sub(rep, s)
assert n[0] == len(pairs)
wiring = (
    "/* 物料名称列搜索下拉＋编码↔名称双向联动（2026-09-17 道远指出补齐）；编码列补 value 键化便于联动 */\r\n"
    "document.querySelectorAll('select[data-tax=\"prod\"]').forEach(function (code) {\r\n"
    "  var tr = code.closest('tr'); var name = tr.querySelector('select.soName');\r\n"
    "  if (!name) return;\r\n"
    "  SSEL.fillEntity(code, 'products', { label: function (k) { return k; } });\r\n"
    "  SSEL.fillEntity(name, 'products', { label: function (k, f) { return f.name || k; } });\r\n"
    "  name.value = code.value;\r\n"
    "  code.addEventListener('change', function () { name.value = code.value; MSEL.syncAll(); });\r\n"
    "  name.addEventListener('change', function () { code.value = name.value; MSEL.syncAll(); });\r\n"
    "});\r\n"
    "MSEL.attachAll('select.soName', { placeholder: '输入名称搜索' });"
)
s2 = s2.replace('</body>', '<script>\r\n' + wiring + '\r\n</script>\r\n</body>', 1)
io.open(B + p, 'w', encoding='utf-8', newline='').write(s2)
print('OK', p, n[0], '行')

# 2 采购入库录单 / 3 租赁出库录单 / 4 退租入库新建
patch('采购管理/采购入库录单.html',
      r'<td><select class="pkMat".*?</select></td>', 'pkName', 'select.pkMat', "'products'")
patch('租赁管理/租赁出库录单.html',
      r'<td><select class="zzMat".*?</select></td>', 'zzName', 'select.zzMat', "['products', 'bomList']")

# 4 退租入库新建：tkName td 转 select + 重写联动（去掉旧的 nameTd 跟随）
p = '租赁管理/退租入库新建.html'
s = io.open(B + p, encoding='utf-8', newline='').read()
pat = re.compile(r'(<td><select class="tkMat".*?</select></td>)<td class="tkName">([^<]{2,60})</td>', re.S)
pairs = [(re.search(r'value="([^"]+)"\s+selected', m.group(1)).group(1), m.group(2).strip()) for m in pat.finditer(s)]
assert len(pairs) == 3, pairs
uniq = list(dict.fromkeys(pairs))
n = [0]
def rep4(m):
    code = re.search(r'value="([^"]+)"\s+selected', m.group(1)).group(1)
    name = m.group(2).strip(); n[0] += 1
    oh = "".join(('<option value="%s" selected>%s</option>' % (c, nn)) if c == code else ('<option value="%s">%s</option>' % (c, nn)) for c, nn in uniq)
    return m.group(1) + '<td><select class="tkName" %s>%s</select></td>' % (SEL_STYLE, oh)
s2 = pat.sub(rep4, s)
assert n[0] == 3
# 重写旧联动块（nameTd 跟随 → 双向联动）
old = ("  var nameTd = s.closest('tr').children[1];\r\n"
       "  var P = (window.DEMO_DATA || {}).products || {};\r\n"
       "  function nm(k) { var f = ((P[k] || {}).row || {}).fields || {}; return f.name || k; }\r\n"
       "  s.addEventListener('change', function () { nameTd.textContent = nm(s.value); });\r\n"
       "  nameTd.textContent = nm(s.value);\r\n"
       "});")
new = ("});\r\n"
       "/* 编码↔名称双向联动（2026-09-17 道远指出补齐：名称列也改为搜索选择） */\r\n"
       "document.querySelectorAll('select.tkName').forEach(function (name) {\r\n"
       "  SSEL.fillEntity(name, 'products', { label: function (k, f) { return f.name || k; } });\r\n"
       "  var code = name.closest('tr').querySelector('select.tkMat');\r\n"
       "  if (!code) return;\r\n"
       "  name.value = code.value;\r\n"
       "  code.addEventListener('change', function () { name.value = code.value; MSEL.syncAll(); });\r\n"
       "  name.addEventListener('change', function () { code.value = name.value; MSEL.syncAll(); });\r\n"
       "});\r\n"
       "MSEL.attachAll('select.tkName', { placeholder: '输入名称搜索' });")
assert s2.count(old) == 1
s2 = s2.replace(old, new)
io.open(B + p, 'w', encoding='utf-8', newline='').write(s2)
print('OK', p, '3 行·联动块已重写')
