# -*- coding: utf-8 -*-
"""客商收货信息：列表 ops +收货信息按钮（demo-data partners×8 + 客商管理.html 静态行×8）
+ 列表页新增 recvInfoModal + 弹窗/客商收货信息.html 模板（镜像客商开票资料.html）。
纪律：读取-精确替换+assert；newline='' 保 EOL；改后 node --check。"""
import io, sys, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

# ---------- ① demo-data.js partners ops ×8 ----------
P = ROOT + r'\_data\demo-data.js'
t = io.open(P, encoding='utf-8', newline='').read()
assert t.count('\r\n') > 1000
A_OPS = '"开票资料", "act": "openModal(\'invoiceInfoModal\')"}]'
N_OPS = ('"开票资料", "act": "openModal(\'invoiceInfoModal\')"}, '
         '{"t": "收货信息", "act": "openModal(\'recvInfoModal\')"}]')
if t.count(A_OPS) == 8:
    assert t.count('收货信息') == 0 and t.count('recvInfoModal') == 0, '幂等：收货信息已存在'
    t = t.replace(A_OPS, N_OPS)
    assert t.count('recvInfoModal') == 8
    io.open(P, 'w', encoding='utf-8', newline='').write(t)
    print('PASS ① demo-data.js partners ops ×8 +收货信息')
else:
    assert t.count(N_OPS) == 8, 'ops 既非改前也非改后态：A=%d N=%d' % (t.count(A_OPS), t.count(N_OPS))
    print('SKIP ① demo-data.js 已是改后态')

# ---------- ② 客商管理.html：静态 ops ×8 + recvInfoModal ----------
P2 = ROOT + r'\基础数据\客商管理.html'
t = io.open(P2, encoding='utf-8', newline='').read()
crlf = t.count('\r\n')
assert crlf > 500, '客商管理应为 CRLF'
if t.count('recvInfoModal') == 12:
    print('SKIP ② 客商管理.html 已是改后态')
else:
    assert t.count('收货信息') == 0, '幂等：页面已有收货信息'

    A_ST = '<a onclick="openModal(\'invoiceInfoModal\')">开票资料</a></span></td>'
    n = t.count(A_ST)
    assert n == 8, '静态 ops 锚 %d≠8' % n
    N_ST = ('<a onclick="openModal(\'invoiceInfoModal\')">开票资料</a>'
            '<a onclick="openModal(\'recvInfoModal\')">收货信息</a></span></td>')
    t = t.replace(A_ST, N_ST)
    assert t.count(N_ST) == 8

    MODAL = (
        '\r\n<!-- 收货信息维护（独立弹窗·收货人/收货电话/收货地址，与联系人/联系电话商务信息区分·参照开票资料先例） -->\r\n'
        '<div class="modal-overlay" id="recvInfoModal">\r\n'
        '  <div class="modal" style="width:640px">\r\n'
        '    <div class="modal-header">\r\n'
        '      <h3 class="modal-title">收货信息</h3>\r\n'
        '      <span class="modal-close" onclick="closeModal(\'recvInfoModal\')">×</span>\r\n'
        '    </div>\r\n'
        '    <div class="modal-body">\r\n'
        '<div class="form-row">\r\n'
        '    <span class="form-label">收货人</span>\r\n'
        '    <div class="input-box"><input value="袁明" placeholder="请输入"></div>\r\n'
        '  </div><div class="form-row">\r\n'
        '    <span class="form-label">收货电话</span>\r\n'
        '    <div class="input-box"><input value="138****6621" placeholder="请输入"></div>\r\n'
        '  </div><div class="form-row">\r\n'
        '    <span class="form-label">收货地址</span>\r\n'
        '    <div class="input-box"><input value="吉林省长春市汽开区东风大街 2222 号 · 1 号收货口" placeholder="请输入"></div>\r\n'
        '  </div>\r\n'
        '    </div>\r\n'
        '    <div class="modal-footer">\r\n'
        '      <button class="btn btn-default" onclick="closeModal(\'recvInfoModal\')">取消</button>\r\n'
        '      <button class="btn" onclick="closeModal(\'recvInfoModal\')">保存</button>\r\n'
        '    </div>\r\n'
        '  </div>\r\n'
        '</div>\r\n')
    A_INS = ('      <button class="btn" onclick="closeModal(\'invoiceInfoModal\')">保存</button>\r\n'
             '    </div>\r\n'
             '  </div>\r\n'
             '</div>\r\n')
    assert t.count(A_INS) == 1, '插入锚 %d≠1' % t.count(A_INS)
    t = t.replace(A_INS, A_INS + MODAL)

    assert t.count('<div') == t.count('</div>'), 'div 配平 %d/%d' % (t.count('<div'), t.count('</div>'))
    assert t.count('recvInfoModal') == 12, 'recvInfoModal 计数异常 %d' % t.count('recvInfoModal')  # 弹窗 id1+close×3+静态 ops×8
    io.open(P2, 'w', encoding='utf-8', newline='').write(t)
    print('PASS ② 客商管理.html：静态 ops×8 + recvInfoModal（div 配平·CRLF %d 行保持）' % crlf)

