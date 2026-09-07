# -*- coding: utf-8 -*-
"""
任务三b：销售出库新建弹窗·库存可用量不足禁用态（双层同步）
- 预置不足示例沿用现有数据：申请 5,000 件 vs 可用 1,520 件
- 蓝色可用量提示行后加橙字"库存可用量不足"提示行
- footer 提交审核按钮 disabled + 禁用样式
- 顺手修：明细行备注 input placeholder 误为"跳转页码"（历史批量修复误伤）→"选填"
- 目标：仓储作业/销售出库列表.html（../）+ 仓储作业/弹窗/销售出库新建.html（双层）
"""
from pathlib import Path
import shutil

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
BK = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-goal-t3-20260905")

HINT_ANCHOR = "—— 按库存可用量发货，超量需先入库</div>".encode("utf-8")
BTN_OLD = "<button class=\"btn\" onclick=\"closeModal('createModal')\">提交审核</button>".encode("utf-8")
BTN_NEW = "<button class=\"btn\" disabled title=\"库存可用量不足\" style=\"opacity:.45;cursor:not-allowed;\">提交审核</button>".encode("utf-8")
PH_OLD = '<td><input value="" placeholder="跳转页码"></td>'.encode("utf-8")
PH_NEW = '<td><input value="" placeholder="选填"></td>'.encode("utf-8")

def build_hint_row(nl):
    assert isinstance(nl, str)
    return ("<div class=\"form-row\">" + nl + "    <span class=\"form-label\"></span>" + nl
            + "    <div style=\"font-size:12px;color:#fa8c16;line-height:1.7;font-weight:600;\">"
            + "库存可用量不足：本次申请 5,000 件 &gt; 可用 1,520 件，无法提交 —— 请先补货入库或调减出库数量</div>" + nl + "  </div>").encode("utf-8")

TARGETS = ["仓储作业/销售出库列表.html", "仓储作业/弹窗/销售出库新建.html"]

def insert_shortage(b):
    """在可用量提示行之后插入橙字不足行；返回新 bytes 与插入标记"""
    assert b.count(HINT_ANCHOR) == 1, f"可用量锚点 {b.count(HINT_ANCHOR)} != 1"
    i = b.find(HINT_ANCHOR) + len(HINT_ANCHOR)
    for tail in (b"\r\n  </div>", b"\n  </div>"):
        if b[i:i+len(tail)] == tail:
            nl = "\r\n" if tail.startswith(b"\r\n") else "\n"
            return b[:i+len(tail)] + build_hint_row(nl) + b[i+len(tail):]
    raise AssertionError("可用量提示行后未找到 </div> 收尾（结构不符）")

def main():
    BK.mkdir(parents=True, exist_ok=True)
    for f in TARGETS:
        p = ROOT / f
        b = p.read_bytes()
        dst = BK / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copy2(p, dst)
        if "库存可用量不足：本次申请".encode("utf-8") in b:
            print(f"{f}: 已改过，跳过")
            continue
        nb = insert_shortage(b)
        assert nb.count(BTN_OLD) == 1, f"{f} 按钮锚点 {nb.count(BTN_OLD)} != 1"
        assert nb.count(PH_OLD) == 1, f"{f} placeholder 锚点 {nb.count(PH_OLD)} != 1"
        nb = nb.replace(BTN_OLD, BTN_NEW).replace(PH_OLD, PH_NEW)
        assert nb.count(BTN_NEW) == 1 and nb.count(PH_NEW) == 1
        p.write_bytes(nb)
        print(f"{f}: 完成（提示行+禁用按钮+placeholder 修正）")

if __name__ == "__main__":
    main()
