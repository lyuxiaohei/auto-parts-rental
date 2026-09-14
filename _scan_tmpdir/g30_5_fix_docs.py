# -*- coding: utf-8 -*-
"""G30.5 审计修复：P2-R01 与会议纪要 md 的 6 处文档漂移更正
只做精确替换 + assert 计数；Windows 用 newline='' 防行尾改写。
用法：python g30_5_fix_docs.py [dry|write]
"""
import io, sys

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁"
P2 = ROOT + r"\P2-R01-产品需求文档.md"
MD = ROOT + r"\2026-09-14 汽车物流包装租赁第4次会议原型演示\2026-09-14 汽车物流包装租赁第4次会议原型演示 [会议纪要].md"
DRY = "write" not in sys.argv

EDITS = [
    # (文件, 旧, 新, 标签)
    (P2, "A.5·D-97~D-125）", "A.5·D-97~D-126）", "P2 头部版本行范围"),
    (P2, "### A.5 第 4 次沟通拍板（D-97~D-125 · 2026-09-14）",
         "### A.5 第 4 次沟通拍板（D-97~D-126 · 2026-09-14）", "P2 A.5 节标题范围"),
    (P2, "| 第4次沟通 3:25-3:59 | ✅ |", "| 第4次沟通 2:58-3:59 | ✅ |", "P2 D-97 时间戳起点"),
    (P2,
     "（袁工会后确认 2026-09-14）；库存查询行内「转租登记」保留不动（D-78 落法不变） | 第4次沟通 41:50-47:46＋会后确认",
     "（袁工会后确认 2026-09-14＋道远 09-14 确认）；库存查询行内「转租登记」保留不动（D-78 落法不变·沿革：转写 43:01 吕曾议「这里的这个转租直接去掉」·终态以 49:08 段客户确认在用为准） | 第4次沟通 41:50-47:46＋会后确认",
     "P2 D-106 补道远确认+沿革注记"),
    (P2, "⏳（G31 T10 小任务）", "⏳（G31 T8 小任务）", "P2 D-126 任务号 T10→T8"),
    (P2,
     "存疑条目经道远两批逐条确认（计费按天挂起/移动端不改/以销定采并行/菜单 v4/租期两层/不加按周/转移退租不勾稽/退货退款先竞品调研）。",
     "存疑条目经道远两批逐条确认（计费按天挂起=D-122／移动端不改=D-121／以销定采并行=D-104／菜单 v4=D-114／租期两层=D-117／不加按周=D-122 行内／转移退租不勾稽=D-106／退货退款先竞品调研=D-123）。",
     "P2 A.5 引言 8 项补落账锚点"),
    (MD, "P2-R01 附录 A.5·D-97~D-125", "P2-R01 附录 A.5·D-97~D-126", "MD 头部范围"),
    (MD, "> **落账**：P2-R01 附录 A.5（29 条·含 3 ⏸ 挂起）",
         "> **落账**：P2-R01 附录 A.5（D-97~D-126 共 30 条·26 ✅/2 ⏸/1 🔄/1 ⏳）", "MD 落账统计刷新"),
]

cache = {}
def load(p):
    if p not in cache:
        f = io.open(p, encoding="utf-8", newline="")
        cache[p] = f.read()
        f.close()
    return cache[p]

for path, old, new, label in EDITS:
    cnt = load(path).count(old)
    assert cnt == 1, "锚点计数异常 %s：%d 次（期望 1）" % (label, cnt)
    print("[OK-锚点] %-38s %d/1" % (label, cnt))

print("---- 锚点全部唯一，%s ----" % ("DRY RUN（未写入）" if DRY else "执行写入"))

if not DRY:
    for path, old, new, label in EDITS:
        c = cache[path]
        cache[path] = c.replace(old, new, 1)
    for path in cache:
        f = io.open(path, "w", encoding="utf-8", newline="")
        f.write(cache[path])
        f.close()
        print("[WROTE] %s" % path)
    # 写后复验
    print("---- 写后复验 ----")
    for path, old, new, label in EDITS:
        f = io.open(path, encoding="utf-8", newline="")
        c = f.read()
        f.close()
        assert new in c and old not in c, "写后复验失败：" + label
        print("[VERIFY] %-38s new-in=Y old-out=Y" % label)
    print("全部 8 处替换落盘并复验通过")
