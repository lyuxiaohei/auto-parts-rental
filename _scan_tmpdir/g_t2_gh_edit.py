# -*- coding: utf-8 -*-
"""T2+T3 页面编辑（租入归还弹窗双层）：删遗留单行（物料/归还数量）+备注上移到归还明细前+pn-hint 摘除（转标注）"""
import io, sys

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
FILES = [ROOT + r"\租赁管理\租入归还列表.html", ROOT + r"\租赁管理\弹窗\租入归还新建.html"]
NL = "\r\n"

TAIL_OLD = ("      <div class=\"form-row\">" + NL +
            "        <span class=\"form-label\"><span class=\"req\">*</span>物料</span>" + NL +
            "        <div class=\"select-box input-box\"><select style=\"flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;\"><option selected>围板箱 1200×1000×970</option><option>WBX-1210L 围板箱 1200×1000×970</option><option>PLT-1210P 塑料托盘 1200×1000</option><option>BTC-6040 料箱 600×400×340</option><option>ZH-2601-A 驾驶室围板箱整箱套件</option></select><span class=\"caret\">▾</span></div>" + NL +
            "      </div>" + NL +
            "      <div class=\"form-row\">" + NL +
            "        <span class=\"form-label\"><span class=\"req\">*</span>归还数量（只）</span>" + NL +
            "        <div class=\"input-box\"><input placeholder=\"请输入归还数量\"></div>" + NL +
            "      </div>" + NL +
            "      <div class=\"form-row\">" + NL +
            "        <span class=\"form-label\">备注</span>" + NL +
            "        <div class=\"input-box\"><input placeholder=\"选填，如：退租拆散后 4 只破损归还，6 只留用循环\"></div>" + NL +
            "      </div>" + NL +
            "    </div>")
TAIL_NEW = "    </div>"

PNHINT_OLD = (NL + "          <div class=\"pn-hint\">支持分批：多个归还单可对应一个租入单；逐货品填写本次归还数量，「已归还」为该租入单历史累计（数据源：demo-data rentInOrders）。</div>")

INS_OLD = "      <div class=\"form-row\" id=\"riDetailRow\">"
INS_NEW = ("      <div class=\"form-row\">" + NL +
           "        <span class=\"form-label\">备注</span>" + NL +
           "        <div class=\"input-box\"><input placeholder=\"选填，如：退租拆散后 4 只破损归还，6 只留用循环\"></div>" + NL +
           "      </div>" + NL +
           "      <div class=\"form-row\" id=\"riDetailRow\">")

for fp in FILES:
    raw = open(fp, "rb").read()
    c0, l0 = raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")
    t = io.open(fp, encoding="utf-8", newline="").read()
    name = fp.split(chr(92))[-1]
    if 'id="riDetailRow"><span' in t.replace("\r\n", "").replace("\n", "") or (TAIL_OLD not in t and "归还明细</span>" in t and "物料</span>" not in t.split('id="riDetailRow"')[1][:3000]):
        print("SKIP 已完成", name)
        continue
    assert t.count(TAIL_OLD) == 1, name + " 尾块锚点=" + str(t.count(TAIL_OLD))
    assert t.count(PNHINT_OLD) == 1, name + " pn-hint 锚点=" + str(t.count(PNHINT_OLD))
    assert t.count(INS_OLD) == 1, name + " riDetailRow 锚点=" + str(t.count(INS_OLD))
    t = t.replace(TAIL_OLD, TAIL_NEW, 1)
    t = t.replace(PNHINT_OLD, "", 1)
    t = t.replace(INS_OLD, INS_NEW, 1)
    # 断言：备注在 riDetailRow 之前；物料/归还数量单行已消失（弹窗内）；pn-hint 0
    body = t[t.find('id="createModal"'):t.find("modal-footer", t.find('id="createModal"'))]
    assert body.find("备注") < body.find('id="riDetailRow"'), name + " 备注顺序异常"
    assert "物料</span>" not in body and "归还数量（只）" not in body, name + " 遗留行未删净"
    assert "pn-hint" not in body, name + " pn-hint 残留"
    io.open(fp, "w", encoding="utf-8", newline="").write(t)
    raw2 = open(fp, "rb").read()
    c1, l1 = raw2.count(b"\r\n"), raw2.count(b"\n") - raw2.count(b"\r\n")
    net = TAIL_OLD.count(NL) - TAIL_NEW.count(NL) + PNHINT_OLD.count(NL) - INS_NEW.count(NL) + INS_OLD.count(NL)
    assert (c1, l1) == (c0 - net if NL == "\r\n" else c0, l0 - net if NL == "\n" else l0), name + " EOL 漂移 %s→%s 预期净 %d" % ((c0, l0), (c1, l1), net)
    print("PASS", name, "·遗留行删+备注上移+pn-hint 摘除·CRLF=%d LF=%d" % (c1, l1))
