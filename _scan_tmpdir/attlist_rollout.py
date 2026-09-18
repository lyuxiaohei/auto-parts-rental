# -*- coding: utf-8 -*-
"""附件上传列表（2026-09-17 道远指示）：销售订单/采购订单新建——换掉旧附件区（销售）/新增（采购）"""
import io, re

B = "P3-R01-包装租赁管理后台原型/"

def att_card(demo_rows, back):
    rows = ""
    for name, size, who, t in demo_rows:
        icon = "📊" if name.endswith((".xlsx", ".xls", ".csv")) else ("📧" if name.endswith((".png", ".jpg", ".jpeg")) else "📄")
        rows += ('          <tr><td>%s %s</td><td>%s</td><td>%s</td><td>%s</td>'
                 '<td class="sticky-op"><span class="ops"><a onclick="delAttach(this)">删除</a></span></td></tr>\r\n') % (icon, name, size, who, t)
    return (
        '<div class="card">\r\n'
        '  <div class="card-head">\r\n'
        '    <h3 class="card-title">附件</h3>\r\n'
        '    <div class="head-btns"><button class="btn btn-dashed btn-sm" type="button" onclick="attPick(this)">📎 上传附件</button></div>\r\n'
        '  </div>\r\n'
        '  <div class="pn-hint">支持 PDF / 图片 / Excel，可多选 · 演示上传（文件不真实传输）</div>\r\n'
        '  <input type="file" id="attFilePick" multiple style="display:none">\r\n'
        '  <div class="table-wrap" style="border:1px solid var(--border);border-radius:6px;">\r\n'
        '    <table>\r\n'
        '      <thead><tr><th>文件名</th><th style="width:90px;">大小</th><th style="width:90px;">上传人</th><th style="width:120px;">上传时间</th><th class="sticky-op">操作</th></tr></thead>\r\n'
        '      <tbody id="attList">\r\n' + rows + '      </tbody>\r\n'
        '    </table>\r\n'
        '  </div>\r\n'
        '</div>\r\n'
    )

ATT_JS = (
    '<script>\r\n'
    '/* 附件上传列表（2026-09-17 道远指示）：真实文件选择器取文件名/大小（演示上传·不做真传输） */\r\n'
    'function attPick(btn) {\r\n'
    '  var pick = document.getElementById(\'attFilePick\');\r\n'
    '  if (!pick) return;\r\n'
    '  btn.style.borderColor = \'#1677ff\';\r\n'
    '  setTimeout(function () { btn.style.borderColor = \'\'; }, 300);\r\n'
    '  pick.click();\r\n'
    '}\r\n'
    'function delAttach(a) { var r = a.closest(\'tr\'); if (r) r.remove(); }\r\n'
    '(function () {\r\n'
    '  var pick = document.getElementById(\'attFilePick\');\r\n'
    '  if (!pick) return;\r\n'
    '  function esc(t) { return String(t).replace(/&/g, \'&amp;\').replace(/</g, \'&lt;\').replace(/>/g, \'&gt;\'); }\r\n'
    '  function fmtSize(n) {\r\n'
    '    if (n >= 1048576) return (n / 1048576).toFixed(1) + \' MB\';\r\n'
    '    if (n >= 1024) return (n / 1024).toFixed(0) + \' KB\';\r\n'
    '    return n + \' B\';\r\n'
    '  }\r\n'
    '  function now() {\r\n'
    '    var d = new Date();\r\n'
    '    function p(x) { return (x < 10 ? \'0\' : \'\') + x; }\r\n'
    '    return (d.getMonth() + 1) + \'-\' + p(d.getDate()) + \' \' + p(d.getHours()) + \':\' + p(d.getMinutes());\r\n'
    '  }\r\n'
    '  pick.addEventListener(\'change\', function () {\r\n'
    '    var list = document.getElementById(\'attList\');\r\n'
    '    Array.prototype.forEach.call(pick.files, function (f) {\r\n'
    '      var icon = /\\.(png|jpe?g|gif)$/i.test(f.name) ? \'📧\' : (/\\.(xlsx?|csv)$/i.test(f.name) ? \'📊\' : \'📄\');\r\n'
    '      var tr = document.createElement(\'tr\');\r\n'
    '      tr.innerHTML = \'<td>\' + icon + \' \' + esc(f.name) + \'</td><td>\' + fmtSize(f.size) + \'</td><td>当前用户</td><td>\' + now() + \'</td><td class="sticky-op"><span class="ops"><a onclick="delAttach(this)">删除</a></span></td>\';\r\n'
    '      list.appendChild(tr);\r\n'
    '    });\r\n'
    '    pick.value = \'\';\r\n'
    '  });\r\n'
    '})();\r\n'
    '</script>\r\n'
)

# ---- 1 销售订单新建：移除旧附件卡 + G13 假上传脚本，插入新列表 ----
p = B + "销售管理/销售订单新建.html"
s = io.open(p, encoding="utf-8", newline="").read()
i = s.index('<div class="card">\r\n  <div class="card-head">\r\n    <h3 class="card-title">订单附件</h3>')
j = s.index("</div>\r\n\r\n<div class=\"submit-bar\">", i) + len("</div>\r\n")
old_card = s[i:j]
assert "订单附件" in old_card and "attList" in old_card and len(old_card) < 1400, "旧附件卡边界异常"
s = s[:i] + att_card([
    ("PO-2601-围板箱采购合同.pdf", "1.2 MB", "陈锋", "09-16 16:40"),
    ("客户下单确认邮件截图.png", "356 KB", "沈婷", "09-17 09:12"),
], "../销售管理/") + s[j:]
# 移除 G13 假上传脚本块（addAttach/delAttach 旧实现）
k = s.index("<script>/* G13 ⑩ 订单附件假上传")
k2 = s.index("</script>", k) + len("</script>")
s = s[:k] + ATT_JS.replace("\r\n", "\r\n") + s[k2:]
assert "addAttach" not in s and s.count("attFilePick") == 3
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("OK 销售订单新建：旧附件区已换附件上传列表")

# ---- 2 采购订单新建：新增附件上传列表（原无附件区）----
p = B + "采购管理/采购订单新建.html"
s = io.open(p, encoding="utf-8", newline="").read()
assert "attFilePick" not in s
anchor = '<div class="submit-bar">'
assert s.count(anchor) == 1
s = s.replace(anchor, att_card([
    ("供应商报价单-甬城塑业.pdf", "860 KB", "林国栋", "09-17 08:55"),
    ("到货质检报告-0902批次.xlsx", "128 KB", "徐文", "09-17 09:30"),
], "../采购管理/") + ATT_JS + anchor, 1)
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("OK 采购订单新建：附件上传列表已插入")
