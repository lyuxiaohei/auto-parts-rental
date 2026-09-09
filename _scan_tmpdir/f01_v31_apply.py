# -*- coding: utf-8 -*-
"""G06-F01 v3.0→v3.1 改造（合并命令 T1）：租赁四线插库存节点 + 标签 组合出库→租赁出库 + 版本叙事。
纪律：读取-精确替换 + assert 计数；二进制读写保行尾；只改 F01 一个文件。"""
import sys

P = r"P3-R01-包装租赁管理后台原型/P3-R01-F01-业务流程导航图.html"
data = open(P, "rb").read()
t = data.decode("utf-8")
assert b"\r" not in data, "含 CR，行尾口径变化"

def rep(old, new, n=1):
    global t
    c = t.count(old)
    assert c == n, f"匹配数 {c} != {n}：{old[:60]!r}"
    t = t.replace(old, new)

ARROW = 'stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>'

# ---------- B1 L1：采购入库→[库存 自有在库]→租赁单→租赁出库 ----------
rep(f'    <line x1="492" y1="310" x2="508" y2="310" {ARROW}\n',
    f'    <line x1="492" y1="310" x2="508" y2="310" {ARROW}\n\n    <line x1="648" y1="310" x2="664" y2="310" {ARROW}\n')
rep('''    <a href="租赁管理/租赁单列表.html">
      <rect x="352" y="282" width="140" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="422" y="307" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租赁单</text>
      <text x="422" y="326" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">单一器具 · 直接出租</text>
    </a>''',
'''    <a href="仓储作业/库存查询.html">
      <rect x="352" y="282" width="140" height="56" rx="6" fill="rgba(37,99,235,0.08)" stroke="#2563eb" stroke-width="1"/>
      <text x="422" y="307" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">库存</text>
      <text x="422" y="326" fill="#2563eb" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">自有在库</text>
    </a>

    <a href="租赁管理/租赁单列表.html">
      <rect x="508" y="282" width="140" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="578" y="307" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租赁单</text>
      <text x="578" y="326" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">单一器具 · 直接出租</text>
    </a>''')
rep('''    <a href="租赁管理/组合出库列表.html">
      <rect x="508" y="282" width="140" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="578" y="307" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">组合出库</text>
      <text x="578" y="326" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">出库确认</text>
    </a>
    <text x="664" y="314" fill="#9ca3af" font-size="9.5" font-family="'Geist Mono',monospace">→ 退租及后续见 T1 专项</text>''',
'''    <a href="租赁管理/组合出库列表.html">
      <rect x="664" y="282" width="140" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="734" y="307" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租赁出库</text>
      <text x="734" y="326" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">出库确认</text>
    </a>
    <text x="820" y="314" fill="#9ca3af" font-size="9.5" font-family="'Geist Mono',monospace">→ 退租及后续见 T1 专项</text>''')

# ---------- B1 L2：采购入库→[库存 自有在库·组合前]→BOM→按BOM租赁出库→租赁单→租赁出库 ----------
rep(f'    <line x1="648" y1="450" x2="660" y2="450" {ARROW}\n',
    f'    <line x1="648" y1="450" x2="660" y2="450" {ARROW}\n\n    <line x1="772" y1="450" x2="784" y2="450" {ARROW}\n')
rep('''    <a href="基础数据/BOM.html">
      <rect x="288" y="422" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="344" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">BOM</text>
      <text x="344" y="466" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">定义配方 A+B→C</text>
    </a>''',
'''    <a href="仓储作业/库存查询.html">
      <rect x="288" y="422" width="112" height="56" rx="6" fill="rgba(37,99,235,0.08)" stroke="#2563eb" stroke-width="1"/>
      <text x="344" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">库存</text>
      <text x="344" y="466" fill="#2563eb" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">自有在库·组合前</text>
    </a>

    <a href="基础数据/BOM.html">
      <rect x="412" y="422" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="468" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">BOM</text>
      <text x="468" y="466" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">定义配方 A+B→C</text>
    </a>''')
rep('''    <a href="租赁管理/组合出库列表.html">
      <rect x="412" y="422" width="112" height="56" rx="6" fill="rgba(37,99,235,0.08)" stroke="#2563eb" stroke-width="1"/>
      <text x="468" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">按 BOM 组合出库</text>''',
'''    <a href="租赁管理/组合出库列表.html">
      <rect x="536" y="422" width="112" height="56" rx="6" fill="rgba(37,99,235,0.08)" stroke="#2563eb" stroke-width="1"/>
      <text x="592" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">按 BOM 租赁出库</text>''')
