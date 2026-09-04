# -*- coding: utf-8 -*-
# F01 v2.7 -> v2.8：B1 拆销售/采购双行+库存桥；L1/L2/L4 补采购订单节点；L4 补退租申请；
# 决策变更+入库来源注记；页脚演示提示；版本号。纪律：锚点精确替换 + assert 计数，禁整页写。
import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')

P = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\P3-R01-F01-业务流程导航图.html'
raw = open(P, 'rb').read()
NL = '\r\n' if b'\r\n' in raw else '\n'
s = raw.decode('utf-8')
print('行尾:', 'CRLF' if NL == '\r\n' else 'LF', ' 原长度:', len(s))

def rep(old, new, n=1):
    """精确字符串替换 + assert 计数（自动适配行尾）"""
    global s
    old = old.replace('\n', NL); new = new.replace('\n', NL)
    c = s.count(old)
    assert c == n, '匹配数异常 expect=%d got=%d : %r' % (n, c, old[:70])
    s = s.replace(old, new)

def block_replace(a1, a2, tail, new):
    """锚点定界块替换：从 a1 所在行行首，到 a2 结束（可延伸到 tail），整块换新"""
    global s
    new = new.replace('\n', NL)
    assert s.count(a1) == 1, 'a1 不唯一: %r' % a1
    assert s.count(a2) == 1, 'a2 不唯一: %r' % a2
    i = s.index(a1)
    i = s.rfind('\n', 0, i) + 1
    j = s.index(a2, i) + len(a2)
    if tail:
        j = s.index(tail, j) + len(tail)
    s = s[:i] + new + s[j:]

# ---------- 0. defs 加蓝色箭头 marker ----------
rep('''      <marker id="arr-soft" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#9ca3af"/></marker>''',
    '''      <marker id="arr-soft" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#9ca3af"/></marker>
      <marker id="arr-blue" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#2563eb"/></marker>''')

# ---------- 1. 第一张 SVG viewBox 加高 76 ----------
rep('<svg viewBox="0 0 1280 860"', '<svg viewBox="0 0 1280 936"')

# ---------- 2. B1 块：7节点单行 → 采购行+销售行+库存桥+注记 ----------
NEW_B1 = '''    <text x="40" y="80" fill="#9ca3af" font-size="8.5" font-family="'Geist Mono',monospace">采购线（独立 · 不以销定采）</text>

    <line x1="190" y1="114" x2="212" y2="114" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="362" y1="114" x2="384" y2="114" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <a href="采购管理/采购订单列表.html">
      <rect x="40" y="86" width="150" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="115" y="111" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">采购订单</text>
      <text x="115" y="130" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">零部件/器具 · 两类公用</text>
    </a>

    <a href="仓储作业/采购入库列表.html">
      <rect x="212" y="86" width="150" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="287" y="111" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">采购入库</text>
      <text x="287" y="130" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">凭订单到货验收</text>
    </a>

    <a href="仓储作业/库存查询.html">
      <rect x="384" y="86" width="150" height="56" rx="6" fill="rgba(37,99,235,0.08)" stroke="#2563eb" stroke-width="1"/>
      <text x="459" y="111" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">库存</text>
      <text x="459" y="130" fill="#2563eb" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">库存缓冲 · 五态统计</text>
    </a>

    <rect x="560" y="76" width="680" height="52" rx="6" fill="rgba(17,24,39,0.02)" stroke="#d1d5db" stroke-width="0.8" stroke-dasharray="4,3"/>
    <text x="574" y="94" fill="#9ca3af" font-size="8.5" font-family="'Geist Mono',monospace">决策变更：原"先销后采互通"（袁丽晶 21:46）→ 2026-09-04 王琳总拍板：销售/采购两条独立线 · 库存缓冲 · 不以销定采</text>
    <text x="574" y="112" fill="#9ca3af" font-size="8.5" font-family="'Geist Mono',monospace">入库凭单验收 · 指令来源4种：采购入库←采购订单 ｜ 租入入库←租入单 ｜ 退租入库←退租申请 ｜ 其他入库←手工（例外）</text>

    <path d="M 459 142 V 156 H 287 V 168" fill="none" stroke="#2563eb" stroke-width="1" stroke-dasharray="4,3" marker-end="url(#arr-blue)"/>
    <text x="447" y="152" fill="#2563eb" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="end">库存缓冲 · 按可用量发货</text>

    <text x="40" y="162" fill="#9ca3af" font-size="8.5" font-family="'Geist Mono',monospace">销售线（独立）</text>

    <line x1="190" y1="196" x2="212" y2="196" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="362" y1="196" x2="384" y2="196" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="534" y1="196" x2="556" y2="196" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="706" y1="196" x2="728" y2="196" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <a href="销售管理/销售订单列表.html">
      <rect x="40" y="168" width="150" height="56" rx="6" fill="rgba(75,85,99,0.10)" stroke="#4b5563"/>
      <text x="115" y="193" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">销售订单</text>
      <text x="115" y="212" fill="#6b7280" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">客户PO · 代下单</text>
    </a>

    <a href="仓储作业/销售出库列表.html">
      <rect x="212" y="168" width="150" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="287" y="193" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">销售出库</text>
      <text x="287" y="212" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">按库存可用量发货</text>
    </a>

    <a href="财务协同/应收账单.html">
      <rect x="384" y="168" width="150" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="459" y="193" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">应收账单</text>
      <text x="459" y="212" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">销售费自动汇总</text>
    </a>

    <a href="财务协同/开票登记.html">
      <rect x="556" y="168" width="150" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="631" y="193" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">开票登记</text>
      <text x="631" y="212" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">发票登记 · 上传</text>
    </a>

    <a href="财务协同/银行水单核销.html">
      <rect x="728" y="168" width="150" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="803" y="193" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">收款核销</text>
      <text x="803" y="212" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">回款 · 水单勾对</text>
    </a>'''
