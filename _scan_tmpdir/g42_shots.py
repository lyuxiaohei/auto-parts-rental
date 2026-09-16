# -*- coding: utf-8 -*-
import os
from playwright.sync_api import sync_playwright
ROOT='/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型'
OUT='/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/_scan_tmpdir/g42_shots'
JOBS=[
 ('01-客商详情-开票资料税号段.png','基础数据/客商详情.html?id=DW-0001','body',None),
 ('02-租赁单新建-项目下拉六值.png','租赁管理/租赁单新建.html','#detailBody, .content','select'),
 ('03-应收账单-筛选预收.png','财务协同/应收账单.html','.filter-bar, .ff',None),
 ('04-退款登记-4值与静态行.png','财务协同/退款登记.html','.filter-bar, tbody',None),
 ('05-损益报表-单号lk.png','财务协同/损益报表.html','tbody',None),
 ('06-BOM维护-提交条无提交审核.png','基础数据/BOM维护.html','.submit-bar',None),
 ('07-项目看板-收入成本单号.png','首页/项目看板.html','tbody',None),
]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1440,'height':900})
    for fn,page,sel,extra in JOBS:
        pg.goto('file://'+os.path.join(ROOT,page), wait_until='networkidle'); pg.wait_for_timeout(400)
        path=os.path.join(OUT,fn)
        try:
            el=pg.query_selector(sel.split(',')[0].strip())
            if el: el.screenshot(path=path)
            else: pg.screenshot(path=path)
        except Exception:
            pg.screenshot(path=path, full_page=False)
        print('shot', fn)
    b.close()
