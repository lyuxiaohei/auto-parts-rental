# -*- coding: utf-8 -*-
"""退款登记菜单项加「退款」小节标题（参考「应付」组头样式）·全站侧边栏同步
幂等：前面已是退款标签则跳过；保留各页自身缩进与行尾风格"""
import re, time, sys, io
from pathlib import Path

ROOT = (Path(__file__).resolve().parents[1] / "P3-R01-包装租赁管理后台原型")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

STYLE = 'padding:4px 0 2px 48px;font-size:10px;color:#8c8c8c;letter-spacing:.08em;user-select:none;list-style:none'
LABEL = '<li style="' + STYLE + '">退款</li>'

# 菜单行三种形态：子目录页 ../ 前缀 / 根级页直连 / 退款登记页自身 selected
MENU = re.compile(
    r'^([ \t]*)<li><div class="sm-link( selected)?"( onclick="go\(\'(?:\.\./)?财务协同/退款登记\.html\'\)")?>退款登记</div></li>[ \t]*\r?\n',
    re.M)

def write_retry(p, data):
    for i in range(3):
        try:
            tmp = p.with_suffix(p.suffix + ".tmp")
            tmp.write_bytes(data)
            tmp.replace(p)
            return
        except OSError:
            if i == 2:
                raise
            time.sleep(0.3)

changed, skipped, nomatch = [], [], []
for p in sorted(ROOT.rglob("*.html")):
    if "mobile" in p.parts:
        continue
    raw = p.read_bytes()
    try:
        txt = raw.decode("utf-8")
    except UnicodeDecodeError:
        nomatch.append((str(p), "decode"))
        continue
    m = MENU.search(txt)
    if not m:
        continue
    # 幂等：菜单行上一行已是「退款」标签则跳过
    before = txt[:m.start()]
    if before.rstrip().endswith(">退款</li>"):
        skipped.append(str(p))
        continue
    indent = m.group(1)
    txt2 = txt[:m.start()] + indent + LABEL + "\r\n" if "\r\n" in txt[m.start():m.start()+200] else indent + LABEL + "\n"
    txt2 = txt[:m.start()] + indent + LABEL + ("\r\n" if m.group(0).endswith("\r\n") else "\n") + txt[m.start():]
    write_retry(p, txt2.encode("utf-8"))
    changed.append(str(p))

print("changed:", len(changed))
print("already-labeled (idempotent skip):", len(skipped))
print("nomatch/decode-err:", len(nomatch), nomatch[:5])
# 断言：含菜单行且未打标 0 残留
residual = 0
for p in sorted(ROOT.rglob("*.html")):
    if "mobile" in p.parts:
        continue
    txt = p.read_bytes().decode("utf-8", "ignore")
    m = MENU.search(txt)
    if m and not txt[:m.start()].rstrip().endswith(">退款</li>"):
        residual += 1
        print("RESIDUAL:", p)
print("residual:", residual)
sys.exit(1 if residual else 0)