block_replace('x1="190" y1="108" x2="212" y2="108"', '回款 · 水单勾对</text>', '</a>', NEW_B1)
print('B1 双行改造完成')

# ---------- 3. 区域 y 坐标 +76（B1 分隔线 → 第一张 </svg> 前） ----------
i0 = s.index('<line x1="40" y1="172"')
i1 = s.index('</svg>', i0)
seg = s[i0:i1]
cnt_y  = len(re.findall(r'\b(?:y1|y2|y)="\d+"', seg))
cnt_m  = len(re.findall(r'M \d+ \d+', seg))
cnt_v  = len(re.findall(r'V \d+', seg))
seg = re.sub(r'\b(y1|y2|y)="(\d+)"', lambda m: '%s="%d"' % (m.group(1), int(m.group(2)) + 76), seg)
seg = re.sub(r'(M \d+ )(\d+)', lambda m: m.group(1) + str(int(m.group(2)) + 76), seg)
seg = re.sub(r'(V )(\d+)', lambda m: m.group(1) + str(int(m.group(2)) + 76), seg)
assert len(re.findall(r'\b(?:y1|y2|y)="\d+"', seg)) == cnt_y
s = s[:i0] + seg + s[i1:]
print('区域下移 +76：y属性 %d 处 / M起点 %d 处 / V坐标 %d 处' % (cnt_y, cnt_m, cnt_v))
assert cnt_m == 2 and cnt_v == 4, 'L1/L2 回流路径数量异常'

# ---------- 4. L1：头部加采购订单（8节点，140宽16距） ----------
NEW_L1 = '''    <line x1="180" y1="310" x2="196" y2="310" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="336" y1="310" x2="352" y2="310" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="492" y1="310" x2="508" y2="310" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="648" y1="310" x2="664" y2="310" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="804" y1="310" x2="820" y2="310" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="960" y1="310" x2="976" y2="310" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="1116" y1="310" x2="1132" y2="310" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <a href="采购管理/采购订单列表.html">
      <rect x="40" y="282" width="140" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="110" y="307" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">采购订单</text>
      <text x="110" y="326" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">器具 · 资产采购</text>
    </a>

    <a href="仓储作业/采购入库列表.html">
      <rect x="196" y="282" width="140" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="266" y="307" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">采购入库</text>
      <text x="266" y="326" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">凭单验收 · 资产入库</text>
    </a>

    <a href="包装管理/租赁单列表.html">
      <rect x="352" y="282" width="140" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="422" y="307" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租赁单</text>
      <text x="422" y="326" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">单一器具 · 直接出租</text>
    </a>

    <a href="仓储作业/组合出库列表.html">
      <rect x="508" y="282" width="140" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="578" y="307" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">组合出库</text>
      <text x="578" y="326" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">出库确认</text>
    </a>

    <a href="包装管理/退租申请列表.html">
      <rect x="664" y="282" width="140" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="734" y="307" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">退租申请</text>
      <text x="734" y="326" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">客户退回申请</text>
    </a>

    <a href="仓储作业/退租入库列表.html">
      <rect x="820" y="282" width="140" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="890" y="307" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">退租入库</text>
      <text x="890" y="326" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">缺损核对 · 回库</text>
    </a>

    <a href="包装管理/丢损赔偿单.html">
      <rect x="976" y="282" width="140" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="1046" y="307" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">丢损赔偿</text>
      <text x="1046" y="326" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">按对象转 应收/应付</text>
    </a>

    <a href="包装管理/在租台账.html">
      <rect x="1132" y="282" width="140" height="56" rx="6" fill="rgba(37,99,235,0.08)" stroke="#2563eb" stroke-width="1"/>
      <text x="1202" y="307" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">在租台账</text>
      <text x="1202" y="326" fill="#2563eb" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">四态统计 · 平均租期</text>
    </a>

    <path d="M 1046 338 V 358 H 422 V 338" fill="none" stroke="#9ca3af" stroke-width="1" stroke-dasharray="5,4" marker-end="url(#arr-soft)"/>
    <rect x="660" y="351" width="148" height="13" rx="2" fill="#fafafa"/>
    <text x="734" y="361" fill="#9ca3af" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">器具回库 · 循环再出租</text>'''
