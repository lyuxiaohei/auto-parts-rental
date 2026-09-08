# -*- coding: utf-8 -*-
"""任务三收尾：P1-R05 变更记录（四）滚动条改造 + P1-R01 附录 10.2 同步"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
P5 = ROOT / 'P1-R05-agent交接文档.md'
P1 = ROOT / 'P1-R01-需求梳理与功能框架.md'

CHG = """
## 变更记录 · 2026-09-08（四）（全站滚动条浅色改造 · 道远 goal 三任务之三）

**改动**：原型目录 124 个 HTML（45 业务页+79 弹窗独立页+F01，**BOM.html 按道远既有裁定不动**、99-归档不涉及）每页首个 `<style>` 块末尾注入四行固定规范——`::-webkit-scrollbar{width:6px;height:6px}` / thumb `#d9d9d9`+圆角 3px / hover `#c4c4c4` / track 透明（菜单/列表/弹窗滚动条统一浅色细条）；Python 二进制读写保行尾、style 标签配平逐页自检、幂等（页内已有 -webkit-scrollbar 跳过，本轮 0 页触发）。

**验证**：Playwright 遍历全站 `document.styleSheets` 断言 `-webkit-scrollbar-thumb` 规则存在且 background=`#d9d9d9`——**PASS 124/124**；三类 15 页截图（菜单溢出×5 / 宽表列表×5 / 长内容弹窗×5）+横向滚动条放大图存 `_scan_tmpdir/scrollbar-check/`；全量 audit 死链 0 / JS 错 0 / 相对基线新增 0（41 条=31 误报+10 豁免口径不变）。改前备份 `_scan_tmpdir/backup-scrollbar-20260908/`（124 文件按原相对路径）；执行脚本 `scrollbar_inject.py`/`scrollbar_verify.py` 留档。

"""

r5 = P5.read_bytes().decode('utf-8')
assert r5.endswith('\n')
P5.write_bytes((r5 + CHG).encode('utf-8'))
print('P1-R05 变更记录（四）OK')

r1 = P1.read_bytes().decode('utf-8')
old = 'verify_listfull.py 三批 233 断言全绿、三批全量审计死链 0/JS 错 0/新增 0；失败清单空|'
new = 'verify_listfull.py 三批 233 断言全绿、三批全量审计死链 0/JS 错 0/新增 0；失败清单空。**09-08·全站滚动条浅色改造**：124 页（BOM.html 除外）首个 style 块注入统一浅色滚动条规范（6px/thumb #d9d9d9），styleSheets 断言 124/124、三类 15 截图、audit 0/0/0（P1-R05 变更记录 2026-09-08（四））|'
assert r1.count(old) == 1
P1.write_bytes(r1.replace(old, new).encode('utf-8'))
print('P1-R01 附录 10.2 OK')
