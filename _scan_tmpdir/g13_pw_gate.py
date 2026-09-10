# -*- coding: utf-8 -*-
"""G13 验证门 3：PW 抽 4 页（贴 PASS 清单）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright
PROTO = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
fails = []
def chk(name, ok, detail=''):
    print(('PASS' if ok else 'FAIL'), name, '|', detail)
    if not ok: fails.append(name)

with sync_playwright() as pw:
    b = pw.chromium.launch()
    # 1 库存查询：客户端(转租)筛选生效
    pg = b.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto((PROTO / "仓储作业/库存查询.html").as_uri(), wait_until='load'); pg.wait_for_timeout(400)
    t1 = pg.locator('tbody').first.locator('tr').count()
    pg.locator('.filter-card select').first.evaluate("el => { el.value='客户端(转租)'; }")
    pg.evaluate("[...document.querySelectorAll('.filter-actions button')].find(x=>x.textContent.trim()==='查询').click()")
    pg.wait_for_timeout(150)
    t2 = pg.locator('tbody').first.locator('tr').count()
    txt = pg.locator('tbody').first.text_content()
    chk('PW1 库存查询·客户端(转租)筛选生效', t1 == 13 and t2 == 3 and '客户端(转租)' not in txt and '转租终端用户' in txt and not errs, f'{t1}→{t2} 行（余 3 行均为转租演示行）')
    pg.close()
    # 2 租赁单新建（宿主页弹窗）：选产品出库存提示
    pg = b.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto((PROTO / "租赁管理/租赁单列表.html").as_uri(), wait_until='load'); pg.wait_for_timeout(400)
    pg.evaluate("openModal('createModal')"); pg.wait_for_timeout(100)
    h0 = pg.locator('#createModal .stock-hint').count()
    pg.locator('#createModal .edit-tbl td select').first.evaluate("el => { el.selectedIndex = 2; el.dispatchEvent(new Event('change',{bubbles:true})); }")
    pg.wait_for_timeout(150)
    hint = pg.locator('#createModal .stock-hint').first.text_content().strip()
    chk('PW2 租赁单新建·选产品出库存提示', h0 >= 2 and hint == '可用库存 60 块' and not errs, f'提示={hint!r}（切 PLT-1210W 后）')
    pg.close()
    # 3 租入归还新建（宿主页弹窗）：选关联单后明细同步
    pg = b.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto((PROTO / "租赁管理/租入归还列表.html").as_uri(), wait_until='load'); pg.wait_for_timeout(400)
    pg.evaluate("openModal('createModal')"); pg.wait_for_timeout(100)
    rows0 = pg.locator('#riItemsBody tr').count()
    pg.locator('#riSelect').evaluate("el => { el.selectedIndex = 1; el.dispatchEvent(new Event('change',{bubbles:true})); }")
    pg.wait_for_timeout(150)
    rows1 = pg.locator('#riItemsBody tr').count()
    txt = pg.locator('#riItemsBody').text_content()
    chk('PW3 租入归还新建·关联后明细同步', rows0 >= 1 and rows1 > 0 and '30 只' in txt and '本次归还数量' in pg.locator('#createModal').text_content() and not errs, f'默认{rows0}行→RZD-…-003 后{rows1}行（租入 30 只）')
    pg.close()
    # 4 权限配置（模板页）：可审单据勾选区渲染
    pg = b.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto((PROTO / "系统管理/弹窗/权限配置.html").as_uri(), wait_until='load'); pg.wait_for_timeout(400)
    n = pg.locator('#auditPermMatrix [data-audit]').count()
    ck = pg.locator('#auditPermMatrix .checkbox.checked').count()
    pg.locator('#auditPermMatrix [data-audit="盘点"]').first.evaluate("el => el.click()")
    pg.wait_for_timeout(100)
    still = pg.locator('#auditPermMatrix [data-audit="盘点"].checked').count()
    chk('PW4 权限配置·可审单据勾选区渲染', n == 14 and ck == 8 and still == 0 and not errs, f'14 项/默认勾 8/点击盘点可取消')
    pg.close()
    b.close()
print('\n==== PW 抽验门：4 页', '全 PASS ====' if not fails else f'失败 {len(fails)} ====')
sys.exit(1 if fails else 0)
