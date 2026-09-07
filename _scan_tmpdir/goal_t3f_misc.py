# -*- coding: utf-8 -*-
"""
任务三f：
1) 盈亏报表：主表下加"对齐说明"灰字注记（PRJ-2601 收入=AR-2026-08-PRJ2601 486,200；
   PRJ-2604 L4 链成本/应收构成）——P3-R04"对齐示例项目"最简实现
2) 租赁单新建弹窗：押金字段下加口径注记（双层：列表页内嵌 + 弹窗/独立模板）
3) 打印死链改 window.print() 触发（组合出库列表/采购入库列表 各 8 处；
   附 classList.toggle 提供按压自反馈，避免审计死按钮误报）
"""
from pathlib import Path
import shutil

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
BK = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-goal-t3-20260905")

def nl_at(b, pos):
    j = b.rfind(b"\n", 0, pos)
    return "\r\n" if j >= 1 and b[j-1:j] == b"\r" else "\n"

def backup(f):
    p = ROOT / f
    dst = BK / f
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        shutil.copy2(p, dst)
    return p

# ---------- 1) 盈亏报表对齐注记 ----------
def fix_pnl():
    f = "财务协同/盈亏报表.html"
    p = backup(f)
    b = p.read_bytes()
    mark = "对齐说明（演示链数据）".encode("utf-8")
    if mark in b:
        print(f"{f}: 已改过"); return
    anchor = b'</tbody>\n    </table>\n  </div>'
    anchor_c = b'</tbody>\r\n    </table>\r\n  </div>'
    note = ('对齐说明（演示链数据）：PRJ-2601 收入合计 486,200.00 ＝ 应收账单 AR-2026-08-PRJ2601'
            '（已开票 186,200 · 水单部分核销 286,500，见开票登记 / 银行水单核销）；'
            'PRJ-2604 为 L4 混合链演示项目——租入大箱租金应付 AP-20260903-010（12,000.00 / 月）与自购隔板采购摊销计入成本合计，'
            '9 月销售费应收 AR-2026-09-PRJ2604-S1（1,280.00）见应收账单；当前成本大于收入、毛利为负（项目状态：已暂停）。')
    for anc in (anchor_c, anchor):
        if anc in b:
            nl = "\r\n" if anc is anchor_c else "\n"
            ins = (nl + '  <div style="margin:8px 0 0;font-size:12px;color:#8c8c8c;line-height:1.7;">' + note + '</div>').encode("utf-8")
            assert b.count(anc) == 1
            b = b.replace(anc, anc + ins, 1)
            p.write_bytes(b)
            print(f"{f}: 对齐注记已加")
            return
    raise AssertionError("盈亏报表表格收尾锚点未找到")

# ---------- 2) 押金口径注记（双层） ----------
def fix_deposit():
    note = "押金为设计预留字段——两次会议均未涉及，收退与计价商务口径待客户确认（F01 财务通道注记同步）"
    for f in ["包装管理/租赁单列表.html", "包装管理/弹窗/租赁单新建.html"]:
        p = backup(f)
        b = p.read_bytes()
        if note.encode("utf-8") in b:
            print(f"{f}: 已改过"); continue
        core = 'value="50,000.00" placeholder="请输入"></div>'.encode("utf-8")
        assert b.count(core) == 1, f"{f} 押金锚点 {b.count(core)} != 1"
        i = b.find(core) + len(core)
        for tail in (b"\r\n  </div>", b"\n  </div>"):
            if b[i:i+len(tail)] == tail:
                nl = "\r\n" if tail.startswith(b"\r\n") else "\n"
                ins = (nl + '  <div class="form-row">' + nl + '    <span class="form-label"></span>' + nl
                       + '    <div style="font-size:12px;color:#8c8c8c;line-height:1.7;">' + note + '</div>' + nl + '  </div>').encode("utf-8")
                b = b[:i+len(tail)] + ins + b[i+len(tail):]
                p.write_bytes(b)
                print(f"{f}: 押金口径注记已加")
                break
        else:
            raise AssertionError(f"{f} 押金行收尾结构不符")

# ---------- 3) 打印 window.print() ----------
def fix_print():
    old = b"<a>\xe6\x89\x93\xe5\x8d\xb0</a>"  # <a>打印</a>
    new = '<a onclick="window.print();this.classList.toggle(\'printed\')">打印</a>'.encode("utf-8")
    for f in ["仓储作业/组合出库列表.html", "仓储作业/采购入库列表.html"]:
        p = backup(f)
        b = p.read_bytes()
        n = b.count(old)
        if n == 0:
            print(f"{f}: 无旧打印链接（已改过？）"); continue
        b = b.replace(old, new)
        assert old not in b and b.count(new) == n
        p.write_bytes(b)
        print(f"{f}: 打印 ×{n} 已接 window.print()")

if __name__ == "__main__":
    fix_pnl()
    fix_deposit()
    fix_print()
