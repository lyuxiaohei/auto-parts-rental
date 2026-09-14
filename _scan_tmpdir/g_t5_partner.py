# -*- coding: utf-8 -*-
"""T5 客商管理开票资料改造：
A 客商管理.html(CRLF)：createModal 删开票资料行+新增 invoiceInfoModal（含结算周期）+9 行按钮改指
B demo-data.js(CRLF)：partners 8 键 ops 开票资料→invoiceInfoModal+node --check
C 弹窗/新建客商.html(LF)：删开票资料行
D 新建 弹窗/客商开票资料.html(LF)：由新建客商模板派生（标题/弹窗体/发票字段+结算周期）
"""
import io, subprocess

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
SELSTYLE = "style=\"flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;\""
CARET = "<span class=\"caret\"><svg width=\"12\" height=\"12\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><polyline points=\"6 9 12 15 18 9\"/></svg></span>"

INVOICE_ROW_TPL = ("<div class=\"form-row\">{NL}"
    "    <span class=\"form-label\">{LABEL}</span>{NL}"
    "    <div class=\"input-box\"><input {ATTR}></div>{NL}"
    "  </div>")

def invoice_rows(nl):
    def row(label, attr):
        return INVOICE_ROW_TPL.format(NL=nl, LABEL=label, ATTR=attr)
    def selrow(label, req, options, selected):
        opts = "".join("<option%s>%s</option>" % (" selected" if o == selected else "", o) for o in options)
        return ("<div class=\"form-row\">" + nl +
                "    <span class=\"form-label\">" + ("<span class=\"req\">*</span>" if req else "") + label + "</span>" + nl +
                "    <div class=\"input-box select-box\"><select " + SELSTYLE + ">" + opts + "</select>" + CARET + "</div>" + nl +
                "  </div>")
    return (
        row("单位名称", "value=\"一汽解放汽车有限公司\" placeholder=\"请输入\"") +
        selrow("发票类型", False, ["增值税专用发票（13%）", "增值税普通发票"], "增值税专用发票（13%）") +
        row("纳税人识别号", "value=\"91220100MA100000XX\" placeholder=\"请输入\"") +
        row("开户银行", "value=\"中国工商银行长春第一汽车厂支行\" placeholder=\"请输入\"") +
        row("银行账号", "value=\"4200 6710 0987 6543 210\" placeholder=\"请输入\"") +
        selrow("结算周期", True, ["月结 30 天", "月结 60 天", "预付款", "货到付款"], "月结 30 天") +
        row("备注", "placeholder=\"选填\"")
    )

def modal_block(nl, width):
    return ("<!-- 开票资料维护（独立弹窗·开票资料单独维护·含结算周期） -->" + nl +
            "<div class=\"modal-overlay\" id=\"invoiceInfoModal\">" + nl +
            "  <div class=\"modal\" style=\"width:" + width + "\">" + nl +
            "    <div class=\"modal-header\">" + nl +
            "      <h3 class=\"modal-title\">开票资料</h3>" + nl +
            "      <span class=\"modal-close\" onclick=\"closeModal('invoiceInfoModal')\">×</span>" + nl +
            "    </div>" + nl +
            "    <div class=\"modal-body\">" + nl +
            invoice_rows(nl) +
            "    </div>" + nl +
            "    <div class=\"modal-footer\">" + nl +
            "      <button class=\"btn btn-default\" onclick=\"closeModal('invoiceInfoModal')\">取消</button>" + nl +
            "      <button class=\"btn\" onclick=\"closeModal('invoiceInfoModal')\">保存</button>" + nl +
            "    </div>" + nl +
            "  </div>" + nl +
            "</div>")

# ---------- A 客商管理.html ----------
fp = ROOT + r"\基础数据\客商管理.html"
raw = open(fp, "rb").read()
c0 = raw.count(b"\r\n")
t = io.open(fp, encoding="utf-8", newline="").read()
NL = "\r\n"
if 'openModal(\'invoiceInfoModal\')\">开票资料' in t:
    print("SKIP A 已完成")
