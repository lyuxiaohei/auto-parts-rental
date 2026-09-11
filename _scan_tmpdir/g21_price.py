# -*- coding: utf-8 -*-
"""物料档案四参考价（道远 2026-09-11 指令）：
参考未税采购价/参考未税销售价/参考未税租入价/参考未税租赁价（物料粒度·不落供应商）。
租价单位=按时间周期(月)或按次数(次)——09-08 纪要 L70-81「月租金+按套数单价·无日租金·按次/套数」印证。
原「参考单价(元)/租金单价(元/天)」去掉；「元/天」与「无日租金」口径冲突一并修正。"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROT = ROOT/'P3-R01-包装租赁管理后台原型'
DD = PROT/'_data/demo-data.js'
PAGE = PROT/'基础数据'/'产品档案.html'
TPL = PROT/'基础数据'/'弹窗'/'新建产品.html'

def td(v):
    if v == '—':
        return '"—"'
    return '"<span class=\\"td-num\\">' + v + '</span>"'

# 12 行四价表：key -> (采购, 销售, 租入, 租赁)
P4 = {
 'WBX-1210L': ('380.00', '—', '45.00 元/只·月', '60.00 元/只·月'),
 'WBX-1210M': ('340.00', '—', '—', '55.00 元/只·月'),
 'PLT-1210W': ('95.00', '—', '—', '15.00 元/块·次'),
 'PLT-1210P': ('110.00', '—', '12.00 元/块·月', '18.00 元/块·月'),
 'BTC-6040S': ('78.00', '—', '—', '—'),
 'BTC-6040':  ('85.00', '—', '10.00 元/只·月', '14.00 元/只·次'),
 'LJ-A100':   ('6.80', '9.80', '—', '—'),
 'LJ-B200':   ('4.20', '6.50', '—', '—'),
 'LJ-C300':   ('52.00', '68.00', '—', '—'),
 'LJ-D400':   ('36.00', '48.00', '—', '—'),
 'LJ-E500':   ('78.00', '98.00', '—', '—'),
 'LJ-F600':   ('15.50', '22.00', '—', '—'),
}
P4['BTC-6040'] = P4['BTC-6040']  # 键名自检：demo-data 实键=BTC-4060（productTaxes 外键笔误 BTC-6040 另修）

def info4(prices):
    buy, sell, rin, lease = prices
    def blk(label, text):
        return ("{\n          'label': '" + label + "',\n          'text': '" + text + "'\n        },")
    return (blk('参考未税采购价', buy + ' 元') + '\n        ' +
            blk('参考未税销售价', (sell + ' 元') if sell != '—' else '—（租赁器具不零售）') + '\n        ' +
            blk('参考未税租入价', rin if rin != '—' else '—（无租入来源）') + '\n        ' +
            blk('参考未税租赁价', lease if lease != '—' else '—（采购件 / 停用不计租）'))

# ---------- ① demo-data products ----------
d = DD.read_text(encoding='utf-8')
i = d.find('products:'); j = d.find('\n  },', i)
seg = d[i:j]
keys = [m.group(1) for m in re.finditer(r"'([A-Z][A-Z0-9-]*[0-9A-Z])': \{", seg)]
assert len(keys) == 12 and set(keys) == set(P4.keys()), f'键不齐: {keys}'

for k in keys:
    buy, sell, rin, lease = P4[k]
    a = seg.find("'" + k + "': {")
    b = min([seg.find("'" + kk + "': {", a+10) for kk in keys if seg.find("'" + kk + "': {", a+10) != -1] or [len(seg)])
    blk = seg[a:b]
    # cells：两价格（第6/7格）→ 四格——按每行真实旧值精确替换（表见 OLD）
    OLD = {
     'WBX-1210L': ('38.00', '38.00'), 'WBX-1210M': ('32.00', '32.00'),
     'PLT-1210W': ('12.00', '12.00'), 'PLT-1210P': ('18.00', '18.00'),
     'BTC-6040S': ('7.80', '7.80'),   'BTC-6040': ('8.50', '8.50'),
     'LJ-A100': ('6.80', '—'), 'LJ-B200': ('4.20', '—'), 'LJ-C300': ('52.00', '—'),
     'LJ-D400': ('36.00', '—'), 'LJ-E500': ('78.00', '—'), 'LJ-F600': ('15.50', '—'),
    }
    o1, o2 = OLD[k]
    g1 = '"<span class=\\"td-num\\">' + o1 + '</span>"'
    g2 = ('"<span class=\\"td-num\\">' + o2 + '</span>"') if o2 != '—' else '"—"'
    old_pair = g1 + ', ' + g2
    new4 = ', '.join([td(buy), td(sell), td(rin), td(lease)])
    assert blk.count(old_pair) == 1, f'{k} cells 价格对锚 {blk.count(old_pair)}: {old_pair[:60]}'
    blk2 = blk.replace(old_pair, new4)
    # info 价格行
    if '日租金' in blk2:  # 器具行
        pat = re.compile(r"\{\s*'label': '日租金',\s*'text': '[^']*'\s*\},")
        assert len(pat.findall(blk2)) == 1, k + ' 日租金锚'
        blk2 = pat.sub(info4(P4[k]), blk2)
    else:  # 组件行：参考单价 + 租金单价 两块
        pat2 = re.compile(r"\{\s*'label': '参考单价',\s*'text': '[^']*'\s*\},\s*\{\s*'label': '租金单价',\s*'text': '[^']*'\s*\},")
        assert len(pat2.findall(blk2)) == 1, k + ' 组件价锚'
        blk2 = pat2.sub(info4(P4[k]), blk2)
    assert '日租金' not in blk2 and '参考单价' not in blk2 and '租金单价' not in blk2, k + ' 价格旧词残留'
    seg = seg[:a] + blk2 + seg[b:]

d = d[:i] + seg + d[j:]
DD.write_text(d, encoding='utf-8')
print('demo-data products：12 行 cells 2→4 格 + info 四价块 全换')

# ---------- ② 产品档案页 ----------
s = PAGE.read_text(encoding='utf-8')
old_th = '''          <th>参考单价(元)</th>
          <th>租金单价(元/天)</th>'''
assert s.count(old_th) == 1
new_th = '''          <th>参考未税采购价(元)</th>
          <th>参考未税销售价(元)</th>
          <th>参考未税租入价</th>
          <th>参考未税租赁价</th>'''
s = s.replace(old_th, new_th)

# 弹窗表单（页内）
pat_form = re.compile(r'\s*<div class="form-row">\s*<span class="form-label">租金单价\(元/天\)</span>.*?</div>\s*</div>\s*', re.S)
assert len(pat_form.findall(s)) == 1, '页内表单锚'
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
s = pat_form.sub('\n' + FORM4, s)
assert '租金单价' not in s and '参考单价' not in s, '页内旧价词残留'
PAGE.write_text(s, encoding='utf-8')
print('产品档案.html：列头 2→4 + 弹窗表单四价')

# ---------- ③ 模板 ----------
s2 = TPL.read_text(encoding='utf-8')
assert len(pat_form.findall(s2)) == 1, '模板表单锚'
s2 = pat_form.sub('\n' + FORM4, s2)
assert '租金单价' not in s2 and '参考单价' not in s2, '模板旧价词残留'
TPL.write_text(s2, encoding='utf-8')
print('新建产品.html：表单四价（双层同步）')
