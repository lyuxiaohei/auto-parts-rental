# -*- coding: utf-8 -*-
"""
任务三d：水单部分核销·核销后余额展示（双层同步）
- 核销勾对明细表下方加静态行：本次核销后余额 ¥199,700.00（486,200.00 − 286,500.00）
- 注：goal 指定示例数 ¥4,270.00 与本弹窗既有数据算术矛盾，按自洽数改用 199,700.00（默认决策，报告注明）
"""
from pathlib import Path
import shutil

ROOT = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
BK = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-goal-t3-20260905")
TARGETS = ["财务协同/银行水单核销.html", "财务协同/弹窗/水单核销详情.html"]

ANCHOR_CORE = '286,500.00（部分核销）</td></tr>'.encode("utf-8")
MARK = "本次核销后余额".encode("utf-8")

def build_line(nl):
    return (nl + '      <div style="margin-top:8px;font-size:12.5px;color:#1a1a1a;">本次核销后余额：'
            + '<b style="color:#fa8c16;">¥199,700.00</b>'
            + '（账单 486,200.00 − 本次核销 286,500.00 · 部分核销后账单余额继续挂账，水单额度已用完）</div>').encode("utf-8")

def main():
    BK.mkdir(parents=True, exist_ok=True)
    for f in TARGETS:
        p = ROOT / f
        b = p.read_bytes()
        dst = BK / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copy2(p, dst)
        if MARK in b:
            print(f"{f}: 已改过，跳过")
            continue
        assert b.count(ANCHOR_CORE) == 1, f"{f} 锚点 {b.count(ANCHOR_CORE)} != 1"
        i = b.find(ANCHOR_CORE) + len(ANCHOR_CORE)
        # 期望随后是 {EOL}</tbody></table></div>
        for tail in (b"\r\n</tbody></table></div>", b"\n</tbody></table></div>"):
            if b[i:i+len(tail)] == tail:
                nl = "\r\n" if tail.startswith(b"\r\n") else "\n"
                b = b[:i+len(tail)] + build_line(nl) + b[i+len(tail):]
                break
        else:
            raise AssertionError(f"{f} 明细表收尾结构不符: {b[i:i+30]!r}")
        assert b.count(MARK) == 1
        p.write_bytes(b)
        print(f"{f}: 余额行已加")

if __name__ == "__main__":
    main()
