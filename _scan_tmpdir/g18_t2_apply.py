# -*- coding: utf-8 -*-
"""G18 T2：全量复扫命中处理——A 类 20 条转标注 + 保留项注记 + 失败清单。
含 A04 重叠页补录（银行水单核销/应付账单/我的待办——A04 后注覆盖 A03 机制）。
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROT = ROOT/'P3-R01-包装租赁管理后台原型'
A03, A04 = PROT/'P3-R01-A03-标注数据.json', PROT/'P3-R01-A04-流程链标注数据.json'
APPLY = '--apply' in sys.argv

DELS = [
    # 1) 用户权限:595 灰字行（G13 第三处同源同步注记）
    ('系统管理/用户权限.html',
     '      <div style="font-size:12px;color:#8c8c8c;padding-top:6px;line-height:1.7;">与角色管理页·权限配置「可审单据」同源同步（双层同步 · G13）；正式版按所选角色加载勾选态。</div>\n',
     ''),
    # 2) 我的待办 5 条 st-foot（行内子串）
    ('我的待办.html', '<div class="st-foot">覆盖 15 类单据 · 点击"去审核"直达审核弹窗</div>', ''),
    ('我的待办.html', '<div class="st-foot">订单/出入库/租赁/盘点等</div>', ''),
    ('我的待办.html', '<div class="st-foot">采购入库到货验收</div>', ''),
    ('我的待办.html', '<div class="st-foot">付款 / 收款登记确认</div>', ''),
    ('我的待办.html', '<div class="st-foot">租入入库 · 确认后计租入资产库存</div>', ''),
    # 3) 项目看板 4 行
    ('首页/项目看板.html', '    <div class="st-foot">较上月 <em>+3.2%</em> · 覆盖 4 个项目</div>\n', ''),
    ('首页/项目看板.html', '    <div class="st-foot">较上月 <em>+8.6%</em> · 一箱一件交付</div>\n', ''),
    ('首页/项目看板.html', '    <div class="st-foot">较上月 <em>+12.4%</em> · 收款核销 5 笔</div>\n', ''),
    ('首页/项目看板.html', '    <div class="st-foot">其中逾期 <em class=\'down\'>318,600 元</em></div>\n', ''),
    # 4) 项目详情 4 行
    ('项目管理/项目详情.html', '    <div class="st-foot">围板箱 3,120 / 托盘 740</div>\n', ''),
    ('项目管理/项目详情.html', '    <div class="st-foot">组合件 1,120 / 散件 120</div>\n', ''),
    ('项目管理/项目详情.html', '    <div class="st-foot">已开票 <em>312,000</em> 元</div>\n', ''),
    ('项目管理/项目详情.html', '    <div class="st-foot">毛利率 <em>21.8%</em></div>\n', ''),
    # 5) 盈亏报表 4 行
    ('财务协同/盈亏报表.html', '    <div class="st-foot">租赁 990,700 / 组装 130,000 / 赔偿 18,200</div>\n', ''),
    ('财务协同/盈亏报表.html', '    <div class="st-foot">器具摊销 505,200 / 仓储 154,300</div>\n', ''),
    ('财务协同/盈亏报表.html', '    <div class="st-foot">毛利率 <em>42.1%</em></div>\n', ''),
    ('财务协同/盈亏报表.html', '    <div class="st-foot">PRJ-2604 <em class=\'down\'>-18,600</em> 元（已暂停）</div>\n', ''),
    # 6) mobile 标题括号
    ('mobile/审批详情.html', '单据明细（演示数据）', '单据明细'),
    # 7) mobile 审批说明灰字卡整块
    ('mobile/审批详情.html',
     '    <div class="m-card" style="font-size:12px;color:#8c8c8c;line-height:1.8;">\n      审批说明：通过后单据进入下一环节并通知提交人；驳回后退回提交人修改后重新提交。移动端为演示形态，明细为静态示例。\n    </div>\n',
     ''),
]

def E(id, sel, title, note, fp=None, req=None):
    e = {'id': id, 'selector': sel, 'title': title, 'note': note}
    if fp: e['fp'] = fp
    if req: e['req'] = req
    return e

def ST(label, note, title):
    return '<div class="st-label"><span>%s</span></div>' % label, note, title

TODO5 = [
    ST('我的待办', '覆盖 15 类单据 · 点击“去审核”直达审核弹窗', '待办总量口径'),
    ST('待审核', '订单/出入库/租赁/盘点等', '待审核构成'),
    ST('待验收', '采购入库到货验收', '待验收含义'),
    ST('待确认', '付款 / 收款登记确认', '待确认含义'),
    ST('待入库', '租入入库 · 确认后计租入资产库存', '待入库含义'),
]
KB4 = [
    ST('在租资产总量', '较上月 +3.2% · 覆盖 4 个项目', '在租资产口径'),
    ST('本月组合出库', '较上月 +8.6% · 一箱一件交付', '组合出库口径'),
    ST('本月收款', '较上月 +12.4% · 收款核销 5 笔', '本月收款口径'),
    ST('应收余额', '其中逾期 318,600 元', '应收余额口径'),
]
PD4 = [
    ST('在租数量', '围板箱 3,120 / 托盘 740', '在租数量构成'),
    ST('本月出库', '组合件 1,120 / 散件 120', '本月出库构成'),
    ST('本月营收', '已开票 312,000 元', '营收开票口径'),
    ST('累计毛利', '毛利率 21.8%', '毛利率口径'),
]
PL4 = [
    ST('本月营业收入', '租赁 990,700 / 组装 130,000 / 赔偿 18,200', '营收构成'),
    ST('本月营业成本', '器具摊销 505,200 / 仓储 154,300', '成本构成'),
    ST('本月毛利', '毛利率 42.1%', '毛利率'),
    ST('亏损项目', 'PRJ-2604 -18,600 元（已暂停）', '亏损项目口径'),
]

ADDS_A03 = {
    '系统管理/用户权限.html': [E(3, '<h3 class="modal-title">角色管理</h3>', '可审单据同源同步',
        '与角色管理页·权限配置「可审单据」同源同步（双层同步 · G13）；正式版按所选角色加载勾选态。', 'FP7-01', 'REQ-01')],
    '我的待办.html': [E(i+1, s, t, n) for i, (s, n, t) in enumerate(TODO5)],
    '首页/项目看板.html': [E(i+4, s, t, n, 'FP2-03', 'REQ-02') for i, (s, n, t) in enumerate(KB4)],
    '项目管理/项目详情.html': [E(i+4, s, t, n, 'FP2-04', 'REQ-02') for i, (s, n, t) in enumerate(PD4)],
    '财务协同/盈亏报表.html': [E(i+3, s, t, n, 'FP6-05', 'REQ-02') for i, (s, n, t) in enumerate(PL4)],
    'mobile/审批详情.html': [
        E(1, '<div class="m-sec-title">单据明细</div>', '明细=静态演示数据',
          '单据明细为静态示例（演示数据），演示移动端审批详情形态。'),
        E(2, '<div class="m-sec-title">单据摘要</div>', '审批动作口径',
          '通过后单据进入下一环节并通知提交人；驳回后退回提交人修改后重新提交。移动端为演示形态。')],
}
# A04 补录（A04 后注覆盖 A03 → 重叠页条目须进 A04 才能显示）
ADDS_A04 = {
    '财务协同/银行水单核销.html': [E(2, '<h3 class="card-title">② 待核销单据</h3>', '核销金额口径',
        '单据金额取自应收账单 / 丢损赔偿单；勾选两侧后点击「生成核销记录」，系统按回单未核销金额与单据未核销金额取小核销。', 'FP6-04', 'REQ-09')],
    '财务协同/应付账单.html': [E(5, '<h3 class="card-title">应付账单</h3>', '应付账单生成方式',
        '应付账单可由采购入库单审核后自动生成（第一期支持手动创建）；租入业务（路凯）按周期生成应付账单。', 'FP4-02', 'REQ-03')],
    '我的待办.html': [E(i+2, s, t, n) for i, (s, n, t) in enumerate(TODO5)],
}

fail = 0
print(f"=== T2 {'APPLY' if APPLY else 'DRY-RUN'} ===")
# 先在内存中对每页应用全部删除，selector 检查用删除后文本（mobile 锚依赖括号删除）
page_text = {}
for f, old, new in DELS:
    p = PROT/f
    s = page_text.get(f, p.read_text(encoding='utf-8'))
    n = s.count(old)
    ok = n == 1
    print(f"[{'PASS' if ok else 'FAIL'}] 删除 {f}: {old.strip()[:44]}… 命中 {n}/1")
    if not ok:
        fail += 1
    else:
        s = s.replace(old, new, 1)
        page_text[f] = s
        if APPLY:
            p.write_text(s, encoding='utf-8')

def add_entries(path, adds, label):
    global fail
    d = json.loads(path.read_text(encoding='utf-8'))
    for k, items in adds.items():
        cur = d.get(k, [])
        ids = [e['id'] for e in cur]
        s = page_text.get(k, (PROT/k).read_text(encoding='utf-8') if (PROT/k).exists() else '')
        for e in items:
            c = s.count(e['selector'])
            dup = e['id'] in ids
            ok = c == 1 and not dup
            print(f"[{'PASS' if ok else 'FAIL'}] {label} {k} +id={e['id']} sel命中{c}/1 dup={dup}: {e['title']}")
            if not ok:
                fail += 1
        if APPLY and not any(e['id'] in ids for e in items):
            d[k] = cur + items
    if APPLY:
        path.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        json.loads(path.read_text(encoding='utf-8'))
        print(f"{label} 写回+json.load OK")

add_entries(A03, ADDS_A03, 'A03')
add_entries(A04, ADDS_A04, 'A04')

if APPLY:
    import re
    for f in sorted(set(x[0] for x in DELS)):
        s = (PROT/f).read_text(encoding='utf-8')
        o, c = len(re.findall(r'<div\b', s)), len(re.findall(r'</div>', s))
        print(f"[{'PASS' if o == c else 'INFO'}] 配平 {f}: {o}/{c}")
print(f"=== {'FAIL=' + str(fail) if fail else 'ALL PASS'} ===")
sys.exit(1 if fail else 0)