block_replace('x1="190" y1="310" x2="212" y2="310"', '器具回库 · 循环再出租</text>', None, NEW_L1)
print('L1 补采购订单完成（8节点）')

# ---------- 5. L2：头部加采购订单（10节点，112宽12距） ----------
NEW_L2 = '''    <line x1="152" y1="450" x2="164" y2="450" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="276" y1="450" x2="288" y2="450" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="400" y1="450" x2="412" y2="450" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="524" y1="450" x2="536" y2="450" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="648" y1="450" x2="660" y2="450" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="772" y1="450" x2="784" y2="450" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="896" y1="450" x2="908" y2="450" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="1020" y1="450" x2="1032" y2="450" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="1144" y1="450" x2="1156" y2="450" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <a href="采购管理/采购订单列表.html">
      <rect x="40" y="422" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="96" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">采购订单</text>
      <text x="96" y="466" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">器具A/B/C 采购</text>
    </a>

    <a href="仓储作业/采购入库列表.html">
      <rect x="164" y="422" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="220" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">采购入库</text>
      <text x="220" y="466" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">凭单验收 · 入库</text>
    </a>

    <a href="基础数据/BOM.html">
      <rect x="288" y="422" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="344" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">BOM</text>
      <text x="344" y="466" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">定义配方 A+B→C</text>
    </a>

    <a href="仓储作业/组装列表.html">
      <rect x="412" y="422" width="112" height="56" rx="6" fill="rgba(37,99,235,0.08)" stroke="#2563eb" stroke-width="1"/>
      <text x="468" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">组装</text>
      <text x="468" y="466" fill="#2563eb" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">选父项C·自动带子件</text>
    </a>

    <a href="包装管理/租赁单列表.html">
      <rect x="536" y="422" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="592" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租赁单</text>
      <text x="592" y="466" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">组合件C·收租金</text>
    </a>

    <a href="仓储作业/组合出库列表.html">
      <rect x="660" y="422" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="716" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">组合出库</text>
      <text x="716" y="466" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">一箱一件·出库确认</text>
    </a>

    <a href="包装管理/退租申请列表.html">
      <rect x="784" y="422" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="840" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">退租申请</text>
      <text x="840" y="466" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">客户退回申请</text>
    </a>

    <a href="仓储作业/退租入库列表.html">
      <rect x="908" y="422" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="964" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">退租入库</text>
      <text x="964" y="466" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">按BOM拆散·缺损核对</text>
    </a>

    <a href="包装管理/丢损赔偿单.html">
      <rect x="1032" y="422" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="1088" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">丢损赔偿</text>
      <text x="1088" y="466" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">按对象转应收/应付</text>
    </a>

    <a href="包装管理/在租台账.html">
      <rect x="1156" y="422" width="112" height="56" rx="6" fill="rgba(37,99,235,0.08)" stroke="#2563eb" stroke-width="1"/>
      <text x="1212" y="447" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">在租台账</text>
      <text x="1212" y="466" fill="#2563eb" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">四态统计·平均租期</text>
    </a>

    <path d="M 964 478 V 498 H 468 V 478" fill="none" stroke="#9ca3af" stroke-width="1" stroke-dasharray="5,4" marker-end="url(#arr-soft)"/>
    <rect x="638" y="491" width="156" height="13" rx="2" fill="#fafafa"/>
    <text x="716" y="501" fill="#9ca3af" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">拆回散件 · 循环再组装</text>'''
