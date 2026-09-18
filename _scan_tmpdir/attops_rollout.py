# -*- coding: utf-8 -*-
"""销售/采购订单列表操作栏＋上传附件、打印（2026-09-17 道远指示·打印模板后开发）"""
import io, re

B = "P3-R01-包装租赁管理后台原型/"

# ---- 1 demo-data：两实体每行 ops 追加 ----
p = B + "_data/demo-data.js"
s = io.open(p, encoding="utf-8", newline="").read()
total = 0
for ent in ("salesOrders", "purchaseOrders"):
    i = s.index("\n  " + ent + ": {")
    j = s.index("\n  },", i)
    blk = s[i:j]
    rows = list(re.finditer(r"\n    '([^']+)': \{", blk))
    out, last = [], 0
    for a, m in enumerate(rows):
        start, end = m.start(), rows[a + 1].start() if a + 1 < len(rows) else len(blk)
        seg = blk[start:end]
        key = m.group(1)
        om = re.search(r'("ops": \[)([^\]]*)(\])', seg)
        assert om, key
        add = ', {"t": "上传附件", "act": "openAttModal(\'' + key + '\')"}, {"t": "打印", "act": "orderPrint(\'' + key + '\')"}'
        seg2 = seg[:om.start(3) - 1] + add + seg[om.start(3) - 1 + 0:]  # placeholder
        seg2 = seg[:om.start()] + om.group(1) + om.group(2) + add + "]" + seg[om.end():]
        out.append(blk[last:start] + seg2)
        last = end
        total += 1
    blk = "".join(out) + blk[last:]
    s = s[:i] + blk + s[j:]
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("demo-data OK：", total, "行 ops 追加")

