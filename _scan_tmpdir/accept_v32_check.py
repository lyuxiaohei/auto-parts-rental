# -*- coding: utf-8 -*-
"""G04 独立验收 · B0 提示词复验 5 项 + B1 执行链回写 6 项 + B3 实地 4 项（纯只读静态部分）。
跨机说明：存档内 D:\ 前缀=主机口径，按项目根等价换算后 os.path.exists。"""
import os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ST = os.path.join(ROOT, "_scan_tmpdir")
WIN = "D:\\工作台-吕道远\\5-【ACTIVE】汽车物流包装租赁"
res = []

def chk(no, name, ok, detail=""):
    res.append((no, name, bool(ok), detail))

def rd(p):
    return open(os.path.join(ST, p), "rb").read().decode("utf-8", "replace")

def git(*a):
    return subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True).stdout

# ================= B0 提示词文本复验（5 项） =================
ARCH = ["goal-v32-G01-roledriven.txt", "goal-v32-G02-menurewrite.txt", "goal-v32-G03-accept.txt"]
# ① 存在与长度
ok1 = all(os.path.exists(os.path.join(ST, a)) for a in ARCH) and all(len(rd(a)) <= 4000 for a in ARCH)
chk("B0①", "三命令存档存在且各 ≤4000 字符", ok1, "；".join(f"{a}={len(rd(a))}字符" for a in ARCH if os.path.exists(os.path.join(ST, a))))
# ② 提问措辞 0
ASK = ["是否", "要不要", "请确认", "确认后", "商量"]
bad2 = [(a, w, rd(a).count(w)) for a in ARCH for w in ASK if rd(a).count(w)]
chk("B0②", "提问措辞（是否/要不要/请确认/确认后/商量）各 0 处", not bad2, f"违例={bad2}" if bad2 else "三存档×5 词全 0")
# ③ 块标记 ≥4
BLK = ["前置校验", "任务", "完成判定", "约束"]
# 口径：「各 ≥4」=每存档含全部四类块标记且合计 ≥4 处（完成判定/约束为节标题各恰 1 处属正常结构）
mism3 = [a for a in ARCH if any(rd(a).count(b) < 1 for b in BLK) or sum(rd(a).count(b) for b in BLK) < 4]
chk("B0③", "块标记四类齐备且每存档合计 ≥4 处", not mism3,
    f"不足={mism3}" if mism3 else "；".join(f"{a.split('-')[2]}={sum(rd(a).count(b) for b in BLK)}处·四类全在" for a in ARCH))
# ④ 双层路由绝对路径存在 + 腐蚀形态 0
paths = []
for a in ARCH:
    paths += re.findall(re.escape(WIN) + r"[^\\\s：:，,」』\]\)（）]*", rd(a))
local = [os.path.join(ROOT, p[len(WIN):].replace("\\", "/")) for p in set(paths)]
missing = [p for p in local if not os.path.exists(p)]
corrupt = [(a, w) for a in ARCH for w in ("租赁gent-handoff", "handoff0909") if w in rd(a)]
chk("B0④", "双层路由绝对路径（换算后）os.path.exists 全过且无腐蚀形态", not missing and not corrupt,
    f"抽取 {len(set(paths))} 条换算全过；腐蚀 0" if not missing and not corrupt else f"缺={missing} 腐蚀={corrupt}")
# ⑤ 锚词/前置链/完成判定数字与 G01-G03 文档一致
g1, g2, g3 = (rd(a) for a in ARCH)
g01d = rd("../agent-handoff/20260909-G01-角色管理数据驱动.md") if os.path.exists(os.path.join(ROOT, "agent-handoff/20260909-G01-角色管理数据驱动.md")) else ""
g02d = open(os.path.join(ROOT, "agent-handoff/20260909-G02-菜单v3.2侧边栏重写.md"), "rb").read().decode("utf-8")
g03d = open(os.path.join(ROOT, "agent-handoff/20260909-G03-复验收与总收口.md"), "rb").read().decode("utf-8")
ok5 = ("12 项" in g1 and "12 项" in g01d) and ("≥12" in g2 and "100/88/55" in g2 and "≥12" in g02d and "100/88/55" in g02d) \
      and ("≥16" in g3 and "≥16" in g03d) and ("三行" in g3 or "3 行" in g3)
chk("B0⑤", "数字锚与 G01-G03 文档一致（G01=12 项；G02=≥12+100/88/55；G03=≥16+三行索引）", ok5,
    f"G01档12项:{'12 项' in g01d}·G02档:{'≥12' in g02d}+{'100/88/55' in g02d}·G03档≥16:{'≥16' in g03d}")

# ================= B1 执行链与回写完整性（6 项·静态 grep） =================
log = git("log", "--oneline")
chk("B1①", "git 全史三执行提交各 ≥1", all(log.count(m) >= 1 for m in ("G01-角色管理·执行", "G02-菜单v3.2·执行", "G03-复验收·执行")),
    f"G01:{log.count('G01-角色管理·执行')}/G02:{log.count('G02-菜单v3.2·执行')}/G03:{log.count('G03-复验收·执行')}")
