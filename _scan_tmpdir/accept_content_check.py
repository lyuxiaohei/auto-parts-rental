# -*- coding: utf-8 -*-
"""任务一·内容质量抽验（2026-09-08）：5 个弹窗四段内容与行数据自洽"""
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from urllib.parse import quote
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
BASE = 'http://127.0.0.1:8907/' + quote(str(PROTO.name))

# (页面, 锚文本, modalId, 行内须含的定位文本, 预期弹窗四段须出现的内容片段[来自行数据])
CASES = [
    ('销售管理/租赁单列表.html', '详情', 'detailModal', 'ZL-20260816-029',
     ['ZL-20260816-029', '上汽大众汽车有限公司宁波分公司', 'PRJ-2603', '2026-08-16', '已退租', 'RZD-20260815-003',
      '流转时间线', '租金明细']),
    ('仓储作业/组装列表.html', '详情', 'detailModal', 'ZZ-20260822-006',
     ['ZZ-20260822-006', '混合', 'ZH-2604-D', '流转时间线', '关联单据']),
    ('仓储作业/盘点列表.html', '详情', 'detailModal', 'PD-202608-03',
     ['PD-202608-03', '盘点', '流转时间线']),
    ('基础数据/客商管理.html', '详情', 'detailModal', 'DW-0001',
     ['一汽解放汽车有限公司', '客户', '袁明', '138****6621', 'DW-0001']),
    ('基础数据/BOM维护.html', '查看', 'bomViewModal', 'V2.1',
     ['ZH-2601-A', 'V2.1', '配方', '围板', '锁扣']),
]

results, fails = [], []
def check(item, ok, detail=''):
    results.append((item, ok, detail))
    if not ok: fails.append(item)
    print(('✅' if ok else '❌'), '|', item, '|', detail[:200])

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for page_f, anchor, mid, locator_txt, expects in CASES:
        page = browser.new_page()
        page.goto(BASE + '/' + quote(page_f), wait_until='load')
        page.wait_for_timeout(250)
        row = page.locator('tbody tr', has_text=locator_txt).first
        row_text = ' '.join(row.text_content().split())
        a = row.locator('a', has_text=anchor).first
        a.click()
        page.wait_for_timeout(120)
        body_txt = ' '.join(page.locator('#detailBody').text_content().split())
        title = page.locator('#detailTitle').text_content()
        segs = page.evaluate("""() => Array.from(document.querySelectorAll('#detailBody .dt-sec')).map(e => e.textContent.trim())""")
        missing = [e for e in expects if e not in body_txt]
        check(f'{page_f} · {locator_txt}', not missing and len(segs) >= 3,
              f'标题={title.strip()!r} 四段={segs} 缺失={missing} 行文本={row_text[:60]!r}')
        page.close()
    browser.close()

print()
print(f'==== 内容抽验汇总：{len(results)} 项，失败 {len(fails)} 项 ====')
sys.exit(1 if fails else 0)
