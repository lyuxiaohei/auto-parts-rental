# -*- coding: utf-8 -*-
"""出货单打印：P2-R01 D-144 落账 + demo-data comboOutbounds ops + 录单页改动"""
import io, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'
FAILS = []
def rd(p):
    return io.open(ROOT + '\\' + p, encoding='utf-8', newline='').read()
def wr(p, t):
    io.open(ROOT + '\\' + p, 'w', encoding='utf-8', newline='').write(t)

# ---------- 1. P2-R01 D-144 ----------
p = r'P2-R01-产品需求文档.md'
t = rd(p)
if '| D-144 |' in t:
    print('D-144 已存在，跳过')
else:
    nums = sorted(int(x) for x in re.findall(r'^\| D-(\d+) \|', t, re.M))
    assert nums[-1] == 143, 'max D=%d 非 143' % nums[-1]
    i = t.find('| D-143 |')
    j = t.find('\n', i)
    row144 = ('\n| D-144 | **出货单打印页＋新建租赁出库简化**：①租赁出库列表操作栏加「**打印出货单**」→独立打印页'
              '（按道远 09-15 图样送货单版式：我方抬头＝环通循环包装运营（上海）有限公司／收货单位／送货日期／收货地址／收货人／'
              '送货单号 S+日期+序号／明细[订单号·Description物料描述·送货箱数·备注]·固定3行／一式三联[仓库·环通·客户留存]／'
              '司机·收货人签字／车牌号／签收日期·数据驱动取 comboOutbounds）；②录单页「出库备注」**移入基本信息**；'
              '③**随箱资料删除**；④**其他信息模块删除** | 道远 09-15 指示 | ✅（本轮落地） |')
    t = t[:j] + row144 + t[j:]
    hdr_old = '**G36 B1 弹窗页面化＋C2 库存查询项目闭环（D-132／D-130）✅**'
    hdr_new = '**出货单打印页＋录单简化（D-144）✅；前批 G36 B1 弹窗页面化＋C2 库存查询项目闭环（D-132／D-130）✅**'
    assert t.count(hdr_old) == 1
    t = t.replace(hdr_old, hdr_new)
    wr(p, t)
    print('D-144 落账 + 头部刷新')

# ---------- 2. demo-data comboOutbounds ops ----------
p = r'P3-R01-包装租赁管理后台原型\_data\demo-data.js'
t = rd(p)
if '打印出货单' in t:
    print('ops 已加过，跳过')
else:
    eol = '\r\n' if '\r\n' in t else '\n'
    lines = t.split(eol)
    # 定位 comboOutbounds 块
    i0 = next(i for i, l in enumerate(lines) if l.startswith('  comboOutbounds: {'))
    i1 = next(i for i, l in enumerate(lines) if i > i0 and l == '  },')
    patched = 0
    cur_key = None
    for idx in range(i0, i1 + 1):
        l = lines[idx]
        km = re.match(r"    '([A-Z][A-Z0-9-]+)': \{", l)
        if km:
            cur_key = km.group(1)
        if '"ops": [' in l and '打印出货单' not in l and cur_key:
            l2 = l.replace('"ops": [', '"ops": [{"t": "打印出货单", "act": "go(\'出货单打印.html?key=' + cur_key + '\')"}, ', 1)
            assert l2 != l
            lines[idx] = l2
            patched += 1
    print('comboOutbounds ops patched:', patched)
    if patched != 10:
        FAILS.append(('demo-ops', p, 'patched=%d expect 10' % patched))
    else:
        wr(p, eol.join(lines))

# ---------- 3. 录单页：备注移基本信息 + 删其他信息卡 ----------
p = r'P3-R01-包装租赁管理后台原型\租赁管理\租赁出库录单.html'
t = rd(p)
eol = '\r\n' if '\r\n' in t else '\n'
NOTE_ROW = (
'  <div class="form-row">' + eol +
'    <div class="form-label">出库备注：</div>' + eol +
'    <div>' + eol +
'      <div class="input-box" style="width:520px;"><input type="text" value="" placeholder="选填"></div>' + eol +
'    </div>' + eol +
'  </div>'
)
if '<div class="card">\r\n  <h3 class="card-title">其他信息</h3>' not in t and '<div class="card">\n  <h3 class="card-title">其他信息</h3>' not in t:
    if '出库备注' in t and '随箱资料' not in t:
        print('录单页已改过，跳过')
    else:
        FAILS.append(('recform', p, '锚未命中且非已完成态'))
else:
    # 3a. 删其他信息整卡（从 <div class="card"> 含其他信息 到其配平 </div>）
    m = re.search(r'<div class="card">[\s\S]*?<h3 class="card-title">其他信息</h3>[\s\S]*?</div>\s*</div>', t)
    assert m, '其他信息卡定位失败'
    card = m.group(0)
    assert '随箱资料' in card and '出库备注' in card
    opens = len(re.findall(r'<div\b', card)); closes = len(re.findall(r'</div>', card))
    assert opens == closes, '卡配平异常 %d/%d' % (opens, closes)
    t = t.replace(card + eol, '', 1) if (card + eol) in t else t.replace(card, '', 1)
    # 3b. 备注行插入基本信息卡末尾（要货日期 row 之后、基本信息卡闭合前）
    anchor = (
'  <div class="form-row">' + eol +
'    <div class="form-label"><span class="req">*</span>要货日期：</div>' + eol +
'    <div>' + eol +
'      <div class="input-box" style="width:180px;"><input type="text" value="2026-08-31" placeholder="请输入"></div>' + eol +
'    </div>' + eol +
'  </div>'
    )
    assert t.count(anchor) == 1, '要货日期锚 count=%d' % t.count(anchor)
    t = t.replace(anchor, anchor + eol + NOTE_ROW, 1)
    assert '随箱资料' not in t and '其他信息' not in t
    wr(p, t)
    print('录单页：备注移入基本信息 + 其他信息卡已删')

for f in FAILS:
    print('FAIL:', f)
print('DONE' if not FAILS else 'HAS FAILS')
