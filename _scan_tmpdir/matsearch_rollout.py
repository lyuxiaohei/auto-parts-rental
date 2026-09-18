# -*- coding: utf-8 -*-
"""物料搜索下拉共享件铺开（2026-09-17·道远指示）：9 页接线 + 2 页假下拉转真 select"""
import io, re

B = "P3-R01-包装租赁管理后台原型/"

def load(p):
    return io.open(B + p, encoding="utf-8", newline="").read()

def save(p, s):
    io.open(B + p, "w", encoding="utf-8", newline="").write(s)

def wire(p, js, need_demo_data=False):
    """页尾 </body> 前插入 mat-search 接线块（附 demo-data 兜底可选）"""
    s = load(p)
    assert s.count("</body>") == 1
    assert "mat-search.js" not in s, p + " 已接"
    inc = '<script src="../_data/mat-search.js"></script>\r\n'
    if need_demo_data and "demo-data.js" not in s:
        inc = '<script src="../_data/demo-data.js"></script>\r\n<script src="../_data/select-source.js"></script>\r\n' + inc
    block = inc + "<script>\r\n" + js + "\r\n</script>\r\n"
    s = s.replace("</body>", block + "</body>", 1)
    save(p, s)
    print("OK wire", p)

# ---- A. 真 select 页：一行接线 ----
wire("销售管理/销售订单新建.html",
     "/* 物料搜索下拉（2026-09-17 道远指示）：明细物料列换搜索选择 */\r\n"
     "MSEL.attachAll('.edit-tbl select[data-tax=\"prod\"]');")
wire("租赁管理/租赁单新建.html",
     "/* 物料搜索下拉（2026-09-17 道远指示）：明细物料列换搜索选择 */\r\n"
     "MSEL.attachAll('.edit-tbl td select.g39mat');")
wire("租入管理/租入单新建.html",
     "/* 物料搜索下拉（2026-09-17 道远指示）：明细物料列换搜索选择 */\r\n"
     "MSEL.attachAll('.edit-tbl td select.g39mat');")
for f, lab in (("仓储作业/调拨新建.html", "物料"), ("仓储作业/其他入库新建.html", "物料"), ("仓储作业/其他出库新建.html", "物料")):
    wire(f,
         "/* 物料搜索下拉（2026-09-17 道远指示）：头部物料字段换搜索选择（input-box 内保框保箭头） */\r\n"
         "MSEL.attach(SSEL.byFormLabel('物料'));")

# ---- B. 假下拉转真 select：租赁出库录单（组合件编码列） ----
p = "租赁管理/租赁出库录单.html"
s = load(p)
pat = re.compile(r'<div class="ctl sel" style="min-width:120px;"><span class="v">((?:ZH|ZT|JP|WBX|PLT|BTC|LJ)-[A-Za-z0-9\-]+)</span>.*?</div></td>', re.S)
found = pat.findall(s)
assert len(found) >= 3, "组合件假下拉定位失败: %r" % found
opts = sorted(set(found))
opt_html = "".join("<option%s>%s</option>" % (" selected" if False else "", k) for k in opts)
def repl(m):
    code = m.group(1)
    oh = "".join(('<option selected>' + k + '</option>') if k == code else ('<option>' + k + '</option>') for k in opts)
    return ('<select class="zzMat" style="width:100%;min-width:120px;border:1px solid #d9d9d9;border-radius:4px;padding:2px 4px;font:inherit;background:#fff;cursor:pointer;">'
            + oh + '</select></td>')
s2, n = pat.subn(repl, s)
assert n == len(found) and n >= 3
save(p, s2)
print("OK 转真select", p, n, "处·选项", opts)
wire(p,
     "/* 物料搜索下拉（2026-09-17 道远指示）：组合件编码列换搜索选择（原假下拉转真 select） */\r\n"
     "document.querySelectorAll('select.zzMat').forEach(function (s) { SSEL.fillEntity(s, ['products', 'bomList'], { label: function (k) { return k; } }); });\r\n"
     "MSEL.attachAll('.edit-tbl select.zzMat', { placeholder: '输入编码搜索' });")

# ---- C. 假下拉转真 select：采购入库录单（物料编码列） ----
p = "采购管理/采购入库录单.html"
s = load(p)
pat = re.compile(r'<div class="ctl sel" style="min-width:110px;"><span class="v">((?:ZH|ZT|JP|WBX|PLT|BTC|LJ)-[A-Za-z0-9\-]+)</span>.*?</div></td>', re.S)
found = pat.findall(s)
assert len(found) >= 3, "物料假下拉定位失败: %r" % found
opts = sorted(set(found))
def repl2(m):
    code = m.group(1)
    oh = "".join(('<option selected>' + k + '</option>') if k == code else ('<option>' + k + '</option>') for k in opts)
    return ('<select class="pkMat" style="width:100%;min-width:110px;border:1px solid #d9d9d9;border-radius:4px;padding:2px 4px;font:inherit;background:#fff;cursor:pointer;">'
            + oh + '</select></td>')
s2, n = pat.subn(repl2, s)
assert n == len(found) and n >= 3
save(p, s2)
print("OK 转真select", p, n, "处·选项", opts)
wire(p,
     "/* 物料搜索下拉（2026-09-17 道远指示）：物料编码列换搜索选择（原假下拉转真 select） */\r\n"
     "document.querySelectorAll('select.pkMat').forEach(function (s) { SSEL.fillEntity(s, 'products', { label: function (k) { return k; } }); });\r\n"
     "MSEL.attachAll('.edit-tbl select.pkMat', { placeholder: '输入编码搜索' });")

# ---- D. 退租入库新建：静态 td 转真 select（编码可选·名称跟随） ----
p = "租赁管理/退租入库新建.html"
s = load(p)
pat = re.compile(r'<tr><td>((?:ZH|ZT|JP|WBX|PLT|BTC|LJ)-[A-Za-z0-9\-]+)</td><td>([^<]+)</td>')
found = pat.findall(s)
assert len(found) == 3, "退租明细行定位失败: %r" % found
opts = sorted(set(k for k, _ in found))
sel_style = 'style="width:100%;min-width:90px;border:1px solid #d9d9d9;border-radius:4px;padding:2px 4px;font:inherit;background:#fff;cursor:pointer;"'
def repl3(m):
    code, name = m.group(1), m.group(2)
    oh = "".join(('<option selected>' + k + '</option>') if k == code else ('<option>' + k + '</option>') for k in opts)
    return '<tr><td><select class="tkMat" ' + sel_style + '>' + oh + '</select></td><td class="tkName">' + name + '</td>'
s2, n = pat.subn(repl3, s)
assert n == 3
save(p, s2)
print("OK 静态转select", p, n, "处·选项", opts)
wire(p,
     "/* 物料搜索下拉（2026-09-17 道远指示）：明细物料编码转搜索选择·物料名称跟随（demo-data products） */\r\n"
     "document.querySelectorAll('select.tkMat').forEach(function (s) {\r\n"
     "  SSEL.fillEntity(s, 'products', { label: function (k) { return k; } });\r\n"
     "  var nameTd = s.closest('tr').children[1];\r\n"
     "  var P = (window.DEMO_DATA || {}).products || {};\r\n"
     "  function nm(k) { var f = ((P[k] || {}).row || {}).fields || {}; return f.name || k; }\r\n"
     "  s.addEventListener('change', function () { nameTd.textContent = nm(s.value); });\r\n"
     "  nameTd.textContent = nm(s.value);\r\n"
     "});\r\n"
     "MSEL.attachAll('.edit-tbl select.tkMat', { placeholder: '输入编码搜索' });")

print("\n全部完成")
