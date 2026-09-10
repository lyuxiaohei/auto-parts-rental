# -*- coding: utf-8 -*-
"""G11-B3: 38 业务页元注释清除（A5+B8·精确删除+逐条 assert+备份 backup-g11-20260910）"""
import os, shutil, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
BK = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-g11-20260910"

# (rel, tag, exact_string)  tag: 'comment'|'div'
ITEMS = [
    ('仓储作业/库存查询.html', 'comment',
     '<!-- 客户在租明细（原在租台账并入·2026-09-10 台账合并）+ 资产轨迹（assetTracks 数据渲染） -->'),
    ('仓储作业/库存查询.html', 'comment',
     '/* 客户在租下钻·资产轨迹（原在租台账并入·2026-09-10）：按 assetTracks 键渲染四段式详情 */'),
    ('系统管理/角色管理.html', 'comment',
     '/* G01 角色管理数据驱动（2026-09-09）：roles 实体渲染 + 权限配置矩阵（矩阵口径=G01 文档 C 默认决策表） */'),
    ('租赁管理/组合出库录单.html', 'comment',
     '/* ===== 添加明细：克隆明细表末行示例数据并重排序号（详情落地页补齐 2026-09-04） ===== */'),
    ('采购管理/采购入库录单.html', 'comment',
     '/* ===== 添加明细：克隆明细表末行示例数据并重排序号（详情落地页补齐 2026-09-04） ===== */'),
    ('仓储作业/库存查询.html', 'div',
     '<div class="pn-hint">客户虚拟仓＝在客户处的租赁资产按客户归集（on-hire）；客户转租为其子状态（2026-09-08 会议 T1 方向）。</div>'),
    ('仓储作业/库存查询.html', 'div',
     '<div class="pn-hint">客户在租明细（原在租台账·2026-09-10 并入）＝行内「客户在租」按客户/项目下钻；租出与退回进度在租赁单列表「退回进度」列跟踪。</div>'),
    ('基础数据/产品档案.html', 'div',
     '<div class="pn-hint">口径：同一产品可按供应商维护不同税率（默认 13%；运费/杂费后续可能 6%/9%）；单据明细税率默认带出、可手动覆盖。产品档案 = 器具档案 + 零部件档案合并（2026-09-08 会议 N4）。</div>'),
    ('租赁管理/租入单列表.html', 'div',
     '<div style="margin-top:6px;font-size:12px;color:#8c8c8c;">计费＝月租金 + 按套数单价（无日租金，2026-09-08 会议）；应付生成方式取决于租入单模式（静态租入 / 背靠背）。</div>'),
    ('租赁管理/退租入库列表.html', 'div',
     '<div class="pn-hint" style="padding:0 4px;">退租无申请单：客户退回后直接录入退租入库单（按拆后零件·单一产品记录）；入库仅更新库存状态，与财务结算解耦——租金只要发出去就要收，还了也收（2026-09-08 会议拍板）。</div>'),
    ('财务协同/应付账单.html', 'div',
     '<div class="pn-hint">分期互算：填比例自动算金额、填金额自动算比例，末期自动补差；账单头部展示「账单金额 / 已付 / 剩余」，付款时选金额，超出账单金额拦截（2026-09-08 会议 M2/C-C）。</div>'),
    ('租赁管理/租赁单列表.html', 'div',
     '<div style="font-size:12px;color:#8c8c8c;line-height:1.7;">押金为设计预留字段——两次会议均未涉及，收退与计价商务口径待客户确认（F01 财务通道注记同步）</div>'),
    ('财务协同/盈亏报表.html', 'div',
     '<div style="margin:8px 0 0;font-size:12px;color:#8c8c8c;line-height:1.7;">对齐说明（演示链数据）：PRJ-2601 收入合计 486,200.00 ＝ 应收账单 AR-2026-08-PRJ2601（已开票 186,200 · 水单部分核销 286,500，见开票登记 / 银行水单核销）；PRJ-2604 为 L4 混合链演示项目——租入大箱租金应付 AP-20260903-010（12,000.00 / 月）与自购隔板采购摊销计入成本合计，9 月销售费应收 AR-2026-09-PRJ2604-S1（1,280.00）见应收账单；当前成本大于收入、毛利为负（项目状态：已暂停）。</div>'),
]

by_file = {}
for rel, tag, s in ITEMS:
    by_file.setdefault(rel, []).append((tag, s))

fails = []
for rel, items in by_file.items():
    p = os.path.join(ROOT, rel)
    try:
        txt0 = open(p, encoding='utf-8').read()
        if all(txt0.count(s) == 0 for _, s in items):
            print(f'SKIP {rel}（目标串均已不在·上轮已清）')
            continue
        dst = os.path.join(BK, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if not os.path.exists(dst):
            shutil.copy2(p, dst)
        raw = open(p, 'rb').read()
        txt = raw.decode('utf-8')
        bal_before = (txt.count('<div'), txt.count('</div>'), txt.count('<!--'), txt.count('-->'))
        for tag, s in items:
            n = txt.count(s)
            assert n == 1, f'{rel}: 预期 1 处实际 {n}: {s[:50]}'
            i = txt.find(s)
            j = i + len(s)
            nl = txt.rfind('\n', 0, i)
            line_head = txt[nl + 1:i]
            line_rest = txt[j:txt.find('\n', j) if txt.find('\n', j) != -1 else len(txt)]
            if line_head.strip() == '' and line_rest.strip() == '':
                # 整行删除（含行尾换行）
                eol = txt.find('\n', j)
                txt = txt[:nl + 1] + txt[eol + 1:] if eol != -1 else txt[:nl + 1]
            else:
                txt = txt[:i] + txt[j:]
        n_div = sum(1 for t, _ in items if t == 'div')
        n_html_com = sum(1 for t, s in items if '<!--' in s)
        assert txt.count('<div') == bal_before[0] - n_div, f'{rel}: <div> 配平异常'
        assert txt.count('</div>') == bal_before[1] - n_div, f'{rel}: </div> 配平异常'
        # 仅 HTML 注释影响 <!-- / --> 计数；JS 注释 /* */ 以原串 0 命中复核（见下）
        assert txt.count('<!--') == bal_before[2] - n_html_com, f'{rel}: <!-- 配平异常'
        assert txt.count('-->') == bal_before[3] - n_html_com, f'{rel}: --> 配平异常'
        # 写后复核：全部原串 0 命中
        for _, s in items:
            assert txt.count(s) == 0
        open(p, 'wb').write(txt.encode('utf-8'))
        chk = open(p, encoding='utf-8').read()
        for _, s in items:
            assert chk.count(s) == 0
        print(f'OK  {rel}（删 {len(items)} 处）')
    except Exception as e:
        fails.append((rel, str(e)))
        print(f'FAIL {rel}: {e}')

print(f'==== G11-B3: {len(by_file) - len(fails)}/{len(by_file)} 文件 ok，共删 {len(ITEMS)} 处，fails={len(fails)} ====')
sys.exit(1 if fails else 0)
