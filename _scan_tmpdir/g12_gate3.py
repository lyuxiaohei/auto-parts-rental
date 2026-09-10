# -*- coding: utf-8 -*-
"""G12 T5 验证门 3：PW 抽验 4 页（数据字典筛选交互 + 操作日志/用户权限/项目档案 行≥6+筛选可用）"""
import io, sys, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型')
results = []

def check(name, fn):
    try:
        fn()
        results.append(('PASS', name))
        print('PASS |', name)
    except Exception as e:
        results.append(('FAIL', name + ' :: ' + repr(e)[:150]))
        print('FAIL |', name, '::', repr(e)[:150])

with sync_playwright() as pw:
    b = pw.chromium.launch()

    # ---- 数据字典：字段分类筛选交互生效（切换后主表行数变化） ----
    def t_dict():
        pg = b.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto((ROOT / r'系统管理\数据字典.html').as_uri())
        pg.wait_for_timeout(300)
        main = lambda: pg.eval_on_selector('.dic-wrap .card .table-wrap table', 't => t.querySelectorAll("tbody tr").length')
        n0 = main()                      # 缺损类型(6)
        pg.click('.dic-list .dic-item:nth-child(10)')  # 银行账户(3)
        pg.wait_for_timeout(150)
        n1 = main()
        title = pg.text_content('.dic-wrap .card-head .card-title').strip()
        pg.click('.dic-list .dic-item:nth-child(11)')  # 支付方式(2)
        pg.wait_for_timeout(150)
        n2 = main()
        cnt10 = pg.text_content('.dic-list .dic-item:nth-child(10) .cnt').strip()
        assert not errs, 'JS: %s' % errs
        assert n0 != n1 and n1 != n2, '行数无变化: %s %s %s' % (n0, n1, n2)
        assert title == '字典项 · 银行账户', title
        assert n0 >= 6 and n1 == 3 and n2 == 2, '行数异常: %s %s %s' % (n0, n1, n2)
        assert cnt10 == '3', '计数未联动: ' + cnt10
        print('   数据字典: 缺损=%d 银行账户=%d 支付方式=%d 标题=%s 计数联动=%s' % (n0, n1, n2, title, cnt10))
        pg.close()
    check('数据字典 · 字段分类筛选交互生效（切换行数变化）', t_dict)

    # ---- 通用：行≥6 + 筛选可用 ----
    def t_list(rel, name, ff_label, value, min_rows):
        pg = b.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto((ROOT / rel).as_uri())
        pg.wait_for_timeout(300)
        n0 = pg.eval_on_selector('tbody', 't => t.querySelectorAll("tr").length')
        col = pg.query_selector('.filter-card .link-collapse')
        if col: col.click()
        found = None
        for ff in pg.query_selector_all('.filter-card .ff'):
            lb = ff.query_selector('.ff-label')
            if lb and lb.text_content().strip().rstrip('：:').strip() == ff_label:
                found = ff; break
        assert found, '筛选控件未找到: ' + ff_label
        sel = found.query_selector('select')
        if sel: sel.select_option(value)
        else: found.query_selector('input').fill(value)
        for bt in pg.query_selector_all('.filter-card button, .filter-actions button'):
            if bt.text_content().strip() == '查询': bt.click()
        pg.wait_for_timeout(200)
        n1 = pg.eval_on_selector('tbody', 't => t.querySelectorAll("tr").length')
        assert not errs, 'JS: %s' % errs
        assert n0 >= min_rows, '行数 %d < %d' % (n0, min_rows)
        assert n1 != n0, '筛选无效果: %d -> %d' % (n0, n1)
        print('   %s: 行=%d（≥%d） 筛选「%s=%s」后=%d' % (name, n0, min_rows, ff_label, value, n1))
        pg.close()

    check('操作日志 · 行≥6 + 筛选可用', lambda: t_list(r'系统管理\操作日志.html', '操作日志', '操作类型', '新增', 6))
    check('用户权限 · 行≥6 + 筛选可用', lambda: t_list(r'系统管理\用户权限.html', '用户权限', '所属方', '客户', 6))
    check('项目档案 · 行≥6 + 筛选可用', lambda: t_list(r'项目管理\项目档案.html', '项目档案', '客户名称', '一汽解放', 6))
    b.close()

npass = sum(1 for s, _ in results if s == 'PASS')
print()
print('【门3 PW 抽验】%d/%d PASS → %s' % (npass, len(results), 'PASS' if npass == len(results) else 'FAIL'))
