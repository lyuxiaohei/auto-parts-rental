# -*- coding: utf-8 -*-
"""备注行移动：新建采购订单弹窗（双层同步）——备注从明细下方移到明细上方（表单区末尾）
锚点：①移除底部备注块（添加一行按钮后粘接的 form-row）②在采购明细段标题前插入同构 form-row
"""
import io, sys

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
FILES = [ROOT + r"\采购管理\采购订单列表.html", ROOT + r"\采购管理\弹窗\新建采购订单.html"]

OLD_TAIL = ("<button class=\"btn btn-dashed btn-sm\" style=\"width:100%;margin-top:8px;\">+ 添加一行</button><div class=\"form-row\">" + "\n" +
            "    <span class=\"form-label\">备注</span>" + "\n" +
            "    <div class=\"input-box\" style=\"width:350px;\"><input placeholder=\"选填\"></div>" + "\n" +
            "  </div>" + "\n")
NEW_TAIL = "<button class=\"btn btn-dashed btn-sm\" style=\"width:100%;margin-top:8px;\">+ 添加一行</button>" + "\n"

OLD_MID = "</div><div style=\"margin:4px 0 8px;font-size:13px;font-weight:600;color:#1a1a1a;\">采购明细</div>"
NEW_MID = ("</div><div class=\"form-row\">" + "\n" +
           "    <span class=\"form-label\">备注</span>" + "\n" +
           "    <div class=\"input-box\" style=\"width:350px;\"><input placeholder=\"选填\"></div>" + "\n" +
           "  </div><div style=\"margin:4px 0 8px;font-size:13px;font-weight:600;color:#1a1a1a;\">采购明细</div>")

for fp in FILES:
    raw = open(fp, "rb").read()
    crlf0, lf0 = raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")
    nl = "\r\n" if crlf0 > lf0 else "\n"
    t = io.open(fp, encoding="utf-8", newline="").read()
    # 幂等：已移动（备注 label 在明细标题前）则跳过
    i_note0, i_det0 = t.find('<span class="form-label">备注</span>'), t.find('采购明细</div>')
    if 0 < i_note0 < i_det0 and OLD_TAIL.replace("\n", nl) not in t:
        print("SKIP 已完成", fp.split(chr(92))[-1])
        continue
    ot, nm = OLD_TAIL.replace("\n", nl), OLD_MID
    nt, nm2 = NEW_TAIL.replace("\n", nl), NEW_MID.replace("\n", nl)
    assert t.count(ot) == 1, fp + " 尾部锚点 " + str(t.count(ot))
    assert t.count(nm) == 1, fp + " 明细锚点 " + str(t.count(nm))
    # 顺序约束：备注块当前在明细锚点之后
    assert t.index(ot) > t.index(nm), fp + " 顺序异常"
    t = t.replace(ot, nt, 1).replace(nm, nm2, 1)
    # 断言：备注 label 现在在明细标题之前，且旧粘接消失
    i_note = t.find('<span class="form-label">备注</span>')
    i_det = t.find('采购明细</div>')
    assert 0 < i_note < i_det, fp + " 移动后顺序异常"
    assert t.count(nt) == 1 and t.count(nm2) == 1
    io.open(fp, "w", encoding="utf-8", newline="").write(t)
    raw2 = open(fp, "rb").read()
    crlf1, lf1 = raw2.count(b"\r\n"), raw2.count(b"\n") - raw2.count(b"\r\n")
    assert (crlf1, lf1) == (crlf0, lf0), fp + " EOL 漂移 %s→%s" % ((crlf0, lf0), (crlf1, lf1))
    print("PASS", fp.split(chr(92))[-1], "·备注已上移·CRLF=%d 裸LF=%d" % (crlf1, lf1))
