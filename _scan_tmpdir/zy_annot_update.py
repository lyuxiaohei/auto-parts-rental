# -*- coding: utf-8 -*-
"""A03/A04 标注数据更新：转移出库列表 pin 改审核口径；我的待办 16 类→20 类两处"""
import json, io, os, time

ROOT = u'D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型'

def load(p):
    return json.loads(io.open(p, encoding='utf-8').read())

def save(p, obj):
    tmp = p + u'.tmp'
    io.open(tmp, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(obj, ensure_ascii=False, indent=2) + u'\n')
    os.replace(tmp, p)

# ---- A03 转移出库列表 pin ----
a03p = os.path.join(ROOT, u'P3-R01-A03-标注数据.json')
a03 = load(a03p)
pins = a03[u'租赁管理/转移出库列表.html']
assert len(pins) == 1 and u'确认转移后库存状态转' in pins[0]['note'], pins[0]['note'][:60]
pins[0]['note'] = pins[0]['note'].replace(
    u'确认转移后库存状态转「客户转租出」',
    u'审核通过后转移生效，库存状态转「客户转租出」（09-16 拍板加审·审核页承载）')
save(a03p, a03)
print('A03 OK:', pins[0]['note'][:80])

# ---- A04 我的待办 16 类 → 20 类 ----
a04p = os.path.join(ROOT, u'P3-R01-A04-流程链标注数据.json')
a04 = load(a04p)
pins = a04[u'我的待办.html']
hit = 0
for p in pins:
    if u'16 类单据统一进待办' in p['note']:
        p['note'] = p['note'].replace(
            u'16 类单据统一进待办，搜索/类型速滤后「去审核」跳转列表页并自动弹出审核弹窗（?audit=1）。',
            u'20 类单据统一进待办，搜索/类型速滤后「去审核」直达对应审核页（收款/退款登记为列表页 ?audit=1 自动弹审核弹窗）。')
        hit += 1
    elif u'覆盖 16 类单据' in p['note']:
        p['note'] = p['note'].replace(u'覆盖 16 类单据', u'覆盖 20 类单据')
        hit += 1
assert hit == 2, u'命中 %d 处（预期 2）' % hit
save(a04p, a04)
print('A04 OK: 2 处 16→20 更正')
