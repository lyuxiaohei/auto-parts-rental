# -*- coding: utf-8 -*-
"""G24 验证门：P2-R02 报告结构断言（验证门 1）+ 原型零改动双门（验证门 2/3）"""
import io, os, re, sys, datetime

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁"
REPORT = os.path.join(ROOT, "P2-R02-决策落实与场景闭环检查报告.md")
PROTO = os.path.join(ROOT, "P3-R01-包装租赁管理后台原型")
TS = os.path.join(ROOT, "_scan_tmpdir", "g24_starttime.txt")

fails = []
def check(name, cond, detail=""):
    if cond:
        print(f"PASS  {name}" + (f"  [{detail}]" if detail else ""))
    else:
        print(f"FAIL  {name}  {detail}")
        fails.append(name)

t = io.open(REPORT, encoding="utf-8").read()
lines = t.splitlines()

# 1a 存在且行数
check("报告存在", os.path.exists(REPORT))
check("行数>=400", len(lines) >= 400, f"{len(lines)} 行")

# 1b 章节计数
for hdr in [r"^## 一、", r"^## 二\.1", r"^## 二\.2", r"^## 二\.3", r"^## 三、", r"^## 四、", r"^## 五、", r"^## 六、", r"^## 七、"]:
    n = sum(1 for l in lines if re.match(hdr, l))
    check(f"章节 {hdr} =1", n == 1, f"{n}")

# 1c 决策台账：D- 行五态覆盖 + 总数
d_rows = [l for l in lines if re.match(r"^\| D-\d+ \|", l)]
five = ["✅", "⚠", "❌", "⏸", "⊘"]
d_bad = [l[:12] for l in d_rows if not any(m in l for m in five)]
check("决策行五态覆盖=100%", not d_bad, f"{len(d_rows)} 行" + (f" 未覆盖:{d_bad}" if d_bad else ""))
d_ids = set(re.match(r"^\| (D-\d+) \|", l).group(1) for l in d_rows)
check("决策条数>=70", len(d_ids) >= 70, f"{len(d_ids)} 条")

# 1d 场景主表行（一-~七- 前缀）四态覆盖 + 行数
four = ["✅", "⚠", "❌", "⊘"]
s_rows = [l for l in lines if re.match(r"^\| [一二三四五六七]-\d+ \|", l)]
s_bad = [l[:14] for l in s_rows if not any(m in l for m in four)]
check("场景主表行四态覆盖=100%", not s_bad, f"{len(s_rows)} 行" + (f" 未覆盖:{s_bad}" if s_bad else ""))
check("场景主表行数>=74", len(s_rows) >= 74, f"{len(s_rows)} 行")
b_rows = [l for l in lines if re.match(r"^\| 补-\d+ \|", l)]
b_bad = [l[:8] for l in b_rows if not any(m in l for m in four)]
check("补充条四态覆盖=100%", not b_bad, f"{len(b_rows)} 行")
check("补充条数>=6", len(b_rows) >= 6, f"{len(b_rows)} 行")

# 1e 证据密度
n_html = t.count(".html")
check(".html 引用>=60", n_html >= 60, f"{n_html} 处")

# 1f 四/五/六/七 结构要素（按行首 ## 标题定节界，避免 #### 子节头子串误切）
hl = [(i, l) for i, l in enumerate(lines) if re.match(r"^## ", l)]
def sec_span(prefix):
    s = e = None
    for k, (i, l) in enumerate(hl):
        if re.match(r"^## " + prefix, l):
            s = i
            e = hl[k + 1][0] if k + 1 < len(hl) else len(lines)
            return "\n".join(lines[s:e])
    return ""
sec4 = sec_span("四、")
sec5 = sec_span("五、")
sec6 = sec_span("六、")
sec7 = sec_span("七、")
check("四节存在", sec4 != "")
check("五节存在", sec5 != "")
check("四节含结论行", "❌ 未落实 0 条" in sec4 and "⚠ 部分落实 4 条" in sec4)
check("五节含结论行", "❌ 断链 0 条" in sec5 and "⚠ 口径已变 5 条" in sec5)
check("六节含已知沿用+新发现", "已知沿用" in sec6 and "新发现" in sec6)
check("七节含 R- 编号", "R-01" in sec7 and "R-07" in sec7)

# 1g 术语纪律：含「组合出库」的行必须同行含「原文」
term_bad = [l[:40] for l in lines if "组合出库" in l and "原文" not in l]
check("叙述层旧称=0（引文行均带原文注记）", not term_bad, f"违例 {len(term_bad)} 行" + (f":{term_bad[:3]}" if term_bad else ""))

# 2 原型零改动门：mtime
ts = io.open(TS, encoding="utf-8").read().strip()
t0 = datetime.datetime.fromisoformat(ts)
viol = []
for dp, dns, fns in os.walk(PROTO):
    for fn in fns:
        fp = os.path.join(dp, fn)
        mt = datetime.datetime.fromtimestamp(os.path.getmtime(fp))
        if mt > t0:
            viol.append(os.path.relpath(fp, PROTO))
check("原型零改动·mtime 门", not viol, "违例=" + (";".join(viol) if viol else "空"))

# 汇总
print()
if fails:
    print(f"验证门结论：FAIL {len(fails)} 项 —— {fails}")
    sys.exit(1)
print("验证门结论：全部 PASS")
