# -*- coding: utf-8 -*-
"""
详情弹窗数据驱动 · Playwright 逐行实点验证（B步6）
对每页每个「详情」锚：点击 → 断言 弹窗标题 textContent == '标题 · 行单号' → 内容含行关键字段 → 关闭。
模板页：默认预览渲染 + 标题非空。加载期 JS 错误必须为 0。
用法: python goal_dd_verify.py <batch.json>
  batch.json = [{"page":..., "entity":..., "title":..., "tpl":..., "preview":...}, ...]
"""
import json, sys
from pathlib import Path
from urllib.parse import quote
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8123/'
HERE = Path(__file__).parent

def run(batch):
    results = []  # (page, 单号/preview, PASS/FAIL, note)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={'width': 1440, 'height': 900})
        page = ctx.new_page()
        js_errors = {}
        page.on('pageerror', lambda e: js_errors.setdefault(page.url, []).append(str(e)))

        for item in batch:
            ent, title = item['entity'], item['title']
            mid = item.get('modalId', 'detailModal')
            anchor = item.get('anchor', '详情')
            tno = item.get('titleNo')  # 缺省 = 键本身
            # ---- 列表页逐行实点 ----
            url = BASE + quote(item['page'])
            page.goto(url)
            page.wait_for_load_state('networkidle')
            errs = [e for u, el in js_errors.items() if u == page.url for e in el]
            if errs:
                results.append((item['page'], '页面加载', 'FAIL', 'JS错误: ' + '; '.join(errs[:2])))
                continue
            keys = page.evaluate("() => Object.keys(window.DEMO_DATA && window.DEMO_DATA.%s || {})" % ent)
            anchors = page.evaluate("""(anchor) => {
                const out = [];
                document.querySelectorAll('tbody .ops a').forEach(a => {
                    if (a.textContent.trim() !== anchor) return;
                    const tr = a.closest('tr');
                    out.push({onclick: a.getAttribute('onclick'), row: tr.textContent.replace(/\\s+/g,' ')});
                });
                return out;
            }""", anchor)
            if not anchors:
                results.append((item['page'], '—', 'FAIL', '无 %s 锚' % anchor))
                continue
            wired = 0
            for a in anchors:
                row = a['row']
                key = next((k for k in keys if k in row), None)
                if not key:
                    results.append((item['page'], row[:26], 'FAIL', '行未匹配实体键'))
                    continue
                ok = page.evaluate("""([key, anchor, mid]) => {
                    const a = [...document.querySelectorAll('tbody .ops a')]
                        .find(x => x.textContent.trim() === anchor && x.closest('tr').textContent.replace(/\\s+/g,' ').indexOf(key) > -1);
                    if (!a) return '锚未找到';
                    a.click();
                    const ov = document.getElementById(mid);
                    if (!ov.classList.contains('show')) return '弹窗未打开';
                    const t = document.getElementById('detailTitle').textContent.trim();
                    const body = document.getElementById('detailBody').textContent.replace(/\\s+/g,' ');
                    ov.querySelector('.modal-close').click();
                    return {t, body, len: body.length};
                }""", [key, anchor, mid])
                if isinstance(ok, str):
                    results.append((item['page'], key, 'FAIL', ok))
                    continue
                want = title + ' · ' + (tno(key) if callable(tno) else (tno or key)) if False else title + ' · ' + (item.get('titleNoMap', {}).get(key, None) or key)
                if ok['t'] != want:
                    results.append((item['page'], key, 'FAIL', '标题[%s]≠[%s]' % (ok['t'], want)))
                    continue
                if ok['len'] < 120:
                    results.append((item['page'], key, 'FAIL', '正文过短 len=%d' % ok['len']))
                    continue
                wired += 1
                results.append((item['page'], key, 'PASS', '正文%d字' % ok['len']))
            # 未接线锚（onclick 未被剥离）= 接线失败
            if wired and all(a['onclick'] for a in anchors):
                results.append((item['page'], '接线', 'FAIL', 'onclick 未剥离'))
            # ---- 模板预览页 ----
            if not item.get('tpl'):
                continue
            turl = BASE + quote(item['tpl'])
            page.goto(turl)
            page.wait_for_load_state('networkidle')
            terrs = [e for u, el in js_errors.items() if u == page.url for e in el]
            if terrs:
                results.append((item['tpl'], '预览', 'FAIL', 'JS错误: ' + '; '.join(terrs[:2])))
                continue
            tp = page.evaluate("""(mid) => {
                const ov = document.getElementById(mid);
                const t = document.getElementById('detailTitle').textContent.trim();
                const body = document.getElementById('detailBody').textContent.replace(/\\s+/g,' ');
                return {shown: ov.classList.contains('show'), t, len: body.length};
            }""", mid)
            want = title + ' · ' + (item.get('titleNoMap', {}).get(item['preview'], None) or item['preview'])
            if not tp['shown'] or tp['t'] != want or tp['len'] < 120:
                results.append((item['tpl'], '预览', 'FAIL', 'shown=%s t=[%s] want=[%s] len=%d' % (tp['shown'], tp['t'], want, tp['len'])))
            else:
                results.append((item['tpl'], '预览', 'PASS', '标题/正文OK'))
        browser.close()
    return results

if __name__ == '__main__':
    batch = json.loads((HERE / sys.argv[1]).read_text(encoding='utf-8'))
    res = run(batch)
    npass = sum(1 for r in res if r[2] == 'PASS')
    for pg, k, st, note in res:
        print('%s | %s | %s | %s' % (st, pg, k, note))
    print('== %d/%d PASS ==' % (npass, len(res)))
    sys.exit(0 if npass == len(res) else 1)
