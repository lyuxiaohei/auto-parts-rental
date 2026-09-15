# -*- coding: utf-8 -*-
"""G34 PW 三弹窗抽验：物料（新建物料）/ 客商开票资料 / 库位（新建库位）
口径：编程触发（evaluate openModal·IAB 管道缺陷先例）+ textContent 断言 + 控制台 0 错误 + 截图×3
"""
import io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型')
OUT = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir')
SL = ['0%', '1%', '3%', '6%', '9%', '13%']
JSQ = ['预付', '货到付款', '周结', '半月结', '月结', '发票后 30 天', '发票后 60 天', '发票后 90 天', '发票后 120 天']
KW = ['存储位', '拣选位', '暂存位', '不合格品位']
EXPECT_LABELS = ['物料编码', '物料名称', '物料类型', '供应商内部编码', '物料型号', '规格', '单位',
                 '参考未税采购价(元)', '参考未税销售价(元)', '参考未税租入价', '参考未税租赁价', '备注']

J = lambda v: json.dumps(v, ensure_ascii=False)          # 数组字面量（供 concat/构造用）
JS = lambda v: json.dumps(json.dumps(v, ensure_ascii=False, separators=(',', ':')))  # 紧凑 JSON 字符串字面量（=== JSON.stringify）

results = []

def check(name, page, url, script, shot):
    errs = []
    page.on('pageerror', lambda e: errs.append(str(e)[:150]))
    page.on('console', lambda m: errs.append(m.text[:150]) if m.type == 'error' else None)
    page.goto(url, wait_until='load', timeout=20000)
    page.wait_for_timeout(600)
    r = page.evaluate(script)
    page.wait_for_timeout(200)
    page.screenshot(path=str(OUT / shot))
    print('\n[%s] %s' % (name, url.split('/')[-1]))
    for k, v in r.items():
        print('  %-30s %s' % (k, v))
    print('  JS/console 错误: %d %s' % (len(errs), errs[:3] if errs else ''))
    print('  截图: %s' % (OUT / shot))
    ok = all(r.values()) and not errs
    print('  ==> %s' % ('PASS' if ok else 'FAIL'))
    results.append((name, ok))

with sync_playwright() as pw:
    b = pw.chromium.launch()

    # 1) 物料：产品档案 新建物料弹窗
    pg = b.new_page(viewport={'width': 1440, 'height': 900})
    script1 = """() => {
      const out = {};
      openModal('createModal');
      const body = document.querySelector('#createModal .modal-body');
      const labels = [...body.querySelectorAll('.form-row > .form-label')].map(s => s.textContent.replace('*','').trim());
      out['字段顺序正确'] = JSON.stringify(labels) === __LABELS__;
      const ta = document.getElementById('prodRemarkTa');
      out['备注=textarea(maxlength200)'] = !!(ta && ta.tagName === 'TEXTAREA' && ta.getAttribute('maxlength') === '200');
      const cnt = document.getElementById('prodRemarkCnt');
      ta.value = '测试备注文字'; ta.dispatchEvent(new Event('input'));
      out['字数计数联动'] = cnt.textContent === '6/200';
      ta.value = ''; ta.dispatchEvent(new Event('input'));
      const rows = document.querySelectorAll('#taxEditRows .tax-edit-row');
      out['税率区行数(预填2行)'] = rows.length === 2;
      if (rows.length) {
        const sels = rows[0].querySelectorAll('select');
        out['行内=3个下拉(供应商/税率/周期)'] = sels.length === 3;
        const sl = [...sels[1].options].map(o => o.text);
        const jsq = [...sels[2].options].map(o => o.text);
        out['税率下拉=SL6值'] = JSON.stringify(sl) === __SL__;
        out['结算周期=JSQ9值'] = JSON.stringify(jsq) === __JSQ__;
        out['预填税率选中13pct'] = sels[1].value === '13%';
      }
      const short = [...body.querySelectorAll('.form-row .input-box')].filter(d => (d.getAttribute('style')||'').includes('width:220px'));
      out['短占位220px控件=4'] = short.length === 4;
      const taH = ta.closest('.input-box');
      out['备注高72px样式'] = (taH.getAttribute('style')||'').includes('height:72px');
      return out;
    }""".replace('__LABELS__', JS(EXPECT_LABELS)).replace('__SL__', JS(SL)).replace('__JSQ__', JS(JSQ))
    check('物料弹窗', pg, (ROOT / '基础数据' / '产品档案.html').as_uri(), script1, 'g34_pw_prod.png')
    pg.close()

    # 2) 客商开票资料：客商管理 页内嵌 invoiceInfoModal
    pg = b.new_page(viewport={'width': 1440, 'height': 900})
    script2 = """() => {
      const out = {};
      openModal('invoiceInfoModal');
      const s = document.getElementById('invSettleSel');
      out['弹窗打开'] = !!document.querySelector('#invoiceInfoModal.show');
      out['结算周期select存在'] = !!s;
      const jsq = s ? [...s.options].map(o => o.text) : [];
      out['结算周期=JSQ9值(字典)'] = JSON.stringify(jsq) === __JSQ__;
      out['月结仍在(静态值保留)'] = jsq.indexOf('月结') > -1;
      return out;
    }""".replace('__JSQ__', JS(JSQ))
    check('客商开票资料弹窗', pg, (ROOT / '基础数据' / '客商管理.html').as_uri(), script2, 'g34_pw_kst.png')
    pg.close()

    # 3) 库位：库位档案 新建库位弹窗 + 筛选区
    pg = b.new_page(viewport={'width': 1440, 'height': 900})
    script3 = """() => {
      const out = {};
      openModal('createModal');
      const body = document.querySelector('#createModal .modal-body');
      out['弹窗打开'] = !!document.querySelector('#createModal.show');
      const rows = [...body.querySelectorAll('.form-row')];
      const labels = rows.map(r => ((r.querySelector('.form-label')||{}).textContent || '').replace('*','').trim());
      out['首行=仓库名称'] = labels[0] === '仓库名称';
      const whInput = rows[0].querySelector('input');
      out['仓库=文本输入框'] = !!whInput && whInput.tagName === 'INPUT';
      out['无库区残留(原料区)'] = !document.body.textContent.includes('原料区');
      const s1 = document.getElementById('locTypeSel');
      const kw = s1 ? [...s1.options].map(o => o.text) : [];
      out['库位类型=KW4值(字典)'] = JSON.stringify(kw) === __KW_S__;
      const ta = body.querySelector('textarea');
      out['备注=textarea(不限字数)'] = !!ta && !ta.getAttribute('maxlength');
      const taH = ta ? ta.closest('.input-box') : null;
      out['备注高72px样式'] = !!(taH && (taH.getAttribute('style')||'').includes('height:72px'));
      const s2 = document.getElementById('locTypeFilterSel');
      const kw2 = s2 ? [...s2.options].map(o => o.text) : [];
      out['筛选区=全部+KW4值'] = JSON.stringify(kw2) === JSON.stringify(['全部'].concat(__KW__));
      return out;
    }""".replace('__KW_S__', JS(KW)).replace('__KW__', J(KW))
    check('库位新建弹窗', pg, (ROOT / '基础数据' / '库位档案.html').as_uri(), script3, 'g34_pw_loc.png')
    pg.close()

    b.close()

print('\n==== 汇总 ====')
fails = [n for n, ok in results if not ok]
print('三弹窗抽验: %d/3 PASS %s' % (len(results) - len(fails), ('·FAIL=' + ','.join(fails)) if fails else ''))
sys.exit(1 if fails else 0)