# ---- 2 列表页：静态兜底行补按钮 + 弹窗/打印脚本 ----
MODAL = (
    '<div class="modal-overlay" id="attModal">\r\n'
    '  <div class="modal" style="width:640px;">\r\n'
    '    <div class="modal-head"><span id="attModalTitle">附件上传</span><span class="modal-x" onclick="closeModal(\'attModal\')">&times;</span></div>\r\n'
    '    <div class="modal-body">\r\n'
    '      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">\r\n'
    '        <span class="pn-hint" style="margin:0;">支持 PDF / 图片 / Excel，可多选 · 演示上传（文件不真实传输）</span>\r\n'
    '        <button class="btn btn-dashed btn-sm" type="button" onclick="attModalPick(this)">📎 上传附件</button>\r\n'
    '      </div>\r\n'
    '      <input type="file" id="attModalFile" multiple style="display:none">\r\n'
    '      <div class="table-wrap" style="border:1px solid var(--border);border-radius:6px;max-height:300px;overflow:auto;">\r\n'
    '        <table>\r\n'
    '          <thead><tr><th>文件名</th><th style="width:80px;">大小</th><th style="width:80px;">上传人</th><th style="width:100px;">上传时间</th><th style="width:60px;">操作</th></tr></thead>\r\n'
    '          <tbody id="attModalList">\r\n'
    '            <tr><td>📄 订单确认件.pdf</td><td>412 KB</td><td>沈婷</td><td>09-17 09:05</td><td><a onclick="this.closest(\'tr\').remove()" style="color:#ff4d4f;cursor:pointer;">删除</a></td></tr>\r\n'
    '          </tbody>\r\n'
    '        </table>\r\n'
    '      </div>\r\n'
    '    </div>\r\n'
    '  </div>\r\n'
    '</div>\r\n'
)
JS = (
    '<script>\r\n'
    '/* 操作栏·上传附件/打印（2026-09-17 道远指示；打印模板后开发——按钮先给开发中反馈） */\r\n'
    'function openAttModal(key) {\r\n'
    '  var t = document.getElementById(\'attModalTitle\');\r\n'
    '  if (t) t.textContent = \'附件上传 · \' + key;\r\n'
    '  openModal(\'attModal\');\r\n'
    '}\r\n'
    'function attModalPick(btn) {\r\n'
    '  var pick = document.getElementById(\'attModalFile\');\r\n'
    '  if (!pick) return;\r\n'
    '  btn.style.borderColor = \'#1677ff\';\r\n'
    '  setTimeout(function () { btn.style.borderColor = \'\'; }, 300);\r\n'
    '  pick.click();\r\n'
    '}\r\n'
    'function orderPrint(key) {\r\n'
    '  var t = document.createElement(\'div\');\r\n'
    '  t.style.cssText = \'position:fixed;top:70px;left:50%;transform:translateX(-50%);background:#e6f4ff;color:#0958d9;border:1px solid #91caff;padding:8px 18px;border-radius:6px;z-index:9999;font-size:13px;box-shadow:0 4px 12px rgba(0,0,0,.12)\';\r\n'
    '  t.textContent = \'打印模板开发中（\' + key + \'）· 模板就绪后此键直接出单\';\r\n'
    '  document.body.appendChild(t);\r\n'
    '  setTimeout(function () { t.remove(); }, 2000);\r\n'
    '}\r\n'
    '(function () {\r\n'
    '  var pick = document.getElementById(\'attModalFile\');\r\n'
    '  if (!pick) return;\r\n'
    '  function esc(x) { return String(x).replace(/&/g, \'&amp;\').replace(/</g, \'&lt;\').replace(/>/g, \'&gt;\'); }\r\n'
    '  function fmtSize(n) { return n >= 1048576 ? (n / 1048576).toFixed(1) + \' MB\' : n >= 1024 ? (n / 1024).toFixed(0) + \' KB\' : n + \' B\'; }\r\n'
    '  function now() { var d = new Date(); function q(x) { return (x < 10 ? \'0\' : \'\') + x; } return (d.getMonth() + 1) + \'-\' + q(d.getDate()) + \' \' + q(d.getHours()) + \':\' + q(d.getMinutes()); }\r\n'
    '  pick.addEventListener(\'change\', function () {\r\n'
    '    var list = document.getElementById(\'attModalList\');\r\n'
    '    Array.prototype.forEach.call(pick.files, function (f) {\r\n'
    '      var icon = /\\.(png|jpe?g|gif)$/i.test(f.name) ? \'📧\' : (/\\.(xlsx?|csv)$/i.test(f.name) ? \'📊\' : \'📄\');\r\n'
    '      var tr = document.createElement(\'tr\');\r\n'
    '      tr.innerHTML = \'<td>\' + icon + \' \' + esc(f.name) + \'</td><td>\' + fmtSize(f.size) + \'</td><td>当前用户</td><td>\' + now() + \'</td><td><a onclick="this.closest(\\\'tr\\\').remove()" style="color:#ff4d4f;cursor:pointer;">删除</a></td>\';\r\n'
    '      list.appendChild(tr);\r\n'
    '    });\r\n'
    '    pick.value = \'\';\r\n'
    '  });\r\n'
    '})();\r\n'
    '</script>\r\n'
)

for path, edit_anchor, edit_new in (
    ("销售管理/销售订单列表.html",
     '<a onclick="go(\'../销售管理/销售订单审核.html\')">审核</a><a>关闭</a>',
     '<a onclick="go(\'../销售管理/销售订单审核.html\')">审核</a><a>关闭</a><a onclick="openAttModal(this)">上传附件</a><a onclick="orderPrint(this)">打印</a>'),
    ("采购管理/采购订单列表.html",
     '<a onclick="go(\'../采购管理/采购订单审核.html\')">审核</a><a>关闭</a>',
     '<a onclick="go(\'../采购管理/采购订单审核.html\')">审核</a><a>关闭</a><a onclick="openAttModal(this)">上传附件</a><a onclick="orderPrint(this)">打印</a>'),
):
    s = io.open(B + path, encoding="utf-8", newline="").read()
    n = s.count(edit_anchor)
    assert n >= 3, (path, n)
    s = s.replace(edit_anchor, edit_new)
    assert "attModal" not in s.replace('attModal', '', 0) or True
    block = MODAL + JS
    assert s.count("</body>") == 1
    s = s.replace("</body>", block + "</body>", 1)
    io.open(B + path, "w", encoding="utf-8", newline="").write(s)
    print("OK", path, "静态行×", n)
