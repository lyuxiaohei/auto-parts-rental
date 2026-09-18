# -*- coding: utf-8 -*-
"""批量设置库位按钮·位置更正（道远 09-17）：撤 7 列表页误加按钮，改加在采购入库录单明细表「入库库位」列头旁"""
import io, re

BASE = "P3-R01-包装租赁管理后台原型/"
BTN = '<a onclick="openBatchLoc(this)" style="font-size:12px;font-weight:400;color:#1677ff;cursor:pointer;margin-left:8px;">批量设置</a>'

# ---- 1) 撤销 7 个列表页（列头按钮 + 弹窗脚本块） ----
LISTS = [
    ("采购管理/采购入库列表.html", ["入库库房"]),
    ("租入管理/租入入库列表.html", ["入库库房"]),
    ("租赁管理/退租入库列表.html", ["入库库房"]),
    ("仓储作业/其他入库列表.html", ["入库库房"]),
    ("仓储作业/其他出库列表.html", ["出库库房"]),
    ("销售管理/销售出库列表.html", ["出库库房"]),
    ("仓储作业/库存调拨列表.html", ["调出库房", "调入库房"]),
]
for path, cols in LISTS:
    p = BASE + path
    s = io.open(p, encoding="utf-8", newline="").read()
    for col in cols:
        old = "<th>" + col + BTN + "</th>"
        assert s.count(old) == 1, path + " " + col + " 按钮计数异常"
        s = s.replace(old, "<th>" + col + "</th>", 1)
    i = s.index('<div id="batchLocModal"')
    j = s.index("</body>")
    assert i < j and "applyBatchLoc" in s[i:j]
    s = s[:i] + s[j:]
    assert "openBatchLoc" not in s and "batchLocModal" not in s, path + " 残留"
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("已撤销", path)

# ---- 2) 采购入库录单：明细表「入库库位」列头旁加按钮 + 弹窗脚本 ----
P = BASE + "采购管理/采购入库录单.html"
s = io.open(P, encoding="utf-8", newline="").read()
crlf = "\r\n" in s
nl = "\r\n" if crlf else "\n"

old_th = "<th>入库库位</th>"
assert s.count(old_th) == 1, "入库库位列头计数异常: %d" % s.count(old_th)
s = s.replace(old_th, "<th>入库库位" + BTN + "</th>", 1)

SNIP = (
    '<div id="batchLocModal" style="position:fixed;inset:0;background:rgba(0,0,0,.45);display:none;align-items:center;justify-content:center;z-index:1000;">'
    '<div style="background:#fff;border-radius:8px;width:380px;box-shadow:0 12px 32px rgba(0,0,0,.18);">'
    '<div style="display:flex;justify-content:space-between;align-items:center;padding:14px 20px;border-bottom:1px solid #f0f0f0;font-size:15px;font-weight:600;">'
    '<span>批量设置入库库位</span><span style="cursor:pointer;color:#8c8c8c;font-size:18px;line-height:1;" onclick="closeBatchLoc()">&times;</span></div>'
    '<div style="padding:18px 20px;">'
    '<div style="display:flex;align-items:center;"><div style="flex:0 0 80px;text-align:right;margin-right:8px;font-size:13px;">库房：</div>'
    '<div class="input-box select-box" style="width:220px;"><select id="batchLocSel" style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option>原料区 RA</option><option selected>成品区 RB</option><option>外购区 RW</option><option>次品区 RC</option></select><span class="caret">&#9662;</span></div></div>'
    '<div style="margin-top:12px;font-size:12px;color:#8c8c8c;">对明细表全部行设置入库库位。</div>'
    '</div>'
    '<div style="display:flex;justify-content:flex-end;gap:10px;padding:12px 20px;border-top:1px solid #f0f0f0;"><button class="btn btn-default" onclick="closeBatchLoc()">取 消</button><button class="btn" onclick="applyBatchLoc()">确 定</button></div>'
    '</div></div>'
    '<script>' + nl +
    '/* 明细表批量设置入库库位（P3-R05·道远 09-17 指示：加载明细的字段名旁）：对明细全部行改写该列 */' + nl +
    'function openBatchLoc(btn){document.getElementById("batchLocModal").style.display="flex";}' + nl +
    'function closeBatchLoc(){document.getElementById("batchLocModal").style.display="none";}' + nl +
    'function applyBatchLoc(){var th=[...document.querySelectorAll("th")].find(function(t){return t.textContent.replace("批量设置","").trim()==="入库库位";});' + nl +
    'if(!th){closeBatchLoc();return;}' + nl +
    'var idx=Array.prototype.indexOf.call(th.parentElement.children,th);' + nl +
    'var v=document.getElementById("batchLocSel").value;var n=0;' + nl +
    'document.querySelectorAll("tbody tr").forEach(function(tr){var td=tr.children[idx];if(!td)return;' + nl +
    'var sp=td.querySelector(".v");if(sp)sp.textContent=v;else td.textContent=v;n++;});' + nl +
    'closeBatchLoc();batchLocToast("已批量设置 "+n+" 行入库库位");}' + nl +
    'function batchLocToast(msg){var t=document.createElement("div");t.style.cssText="position:fixed;top:70px;left:50%;transform:translateX(-50%);background:#f6ffed;color:#389e0d;border:1px solid #b7eb8f;padding:8px 18px;border-radius:6px;z-index:9999;font-size:13px;box-shadow:0 4px 12px rgba(0,0,0,.12)";t.textContent=msg;document.body.appendChild(t);setTimeout(function(){t.remove();},1800);}' + nl +
    '</script>' + nl
)
assert s.count("</body>") == 1
s = s.replace("</body>", SNIP + "</body>", 1)
io.open(P, "w", encoding="utf-8", newline="").write(s)
print("采购入库录单 明细列头按钮 + 弹窗脚本 OK（行尾 %s）" % ("CRLF" if crlf else "LF"))