else:
    ROW_OLD = ("<div class=\"form-row\">" + NL +
               "    <span class=\"form-label\">开票资料</span>" + NL +
               "    <div class=\"input-box select-box\"><select " + SELSTYLE + "><option selected>增值税专票 13%</option><option>增值税专用发票（13%）</option><option>增值税普通发票</option></select>" + CARET + "</div>" + NL +
               "  </div>")
    assert t.count(ROW_OLD) == 1, "A1 row 锚点=%d" % t.count(ROW_OLD)
    t = t.replace(ROW_OLD, "", 1)
    anchor = NL + NL + NL + "<script id=\"batch-btn-js\">"
    assert t.count(anchor) == 1, "A2 插入锚=%d" % t.count(anchor)
    t = t.replace(anchor, NL + NL + NL + modal_block(NL, "640px") + anchor, 1)
    n_btn = t.count("<a onclick=\"openModal('createModal')\">开票资料</a>")
    assert n_btn == 8, "A3 按钮=%d" % n_btn
    t = t.replace("<a onclick=\"openModal('createModal')\">开票资料</a>",
                  "<a onclick=\"openModal('invoiceInfoModal')\">开票资料</a>")
    io.open(fp, "w", encoding="utf-8", newline="").write(t)
    raw2 = open(fp, "rb").read()
    print("PASS A 客商管理.html：行删+新弹窗+9 按钮改指·CRLF=%d（%+d）" % (raw2.count(b"\r\n"), raw2.count(b"\r\n") - c0))

# ---------- B demo-data.js ----------
fp = ROOT + r"\_data\demo-data.js"
t = io.open(fp, encoding="utf-8", newline="").read()
if "invoiceInfoModal" in t:
    print("SKIP B 已完成")
else:
    OLD = "\"t\": \"开票资料\", \"act\": \"openModal('createModal')\""
    NEW = "\"t\": \"开票资料\", \"act\": \"openModal('invoiceInfoModal')\""
    n = t.count(OLD)
    assert n == 8, "B ops=%d" % n
    t = t.replace(OLD, NEW)
    io.open(fp, "w", encoding="utf-8", newline="").write(t)
    r = subprocess.run(["node", "--check", fp], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[:200]
    print("PASS B demo-data partners ops×8 改指·node --check 0")

# ---------- C 弹窗/新建客商.html ----------
fp = ROOT + r"\基础数据\弹窗\新建客商.html"
t = io.open(fp, encoding="utf-8", newline="").read()
NL = "\n"
ROW_OLD = ("<div class=\"form-row\">" + NL +
           "    <span class=\"form-label\">开票资料</span>" + NL +
           "    <div class=\"input-box select-box\"><select " + SELSTYLE + "><option selected>增值税专票 13%</option><option>增值税专用发票（13%）</option><option>增值税普通发票</option></select>" + CARET + "</div>" + NL +
           "  </div>")
if ROW_OLD in t:
    assert t.count(ROW_OLD) == 1
    t = t.replace(ROW_OLD, "", 1)
    io.open(fp, "w", encoding="utf-8", newline="").write(t)
    print("PASS C 新建客商模板删开票资料行")
else:
    print("SKIP C 已完成")

# ---------- D 新建 弹窗/客商开票资料.html ----------
fp_new = ROOT + r"\基础数据\弹窗\客商开票资料.html"
import os
if os.path.exists(fp_new):
    print("SKIP D 已存在")
else:
    t = io.open(ROOT + r"\基础数据\弹窗\新建客商.html", encoding="utf-8", newline="").read()
    NL = "\n"
    t = t.replace("<title>新建客商 - 包装租赁管理后台</title>", "<title>客商开票资料 - 包装租赁管理后台</title>", 1)
    t = t.replace("<h3 class=\"modal-title\">新建客商</h3>", "<h3 class=\"modal-title\">开票资料</h3>", 1)
    bi = t.find("<div class=\"modal-body\">", t.find("id=\"createModal\""))
    fi = t.find("<div class=\"modal-footer\">", bi)
    assert bi > 0 and fi > bi, "D body/footer 定位失败"
    t = t[:bi + len("<div class=\"modal-body\">")] + NL + invoice_rows(NL) + "    " + t[fi:]
    io.open(fp_new, "w", encoding="utf-8", newline="").write(t)
    print("PASS D 客商开票资料.html 模板新建（%d 字符·LF）" % len(t))
