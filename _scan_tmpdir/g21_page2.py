# -*- coding: utf-8 -*-
"""g21 ②③ 终版：列头 2→4 + 全部租金单价 form-row → 四价 form-row（页内+模板）"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROT = ROOT/'P3-R01-包装租赁管理后台原型'

FORM4 = '''<div class="form-row">
    <span class="form-label">参考未税采购价(元)</span>
    <div class="input-box"><input value="380.00" placeholder="采购参考单价"></div>
  </div>
  <div class="form-row">
    <span class="form-label">参考未税销售价(元)</span>
    <div class="input-box"><input placeholder="可售物料填写，不适用留空"></div>
  </div>
  <div class="form-row">
    <span class="form-label">参考未税租入价</span>
    <div class="input-box"><input placeholder="如 45.00 元/只·月（无租入来源留空）"></div>
  </div>
  <div class="form-row">
    <span class="form-label">参考未税租赁价</span>
    <div class="input-box"><input placeholder="按周期或按次，如 60.00 元/只·月 / 15.00 元/块·次"></div>
  </div>'''

pat_row = re.compile(r'<div class="form-row">\s*<span class="form-label">租金单价\(元/天\)</span>\s*<div class="input-box">.*?</div>\s*</div>', re.S)

for f, is_page in [(PROT/'基础数据'/'产品档案.html', True), (PROT/'基础数据'/'弹窗'/'新建产品.html', False)]:
    s = f.read_text(encoding='utf-8')
    if is_page:
        old_th = '          <th>参考单价(元)</th>\n          <th>租金单价(元/天)</th>'
        new_th = ('          <th>参考未税采购价(元)</th>\n'
                  '          <th>参考未税销售价(元)</th>\n'
                  '          <th>参考未税租入价</th>\n'
                  '          <th>参考未税租赁价</th>')
        if s.count(old_th) == 1:
            s = s.replace(old_th, new_th)
        else:
            assert s.count('参考未税采购价(元)</th>') >= 1, '列头新态不在且旧锚不匹配'
    n_row = len(pat_row.findall(s))
    print(f'{f.name}: form-row 命中 {n_row}')
    if n_row == 0 and '参考未税采购价' in s:
        print(f'{f.name} ALREADY DONE, skip')
        continue
    assert 1 <= n_row <= 2, f'form-row 异常 {n_row}'
    s = pat_row.sub(FORM4, s)
    for w in ['租金单价', '参考单价(元)</th>', '日租金']:
        n = s.count(w)
        print(f'  残留[{w}] = {n}')
        assert n == 0, f'{f.name} 残留 {w} x{n}'
    f.write_text(s, encoding='utf-8')
    print(f'{f.name} WRITTEN')
