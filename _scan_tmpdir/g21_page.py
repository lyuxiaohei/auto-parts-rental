# -*- coding: utf-8 -*-
"""g21 续跑：② 产品档案页 + ③ 模板（① demo-data 已落盘）"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROT = ROOT/'P3-R01-包装租赁管理后台原型'
PAGE = PROT/'基础数据'/'产品档案.html'
TPL = PROT/'基础数据'/'弹窗'/'新建产品.html'

FORM4 = '''
  <div class="form-row">
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
  </div>
'''

pat_form = re.compile(r'\s*<div class="form-row">\s*<span class="form-label">租金单价\(元/天\)</span>.*?</div>\s*</div>\s*', re.S)

s = PAGE.read_text(encoding='utf-8')
old_th = '          <th>参考单价(元)</th>\n          <th>租金单价(元/天)</th>'
assert s.count(old_th) == 1, f'列头锚 {s.count(old_th)}'
new_th = ('          <th>参考未税采购价(元)</th>\n'
          '          <th>参考未税销售价(元)</th>\n'
          '          <th>参考未税租入价</th>\n'
          '          <th>参考未税租赁价</th>')
s = s.replace(old_th, new_th)
assert len(pat_form.findall(s)) == 1, '页内表单锚'
s = pat_form.sub('\n' + FORM4, s)
for w in ['租金单价', '参考单价', '日租金']:
    assert w not in s, f'页内残留 {w}: ' + str([m.start() for m in re.finditer(w, s)])
PAGE.write_text(s, encoding='utf-8')
print('产品档案.html：列头 2→4 + 弹窗表单四价 ✓')

s2 = TPL.read_text(encoding='utf-8')
assert len(pat_form.findall(s2)) == 1, '模板表单锚'
s2 = pat_form.sub('\n' + FORM4, s2)
for w in ['租金单价', '参考单价']:
    assert w not in s2, f'模板残留 {w}'
TPL.write_text(s2, encoding='utf-8')
print('新建产品.html：表单四价（双层同步）✓')