block_replace('x1="164" y1="450" x2="178" y2="450"', '拆回散件 · 循环再组装</text>', None, NEW_L2)
print('L2 补采购订单完成（10节点）')

# ---------- 6. L4：头部加采购订单 + 补退租申请（10节点） ----------
NEW_L4 = '''    <line x1="152" y1="730" x2="164" y2="730" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="276" y1="730" x2="288" y2="730" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="400" y1="730" x2="412" y2="730" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="524" y1="730" x2="536" y2="730" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="648" y1="730" x2="660" y2="730" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="772" y1="730" x2="784" y2="730" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="896" y1="730" x2="908" y2="730" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="1020" y1="730" x2="1032" y2="730" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <line x1="1144" y1="730" x2="1156" y2="730" stroke="#4b5563" stroke-width="1" marker-end="url(#arr)"/>

    <a href="采购管理/采购订单列表.html">
      <rect x="40" y="702" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="96" y="727" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">采购订单</text>
      <text x="96" y="746" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">自购辅材·器具类</text>
    </a>

    <a href="仓储作业/采购入库列表.html">
      <rect x="164" y="702" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="220" y="727" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">采购入库</text>
      <text x="220" y="746" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">凭单验收 · 入库</text>
    </a>

    <a href="采购管理/租入单列表.html">
      <rect x="288" y="702" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="344" y="727" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租入单</text>
      <text x="344" y="746" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">租入大箱/围板箱</text>
    </a>

    <a href="仓储作业/组装列表.html">
      <rect x="412" y="702" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="468" y="727" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">混合组装</text>
      <text x="468" y="746" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">自购+租入→C</text>
    </a>

    <a href="包装管理/租赁单列表.html">
      <rect x="536" y="702" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="592" y="727" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">租赁单</text>
      <text x="592" y="746" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">组合C出租</text>
    </a>

    <a href="仓储作业/组合出库列表.html">
      <rect x="660" y="702" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="716" y="727" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">组合出库</text>
      <text x="716" y="746" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">出库确认</text>
    </a>

    <a href="包装管理/退租申请列表.html">
      <rect x="784" y="702" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="840" y="727" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">退租申请</text>
      <text x="840" y="746" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">客户退回申请</text>
    </a>

    <a href="仓储作业/退租入库列表.html">
      <rect x="908" y="702" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="964" y="727" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">退租入库</text>
      <text x="964" y="746" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">按BOM拆散件</text>
    </a>

    <a href="仓储作业/租入归还列表.html">
      <rect x="1032" y="702" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="1088" y="727" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">分流归还</text>
      <text x="1088" y="746" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">自购回库·租入归还</text>
    </a>

    <a href="财务协同/应付账单.html">
      <rect x="1156" y="702" width="112" height="56" rx="6" fill="#ffffff" stroke="#111827" stroke-width="1"/>
      <text x="1212" y="727" fill="#111827" font-size="12.5" font-weight="600" font-family="'Geist',sans-serif" text-anchor="middle">多线应付</text>
      <text x="1212" y="746" fill="#4b5563" font-size="8.5" font-family="'Geist Mono',monospace" text-anchor="middle">采购+租金+赔付</text>
    </a>'''
block_replace('x1="180" y1="730" x2="196" y2="730"', '采购+租金+赔付 → 应付</text>', '</a>', NEW_L4)
print('L4 补采购订单+退租申请完成（10节点）')

# ---------- 7. S2 库存查询四态 → 五态（与库存查询页一致） ----------
rep('>库存查询（四态）</text><text x="260" y="170" fill="#6b7280" font-size="8.5" font-family="\'Geist Mono\',monospace" text-anchor="middle">在库/在途/客户端/退租</text>',
    '>库存查询（五态）</text><text x="260" y="170" fill="#6b7280" font-size="8.5" font-family="\'Geist Mono\',monospace" text-anchor="middle">在库/在途/客户/退租/租入</text>')

