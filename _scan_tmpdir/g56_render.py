# -*- coding: utf-8 -*-
"""G56 渲染门：JS 0 / 新节点可见 / 文字溢出实测 / S7 同构 / 截图≥4"""
import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'
F01 = os.path.join(ROOT, 'P3-R01-包装租赁管理后台原型', 'P3-R01-F01-业务流程导航图.html')
OUT = os.path.join(ROOT, '_scan_tmpdir', 'g56_shots')
os.makedirs(OUT, exist_ok=True)
fails, passes = [], []

def check(name, ok, detail=''):
    print(('[PASS] ' if ok else '[FAIL] ') + name + ('  -- ' + detail if detail else ''))
    (passes if ok else fails).append(name)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1000, 'height': 900})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.goto('file:///' + F01.replace('\\', '/'))
    pg.wait_for_timeout(600)
    check('JS errors = 0', len(errs) == 0, '; '.join(errs[:3]))

    # 可见性：文本节点存在且在 viewBox 内渲染
    def txt_visible(t):
        loc = pg.locator('svg text', has_text=t)
        n = loc.count()
        if n == 0: return False, 0
        bb = loc.first.bounding_box()
        return bb is not None and bb['height'] > 0, n

    for t in ['租入单（直发）', '系统自动 · 直发虚拟仓 XNC-ZF', '系统自动 · 供应商直发客户',
              '直发线（背靠背）', '类型＝直发单／自发单（租入单 radio · D-167）',
              '人工单据不可手选虚拟仓', '报数调整：客户报数增减经其他入库',
              '采购退货单', '退款登记', '销售退货单', '两守卫（D-157）', 'D-157 两守卫 · 见右注',
              '退货回程线① · 采购侧', '退货回程线② · 销售侧', '供应商退我方 · ⇢ F2', '我方退客户 · ⇢ F1',
              '收货拒收／入库后退货', '审核后可登记应收退款（对客户 · 客户已付部分）',
              '未收部分冲减应收（G33 负数行 · 历史账单不回改）',
              '直发件退租＝人工录入（客户报数触发）', '背靠背（GHCK）＝系统识别直发类型自动生成',
              '单据审核（20 类）', '20 类单据统一进待办', '按 BOM 扣减组件（无组装单）',
              '验收立应付 · ⇢ F2（按实际入库）', '09-04 拍板：两条独立线', '采购应付 → 应付账单',
              'F1 · 应收（对客户）＋ 销售退货退款', 'F2 · 应付（对供应商/客户）＋ 采购退货退款']:
        ok, n = txt_visible(t)
        check('visible: %s' % t[:24], ok, 'matches=%d' % n)

    # 文字溢出实测：新增副标/注记行宽度 vs 容器（节点宽-8 / 注记框宽-24）
    overflow_checks = [
        ('系统自动 · 直发虚拟仓 XNC-ZF', 132), ('系统自动 · 供应商直发客户', 132),
        ('系统自动 · 审核后启动直发链', 132), ('直发单 · 审核后系统自动' if False else '向供应商租入 · 自发单', 132),
        ('租入资产入库 · 自发', 132), ('D-157 两守卫 · 见右注', 132),
        ('供应商退我方 · ⇢ F2', 132), ('我方退客户 · ⇢ F1', 132),
        ('收货拒收／入库后退货', 132),
        ('审核后可登记应收退款（对客户 · 客户已付部分）', 436),
        ('验收立应付 · ⇢ F2（按实际入库）', 132), ('09-04 拍板：两条独立线 · 不以销定采', 152),
        ('原方案「先销后采互通」· 第2次沟通', 152),
        ('类型＝直发单／自发单（租入单 radio · D-167）', 776),
        ('直发链系统自动：租入入库入直发虚拟仓 XNC-ZF（字典 KW-05 · 系统内置不可删改 · 不占实体库存）→ 自动生成租赁出库', 776),
        ('人工单据不可手选虚拟仓（下拉 filterV 排除）', 776),
        ('两守卫（D-157）：入库前已付 → 生成退款单（退款额 ≤ 已付额）', 300),
        ('入库前未付 → 不立退款（拒收自终结／冲在途应付）', 300),
        ('直发件退租＝人工录入（客户报数触发）→ 系统识别直发类型 → 库位自动带出直发虚拟仓（D-167）', 460),
        ('背靠背（GHCK）＝系统识别直发类型自动生成 · 退租入库=人工 · 归还出库=系统（09-18 口径 · D-167）', 800),
    ]
    for t, budget in overflow_checks:
        w = pg.evaluate("""(t) => {
            const els = [...document.querySelectorAll('svg text')];
            const el = els.find(e => e.textContent.trim() === t.trim());
            if (!el) return -1;
            return el.getComputedTextLength();
        }""", t)
        check('no-overflow (%.0fpx): %s' % (budget, t[:20]), w >= 0 and w <= budget, 'w=%.1f' % w)

    # 截图：L3 全貌 / B1 全貌 / 页脚沿革 / S7 支线
    def clip_between(text_a, text_b, svg_nth=0, pad=8):
        svg = pg.locator('svg').nth(svg_nth)
        sbb = svg.bounding_box()
        scale = sbb['width'] / 880.0
        def y_of(t):
            els = svg.locator('text', has_text=t)
            bb = els.first.bounding_box()
            return (bb['y'] - sbb['y']) / scale
        ya, yb = y_of(text_a), y_of(text_b)
        return {'x': sbb['x'], 'y': sbb['y'] + max(0, ya - pad) * scale,
                'width': sbb['width'], 'height': (yb - ya + 2 * pad) * scale}

    pg.screenshot(path=os.path.join(OUT, '1_L3_直发分叉.png'), full_page=True, clip=clip_between('L3 · 租赁 · 租入转租', 'L4 · 租赁 · 混合转租'))
    pg.screenshot(path=os.path.join(OUT, '2_B1_退货回程.png'), full_page=True, clip=clip_between('B1 · 物料买卖', 'L1 · 租赁 · 单一出租'))
    pg.locator('footer').screenshot(path=os.path.join(OUT, '3_页脚沿革.png'))
    pg.screenshot(path=os.path.join(OUT, '4_S7_转移出库不动证.png'), full_page=True, clip=clip_between('S7 · 转移出库', '图例', svg_nth=1))
    check('screenshots >= 4', len(os.listdir(OUT)) >= 4, str(sorted(os.listdir(OUT))))

    # S7 同构：三节点文本仍在
    for t in ['转移出库列表', '转移出库新建', '转移出库单详情']:
        ok, n = txt_visible(t)
        check('S7 node: %s' % t, ok)

    b.close()

print('SUMMARY: %d PASS / %d FAIL -> %s' % (len(passes), len(fails), fails if fails else 'ALL PASS'))
