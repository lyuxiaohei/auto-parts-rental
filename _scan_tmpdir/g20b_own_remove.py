# -*- coding: utf-8 -*-
"""归属权从物料档案层退场（道远 2026-09-11 澄清：归属权=库存实例层属性，一个物料可能租也可能买，档案层无法指定）：
① demo-data products：fields.src 删 12 + cells 归属权格删 12 + info 归属权块删（全部变体）
② 产品档案页：筛选块/列头/cfg filters/createModal radio/停用弹窗资产来源行
③ 新建产品模板：radio 行
④ A05：src 行注记。精确替换+assert 计数。"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROT = ROOT/'P3-R01-包装租赁管理后台原型'
DD = PROT/'_data/demo-data.js'
PAGE = PROT/'基础数据'/'产品档案.html'
TPL = PROT/'基础数据'/'弹窗'/'新建产品.html'

# ---------- ① demo-data products ----------
d = DD.read_text(encoding='utf-8')
i = d.find('products:')
j = d.find('\n  },', i)
seg = d[i:j]

# 1a. fields.src
n_src = len(re.findall(r'"src": "(?:自有|租入-路凯)", ', seg))
assert n_src == 12, f'fields.src {n_src}≠12'
seg2 = re.sub(r'"src": "(?:自有|租入-路凯)", ', '', seg)
# 1b. cells 归属权格（按精确文本，避免误伤分类/状态格；文件内为 \" 形态=反斜杠+引号）
CELL_PAT = r'"<span class=\\"tag tag-(?:green|orange)\\">(?:自有|租入-路凯)</span>", '
n_cell = len(re.findall(CELL_PAT, seg2))
assert n_cell == 12, f'cells 格 {n_cell}≠12'
seg2 = re.sub(CELL_PAT, '', seg2)
# 1c. info 归属权块（跨行 JSON，label 锚正则；full 标记可有可无、无尾逗号）
pat_info = re.compile(r"\{\s*'label': '归属权',\s*'text': '[^']*',?(\s*'full': true)?\s*\},\s*", re.S)
n_info = len(pat_info.findall(seg2))
assert n_info == 12, f'info 块 {n_info}≠12'
seg2 = pat_info.sub('', seg2)
assert '归属权' not in seg2 and '"src"' not in seg2, 'products 段仍有残留'
d = d[:i] + seg2 + d[j:]
DD.write_text(d, encoding='utf-8')
print(f'demo-data products：fields.src×{n_src} + cells×{n_cell} + info×{n_info} 全清')

# ---------- ② 产品档案页 ----------
s = PAGE.read_text(encoding='utf-8')
# 2a. 筛选块
pat_ff = re.compile(r'<div class="ff ff-row-extra"><span class="ff-label">归属权：</span>.*?</div>\s*', re.S)
assert len(pat_ff.findall(s)) == 1, '筛选块锚'
s = pat_ff.sub('', s)
# 2b. 列头
old_th = '          <th>归属权</th>\n'
assert s.count(old_th) == 1, f'列头 {s.count(old_th)}'
s = s.replace(old_th, '')
# 2c. cfg filters
old_cfg = "    { label: '归属权', field: 'src' },\n"
assert s.count(old_cfg) == 1, f'cfg {s.count(old_cfg)}'
s = s.replace(old_cfg, '')
# 2d. createModal radio 行（精确整块）
pat_radio = re.compile(r'\s*<div class="form-row">\s*<span class="form-label"><span class="req">\*</span>归属权</span>.*?</div>\s*</div>\s*', re.S)
assert len(pat_radio.findall(s)) == 1, 'radio 锚'
s = pat_radio.sub('\n  ', s)
# 2e. 停用弹窗资产来源行
old_drow = '<div class="drow"><div class="dlabel">资产来源</div><div class="dval">自有</div></div>'
assert s.count(old_drow) == 1, f'资产来源行 {s.count(old_drow)}'
s = s.replace(old_drow, '')
assert '归属权' not in s, '页面仍有归属权残留'
PAGE.write_text(s, encoding='utf-8')
print('产品档案.html：筛选/列头/cfg/radio/资产来源 五处全清')

# ---------- ③ 模板 ----------
s2 = TPL.read_text(encoding='utf-8')
assert len(pat_radio.findall(s2)) == 1, '模板 radio 锚'
s2 = pat_radio.sub('\n  ', s2)
assert '归属权' not in s2, '模板残留'
TPL.write_text(s2, encoding='utf-8')
print('新建产品.html：radio 行清除')

# ---------- ④ A05 ----------
a5 = (PROT/'P3-R01-A05-字段字典.md').read_text(encoding='utf-8')
old_row = '| `src` | 归属权 ¹ | 枚举 | 自有 / 租入-路凯 | 12/12 |'
if old_row in a5:
    a5 = a5.replace(old_row, '> **src（归属权）已退场（2026-09-11 道远澄清）**：归属权=库存实例层属性（一物料可租可买），档案层无法指定——fields.src/cells 格/info 行/筛选/列头/表单/停用弹窗资产来源 全部移除；库存查询「资产来源」维度承载。')
    (PROT/'P3-R01-A05-字段字典.md').write_text(a5, encoding='utf-8')
    print('A05：src 行注记化')
else:
    print('A05：src 行形态不同，待人工核对（不阻断）')