rep('''      <text x="468" y="466" fill="#2563eb" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">出库时组合扣减组件（无组装单）</text>''',
'''      <text x="592" y="466" fill="#2563eb" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">出库时组合扣减组件（无组装单）</text>''')
rep('''    <a href="租赁管理/租赁单列表.html">
      <rect x="536" y="422" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="592" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租赁单</text>
      <text x="592" y="466" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">组合件C·收租金</text>
    </a>''',
'''    <a href="租赁管理/租赁单列表.html">
      <rect x="660" y="422" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="716" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租赁单</text>
      <text x="716" y="466" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">组合件C·收租金</text>
    </a>''')
rep('''    <a href="租赁管理/组合出库列表.html">
      <rect x="660" y="422" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="716" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">组合出库</text>
      <text x="716" y="466" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">一箱一件·出库确认</text>
    </a>
    <text x="784" y="454" fill="#9ca3af" font-size="9.5" font-family="'Geist Mono',monospace">→ 退租及后续见 T1 专项</text>''',
'''    <a href="租赁管理/组合出库列表.html">
      <rect x="784" y="422" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="840" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租赁出库</text>
      <text x="840" y="466" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">一箱一件·出库确认</text>
    </a>
    <text x="908" y="454" fill="#9ca3af" font-size="9.5" font-family="'Geist Mono',monospace">→ 退租及后续见 T1 专项</text>''')

# ---------- B1 L3：租入入库→[库存 租入在库]→租赁单→租赁出库 ----------
rep(f'    <line x1="492" y1="590" x2="508" y2="590" {ARROW}\n',
    f'    <line x1="492" y1="590" x2="508" y2="590" {ARROW}\n\n    <line x1="648" y1="590" x2="664" y2="590" {ARROW}\n')
rep('''    <a href="租赁管理/租赁单列表.html">
      <rect x="352" y="562" width="140" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="422" y="587" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租赁单</text>
      <text x="422" y="606" fill="#6b7280" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">转租客户</text>
    </a>''',
'''    <a href="仓储作业/库存查询.html">
      <rect x="352" y="562" width="140" height="56" rx="6" fill="rgba(37,99,235,0.08)" stroke="#2563eb" stroke-width="1"/>
      <text x="422" y="587" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">库存</text>
      <text x="422" y="606" fill="#2563eb" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">租入在库</text>
    </a>

    <a href="租赁管理/租赁单列表.html">
      <rect x="508" y="562" width="140" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="578" y="587" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租赁单</text>
      <text x="578" y="606" fill="#6b7280" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">转租客户</text>
    </a>''')
rep('''    <a href="租赁管理/组合出库列表.html">
      <rect x="508" y="562" width="140" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="578" y="587" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">组合出库</text>
      <text x="578" y="606" fill="#6b7280" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">出库确认</text>
    </a>
    <text x="664" y="594" fill="#9ca3af" font-size="9.5" font-family="'Geist Mono',monospace">→ 退租及后续见 T1 专项</text>''',
'''    <a href="租赁管理/组合出库列表.html">
      <rect x="664" y="562" width="140" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="734" y="587" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租赁出库</text>
      <text x="734" y="606" fill="#6b7280" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">出库确认</text>
    </a>
    <text x="820" y="594" fill="#9ca3af" font-size="9.5" font-family="'Geist Mono',monospace">→ 退租及后续见 T1 专项</text>''')

# ---------- B1 L4：双入库线汇聚→[库存 自有+租入在库]→混合组装→租赁单→租赁出库 ----------
rep('''    <a href="租赁管理/组合出库列表.html">
      <rect x="336" y="768" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="392" y="793" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">混合组装</text>
      <text x="392" y="812" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">自购+租入→C</text>
    </a>''',
'''    <a href="仓储作业/库存查询.html">
      <rect x="336" y="768" width="112" height="56" rx="6" fill="rgba(37,99,235,0.08)" stroke="#2563eb" stroke-width="1"/>
      <text x="392" y="793" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">库存</text>
      <text x="392" y="812" fill="#2563eb" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">自有+租入在库</text>
    </a>
    <a href="租赁管理/组合出库列表.html">
      <rect x="460" y="768" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="516" y="793" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">混合组装</text>
      <text x="516" y="812" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">自购+租入→C</text>
    </a>''')
rep('''    <a href="租赁管理/租赁单列表.html">
      <rect x="460" y="768" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="516" y="793" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租赁单</text>
      <text x="516" y="812" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">组合C出租</text>
    </a>''',
'''    <a href="租赁管理/租赁单列表.html">
      <rect x="584" y="768" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="640" y="793" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租赁单</text>
      <text x="640" y="812" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">组合C出租</text>
    </a>''')
