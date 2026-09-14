# -*- coding: utf-8 -*-
"""T1 租入单新建：押金（元）+备注两字段从租入明细下方上移到表单区末尾（租期起止后·明细标题前）·双层"""
import io

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
FILES = [ROOT + r"\租赁管理\弹窗\租入单新建.html", ROOT + r"\租赁管理\租入单列表.html"]
NL = "\r\n"

REMOVE_OLD = ("+ 添加明细行</button>" + NL + NL + "  <div class=\"form-row\">" + NL +
              "        <span class=\"form-label\">押金（元）</span>" + NL +
              "        <div class=\"input-box\"><input placeholder=\"选填\"></div>" + NL +
              "      </div>" + NL +
              "      <div class=\"form-row\">" + NL +
              "        <span class=\"form-label\">备注</span>" + NL +
              "        <div class=\"input-box\"><input placeholder=\"选填\"></div>" + NL +
              "      </div>" + NL +
              "    </div>")
REMOVE_NEW = "+ 添加明细行</button>" + NL + "    </div>"

INS_ROW = ("      <div class=\"form-row\">" + NL +
           "        <span class=\"form-label\">押金（元）</span>" + NL +
           "        <div class=\"input-box\"><input placeholder=\"选填\"></div>" + NL +
           "      </div>" + NL +
           "      <div class=\"form-row\">" + NL +
           "        <span class=\"form-label\">备注</span>" + NL +
           "        <div class=\"input-box\"><input placeholder=\"选填\"></div>" + NL +
           "      </div>" + NL)
TITLE = "      <div style=\"margin:4px 0 8px;font-size:13px;font-weight:600;color:#1a1a1a;\">租入明细（多货品 · 计费方式：按月 / 按次）</div>"

for fp in FILES:
    raw = open(fp, "rb").read()
    c0, l0 = raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")
    t = io.open(fp, encoding="utf-8", newline="").read()
    name = fp.split(chr(92))[-1]
    note_i = t.find('<span class="form-label">押金（元）</span>')
    det_after = t.find("租入明细（多货品", note_i) if note_i > 0 else -1
    if note_i > 0 and det_after > 0:
        print("SKIP 已完成", name)
        continue
    assert t.count(REMOVE_OLD) == 1, name + " 移除锚点=" + str(t.count(REMOVE_OLD))
    assert t.count(TITLE) == 1, name + " 标题锚点=" + str(t.count(TITLE))
    assert t.index(REMOVE_OLD) > t.index(TITLE), name + " 顺序异常"
    t = t.replace(REMOVE_OLD, REMOVE_NEW, 1).replace(TITLE, INS_ROW + TITLE, 1)
    n2 = t.find('<span class="form-label">押金（元）</span>')
    assert 0 < n2 < t.find("租入明细（多货品"), name + " 移动后顺序异常"
    io.open(fp, "w", encoding="utf-8", newline="").write(t)
    raw2 = open(fp, "rb").read()
    c1, l1 = raw2.count(b"\r\n"), raw2.count(b"\n") - raw2.count(b"\r\n")
    assert (c1, l1) == (c0 - 1, l0), name + " EOL 漂移 %s→%s" % ((c0, l0), (c1, l1))
    print("PASS", name, "·押金备注上移·CRLF=%d" % c1)