# ---------- ③ 弹窗/客商收货信息.html 模板（镜像开票资料模板） ----------
SRC = ROOT + r'\基础数据\弹窗\客商开票资料.html'
DST = ROOT + r'\基础数据\弹窗\客商收货信息.html'
s = io.open(SRC, encoding='utf-8', newline='').read()
assert s.count('收货信息') == 0
s = s.replace('<title>客商开票资料 - 包装租赁管理后台</title>',
              '<title>客商收货信息 - 包装租赁管理后台</title>')
assert s.count('<title>客商收货信息') == 1
s = s.replace('<!-- 弹窗模板：新建客商（createModal） -->',
              '<!-- 弹窗模板：收货信息（recvInfoModal） -->')
s = s.replace('createModal', 'recvInfoModal')
assert s.count('recvInfoModal') >= 4
# 表单区整体替换：modal-body 后第一段 → modal-footer 前（末尾补 modal-body 闭合——源模板此处缺一个 </div>·我的模板修正不继承）
i0 = s.find('<div class="modal-body">')
i1 = s.find('<div class="modal-footer">', i0)
assert 0 < i0 < i1
ROWS = ('<div class="form-row">\r\n'
        '    <span class="form-label">收货人</span>\r\n'
        '    <div class="input-box"><input value="袁明" placeholder="请输入"></div>\r\n'
        '  </div><div class="form-row">\r\n'
        '    <span class="form-label">收货电话</span>\r\n'
        '    <div class="input-box"><input value="138****6621" placeholder="请输入"></div>\r\n'
        '  </div><div class="form-row">\r\n'
        '    <span class="form-label">收货地址</span>\r\n'
        '    <div class="input-box"><input value="吉林省长春市汽开区东风大街 2222 号 · 1 号收货口" placeholder="请输入"></div>\r\n'
        '  </div>\r\n'
        '    </div>\r\n'
        '    ')
s = s[:i0] + '<div class="modal-body">\r\n' + ROWS + s[i1:]
assert s.count('发票类型') == 0 and s.count('结算周期') == 0, '模板旧字段残留'
assert s.count('<div') == s.count('</div>'), '模板 div 配平 %d/%d' % (s.count('<div'), s.count('</div>'))
# 模板页保持源文件行尾（探测）
src_crlf = io.open(SRC, encoding='utf-8', newline='').read().count('\r\n')
if src_crlf == 0:
    s = s.replace('\r\n', '\n')
io.open(DST, 'w', encoding='utf-8', newline='').write(s)
print('PASS ③ 弹窗/客商收货信息.html 模板生成（镜像·EOL %s）' % ('CRLF' if src_crlf else 'LF'))

# ---------- node --check ----------
r = subprocess.run(['node', '--check', ROOT + r'\_data\demo-data.js'], capture_output=True, text=True)
assert r.returncode == 0, r.stderr[:200]
print('PASS node --check demo-data.js')
