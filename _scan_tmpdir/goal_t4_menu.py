# -*- coding: utf-8 -*-
"""
任务四：菜单重组（方案A·仅排序）——"租赁单"菜单项移到"销售订单"之后
- 44 页：标准项 go('../包装管理/租赁单列表.html')；1 页（租赁单列表.html）selected 态
- 销售订单锚点两形态：标准 / selected（销售订单列表.html 自身）
- 二进制替换，行尾自适应；备份 backup-goal-t4-20260905/；幂等
"""
from pathlib import Path
import shutil, sys

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
BK = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-goal-t4-20260905")

ZL_STD = "<li><div class=\"sm-link\" onclick=\"go('../包装管理/租赁单列表.html')\">租赁单</div></li>".encode("utf-8")
ZL_SEL = "<li><div class=\"sm-link selected\">租赁单</div></li>".encode("utf-8")
SO_STD = "<li><div class=\"sm-link\" onclick=\"go('../销售管理/销售订单列表.html')\">销售订单</div></li>".encode("utf-8")
SO_SEL = "<li><div class=\"sm-link selected\">销售订单</div></li>".encode("utf-8")
IND = b"   "

def find_line(b, pat):
    """定位『缩进+pat+行尾』完整行，返回 (start, end) 或 None"""
    i = b.find(IND + pat)
    if i == -1:
        return None
    end = i + len(IND) + len(pat)
    if b[end:end+2] == b"\r\n":
        end += 2
    elif b[end:end+1] == b"\n":
        end += 1
    return (i, end)

def newline_at(b, pos):
    """pos 所在行的行尾符（向前找最近的 \n，看它前面是否 \r）"""
    j = b.rfind(b"\n", 0, pos)
    return b"\r\n" if j >= 1 and b[j-1:j] == b"\r" else b"\n"

def main():
    pages = sorted(ROOT.rglob("*.html"))
    BK.mkdir(parents=True, exist_ok=True)
    log, fails = [], []
    moved = skipped = 0
    for p in pages:
        rel = p.relative_to(ROOT)
        b = p.read_bytes()
        if b'<ul class="sm-sub">' not in b:
            continue  # 无实际侧边栏（F01 / 弹窗壳页仅有 CSS 无菜单 markup）
        so = find_line(b, SO_STD) or find_line(b, SO_SEL)
        if not so:
            fails.append(f"{rel}: 找不到销售订单锚点")
            continue
        # 幂等：销售订单行后紧跟的行已是租赁单项 → 跳过
        if b[so[1]:].startswith(IND + ZL_STD) or b[so[1]:].startswith(IND + ZL_SEL):
            skipped += 1
            log.append(f"{rel}  already-moved skip")
            continue
        zl = find_line(b, ZL_STD) or find_line(b, ZL_SEL)
        if not zl:
            fails.append(f"{rel}: 找不到租赁单菜单项")
            continue
        sel = b[zl[0]+3:zl[0]+3+len(ZL_SEL)] == ZL_SEL
        dst = BK / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copy2(p, dst)
        # 1) 删除租赁单行
        nb = b[:zl[0]] + b[zl[1]:]
        # 2) 重新定位销售订单行并插入其后（保持该行行尾风格）
        so2 = find_line(nb, SO_STD) or find_line(nb, SO_SEL)
        assert so2, f"{rel}: 删行后锚点丢失"
        item = IND + (ZL_SEL if sel else ZL_STD) + newline_at(nb, so2[1] - 1 if so2[1] > 0 else 0)
        nb = nb[:so2[1]] + item + nb[so2[1]:]
        # assert：各项恰 1 次、租赁单在销售订单之后
        zl_n = nb.count(ZL_STD) + nb.count(ZL_SEL)
        so_n = nb.count(SO_STD) + nb.count(SO_SEL)
        assert zl_n == 1 and so_n == 1, f"{rel}: 项数异常 zl={zl_n} so={so_n}"
        pos_zl = max(nb.find(ZL_STD), nb.find(ZL_SEL))
        pos_so = max(nb.find(SO_STD), nb.find(SO_SEL))
        assert pos_zl > pos_so, f"{rel}: 顺序错"
        p.write_bytes(nb)
        moved += 1
        log.append(f"{rel}  moved({'selected' if sel else 'std'})")
    print(f"移动 {moved} 页；幂等跳过 {skipped}；失败 {len(fails)}")
    for f in fails:
        print(" FAIL:", f)
    (BK / "_t4_log.txt").write_text("\n".join(log), encoding="utf-8")
    return fails

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