rep(f'''    <line x1="448" y1="796" x2="460" y2="796" {ARROW}
    <line x1="572" y1="796" x2="584" y2="796" {ARROW}''',
f'''    <line x1="448" y1="796" x2="460" y2="796" {ARROW}
    <line x1="572" y1="796" x2="584" y2="796" {ARROW}
    <line x1="696" y1="796" x2="708" y2="796" {ARROW}''')
rep('''    <a href="租赁管理/组合出库列表.html">
      <rect x="584" y="768" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="640" y="793" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">组合出库</text>
      <text x="640" y="812" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">出库确认</text>
    </a>
    <text x="708" y="800" fill="#9ca3af" font-size="9.5" font-family="'Geist Mono',monospace">→ 退租及后续见 T1 专项</text>''',
'''    <a href="租赁管理/组合出库列表.html">
      <rect x="708" y="768" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="764" y="793" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租赁出库</text>
      <text x="764" y="812" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">出库确认</text>
    </a>
    <text x="832" y="800" fill="#9ca3af" font-size="9.5" font-family="'Geist Mono',monospace">→ 退租及后续见 T1 专项</text>''')

# ---------- T1 泳道 L2 回链标签：再组合出库→再租赁出库 ----------
rep('>再组合出库</text>', '>再租赁出库</text>')

# ---------- B2 叙事层（头部 sub / L2 应收注 / footer / SRC_DATA 弹层 / S5 支线） ----------
rep('（按 BOM 组合出库·按零件入库·赔偿直建账单）', '（按 BOM 租赁出库·按零件入库·赔偿直建账单）')  # 头部 sub
rep('（按组合出库自动汇总）', '（按租赁出库自动汇总）')                                                # L2 应收注
rep('按 BOM 组合出库/按零件入库', '按 BOM 租赁出库/按零件入库')                                        # footer
rep('泳道止于组合出库，退租后链路全部归 T1', '泳道止于租赁出库，退租后链路全部归 T1')                    # SRC_DATA t1
rep('>组合出库录单</text>', '>租赁出库录单</text>', 2)                                                  # S5 两节点
rep('⟷ 组合出库列表</text>', '⟷ 租赁出库列表</text>', 2)                                                # S5 两副标

# ---------- B3 版本叙事 v3.0→v3.1（头部+footer；历史句保留） ----------
rep('<title>P3-R01-F01 · 业务流程导航图（v3.0）</title>', '<title>P3-R01-F01 · 业务流程导航图（v3.1）</title>')
rep('P3-R01-F01 · v3.0 原型业务流程导航', 'P3-R01-F01 · v3.1 原型业务流程导航')
rep('包装租赁管理后台原型 v3.0（2026-09-08 会议改造）', '包装租赁管理后台原型 v3.1（2026-09-09 修正 · v3.0=09-08 会议改造）')
rep('· 财务 4v4 · 客户虚拟仓/客户转租</p>', '· 财务 4v4 · 客户虚拟仓/客户转租 · v3.1（09-09 修正）：租赁四线以库存为联系（与买卖线同构）·出库术语与菜单对齐（租赁出库）</p>')
rep('P3-R01-F01 · v3.0 · 2026-09-09', 'P3-R01-F01 · v3.1 · 2026-09-09')
rep('·客户虚拟仓/客户转租·六角色审核</footer>', '·客户虚拟仓/客户转租·六角色审核 · v3.1（09-09 修正）：租赁四线以库存为联系（与买卖线同构）·出库术语与菜单对齐（租赁出库）</footer>')

# ---------- 收尾自检 ----------
assert t.count('组合出库') == 10, f"组合出库 残留 {t.count('组合出库')} 处（应=10：href 列表 8+录单 2）"
outside = sum(ln.count('组合出库') for ln in t.split('\n') if 'href="' not in ln)
assert outside == 0, f"href 外 组合出库 残留 {outside} 处"
assert t.count('租赁出库') >= 16, f"租赁出库 {t.count('租赁出库')} <16"
assert t.count('v3.1') >= 1 and t.count('v3.0') == 3, f"版本字样 v3.1={t.count('v3.1')} v3.0={t.count('v3.0')}（应保留历史 3）"
assert t.count('<a ') == t.count('</a>'), "a 标签不配平"
assert t.count('<text') == t.count('</text>'), "text 标签不配平"
import re as _re
assert len(_re.findall(r'<rect\b[^>]*?/>', t)) == t.count('<rect'), "rect 标签未全部自闭合"

open(P, "wb").write(t.encode("utf-8"))
print("==== f01_v31_apply 完成：24 组精确替换全过，组合出库仅存 href 路径串 10 处，租赁出库", t.count('租赁出库'), "处，v3.1", t.count('v3.1'), "处 ====")
