# -*- coding: utf-8 -*-
"""G37 T3：转租登记退场（库存查询 zz 双弹窗删除＋行内改转移出库跳转）＋F1 用词收敛
1. 库存查询.html：删 zzRegModal/zzBackModal/zzToast 三件；下钻说明改述；F1 列头（名称→物料名称/仓库→库房）；页面 pin-4 改述
2. demo-data stockFlows：8 行 zz ops 改向（5 转移出库跳新建带参·XNC-ZZ-WBX/BTC→终止转移跳详情·PLT 随 T4 回租出态→转移出库）
3. A03 标注 pin-4 note 改述
幂等：每步先查已改标志。"""
import io, os, re, sys, json
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def rd(p): return io.open(os.path.join(ROOT, p), encoding='utf-8', newline='').read()
def wr(p, s): io.open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='').write(s)

def cut_span(s, start_anchor, end_anchor):
    i = s.index(start_anchor)
    j = s.index(end_anchor, i) + len(end_anchor)
    while j < len(s) and s[j] in '\r\n ':
        j += 1
    return s[:i] + s[j:]

# ================= 1. 库存查询.html =================
p = os.path.join('仓储作业', '库存查询.html')
s = rd(p)
if 'zzRegModal' in s:
    assert s.count('zzRegModal') >= 5 and s.count('zzBackModal') >= 5, 'zz 弹窗计数异常'

if 'zzRegModal' in s:
    # 1a. 删两弹窗块（注释头到 zzBackModal 闭合）
    i = s.index('<!-- 客户转租登记/还回 弹窗')
    j = s.index('确认还回</button>')
    for _k in range(3):  # footer 闭合 → modal 闭合 → overlay 闭合
        j = s.index('</div>', j) + len('</div>')
    while j < len(s) and s[j] in '\r\n ':
        j += 1
    assert 'zzRegModal' in s[i:j] and 'zzBackModal' in s[i:j]
    s = s[:i] + s[j:]
    print('1a 两弹窗块已删')

    # 1b. 删 zz-toast 三件（css+div+两 script）
    s = cut_span(s, '<style id="zz-toast-css">', '</style>')
    s = cut_span(s, '<div id="zzToast"></div>', '<div id="zzToast"></div>')
    s = cut_span(s, '<script>/* 转租弹窗遮罩关闭自绑定', '</script>')
    s = cut_span(s, '<script id="zz-toast-js">', '</script>')
    assert 'zzToast' not in s and 'zzRegModal' not in s and 'zzBackModal' not in s, 'zz 残留'
    print('1b zzToast 三件已删')

    # 1c. 下钻说明改述
    old_desc = '转租＝在租的子状态：客户将器具转租给终端用户，按来源标记区分（库存状态「客户转租出」）。'
    new_desc = '客户转租由「转移出库单」承载（G37·D-146）：行内「转移出库」跳录单页（带出物料与在租客户），审核后库存状态转「客户转租出」。'
    assert s.count(old_desc) == 1
    s = s.replace(old_desc, new_desc)
    print('1c 下钻说明已改述')

    # 1d. F1 列头
    assert s.count('<th>名称</th>') == 1
    s = s.replace('<th>名称</th>', '<th>物料名称</th>')
    assert s.count('<th>仓库</th>') == 1
    s = s.replace('<th>仓库</th>', '<th>库房</th>')
    n_ff = s.count('<span class="ff-label">仓库：</span>')
    assert n_ff == 1, n_ff
    s = s.replace('<span class="ff-label">仓库：</span>', '<span class="ff-label">库房：</span>')
    n_lg = s.count("{ label: '仓库', field: 'area' }")
    assert n_lg == 1, n_lg
    s = s.replace("{ label: '仓库', field: 'area' }", "{ label: '库房', field: 'area' }")
    print('1d F1：物料名称/库房 列头+筛选 4 处')

    # 1e. 页面 pin-4 改述
    i = s.index('id="proto-pin-4"')
    seg = s[i:s.index('</div>', s.index('pnp-src', i)) + 6]
    if '转租还回' in seg or '转租登记' in seg:
        old_d = s.index('<div class="pnp-d">', i)
        old_d_end = s.index('</div>', old_d)
        new_note = ('<div class="pnp-d">转租定义：物料/BOM 已租给客户 A，A 再租给客户 B（终端用户）——记为「客户转租出」，不做所有权变更。<br>'
                    '承载（G37·D-146）：转移出库单——行内「转移出库」跳录单页（带出物料与在租客户）；审核生效后状态转「客户转租出」，单据「终止转移」后回「在客户（租出）」。<br>'
                    '结算：项目档案「转租结算方式」定默认（按租出/按终端·D-132），转移单可按单覆盖。</div>')
        s = s[:old_d] + new_note + s[old_d_end:]
        print('1e 页面 pin-4 改述')
    wr(p, s)
