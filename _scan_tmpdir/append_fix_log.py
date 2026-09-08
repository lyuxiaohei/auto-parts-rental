# -*- coding: utf-8 -*-
"""回归修复台账：P1-R05 变更记录（五）+ P1-R01 10.2 补记 + verify 盲区教训"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
P5 = ROOT / 'P1-R05-agent交接文档.md'
P1 = ROOT / 'P1-R01-需求梳理与功能框架.md'

CHG = """
## 变更记录 · 2026-09-08（五）（列表驱动回归修复 · 道远目检"大部分页面空白列"）

**现象与根因**：道远打开原型发现大部分列表页出现空白列。根因＝2026-09-08（三）列表数据驱动执行器的提取 bug——demo-data.js 新注入的 **192 条 row 的 cells 误带外层 `<td>` 标签**（提取脚本取了完整 td 而非 innerHTML），list-generic 渲染时再包一层 `<td>` 形成嵌套 td，浏览器解析时把每个数据格拆成"空格＋内容格"两个单元格，列数翻倍、表头之下大面积错位出空白列。试点 17 条（上轮会话手写）不带 td 壳故正常——所以恰好是本轮推广的 30 页中招。

**为何验证门没拦住**：verify 断言只查了行数/单号列/详情标题/过滤/计数，**未断言列结构与单元格内容**——嵌套 td 不改变 tr 数、单号列在第 1 格不受影响。教训：**行渲染类改动的验证必须包含"每行 td 数=表头 th 数"与"首行逐格文本=数据源 cells"两条结构断言**（已补入 verify_listfull.py 断言 1b/1c，本轮复跑三批 120+88+85=293 项全绿）。

**修复**（fix_cells_nested_td.py + fix_colparity.py）：
1. 192 条 row 的 cells 剥离外层 `<td...>`/`</td>`（幂等，试点 17 条不含 td 不动；json 逐行重序列化，node 语法前后双门）
2. 顺带修复两处**页面原生列数不匹配**（1b 断言暴露，改动前备份即如此，非本轮引入）：①器具档案行缺「租金单价(元/天)」格（th12 vs td11，页面作者漏格致操作列被挤空）——6 条 row 按详情实体既有「日租金」值补格（38.00/32.00/12.00/18.00/7.80/8.50，数据有据不自造）；②BOM维护版本表行多「配方来源」格（th5 vs td6）——表头补 `<th>配方来源</th>` 对齐（6=6）

**验证**：verify_listfull.py 三批复跑 293 项断言全绿（含新增 1b 列结构=表头列数、1c 首行逐格=实体 cells）；全量 audit 死链 0 / 相对基线新增 0（F01 报 1 条 Google Fonts 外链 ERR_CONNECTION_RESET＝当前网络对该外链持续不可达的资源加载失败，非脚本错误，页面既有外链且本轮 F01 仅注入 4 行滚动条 CSS，按外链网络豁免口径注明）；滚动条 styleSheets 断言复跑 124/124；截图视觉复核（AI 视觉检查器实看）退租入库列表/器具档案/应付账单——无空白列、无列错位、租金单价格就位、操作列复位。执行脚本 `fix_cells_nested_td.py`/`fix_colparity.py` 留档。
"""

r5 = P5.read_bytes().decode('utf-8')
assert r5.endswith('\n')
P5.write_bytes((r5 + CHG).encode('utf-8'))
print('P1-R05 变更记录（五）OK')

r1 = P1.read_bytes().decode('utf-8')
old = 'styleSheets 断言 124/124、三类 15 截图、audit 0/0/0（P1-R05 变更记录 2026-09-08（四））|'
new = 'styleSheets 断言 124/124、三类 15 截图、audit 0/0/0（P1-R05 变更记录 2026-09-08（四））。**09-08·列表驱动回归修复**：道远目检发现空白列——192 条 row cells 误带外层 td 致渲染嵌套、浏览器拆出空白列（执行器提取 bug，验证断言缺列结构检查未拦住）；剥离修复＋verify 补 1b/1c 列结构断言三批 293 项全绿＋器具档案/BOM维护两处页面原生列数不匹配顺手对齐（P1-R05 变更记录 2026-09-08（五））|'
assert r1.count(old) == 1
P1.write_bytes(r1.replace(old, new).encode('utf-8'))
print('P1-R01 附录 10.2 OK')
