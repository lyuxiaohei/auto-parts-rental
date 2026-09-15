# -*- coding: utf-8 -*-
"""G35 T5 PW 抽验：
A. 实施落位——11 页新增 g35 筛选控件在 DOM 且动态值域已填充（option≥2）
B. 筛选可用——3 页选值后表格行数变化（编程 set + 查询编程点击）
C. 我的待办——自定义页 select 联动 filterTodo 行可见数变化
D. 脱敏落位——抽样页面文本含杜撰名、不含映射真名
"""
import io, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.parse import quote

ROOT = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型')

def page_url(rel):
    return (ROOT / rel).as_uri()

def open(pg, url):
    pg.goto(url)
    pg.wait_for_load_state('networkidle')

A_PAGES = [
    ('财务协同/应付账单.html', ['g35ProjectSel', 'g35PeriodSel']),
    ('仓储作业/库存查询.html', ['g35ClsSel']),
    ('基础数据/BOM.html', ['g35UpdaterSel']),
    ('租入管理/租入入库列表.html', ['g35MakerSel', 'g35AreaSel']),
    ('租入管理/租入归还列表.html', ['g35MakerSel']),
    ('租赁管理/退租入库列表.html', ['g35WhSel']),
    ('采购管理/采购入库列表.html', ['g35MakerSel', 'g35AreaSel']),
    ('销售管理/销售出库列表.html', ['g35WhSel']),
    ('销售管理/销售订单列表.html', ['g35AgentSel']),
    ('系统管理/操作日志.html', ['g35ResultSel']),
    ('系统管理/用户权限.html', ['g35StatusSel']),
]

def main():
    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        pg = browser.new_page()
        errors = []
        pg.on('pageerror', lambda e: errors.append(str(e)))

        print('== A. 实施落位（新增筛选控件 + 动态值域） ==')
        a_ok = 0
        for rel, ids in A_PAGES:
            open(pg, page_url(rel))
            row = []
            ok = True
            for sid in ids:
                n = pg.evaluate("id => { var s = document.getElementById(id); return s ? s.options.length : -1; }", sid)
                row.append('%s:%d项' % (sid.replace('g35', '').replace('Sel', ''), n))
                if n is None or n < 2:
                    ok = False
            a_ok += ok
            print('  %-22s %s %s' % (rel.split("/")[-1], 'PASS' if ok else 'FAIL', ' '.join(row)))
        print('A 通过页数: %d/%d' % (a_ok, len(A_PAGES)))

        print('== B. 筛选可用（选值→行数变化） ==')
        B = [
            ('财务协同/应付账单.html', 'g35ProjectSel', 'tbody tr'),
            ('系统管理/操作日志.html', 'g35ResultSel', 'tbody tr'),
            ('采购管理/采购入库列表.html', 'g35MakerSel', 'tbody tr'),
        ]
        b_ok = 0
        for rel, sid, sel in B:
            open(pg, page_url(rel))
            before = pg.evaluate("s => document.querySelectorAll(s).length", sel)
            val = pg.evaluate("id => { var s = document.getElementById(id); var v = s.options[1].value || s.options[1].text; s.value = (s.options[1].value || v); if (!s.value) s.selectedIndex = 1; return s.options[s.selectedIndex].text; }", sid)
            pg.evaluate("() => { var bs = document.querySelectorAll('.filter-actions button, .filter-card button'); for (var b of bs) { if (b.textContent.trim() === '查询') { b.click(); return true; } } return false; }")
            pg.wait_for_timeout(300)
            after = pg.evaluate("s => document.querySelectorAll(s).length", sel)
            ok = after != before and after > 0
            b_ok += ok
            print('  %-18s 选[%s] 行数 %d → %d %s' % (rel.split('/')[-1], val, before, after, 'PASS' if ok else 'FAIL'))
        print('B 通过: %d/%d' % (b_ok, len(B)))

        print('== B2. label 修复页抽验（租赁单列表·客户名称） ==')
        open(pg, page_url('租赁管理/租赁单列表.html'))
        before = pg.evaluate("() => document.querySelectorAll('tbody tr').length")
        val = pg.evaluate("() => { var ff = null; document.querySelectorAll('.filter-card .ff').forEach(function(e){ var l = e.querySelector('.ff-label'); if (l && l.textContent.indexOf('客户名称') > -1) ff = e; }); var s = ff.querySelector('select'); s.selectedIndex = 1; return s.options[s.selectedIndex].text; }")
        pg.evaluate("() => { var bs = document.querySelectorAll('.filter-actions button, .filter-card button'); for (var b of bs) { if (b.textContent.trim() === '查询') { b.click(); return true; } } return false; }")
        pg.wait_for_timeout(300)
        after = pg.evaluate("() => document.querySelectorAll('tbody tr').length")
        print('  租赁单列表 客户名称 选[%s] 行数 %d → %d %s' % (val, before, after, 'PASS' if after != before else 'FAIL'))

        print('== C. 我的待办（自定义页联动） ==')
        open(pg, page_url('我的待办.html'))
        before = pg.evaluate("() => document.querySelectorAll('#todoBody tr').length")
        val = pg.evaluate("id => { var s = document.getElementById(id); s.selectedIndex = 1; filterTodo(); return s.options[s.selectedIndex].text; }", 'todoProject')
        pg.wait_for_timeout(200)
        vis = pg.evaluate("() => Array.from(document.querySelectorAll('#todoBody tr')).filter(function(t){ return t.style.display !== 'none'; }).length")
        print('  我的待办 所属项目 选[%s] 可见行 %d → %d %s' % (val, before, vis, 'PASS' if vis != before else 'FAIL'))
        sb = pg.evaluate("id => { var s = document.getElementById(id); s.selectedIndex = 1; filterTodo(); return s.options[s.selectedIndex].text; }", 'todoSubmitter')
        pg.wait_for_timeout(200)
        vis2 = pg.evaluate("() => Array.from(document.querySelectorAll('#todoBody tr')).filter(function(t){ return t.style.display !== 'none'; }).length")
        print('  我的待办 提交人 选[%s] 叠加后可见行 %d %s' % (sb, vis2, 'PASS' if vis2 <= vis else 'FAIL'))

        print('== D. 脱敏落位抽样 ==')
        open(pg, page_url('财务协同/应付账单.html'))
        opts = pg.evaluate("() => { var s = document.getElementById('g35ProjectSel'); return s ? Array.from(s.options).map(function(o){return o.text;}).slice(0,4) : []; }")
        print('  应付账单 所属项目 options:', opts)
        body_txt = pg.evaluate("() => document.body.textContent")
        has_fake = any(x in body_txt for x in ['华骏重卡', '东海商用', '环通', '星途新能源'])
        has_real = any(x in body_txt for x in ['一汽解放', '上汽大众', '路凯', '小鹏'])
        print('  杜撰名在页面:%s 真名残留:%s %s' % (has_fake, has_real, 'PASS' if has_fake and not has_real else 'FAIL'))

        print('== JS 错误累计 ==')
        print('  pageerror:', len(errors))
        for e in errors[:5]:
            print('   ', e[:120])
        browser.close()

if __name__ == '__main__':
    main()
