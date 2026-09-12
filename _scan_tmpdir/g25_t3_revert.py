# -*- coding: utf-8 -*-
"""G25 T3 前提修正回退（干净版）：删除插入块 "\r\n\r\n+block"，恢复 14 行态
block=从 G25 注释行到段尾 "\r\n\r\n  }," 之前（含拼接逗号结尾 "    },"）
"""
import io, re, sys, subprocess

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
DD = ROOT + r"\_data\demo-data.js"

txt = io.open(DD, encoding="utf-8", newline="").read()
marker = "    /* ===== 供应商应收（路凯赔付我方 · 租入器具损坏 · 手动建单，2026-09-12 G25 R-01） ===== */"
i = txt.find(marker)
assert i > 0, "未找到插入块注释行"
k = txt.find("\r\n\r\n  },", i)
assert k > i, "未找到段尾"
block = txt[i:k]
assert block.rstrip().endswith("    },"), "块尾异常: %r" % block[-20:]
assert txt.count(block) == 1, "块非唯一"
txt2 = txt.replace("\r\n\r\n" + block, "\r\n\r\n", 1)
io.open(DD, "w", encoding="utf-8", newline="").write(txt2)

# 终态断言
t3 = io.open(DD, encoding="utf-8", newline="").read()
assert t3.count("AR-2026-09-PRJ2601-SUP") == 0, "仍含新键"
assert t3.count("AR-20260904-015") == 3, "既有行 3 处应保留"
assert t3.count("G25 R-01") == 0, "注释残留"
r = subprocess.run(["node", "--check", DD], capture_output=True, text=True)
assert r.returncode == 0, r.stderr[:300]
# 行数与供应商应收行计数（node 执行）
rc = subprocess.run(["node", "-e", (
    "global.window={};const fs=require('fs');"
    "const src=fs.readFileSync(process.argv[1],'utf8');"
    "eval(src);"
    "const D=window.DEMO_DATA.receivableBills;"
    "const ks=Object.keys(D).filter(k=>D[k].row);"
    "console.log('rows='+ks.length+' sup='+ks.filter(k=>D[k].row.fields.btype==='供应商应收').length)"
), DD], capture_output=True, text=True)
print("node 计数:", rc.stdout.strip(), rc.stderr[:150])
raw = open(DD, "rb").read()
print("PASS 回退：node --check=0·CRLF=%d 裸LF=%d" % (raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")))
assert "rows=14 sup=1" in rc.stdout, "回退后应 14 行·供应商应收 1"
print("PASS receivableBills 恢复 14 行（供应商应收既有行 AR-20260904-015 保留）")
