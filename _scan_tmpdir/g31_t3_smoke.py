# -*- coding: utf-8 -*-
"""G31 T3 PW 冒烟：库位档案 + 库存查询（筛选/组合视角 BOM 套数）"""
from playwright.sync_api import sync_playwright
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'file:///D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型'
errs = []
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page()
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(BASE + '/基础数据/库位档案.html')
    pg.wait_for_load_state('load')
    ths = pg.evaluate('() => [...document.querySelectorAll("table thead th")].map(t=>t.textContent.trim())')
    print('库位表头:', ths)
    r1 = pg.evaluate('() => [...document.querySelectorAll("table tbody tr")][0].innerText')
    print('库位首行:', r1.replace('\t', ' | '))
    print('库位行数:', pg.locator('table tbody tr').count())
    pg.evaluate("() => { document.querySelector('.filter-card select').value='正品仓'; }")
    pg.evaluate("() => [...document.querySelectorAll('.filter-actions button')].find(b=>b.textContent.trim()==='查询').click()")
    pg.wait_for_timeout(150)
    print('筛 正品仓 行数:', pg.locator('table tbody tr').count())
    pg.goto(BASE + '/仓储作业/库存查询.html')
    pg.wait_for_load_state('load'); pg.wait_for_timeout(250)
    ths2 = pg.evaluate('() => [...document.querySelectorAll("#partView table thead th")].map(t=>t.textContent.trim())')
    print('散件表头尾3:', ths2[-3:])
    print('筛选 ff 数:', pg.evaluate("() => document.querySelectorAll('.filter-card .ff').length"))
    pg.evaluate("() => switchView('combo')")
    pg.wait_for_timeout(150)
    print('组合摘要:', pg.evaluate("() => document.getElementById('comboBomSum').textContent"))
    print('组合行数:', pg.evaluate("() => document.getElementById('comboBomBody').children.length"))
    pg.select_option('#comboBomSel', 'ZH-2602-B'); pg.wait_for_timeout(120)
    print('切 2602 摘要:', pg.evaluate("() => document.getElementById('comboBomSum').textContent"))
    pg.evaluate("() => switchView('part')"); pg.wait_for_timeout(100)
    # 仓库筛选联动（选 正品仓）
    sels = pg.evaluate("() => [...document.querySelectorAll('.filter-card .ff select')].map(s=>s.parentElement.previousElementSibling.textContent.trim()+':'+s.options[s.selectedIndex].text)")
    print('筛选清单:', sels)
    pg.evaluate("() => { const sels=[...document.querySelectorAll('.filter-card .ff select')]; const ws=sels.find(s=>[...s.options].some(o=>o.text==='正品仓')); ws.value='正品仓'; }")
    pg.evaluate("() => [...document.querySelectorAll('.filter-actions button')].find(b=>b.textContent.trim()==='查询').click()")
    pg.wait_for_timeout(150)
    print('库存筛 正品仓 行数:', pg.locator('#partView table tbody tr').count())
    br.close()
print('JS 错误:', errs if errs else 0)