else:
    print('1 页面侧：已改（跳过）')

# ================= 2. demo-data ops 改向 =================
p2 = os.path.join('_data', 'demo-data.js')
d = rd(p2)
if "zzRegModal" in d or "zzBackModal" in d:
    i = d.index('stockFlows: {')
    j = d.index('\n  },', i)
    blk = d[i:j]
    ZY_NEW = "../租赁管理/转移出库新建.html"
    # 转出客户/物料映射（演示数据：在租客户）
    cust = {'XNC-AJZX-WBX': '安吉智行物流', 'WBX-1210L': '华骏重卡汽车有限公司', 'WBX-1210M': '华骏重卡汽车有限公司',
            'PLT-1210P': '华骏重卡汽车有限公司', 'BTC-6040': '华骏重卡汽车有限公司'}
    mat = {'XNC-AJZX-WBX': '围板箱 1200×1000×970', 'WBX-1210L': '围板箱 1200×1000×970', 'WBX-1210M': '围板箱 1200×1000×590',
           'PLT-1210P': '塑料托盘 1200×1000', 'BTC-6040': '料箱 600×400×340'}
    stop_detail = {'XNC-ZZ-WBX': 'ZY-20260914-001', 'XNC-ZZ-BTC': 'ZY-20260914-003'}
    lines = blk.split('\n')
    cur = None
    n_reg = n_stop = 0
    for idx, ln in enumerate(lines):
        mk = re.match(r"\s*'([A-Za-z0-9\-\.]+)': \{", ln)
        if mk and mk.group(1) != 'row':
            cur = mk.group(1)
        if 'zzRegModal' in ln:
            assert cur in cust, cur
            old_op = '{"t": "转租登记", "act": "openModal(\'zzRegModal\')"}'
            new_op = '{"t": "转移出库", "act": "go(\'%s?mat=%s&cust=%s\')"}' % (ZY_NEW, mat[cur], cust[cur])
            assert old_op in ln, cur
            lines[idx] = ln.replace(old_op, new_op)
            n_reg += 1
        elif 'zzBackModal' in ln:
            old_op = '{"t": "转租还回", "act": "openModal(\'zzBackModal\')"}'
            assert cur, 'zzBack 无键'
            if cur in stop_detail:
                new_op = '{"t": "终止转移", "act": "go(\'../租赁管理/转移出库单详情.html?id=%s\')"}' % stop_detail[cur]
            else:  # XNC-ZZ-PLT：该行随 T4 回租出态→跳新建
                new_op = '{"t": "转移出库", "act": "go(\'%s?mat=%s&cust=%s\')"}' % (ZY_NEW, '塑料托盘 1200×1000', '安吉智行物流')
            assert old_op in ln, cur
            lines[idx] = ln.replace(old_op, new_op)
            n_stop += 1
    assert n_reg == 5 and n_stop == 3, (n_reg, n_stop)
    blk2 = '\n'.join(lines)
    d = d[:i] + blk2 + d[j:]
    wr(p2, d)
    assert 'zzRegModal' not in d and 'zzBackModal' not in d
    print('2 demo-data ops 改向：转移出库 %d 行 / 终止转移+PLT %d 行' % (n_reg, n_stop))
else:
    print('2 demo-data：已改（跳过）')

# ================= 3. A03 pin-4 改述 =================
p3 = 'P3-R01-A03-标注数据.json'
j = json.loads(io.open(os.path.join(ROOT, p3), encoding='utf-8').read())
pin4 = next(p for p in j['仓储作业/库存查询.html'] if p.get('id') == 4)
if '转租登记' in pin4['note']:
    pin4['note'] = ('转租定义：物料/BOM 已租给客户 A，A 再租给客户 B（终端用户）——记为「客户转租出」，不做所有权变更。\n'
                    '承载（2026-09-15 G37·D-146）：转移出库单——库存查询行内「转移出库」跳录单页（带出物料与在租客户），审核生效后状态转「客户转租出」；单据「终止转移」后回「在客户（租出）」（原转租登记/转租还回弹窗退场）。\n'
                    '结算：项目档案「转租结算方式」定默认（按租出结算/按终端结算·D-132），转移单可按单覆盖。')
    io.open(os.path.join(ROOT, p3), 'w', encoding='utf-8', newline='\n').write(json.dumps(j, ensure_ascii=False, indent=2))
    print('3 A03 pin-4 note 已改述')
else:
    print('3 A03：已改（跳过）')
print('T3 DONE')