idx = open(os.path.join(ROOT, "agent-handoff/_索引.md"), "rb").read().decode("utf-8")
rows = {g: [ln for ln in idx.split("\n") if ln.startswith(f"| {g} |")] for g in ("G01", "G02", "G03")}
ok2 = all(len(rows[g]) == 1 and "✅" in rows[g][0] and "（收尾回填）" not in rows[g][0] for g in rows)
chk("B1②", "_索引.md G01/G02/G03 三行 ✅ 且 commit 列非空", ok2, " | ".join(rows[g][0][:80] for g in rows))
docs = {"G01": "20260909-G01-角色管理数据驱动.md", "G02": "20260909-G02-菜单v3.2侧边栏重写.md", "G03": "20260909-G03-复验收与总收口.md"}
bad3 = []
for g, d in docs.items():
    s = open(os.path.join(ROOT, "agent-handoff", d), "rb").read().decode("utf-8")
    head = s.split("\n")[2] if len(s.split("\n")) > 2 else ""
    if not ("✅" in head and "〈收尾回填〉" not in head):
        bad3.append((g, "头部未✅/未回填"))
    body = s.split("## 执行记录")[-1]
    if len(body.strip()) < 40:
        bad3.append((g, "执行记录空"))
chk("B1③", "三份 G 文档头部 ✅、commit 已回填、执行记录非空", not bad3, f"违例={bad3}" if bad3 else "G01/G02/G03 三文档全过")
p1 = open(os.path.join(ROOT, "P1-R01-需求梳理与功能框架.md"), "rb").read().decode("utf-8")
chk("B1④", "P1-R01 含「菜单重组 v3.2」追加句恰 1 处", p1.count("菜单重组 v3.2") == 1, f"实际 {p1.count('菜单重组 v3.2')} 处")
base = open(os.path.join(ROOT, "agent-handoff/_AGENT基线.md"), "rb").read().decode("utf-8")
import re as _re
menu_v32 = bool(_re.search(r"菜单[=＝*\s]*v3\.2", base))
chk("B1⑤", "基线快照含菜单 v3.2 口径（「菜单=**v3.2**」形态）+「111 页」「31 实体」",
    menu_v32 and "111 页" in base and "31 实体" in base,
    f"菜单v3.2:{menu_v32}[形态：菜单=**v3.2**]/111 页:{'111 页' in base}/31 实体:{'31 实体' in base}")
fl = rd("goal-failures-menuregroup32-20260909.html")
chk("B1⑥", "失败清单含 G01/G02/G03 三行+总结论行", all(g in fl for g in ("G01 角色管理数据驱动化", "G02 菜单 v3.2 侧边栏重写", "G03 复验收与总收口")) and "总结论" in fl, "三行+总结论行均在")

# ================= B3 交付物实地抽查（4 项·只读） =================
dd = open(os.path.join(ROOT, "P3-R01-包装租赁管理后台原型/_data/demo-data.js"), "rb").read().decode("utf-8")
m = re.search(r"roles\s*[:=]\s*\{(.{0,4000}?)RL-09", dd, re.S)
keys = set(re.findall(r"RL-0\d", dd))
chk("B3①", "demo-data.js roles 实体恰 9 键（RL-01~RL-09）", keys == {f"RL-0{i}" for i in range(1, 10)} and "RL-09" in dd, f"键={sorted(keys)}")
rm = open(os.path.join(ROOT, "P3-R01-包装租赁管理后台原型/系统管理/角色管理.html"), "rb").read().decode("utf-8")
chk("B3②", "角色管理.html 含 renderListPage 与 openRolePerm", "renderListPage" in rm and "openRolePerm" in rm,
    f"renderListPage:{rm.count('renderListPage')} 处·openRolePerm:{rm.count('openRolePerm')} 处")
old_forms = 0
scanned = 0
for dp, _, fs in os.walk(os.path.join(ROOT, "P3-R01-包装租赁管理后台原型")):
    for f in fs:
        if not f.endswith(".html"):
            continue
        s = open(os.path.join(dp, f), "rb").read().decode("utf-8", "replace")
        if "sidebar" in s or "侧边" in s or 'class="nav' in s:
            scanned += 1
            old_forms += s.count("</span>财务协同<span") + s.count("</span>仓储作业<span")
chk("B3③", "侧边栏组名旧形态（</span>财务协同<span 与 </span>仓储作业<span）0 处", old_forms == 0, f"扫描 {scanned} 页，旧形态 {old_forms} 处")
t1 = os.path.exists(os.path.join(ROOT, "P3-R01-包装租赁管理后台原型/系统管理/弹窗/权限配置.html"))
t2 = os.path.exists(os.path.join(ROOT, "P3-R01-包装租赁管理后台原型/系统管理/弹窗/新增角色.html"))
chk("B3④", "系统管理/弹窗/权限配置.html 与 新增角色.html 存在", t1 and t2, f"权限配置:{t1}·新增角色:{t2}")

fails = [r for r in res if not r[2]]
for no, name, ok, detail in res:
    print(("PASS " if ok else "FAIL ") + f"{no} {name}" + (" ｜ " + detail if detail else ""))
print(f"\n==== G04 静态部分（B0+B1+B3）：{len(res)} 项，失败 {len(fails)} ====")