# ---------- 8. 版本号 v2.7 → v2.8（title/eyebrow/sub/footer） ----------
rep('<title>P3-R01-F01 · 业务流程导航图（v2.7）</title>', '<title>P3-R01-F01 · 业务流程导航图（v2.8）</title>')
rep('<p class="eyebrow">P3-R01-F01 · v2.7 原型业务流程导航</p>', '<p class="eyebrow">P3-R01-F01 · v2.8 原型业务流程导航</p>')
rep('包装租赁管理后台原型 v2.7 · ', '包装租赁管理后台原型 v2.8 · ')
rep('· <b>7</b> 条支线 · 实体节点点击直达</p>',
    '· <b>7</b> 条支线 · B1 销售/采购双线独立+库存缓冲（09-04 王琳总拍板）· 实体节点点击直达</p>')
rep('<footer>P3-R01-F01 · v2.7 · 2026-09-04 · 汽车物流包装租赁 · 包装租赁管理后台原型 · 45 页 / 5 条主线泳道（B1/L1/L2/L3/L4 全部第一期实现·L3/L4 为 2026-09-04 拍板升级）+ 7 条支线 · 全部流程化跳转 · 44 个弹窗可独立演示 · 单一管理端 · 订单唯一来源：项目经理代下销售订单（客户PO）</footer>',
    '<footer>P3-R01-F01 · v2.8 · 2026-09-04 · 汽车物流包装租赁 · 包装租赁管理后台原型 · 45 页 / 5 条主线泳道（B1/L1/L2/L3/L4 全部第一期实现·L3/L4 为 2026-09-04 拍板升级）+ 7 条支线 · 全部流程化跳转 · 44 个弹窗可独立演示 · 单一管理端 · 订单唯一来源：项目经理代下销售订单（客户PO）· 演示建议：从 L1/L2 租赁线开始（在租台账四态卡为亮点），再走 B1 买卖线（更简单快速）· F02 演示流程图已归档，演示统一用本图</footer>')

# ---------- 9. B1 会议材料弹窗补 2026-09-04 录音依据 ----------
rep("""    ['第2次沟通 [音频转写] · 袁丽晶 21:46','"先销售后采购，或者我采购订单先入库之后再生成销售订单，我觉得这个可以互通关系都没问题"'],
  ]},""",
    """    ['第2次沟通 [音频转写] · 袁丽晶 21:46','"先销售后采购，或者我采购订单先入库之后再生成销售订单，我觉得这个可以互通关系都没问题"'],
    ['决策变更 · 第3次沟通前内部沟通 [音频转写] · 王琳总 2:18 / 2:36','"销售和采购不是匹配关系……不是以销定产，肯定不是以销定产。即使它是，也要人为把它拆开"；"这是两条线，销售直接就是销售出入，采购是单独的"'],
    ['同上 · 王琳总 0:40 / 1:35 / 3:27','"采购订单分两类，一类是采购零件的……可以公用"；"肯定要入库指令才能入库……知道你要入十个，我还验收，来的是不是十个……信息和物资去匹配才能形成完整的闭环"；"入库的指令来源于4种"'],
    ['同上 · 道远 3:49（王琳总确认）','"这个退租入库给它拆出来……主要复杂就在于要退租"——各租赁线 退租申请→退租入库 独立成段'],
  ]},""")
rep("出处：2026-09-02 第2次沟通材料（转写/纪要/会后补充/落实计划）</div>",
    "出处：2026-09-02 第2次沟通材料（转写/纪要/会后补充/落实计划）＋ 2026-09-04 第3次沟通前内部沟通 [音频转写]</div>")

# ---------- 写回 + 校验 ----------
open(P, 'wb').write(s.encode('utf-8'))
print('已写回，新长度:', len(s))

# 校验1：被否画法已清除
assert '关联销售单生成' not in s, '残留被否副标'
# 校验2：两张 SVG 均可被 XML 解析（标签配平）
import xml.etree.ElementTree as ET
for k, m in enumerate(re.finditer(r'<svg.*?</svg>', s, re.S), 1):
    ET.fromstring(m.group(0))
    print('SVG%d 标签配平 OK' % k)
# 校验3：节点计数
svg1 = re.search(r'<svg.*?</svg>', s, re.S).group(0)
print('第一张SVG：采购订单节点=%d（应4：B1/L1/L2/L4） 退租申请节点=%d（应4） 库存节点=%d（应1）' % (
    svg1.count('>采购订单</text>'), svg1.count('>退租申请</text>'), svg1.count('>库存</text>')))
print('全部校验通过')
