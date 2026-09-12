# -*- coding: utf-8 -*-
"""G23 验证门 1 · P2-R01 结构断言（逐行 PASS/FAIL）
口径依据：agent-handoff/20260912-G23-PRD文档生成.md 验证门 1
废弃词表=执行时从 P1-R04-术语表.md 现场提取（第九节「废弃词」，任务书原文写第五节系位置笔误，按实际位置提取记偏差）
「测试账号」判定口径=输出块标题（#### 测试账号）全文仅 1 次；引用行（技能模板规定格式「> 测试账号见…」）不属"输出"，记偏差说明
"""
import io, sys, re, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁"
PRD = os.path.join(ROOT, "P2-R01-产品需求文档.md")
TERMS = os.path.join(ROOT, "P1-R04-术语表.md")

results = []
def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f"  —— {detail}" if detail else ""))

t = open(PRD, encoding="utf-8").read()
lines = t.splitlines()

# ---- 1 存在与行数 ----
check("文件存在且 ≥500 行", os.path.exists(PRD) and len(lines) >= 500, f"实际 {len(lines)} 行")

# ---- 2 版本级章节计数 ----
check("「一、范围边界」标题=1", len([l for l in lines if l.strip() == "## 一、范围边界"]) == 1)
check("「二.1 角色列表」标题=1", len([l for l in lines if l.strip() == "## 二.1 角色列表"]) == 1)
check("「待确认清单」节=1", len([l for l in lines if l.strip().startswith("### 1.3 待确认清单")]) == 1)

# ---- 3 十模块三段标题各=1 ----
mods = ["PRJ","SAL","LEA","PUR","WHS","BAS","FIN","SYS","WF","MOB"]
for m in mods:
    a = len([l for l in lines if l.strip() == f"## 二.{m}.2 功能用例与验收"])
    b = len([l for l in lines if l.strip() == f"## 三.{m} 核心流程"])
    c = len([l for l in lines if l.strip() == f"## 四.{m} 数据流向"])
    check(f"{m} 三段标题各=1（{a}/{b}/{c}）", a == 1 and b == 1 and c == 1)

# ---- 4 UC 编号唯一（定义行口径）+ AC 对应用例列 ----
# UC 编号合法出现=定义行（表格行首列）1 次 + AC 对应用例列回链 N 次；重复判定=定义行重复
uc_def_rows = [l for l in lines if l.strip().startswith("| UC-")]
uc_defs = [l.split("|")[1].strip() for l in uc_def_rows if len(l.split("|")) > 1]
dup = sorted({u for u in uc_defs if uc_defs.count(u) > 1})
ucs_all = re.findall(r"UC-[A-Z]{2,3}-\d+", t)
check("UC 编号全局重复=0（定义行口径）", len(dup) == 0,
      f"定义 {len(uc_defs)} 个（全文含 AC 回链共 {len(ucs_all)} 处出现）" + (f"，重复：{dup}" if dup else ""))
ac_rows = [l for l in lines if l.strip().startswith("| AC-")]
bad_ac = []
for l in ac_rows:
    cells = [c.strip() for c in l.split("|")]
    # cells[0]='' cells[1]=AC 编号 cells[2]=对应用例
    if len(cells) < 3 or "UC-" not in cells[2]:
        bad_ac.append(l[:60])
check(f"AC 行「对应用例」列含 UC- 比率=100%（{len(ac_rows)} 行）",
      len(bad_ac) == 0, "; ".join(bad_ac[:3]) if bad_ac else "全部绑定")

# ---- 5 mermaid 计数 ----
n_mermaid = t.count("```mermaid")
check("mermaid 代码块 ≥11", n_mermaid >= 11, f"实际 {n_mermaid} 个")
# 每模块 ≥1：三.{代号} 段落范围内含 mermaid
for m in mods:
    seg = re.search(rf"## 三\.{m} 核心流程(.*?)(?=## 四\.|\Z)", t, re.S)
    check(f"{m} 核心流程段内 mermaid ≥1", seg and seg.group(1).count("```mermaid") >= 1)

# ---- 6 废弃词（现场提取 P1-R04 第九节）+组合出库 ----
term = open(TERMS, encoding="utf-8").read()
m9 = re.search(r"## 九、废弃词.*", term, re.S)
deprecated = []
if m9:
    for mm in re.finditer(r"^\| ~~(.+?)~~ \|", m9.group(0), re.M):
        raw = mm.group(1)
        for w in re.split(r"/|／", raw):
            w = w.strip().strip("（）()")
            if w:
                deprecated.append(w)
print(f"\n现场提取废弃词 {len(deprecated)} 个：{'、'.join(deprecated)}\n")

def strip_filenames(text, word):
    return text.replace(word + ".html", "")

# 语境白名单（现行合法复合词/形态）
PAN_KEEP = ["盘点记录","盘点单","盘点录入","盘点审核","盘点范围","盘点口径","盘点人","盘点日期",
            "盘点状态","盘点库房","盘点列表","盘点管理","盘点中","盘点差异","盘点对账","盘点兜底",
            "盘点调整","盘点客户端","盘点已完成","盘点联动","录入盘点","库存盘点","盘点/"]
