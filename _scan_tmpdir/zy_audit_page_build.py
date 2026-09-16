# -*- coding: utf-8 -*-
"""转移出库审核.html 构建：侧边栏取自转移出库列表.html + 七处文字替换（锚点断言）"""
import io, os, sys, time

ROOT = u'D:/工作台-吕道远/5-【ACTIVE】汽车物流包装租赁/P3-R01-包装租赁管理后台原型'
SRC_LIST = os.path.join(ROOT, u'租赁管理', u'转移出库列表.html')
NEW_PAGE = os.path.join(ROOT, u'租赁管理', u'转移出库审核.html')

def read(p):
    return io.open(p, encoding='utf-8').read()

def write(p, s):
    for i in range(3):
        try:
            tmp = p + u'.tmp'
            io.open(tmp, 'w', encoding='utf-8', newline='').write(s)
            os.replace(tmp, p)
            return
        except Exception as e:
            if i == 2:
                raise
            time.sleep(1)

lst = read(SRC_LIST)
new = read(NEW_PAGE)

# ---- 1. 侧边栏换血 ----
a = lst.index(u'<aside')
b = lst.index(u'</aside>') + len(u'</aside>')
side_list = lst[a:b]
assert u'sm-link selected">转移出库<' in side_list, u'源侧边栏无 转移出库 selected'

a2 = new.index(u'<aside')
b2 = new.index(u'</aside>') + len(u'</aside>')
assert u'sm-link selected">租入归还<' in new[a2:b2], u'克隆页侧边栏 selected 应在 租入归还'
new = new[:a2] + side_list + new[b2:]

# ---- 2. 文字替换（逐条锚点断言） ----
reps = [
    (u'<title>租入归还审核 - 包装租赁管理后台</title>',
     u'<title>转移出库审核 - 包装租赁管理后台</title>'),
    (u'<span class="tab">租入归还 <span class="close">×</span></span>',
     u'<span class="tab">转移出库 <span class="close">×</span></span>'),
    (u'<span class="tab active">租入归还审核 <span class="close">×</span></span>',
     u'<span class="tab active">转移出库审核 <span class="close">×</span></span>'),
    (u'<h3 class="card-title" id="dtTitle">租入归还审核</h3>',
     u'<h3 class="card-title" id="dtTitle">转移出库审核</h3>'),
    (u'审核通过后归还出库并终止租金应付；支持分批归还（未还数量继续计租）。',
     u'审核通过后转移生效，库存状态转「客户转租出」；按终端结算的后续账单主体切换为终端客户；驳回退回修改。'),
    (u"""<div class="submit-bar"><button class="btn btn-default" onclick="go('../租入管理/租入归还列表.html')">取 消</button>""",
     u"""<div class="submit-bar"><button class="btn btn-default" onclick="go('../租赁管理/转移出库列表.html')">取 消</button>"""),
    (u"var ENT = 'rentInReturns', DEF = 'GHCK-20260903-001';",
     u"var ENT = 'transferOutbounds', DEF = 'ZY-20260915-005';"),
    (u"(rec.title || '租入归还审核')",
     u"(rec.title || '转移出库审核')"),
]
for old, rep in reps:
    assert new.count(old) == 1, u'锚点非唯一(%d)：%s' % (new.count(old), old[:40])
    new = new.replace(old, rep)

# ---- 3. 残留断言 ----
for bad in (u'租入归还审核', u'rentInReturns', u'GHCK-', u'zyList'):
    assert bad not in new, u'残留：%s' % bad

write(NEW_PAGE, new)
print('OK 侧边栏+8 处替换完成，残留断言全过')
