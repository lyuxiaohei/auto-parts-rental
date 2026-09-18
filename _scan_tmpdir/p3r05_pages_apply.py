# -*- coding: utf-8 -*-
"""P3-R05 收口·页面层批量施工（标签 4 组 + 静态兜底区名化 + 调拨下拉接线）"""
import io, re

BASE = "P3-R01-包装租赁管理后台原型/"
FILES = {}

def ed(path, old, new, expect=1):
    FILES.setdefault(path, []).append((old, new, expect))

# 1 付款登记 列头
ed("财务协同/付款登记.html", "<th>付款银行</th>", "<th>付款账户</th>", 1)
# 2 付款新建 表单标签 + SSEL 定位
ed("财务协同/付款新建.html", "<div class=\"form-label\">付款银行：</div>", "<div class=\"form-label\">付款账户：</div>", 1)
ed("财务协同/付款新建.html", "byFormLabel('付款银行')", "byFormLabel('付款账户')", 1)
# 3 收款登记 筛选标签 + 列头 + cfg（三者须同改以保 readFilters 匹配）
ed("财务协同/收款登记.html", "<span class=\"ff-label\">银行账户：</span>", "<span class=\"ff-label\">收款账户：</span>", 1)
ed("财务协同/收款登记.html", "<th>银行账户</th>", "<th>收款账户</th>", 1)
ed("财务协同/收款登记.html", "{ label: '银行账户', field: 'bank' }", "{ label: '收款账户', field: 'bank' }", 1)
# 4 收款新建
ed("财务协同/收款新建.html", "<div class=\"form-label\">收款银行：</div>", "<div class=\"form-label\">收款账户：</div>", 1)
ed("财务协同/收款新建.html", "byFormLabel('收款银行')", "byFormLabel('收款账户')", 1)
# 5/6 其他入库/出库新建 静态兜底
ed("仓储作业/其他入库新建.html",
   "<option selected>原料区 RA</option><option>华东中心仓（WH-01）</option><option>华南仓（WH-02）</option><option>西南仓（WH-03）</option>",
   "<option selected>原料区 RA</option><option>成品区 RB</option><option>外购区 RW</option><option>次品区 RC</option>", 1)
ed("仓储作业/其他出库新建.html",
   "<option selected>成品区 RB</option><option>华东中心仓（WH-01）</option><option>华南仓（WH-02）</option><option>西南仓（WH-03）</option>",
   "<option selected>成品区 RB</option><option>原料区 RA</option><option>外购区 RW</option><option>次品区 RC</option>", 1)
# 7 调拨新建 调出/调入库房 + SSEL 接线
ed("仓储作业/调拨新建.html",
   "<option selected>原料区 RA</option><option>华东中心仓（WH-01）</option><option>华南仓（WH-02）</option><option>西南仓（WH-03）</option>",
   "<option selected>原料区 RA</option><option>成品区 RB</option><option>外购区 RW</option><option>次品区 RC</option>", 1)
ed("仓储作业/调拨新建.html",
   "<option selected>成品区 RB</option><option>华东中心仓（WH-01）</option><option>华南仓（WH-02）</option><option>西南仓（WH-03）</option>",
   "<option selected>成品区 RB</option><option>原料区 RA</option><option>外购区 RW</option><option>次品区 RC</option>", 1)
ed("仓储作业/调拨新建.html",
   "SSEL.fillEntity(SSEL.byFormLabel('物料'),'products',{label:function(k,f){return k+' '+(f.name||'');}});",
   "SSEL.fillEntity(SSEL.byFormLabel('物料'),'products',{label:function(k,f){return k+' '+(f.name||'');}});\r\nSSEL.fillEntity(SSEL.byFormLabel('调出库房'),'locations',{field:'wh'});\r\nSSEL.fillEntity(SSEL.byFormLabel('调入库房'),'locations',{field:'wh'});", 1)
# 9 库存查询 静态兜底 + append
ed("仓储作业/库存查询.html",
   "<option>正品仓</option><option>次品仓</option><option>客户虚拟仓</option><option>转租终端仓</option><option>上海一号库</option>",
   "<option>原料区 RA</option><option>成品区 RB</option><option>次品区 RC</option><option>客户虚拟仓</option><option>转租终端仓</option><option>上海一号库</option>", 1)
ed("仓储作业/库存查询.html", "append:['次品仓']", "append:['次品区 RC']", 1)
# 11 库位新建 placeholder
ed("基础数据/库位新建.html", "自定义输入，如 上海一号仓 / 正品仓", "自定义输入，如 原料区 RA / 成品区 RB", 1)
# 12 BOM维护 标注 pin 文案
ed("基础数据/BOM维护.html", "实际损耗走库位（次品仓）区分", "实际损耗走库位（次品区 RC）区分", 1)
# 13/14 退租入库新建 + 租赁出库录单（本轮新增的下拉静态兜底）
for f in ("租赁管理/退租入库新建.html", "租赁管理/租赁出库录单.html"):
    ed(f, "<option selected>正品仓</option><option>次品仓</option>",
       "<option selected>成品区 RB</option><option>原料区 RA</option><option>次品区 RC</option>", 1)

for path, edits in FILES.items():
    s = io.open(BASE + path, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    for old, new, expect in edits:
        o = old.replace("\n", "\r\n") if crlf else old
        n = new.replace("\n", "\r\n") if crlf else new
        cnt = s.count(o)
        assert cnt == expect, "%s: %r 计数 %d != %d" % (path, old[:50], cnt, expect)
        s = s.replace(o, n)
    io.open(BASE + path, "w", encoding="utf-8", newline="").write(s)
    print("OK", path, "(%d 处)" % len(edits))

# 库位档案：筛选兜底 + 静态行区名化 + 删 XNC 静态行
p = BASE + "基础数据/库位档案.html"
s = io.open(p, encoding="utf-8", newline="").read()
old_sel = "<option>正品仓</option><option>次品仓</option><option>客户虚拟仓（安吉智行）</option>"
assert s.count(old_sel) == 1
s = s.replace(old_sel, "<option>原料区 RA</option><option>成品区 RB</option><option>次品区 RC</option>")
ZONE = {"RA": "原料区 RA", "RB": "成品区 RB", "RC": "次品区 RC", "RD": "成品区 RB"}
keys = re.findall(r'<span class="lk">([A-Z]{2}-[A-Z0-9\-]+)</span>', s)
n = 0
for k in keys:
    if k == "XNC-AJZX":
        continue
    m = re.search(r'(<span class="lk">' + re.escape(k) + r'</span></td>\s*<td>)[^<]*(</td>)', s)
    assert m, "行未匹配: " + k
    s = s[:m.start()] + m.group(1) + ZONE[k[:2]] + m.group(2) + s[m.end():]
    n += 1
print("库位档案 静态行区名化:", n, "行")
# 删 XNC 静态行（<tr> … </tr>）
i = s.index('<span class="lk">XNC-AJZX</span>')
start = s.rfind("<tr>", 0, i)
end = s.index("</tr>", i) + len("</tr>")
end = s.index("\n", end) + 1 if "\n" in s[end:end+2] else end
removed = s[start:end]
assert "XNC-AJZX" in removed and len(removed) < 900
s = s[:start] + s[end:]
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("OK 基础数据/库位档案.html（筛选+行区名+删XNC 静态行）")