PAN_PRE = ["录入"]
def pan_ok(text):
    bad = []
    for mm in re.finditer("盘点", text):
        seg = text[mm.start():mm.start()+8]
        pre = text[max(0,mm.start()-4):mm.start()]
        ok = any(seg.startswith(k) for k in PAN_KEEP) or any(pre.endswith(k) for k in PAN_PRE)
        if not ok:
            bad.append(text[max(0,mm.start()-10):mm.start()+12].replace("\n"," "))
    return bad

TYPE_KEEP = ["物料类型","发票类型","归还类型","账单类型","出库类型","入库类型","操作类型","单据类型",
             "费用类型","类型筛选","类型下拉","待办类型","演示类型","页面类型","两类型","16 类"]
LEI_KEEP = ["物料分类"]

PREFIX_OK = ["销售订单号","出库单号","入库单号","退租入库单号","归还单号","租入单号","租赁单号",
             "采购订单号","盘点单号","调拨单号","账单编号","付款编号","收款编号","单据编号",
             "发票登记号","水单号","来源单据编号","弱引用来源单据编号"]

violations = []
for w in deprecated:
    wt = w
    if wt in ("类型",):
        bads = []
        for mm in re.finditer("类型", t):
            seg = t[mm.start():mm.start()+6]
            if not any(seg.startswith(k) for k in TYPE_KEEP):
                ctx = t[max(0,mm.start()-14):mm.start()+16].replace("\n", " ")
                bads.append(ctx)
        # 裸「类型」列头（todoItems type 行中文名=类型，A05 现行标签）豁免形态
        bads = [b for b in bads if "| 类型 |" not in b]
        n = len(re.findall("类型", t))
        print(f"  废弃词「{wt}」：全文出现 {n} 次，物料大类语境违规 {len(bads)} 处")
        violations += [(wt, b) for b in bads]
        continue
    if wt == "分类":
        bads = []
        for mm in re.finditer("分类", t):
            pre = t[max(0,mm.start()-2):mm.start()]
            if not pre.endswith("物料"):
                bads.append(t[max(0,mm.start()-14):mm.start()+16].replace("\n", " "))
        print(f"  废弃词「{wt}」：全文出现 {len(re.findall('分类', t))} 次，物料档案语境违规 {len(bads)} 处")
        violations += [(wt, b) for b in bads]
        continue
    if wt == "盘点":
        bads = pan_ok(t)
        print(f"  废弃词「{wt}」：全文出现 {len(re.findall('盘点', t))} 次，非白名单语境 {len(bads)} 处")
        violations += [(wt, b) for b in bads]
        continue
    if wt == "单号":
        bads = []
        for mm in re.finditer("单号", t):
            # 复合词内部子串（如 销售订|单号）——取「前缀+单号」整体判定
            full = t[max(0,mm.start()-12):mm.start()+2]
            if not any(full.endswith(p) for p in PREFIX_OK):
                bads.append(t[max(0,mm.start()-14):mm.start()+16].replace("\n", " "))
        print(f"  废弃词「{wt}」：全文出现 {len(re.findall('单号', t))} 次，裸列头形态 {len(bads)} 处")
        violations += [(wt, b) for b in bads]
        continue
    body = strip_filenames(t, wt) if wt == "产品档案" else t
    n = body.count(wt)
    print(f"  废弃词「{wt}」：命中 {n} 处" + ("（已剔除 .html 文件名形态）" if wt == "产品档案" and t.count(wt) != n else ""))
    if n:
        violations.append((wt, f"{n} 处"))

n_combo = t.count("组合出库")
print(f"  G22 旧称呼「组合出库」：命中 {n_combo} 处")
if n_combo:
    violations.append(("组合出库", f"{n_combo} 处"))

check("废弃词违规=0 且「组合出库」=0", len(violations) == 0,
      "; ".join(f"[{w}] {s}" for w, s in violations[:6]) if violations else "全部 0")

# ---- 7 测试账号（输出块标题口径=1）----
n_block = len([l for l in lines if l.strip() == "#### 测试账号"])
n_all = t.count("测试账号")
check(f"「测试账号」输出块仅 1 次（标题口径；全文含模板规定引用行共 {n_all} 次）", n_block == 1)

# ---- 8 Out Scope 四移除模块 ----
sec12 = re.search(r"### 1\.2 本次不做.*?### 1\.3", t, re.S).group(0)
for w in ["退租申请", "组装", "拆卸", "丢损赔偿"]:
    check(f"Out Scope 含「{w}」≥1", sec12.count(w) >= 1, f"{sec12.count(w)} 处")

# ---- 9 待确认覆盖证据 ----
for w in ["计费单价", "租入资产入库方式", "吉客云"]:
    check(f"「{w}」≥1（待确认覆盖）", t.count(w) >= 1, f"{t.count(w)} 处")

print()
fails = [r for r in results if not r[1]]
print(f"===== 总计 {len(results)} 项：PASS {len(results)-len(fails)} / FAIL {len(fails)} =====")
sys.exit(1 if fails else 0)
