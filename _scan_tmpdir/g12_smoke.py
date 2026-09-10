# -*- coding: utf-8 -*-
"""G12 冒烟：9 页加载 + 行数 + 筛选交互 + JS 错误"""
import io, sys, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型')

def rows(pg, sel='tbody tr'):
    return pg.eval_on_selector_all(sel, 'els => els.length')

def smoke(b, rel, name, actions=None):
    pg = b.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
    pg.on('console', lambda m: errs.append('CONSOLE-ERR: ' + m.text[:120]) if m.type == 'error' else None)
    pg.goto((ROOT / rel).as_uri())
    pg.wait_for_timeout(300)
    n0 = rows(pg)
    log = f'{name}: 初始行={n0} JS错={len(errs)}'
    if actions:
        extra = actions(pg)
        log += f' | 交互后={extra}'
    if errs:
        log += ' | ERR>> ' + ' ;; '.join(errs[:3])
    print(log)
    pg.close()
    return len(errs) == 0

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ok = True
    # renderListPage 7 页：设筛选值→点查询→行数变化
    def mk_filter(label_idx, value, expect_less=True):
        def act(pg):
            ff = pg.query_selector_all('.filter-card .ff')
            if not ff: return '无筛选卡'
            # 展开折叠
            col = pg.query_selector('.filter-card .link-collapse')
            if col: col.click()
            sel = ff[label_idx].query_selector('select') if label_idx < len(ff) else None
            inp = ff[label_idx].query_selector('input') if label_idx < len(ff) else None
            if sel:
                sel.select_option(value)
            elif inp:
                inp.fill(value)
            btn = None
            for bt in pg.query_selector_all('.filter-card button, .filter-actions button'):
                if bt.text_content().strip() == '查询': btn = bt
            if btn: btn.click()
            pg.wait_for_timeout(150)
            return rows(pg)
        return act

    ok &= smoke(b, r'系统管理\操作日志.html', '操作日志', mk_filter(2, '新增'))
    ok &= smoke(b, r'系统管理\用户权限.html', '用户权限', mk_filter(2, '客户'))
    ok &= smoke(b, r'项目管理\项目档案.html', '项目档案', mk_filter(2, '一汽解放'))
    ok &= smoke(b, r'项目管理\项目详情.html', '项目详情', None)
    ok &= smoke(b, r'基础数据\BOM.html', 'BOM', mk_filter(2, 'V1.3'))
    ok &= smoke(b, r'财务协同\盈亏报表.html', '盈亏报表', mk_filter(0, '2026-08'))
    ok &= smoke(b, r'首页\项目看板.html', '项目看板', None)

    # 我的待办：关键词过滤
    def todo_act(pg):
        pg.fill('#todoKw', '一汽解放')
        pg.wait_for_timeout(120)
        vis = pg.eval_on_selector_all('#todoBody tr', 'els => els.filter(e => e.style.display !== "none").length')
        cnt = pg.text_content('#todoCount')
        return f'关键词命中={vis} todoCount={cnt}'
    ok &= smoke(b, r'我的待办.html', '我的待办', todo_act)

    # 数据字典：点击分类切换
    def dict_act(pg):
        n1 = rows(pg)
        pg.click('.dic-list .dic-item:nth-child(4)')  # 计量单位
        pg.wait_for_timeout(150)
        n2 = rows(pg)
        t = pg.text_content('.dic-wrap .card-head .card-title')
        pg.click('.dic-list .dic-item:nth-child(3)')  # 计费方式
        pg.wait_for_timeout(150)
        n3 = rows(pg)
        return f'缺损={n1} 计量单位={n2}({t.strip()}) 计费方式={n3}'
    ok &= smoke(b, r'系统管理\数据字典.html', '数据字典', dict_act)

    b.close()
    print('SMOKE', 'ALL PASS' if ok else 'HAS ERRORS')
