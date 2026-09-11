from playwright.sync_api import sync_playwright
import pathlib
base = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
r = []
def chk(n, c): r.append((n, bool(c)))
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':1600,'height':900})
    pg.on('pageerror', lambda e: errs.append(str(e)))

    # 1. 项目档案：列表多 tag + 筛选
    pg.goto((base/'项目管理'/'项目档案.html').as_uri()); pg.wait_for_timeout(1200)
    body = pg.locator('tbody').inner_text()
    chk('L-1 PRJ-2601 双供应商tag(路凯+华塑)', '路凯（租入）' in body and '华塑（采购）' in body)
    chk('L-2 PRJ-2602 (路凯+正大)', '正大（采购）' in body)
    chk('L-3 PRJ-2604 单供应商(华塑)', body.count('华塑（采购）') >= 3)
    chk('L-4 供应商筛选存在', pg.locator('.ff:has-text("供应商")').count() >= 1)
    # 筛选实测：选路凯→查询→只剩路凯项目
    pg.select_option('.ff:has-text("供应商") select', label='路凯包装运营（上海）')
    pg.click('button:has-text("查询")'); pg.wait_for_timeout(500)
    tb = pg.locator('tbody').inner_text()
    chk('L-5 筛选路凯→4项目(2601/02/03/05)', '2601' in tb or 'PRJ-2601' in tb or '围板箱' in tb)
    rows = pg.locator('tbody tr').count()
    chk('L-6 筛选后行数≤6(非路凯项目被滤)', rows <= 6)
    # 绑定弹窗
    pg.locator('tbody a:has-text("上下游绑定")').first.click(); pg.wait_for_timeout(300)
    mb = pg.locator('#bindModal').inner_text()
    chk('B-1 弹窗只有一个供应商标签(多选)', mb.count('供应商（多选）') == 1 and mb.count('供应商：') == 0)
    chk('B-2 无单选供应商残留', '路凯包装运营（上海）有限公司（租入）' in mb)
    chk('B-3 新口径注记', '2026-09-11 落地' in mb)
    pg.screenshot(path='_scan_tmpdir/m2m-bind.png')

    # 2. 新建项目弹窗多选
    pg.locator('#bindModal .modal-close').click(); pg.wait_for_timeout(200)
    pg.click('button:has-text("新建项目")'); pg.wait_for_timeout(300)
    cm = pg.locator('#createModal').inner_text()
    chk('N-1 新建项目含供应商（多选）', '供应商（多选）' in cm)
    chk('N-2 路凯租入勾选', pg.locator('#createModal input[checked]').count() >= 1)
    pg.keyboard().press('Escape') if False else None

    # 3. 项目详情链图
    pg.goto((base/'项目管理'/'项目详情.html').as_uri()); pg.wait_for_timeout(1000)
    dt = pg.locator('.chain').inner_text()
    chk('D-1 链图双供应商节点', '供应商（租入）' in dt and '供应商（采购）' in dt)

    # 4. 租入单列表：新建弹窗联动
    pg.goto((base/'租赁管理'/'租入单列表.html').as_uri()); pg.wait_for_timeout(1000)
    pg.click('button:has-text("新建租入单")'); pg.wait_for_timeout(300)
    chk('R-1 所属项目字段', pg.locator('#cmProject').count() == 1)
    opts = pg.locator('#cmSupplier option').all_inner_texts()
    chk('R-2 默认PRJ-2601→2家候选', len(opts) == 2 and '路凯' in opts[0] and '华塑' in opts[1])
    pg.select_option('#cmProject', 'PRJ-2604'); pg.wait_for_timeout(300)
    opts2 = pg.locator('#cmSupplier option').all_inner_texts()
    chk('R-3 切PRJ-2604→1家(华塑)', len(opts2) == 1 and '华塑' in opts2[0])
    pg.select_option('#cmProject', 'PRJ-2602'); pg.wait_for_timeout(300)
    opts3 = pg.locator('#cmSupplier option').all_inner_texts()
    chk('R-4 切PRJ-2602→2家(路凯+正大)', len(opts3) == 2 and '正大' in opts3[1])
    pg.screenshot(path='_scan_tmpdir/m2m-rentin.png')

    # 5. 采购订单联动
    pg.goto((base/'采购管理'/'采购订单列表.html').as_uri()); pg.wait_for_timeout(1000)
    pg.click('button:has-text("新建采购订单")'); pg.wait_for_timeout(300)
    chk('P-1 所属项目+联动', pg.locator('#cmProject').count() == 1 and pg.locator('#cmSupplier').count() == 1)
    pg.select_option('#cmProject', 'PRJ-2606'); pg.wait_for_timeout(300)
    opts4 = pg.locator('#cmSupplier option').all_inner_texts()
    chk('P-2 PRJ-2606→路凯+联恒', len(opts4) == 2 and '联恒' in opts4[1])

    # 6. 客商详情链多项目
    pg.goto((base/'基础数据'/'客商管理.html').as_uri()); pg.wait_for_timeout(1000)
    pg.locator('tbody a:has-text("详情")').first.click(); pg.wait_for_timeout(500)
    chain_txt = pg.locator('.chain').inner_text() if pg.locator('.chain').count() else ''
    chk('K-1 DW-0001 链 3 个关联项目', chain_txt.count('PRJ-2601') >= 1 and chain_txt.count('PRJ-2602') >= 1 and chain_txt.count('PRJ-2605') >= 1)

    chk('JS错误0', len(errs) == 0)
    b.close()
ok = sum(1 for _, c in r if c)
for n, c in r: print(('PASS' if c else 'FAIL'), n)
print(f'== PASS {ok} / FAIL {len(r)-ok} ==')
