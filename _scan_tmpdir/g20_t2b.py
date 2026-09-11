# -*- coding: utf-8 -*-
"""G20 T2b：我的待办 15 类——type 修正+todoItems 12→15+A04 18→15+A03 删调拨在途"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DD = ROOT/'P3-R01-包装租赁管理后台原型'/'_data'/'demo-data.js'
A04 = ROOT/'P3-R01-包装租赁管理后台原型'/'P3-R01-A04-流程链标注数据.json'
A03 = ROOT/'P3-R01-包装租赁管理后台原型'/'P3-R01-A03-标注数据.json'

# ① demo-data（幂等：已改过则跳过 type 段）
d = DD.read_text(encoding='utf-8')
old_type = '"type": "租入库"'
if d.count(old_type) == 1:
    d = d.replace(old_type, '"type": "租入入库"')
else:
    assert d.count(old_type) == 0 and d.count('"type": "租入入库"') >= 1, 'type 锚异常'

anchor_sk = "'SK-20260901-003': { 'row': {\"fields\": {\"auditor\": \"袁丽晶\", \"type\": \"收款确认\", \"docNo\": \"SK-20260901-003\", \"summary\": \"一汽解放 · 8 月租金回款\", \"project\": \"PRJ-2601\", \"submitter\": \"李静\", \"time\": \"09-01 09:15\", \"action\": \"待确认\"}}, 'link': '财务协同/回款登记.html?audit=1' },"
assert d.count(anchor_sk) == 1, 'SK 行锚'
NEW3 = """    'QTCK-20260904-003': { 'row': {"fields": {"auditor": "李国栋", "type": "其他出库", "docNo": "QTCK-20260904-003", "summary": "华东中心仓 · 报废隔板 12 块", "project": "华东中心仓", "submitter": "赵磊", "time": "09-04 10:05", "action": "待审核"}}, 'link': '仓储作业/其他出库列表.html?audit=1' },
    'DB-20260906-008': { 'row': {"fields": {"auditor": "李国栋", "type": "库存调拨", "docNo": "DB-20260906-008", "summary": "华东中心仓→华南中心仓 · 围板箱 50 只", "project": "华东中心仓", "submitter": "赵磊", "time": "09-06 11:40", "action": "待审核"}}, 'link': '仓储作业/库存调拨列表.html?audit=1' },
    'RZD-20260909-010': { 'row': {"fields": {"auditor": "王强", "type": "租入单", "docNo": "RZD-20260909-010", "summary": "路凯 · 大箱租入 40 只（月租）", "project": "PRJ-2603", "submitter": "王强", "time": "09-09 09:50", "action": "待审核"}}, 'link': '租赁管理/租入单列表.html?audit=1' },"""
d = d.replace(anchor_sk, anchor_sk + '\n' + NEW3)
DD.write_text(d, encoding='utf-8')

# 复检 15 键
import re
i = d.find('todoItems:'); j = d.find('\n  },', i)
keys = re.findall(r"'([A-Z]+-[0-9-]+)':", d[i:j])
assert len(keys) == 15, f'键数 {len(keys)}'
assert '"type": "租入库"' not in d[i:j], 'type 残留'
print(f'todoItems 15 键 OK: {keys[-4:]}')

# ② A04 18→15（幂等）
a4 = A04.read_text(encoding='utf-8')
if '18 类单据统一进待办' in a4:
    a4 = a4.replace('18 类单据统一进待办', '15 类单据统一进待办')
    A04.write_text(a4, encoding='utf-8')

# ③ A03 删调拨在途（幂等）
a3 = A03.read_text(encoding='utf-8')
old_diaobo = '租入到货待入库 / 调拨在途）'
if old_diaobo in a3:
    a3 = a3.replace(old_diaobo, '租入到货待入库）')
    A03.write_text(a3, encoding='utf-8')

import json
json.loads(a3); json.loads(a4)
print('A04 18→15 OK；A03 调拨在途删 OK；两 json load OK')
