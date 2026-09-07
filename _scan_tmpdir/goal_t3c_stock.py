# -*- coding: utf-8 -*-
"""
任务三c：库存查询（仓储作业/库存查询.html）
1) 五态卡下方加灰字口径注记（09-05 拍板原文）
2) 库存流水弹窗·进出流水顶部加 09-02 退租入库 TZRK-20260902-008 +60 行（L1 完好回库联动演示行；
   结存 5,260 与卡头在库数、下行算术 5,260-1,000=4,260 自洽）
二进制替换 + assert + 幂等；备份 backup-goal-t3-20260905/
"""
from pathlib import Path
import shutil

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
BK = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-goal-t3-20260905")
F = "仓储作业/库存查询.html"

CARD_ANCHOR = "关联租入单 2 张 · 按月生成租金应付</div>".encode("utf-8")
NOTE_TEXT = "在途＝应入库未入库（退租待入库 / 采购到货待入库 / 租入到货待入库 / 调拨在途）；租入＝租入在库未转租，转租后计入客户态（来源标记区分）"

FLOW_ANCHOR = '<tr><td class="td-num">09-01</td><td>调拨出库</td>'.encode("utf-8")
FLOW_NEW_TXT = ('<tr><td class="td-num">09-02</td><td>退租入库</td>'
                + '<td><span class="lk" onclick="go(\'../仓储作业/退租入库列表.html\')">TZRK-20260902-008</span></td>'
                + '<td class="td-num">+60</td><td class="td-num">5,260</td></tr>')

def main():
    p = ROOT / F
    b = p.read_bytes()
    dst = BK / F
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        shutil.copy2(p, dst)

    # 幂等标记
    note_b = NOTE_TEXT.encode("utf-8")
    if note_b in b and b"TZRK-20260902-008</span></td>".replace(b"</span></td>", b"") in b.replace(b"</span></td>", b"") :
        pass  # 由下方精确判断
    changed = False

    # 1) 口径注记：插在 stat-grid 收尾 </div> 之后
    if note_b not in b:
        assert b.count(CARD_ANCHOR) == 1, f"五态卡锚点 {b.count(CARD_ANCHOR)} != 1"
        i = b.find(CARD_ANCHOR) + len(CARD_ANCHOR)
        # 期望随后是 {EOL}  </div>{EOL}</div> （卡片收尾 + 网格收尾）
        for tail in (b"\r\n  </div>\r\n</div>", b"\n  </div>\n</div>"):
            if b[i:i+len(tail)] == tail:
                nl = "\r\n" if tail.startswith(b"\r\n") else "\n"
                note_html = (nl + nl + '<div style="margin:-4px 0 12px;font-size:12px;color:#8c8c8c;line-height:1.7;">'
                             + NOTE_TEXT + "</div>").encode("utf-8")
                b = b[:i+len(tail)] + note_html + b[i+len(tail):]
                changed = True
                break
        else:
            raise AssertionError("五态卡收尾结构不符：" + repr(b[i:i+30]))

    # 2) 流水行：插在 09-01 调拨出库行之前
    if b"TZRK-20260902-008</span>" not in b:
        assert b.count(FLOW_ANCHOR) == 1, f"流水锚点 {b.count(FLOW_ANCHOR)} != 1"
        nl_b = b"\r\n" if b[max(0, b.find(FLOW_ANCHOR)-2):b.find(FLOW_ANCHOR)] == b"\r\n" else b"\n"
        b = b.replace(FLOW_ANCHOR, FLOW_NEW_TXT.encode("utf-8") + nl_b + b"        " + FLOW_ANCHOR, 1)
        changed = True

    if changed:
        p.write_bytes(b)
        print(f"{F}: 完成（口径注记 + L1 退租回库流水行）")
    else:
        print(f"{F}: 均已存在，跳过")

    # 终态 assert
    assert NOTE_TEXT.encode("utf-8") in b and b"TZRK-20260902-008</span>" in b

if __name__ == "__main__":
    main()
