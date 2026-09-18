# -*- coding: utf-8 -*-
"""采购订单列表：静态行补按钮 + 附件弹窗/打印脚本（与销售页同款）"""
import io

B = "P3-R01-包装租赁管理后台原型/"

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

p = B + "采购管理/采购订单列表.html"
s = io.open(p, encoding="utf-8", newline="").read()
assert "attModalFile" not in s
anchor = '<a onclick="go(\'../采购管理/采购订单审核.html\')">审核</a><a>关闭</a>'
n = s.count(anchor)
assert n >= 2, n
s = s.replace(anchor, '</a>'.join([anchor.rsplit('</a><a>关闭</a>', 1)[0]]) + '</a><a>关闭</a><a onclick="openAttModal(this)">上传附件</a><a onclick="orderPrint(this)">打印</a>' if False else anchor.replace('<a>关闭</a>', '<a>关闭</a><a onclick="openAttModal(this)">上传附件</a><a onclick="orderPrint(this)">打印</a>'))
assert s.count("</body>") == 1
s = s.replace("</body>", MODAL + JS + "</body>", 1)
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("OK 采购订单列表 静态行×", n)
