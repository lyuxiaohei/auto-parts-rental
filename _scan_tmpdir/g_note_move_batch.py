# -*- coding: utf-8 -*-
"""备注上移批量（5 弹窗 6 文件·双层）——A 租赁单新建×2 / B 新建销售订单×2 / C 销售出库新建×2
统一目标形态：备注 form-row 移到明细段标题之前；移除尾部原块（A 从警告框后摘除/B 从附件区前摘除/C 从添加一行后摘除）。
"""
import io, sys

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"

NOTE_ROW = ("<div class=\"form-row\">" + "{NL}" +
            "    <span class=\"form-label\">备注</span>" + "{NL}" +
            "    <div class=\"input-box\" style=\"width:350px;\"><input placeholder=\"选填\"></div>" + "{NL}" +
            "  </div>")

# (文件, 移除旧块[旧, 新], 插入锚[旧, 新])  — 全部用 {NL} 占位
JOBS = [
    # A1/A2 租赁单新建：旧=警告框</div>粘接备注块到 modal-body 尾；插入=billingHint 后、租赁器具明细前
    (ROOT + r"\租赁管理\弹窗\租赁单新建.html",
     ("</div><div class=\"form-row\">{NL}    <span class=\"form-label\">备注</span>{NL}    <div class=\"input-box\" style=\"width:350px;\"><input placeholder=\"选填\"></div>{NL}  </div>{NL}    </div>",
      "</div>{NL}    </div>"),
     ("（G13 演示注记）。</div><div style=\"margin:4px 0 8px;font-size:13px;font-weight:600;color:#1a1a1a;\">租赁器具明细</div>",
      "（G13 演示注记）。</div>{INS}<div style=\"margin:4px 0 8px;font-size:13px;font-weight:600;color:#1a1a1a;\">租赁器具明细</div>")),
    (ROOT + r"\租赁管理\租赁单列表.html", None, None),  # 同 A1（占位，循环内复制）
    # B1/B2 新建销售订单：旧=备注块后接订单附件标题；插入=要求交货日期后、订单明细前
    (ROOT + r"\销售管理\弹窗\新建销售订单.html",
     ("</div><div class=\"form-row\">{NL}    <span class=\"form-label\">备注</span>{NL}    <div class=\"input-box\" style=\"width:350px;\"><input placeholder=\"选填\"></div>{NL}  </div>{NL}  <div style=\"margin:12px 0 8px;font-size:13px;font-weight:600;color:#1a1a1a;\">订单附件",
      "</div>{NL}  <div style=\"margin:12px 0 8px;font-size:13px;font-weight:600;color:#1a1a1a;\">订单附件"),
     ("    <div class=\"input-box\" style=\"width:350px;\"><input value=\"2026-09-12\" placeholder=\"请输入\"></div>{NL}  </div><div style=\"margin:4px 0 8px;font-size:13px;font-weight:600;color:#1a1a1a;\">订单明细</div>",
      "    <div class=\"input-box\" style=\"width:350px;\"><input value=\"2026-09-12\" placeholder=\"请输入\"></div>{NL}  </div>{INS}<div style=\"margin:4px 0 8px;font-size:13px;font-weight:600;color:#1a1a1a;\">订单明细</div>")),
    (ROOT + r"\销售管理\销售订单列表.html", None, None),
    # C1/C2 销售出库新建：旧=粘接添加一行（同样板）；插入=出库日期后、出库明细前
    (ROOT + r"\销售管理\弹窗\销售出库新建.html",
     ("<button class=\"btn btn-dashed btn-sm\" style=\"width:100%;margin-top:8px;\">+ 添加一行</button><div class=\"form-row\">{NL}    <span class=\"form-label\">备注</span>{NL}    <div class=\"input-box\" style=\"width:350px;\"><input placeholder=\"选填\"></div>{NL}  </div>{NL}",
      "<button class=\"btn btn-dashed btn-sm\" style=\"width:100%;margin-top:8px;\">+ 添加一行</button>{NL}"),
     ("    <div class=\"input-box\" style=\"width:350px;\"><input value=\"2026-09-03\" placeholder=\"请输入\"></div>{NL}  </div><div style=\"margin:4px 0 8px;font-size:13px;font-weight:600;color:#1a1a1a;\">出库明细</div>",
      "    <div class=\"input-box\" style=\"width:350px;\"><input value=\"2026-09-03\" placeholder=\"请输入\"></div>{NL}  </div>{INS}<div style=\"margin:4px 0 8px;font-size:13px;font-weight:600;color:#1a1a1a;\">出库明细</div>")),
    (ROOT + r"\销售管理\销售出库列表.html", None, None),
]
JOBS[1] = (JOBS[0][0].replace("弹窗" + chr(92) + "租赁单新建", "租赁单列表"), JOBS[0][1], JOBS[0][2])
JOBS[3] = (JOBS[2][0].replace("弹窗" + chr(92) + "新建销售订单", "销售订单列表"), JOBS[2][1], JOBS[2][2])
JOBS[5] = (JOBS[4][0].replace("弹窗" + chr(92) + "销售出库新建", "销售出库列表"), JOBS[4][1], JOBS[4][2])

NOTE_ROW_PLAIN = NOTE_ROW.replace("{NL}", "{NL}")  # template

for fp, rem, ins in JOBS:
    raw = open(fp, "rb").read()
    crlf0, lf0 = raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")
    nl = "\r\n" if crlf0 > lf0 else "\n"
    t = io.open(fp, encoding="utf-8", newline="").read()
    name = fp.split(chr(92))[-1]

    note_i = t.find('<span class="form-label">备注</span>')
    det_after = t.find("明细</div>", note_i)  # 完成态：备注之后存在明细标题
    if note_i > 0 and det_after > 0:
        print("SKIP 已完成", name)
        continue

    ins_row = NOTE_ROW.replace("{NL}", nl)
    old_r = rem[0].replace("{NL}", nl)
    new_r = rem[1].replace("{NL}", nl)
    old_i = ins[0].replace("{NL}", nl).replace("{INS}", "")
    new_i = ins[1].replace("{NL}", nl).replace("{INS}", ins_row)

    assert t.count(old_r) == 1, name + " 移除锚点=" + str(t.count(old_r))
    assert t.count(old_i) == 1, name + " 插入锚点=" + str(t.count(old_i))
    assert t.index(old_r) > t.index(old_i), name + " 顺序异常"
    t = t.replace(old_r, new_r, 1).replace(old_i, new_i, 1)

    n2 = t.find('<span class="form-label">备注</span>')
    d2 = t.find("明细</div>")
    assert 0 < n2 < d2, name + " 移动后顺序异常"
    io.open(fp, "w", encoding="utf-8", newline="").write(t)
    raw2 = open(fp, "rb").read()
    crlf1, lf1 = raw2.count(b"\r\n"), raw2.count(b"\n") - raw2.count(b"\r\n")
    assert (crlf1, lf1) == (crlf0, lf0), name + " EOL 漂移"
    print("PASS", name, "·备注上移·CRLF=%d 裸LF=%d" % (crlf1, lf1))
