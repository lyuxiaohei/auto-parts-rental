# -*- coding: utf-8 -*-
"""P3-R05 收口追加批·单据库位显示仓库名称 + 列表库位列批量设置按钮
用户拍板：标签保持「XX库位」不变；值显示仓库名称（库位编码是独立字段）；
列表列头旁加「批量设置」按钮对勾选行批量设置。"""
import io, re

BASE = "P3-R01-包装租赁管理后台原型/"
ZONE = {"RA": "原料区 RA", "RB": "成品区 RB", "RC": "次品区 RC", "RD": "成品区 RB"}

# ---- 1) demo-data：详情 fees 单元格编码 → 区名（列头「库位」名保留·用户拍板） ----
P = BASE + "_data/demo-data.js"
s = io.open(P, encoding="utf-8", newline="").read()
total = 0
for ent in ("comboOutbounds", "purchaseInbounds", "salesOutbounds"):
    i = s.index("\n  " + ent + ": {")
    j = s.index("\n  },", i)
    blk = s[i:j]

    def cellmap(m):
        global total
        code = m.group(1)
        wh = ZONE.get(code[:2], "成品区 RB")
        total += 1
        return "('" + wh + "')"

    blk2 = re.sub(r"'(R[A-Z]-[A-Z0-9\-]+)'", cellmap, blk)
    s = s[:i] + blk2 + s[j:]
    print(ent, "fees 编码→区名:", blk2.count("成品区 RB") + blk2.count("原料区 RA") + blk2.count("次品区 RC") - blk.count("成品区 RB") - blk.count("原料区 RA") - blk.count("次品区 RC"))
io.open(P, "w", encoding="utf-8", newline="").write(s)
print("demo-data 合计替换:", total, "| 残留单引号编码:", len(re.findall(r"'R[A-Z]-[A-Z0-9\-]+'", s)))

# ---- 2) 采购入库录单：明细假下拉显示值（标签「入库库位」保留） ----
P = BASE + "采购管理/采购入库录单.html"
s = io.open(P, encoding="utf-8", newline="").read()
for old, new in ((">RA-A-01-01<", ">原料区 RA<"), (">RA-A-01-02<", ">原料区 RA<"), (">RA-B-02-01<", ">成品区 RB<")):
    assert s.count(old) == 1, (old, s.count(old))
    s = s.replace(old, new)
io.open(P, "w", encoding="utf-8", newline="").write(s)
print("采购入库录单 显示值 3 处 OK")

# ---- 3) 七个出入库列表：列头旁批量设置按钮 + 弹窗 + 脚本 ----
SNIP = (
    '<div id="batchLocModal" style="position:fixed;inset:0;background:rgba(0,0,0,.45);display:none;align-items:center;justify-content:center;z-index:1000;">'
    '<div style="background:#fff;border-radius:8px;width:380px;box-shadow:0 12px 32px rgba(0,0,0,.18);">'
    '<div style="display:flex;justify-content:space-between;align-items:center;padding:14px 20px;border-bottom:1px solid #f0f0f0;font-size:15px;font-weight:600;">'
    '<span id="batchLocTitle">批量设置库位</span><span style="cursor:pointer;color:#8c8c8c;font-size:18px;line-height:1;" onclick="closeBatchLoc()">&times;</span></div>'
    '<div style="padding:18px 20px;">'
    '<div style="display:flex;align-items:center;"><div style="flex:0 0 80px;text-align:right;margin-right:8px;font-size:13px;">库房：</div>'
    '<div class="input-box select-box" style="width:220px;"><select id="batchLocSel" style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option>原料区 RA</option><option selected>成品区 RB</option><option>外购区 RW</option><option>次品区 RC</option></select><span class="caret">&#9662;</span></div></div>'
    '<div style="margin-top:12px;font-size:12px;color:#8c8c8c;">对已勾选行批量设置库位；请先在列表勾选行。</div>'
    '</div>'
    '<div style="display:flex;justify-content:flex-end;gap:10px;padding:12px 20px;border-top:1px solid #f0f0f0;"><button class="btn btn-default" onclick="closeBatchLoc()">取 消</button><button class="btn" onclick="applyBatchLoc()">确 定</button></div>'
    '</div></div>'
    '<script>\r\n'
    '/* 列头批量设置库位（P3-R05 收口·演示交互）：按勾选行改写本列单元格 */\r\n'
    'function openBatchLoc(btn){var th=btn.closest("th");window.__batchColIdx=Array.prototype.indexOf.call(th.parentElement.children,th);window.__batchColName=th.childNodes[0].textContent.trim();document.getElementById("batchLocTitle").textContent="批量设置"+window.__batchColName;document.getElementById("batchLocModal").style.display="flex";}\r\n'
    'function closeBatchLoc(){document.getElementById("batchLocModal").style.display="none";}\r\n'
    'function applyBatchLoc(){var rows=Array.prototype.filter.call(document.querySelectorAll("tbody tr"),function(tr){var cb=tr.querySelector("input.cb");return cb&&cb.checked;});\r\n'
    'if(!rows.length){batchLocToast("请先勾选要设置的行",true);return;}\r\n'
    'var v=document.getElementById("batchLocSel").value;\r\n'
    'rows.forEach(function(tr){var td=tr.children[window.__batchColIdx];if(td)td.textContent=v;});\r\n'
    'closeBatchLoc();batchLocToast("已批量设置 "+rows.length+" 行「"+window.__batchColName+"」");}\r\n'
    'function batchLocToast(msg,warn){var t=document.createElement("div");t.style.cssText="position:fixed;top:70px;left:50%;transform:translateX(-50%);background:"+(warn?"#fff7e6":"#f6ffed")+";color:"+(warn?"#d46b08":"#389e0d")+";border:1px solid "+(warn?"#ffd591":"#b7eb8f")+";padding:8px 18px;border-radius:6px;z-index:9999;font-size:13px;box-shadow:0 4px 12px rgba(0,0,0,.12)";t.textContent=msg;document.body.appendChild(t);setTimeout(function(){t.remove();},1800);}\r\n'
    '</script>\r\n'
)

PAGES = [
    ("采购管理/采购入库列表.html", ["入库库房"]),
    ("租入管理/租入入库列表.html", ["入库库房"]),
    ("租赁管理/退租入库列表.html", ["入库库房"]),
    ("仓储作业/其他入库列表.html", ["入库库房"]),
    ("仓储作业/其他出库列表.html", ["出库库房"]),
    ("销售管理/销售出库列表.html", ["出库库房"]),
    ("仓储作业/库存调拨列表.html", ["调出库房", "调入库房"]),
]
for path, cols in PAGES:
    p = BASE + path
    s = io.open(p, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    nl = "\r\n" if crlf else "\n"
    for col in cols:
        old = "<th>" + col + "</th>"
        assert s.count(old) == 1, path + " 列头异常: " + col
        btn = '<a onclick="openBatchLoc(this)" style="font-size:12px;font-weight:400;color:#1677ff;cursor:pointer;margin-left:8px;">批量设置</a>'
        s = s.replace(old, "<th>" + col + btn + "</th>", 1)
    assert s.count("</body>") == 1
    snip = SNIP.replace("\r\n", nl)
    s = s.replace("</body>", snip + "</body>", 1)
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("OK", path, "列头按钮×%d + 弹窗脚本" % len(cols))
