# -*- coding: utf-8 -*-
"""库存状态口径去数量词（道远 2026-09-11 拍板：完全不用体现几态）
规则：四态→状态；五态标记移除（状态枚举保留）；A02 md 历史记录不动
精确替换+assert；CRLF 保持原样（demo-data 为 CRLF，页面 LF/混合按原样读回）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def patch(rel, pairs, expect_zero=('四态',)):
    p = ROOT + '\\' + rel.replace('/', '\\')
    raw = open(p, 'rb').read().decode('utf-8')
    for old, new, cnt in pairs:
        n = raw.count(old)
        assert n == cnt, '%s 「%s」出现 %d 次，期望 %d' % (rel, old, n, cnt)
        raw = raw.replace(old, new)
    for kw in expect_zero:
        assert kw not in raw, '%s 仍含 %s' % (rel, kw)
    # 保持原行尾风格写回
    open(p, 'wb').write(raw.encode('utf-8'))
    print('✓', rel)

# 1. PC 库存查询页标题（data-note 锚保留，仅改文字）
patch(r'仓储作业/库存查询.html', [
    ('>库存四态查询</h3>', '>库存状态查询</h3>', 1),
])
# 2. mobile 副标题
patch(r'mobile/库存查询.html', [
    ('— · 四态筛选', '— · 状态筛选', 1),
])
# 3. demo-data：26 处统一 四态→状态（统计/口径/段名/注释）
p = ROOT + r'\_data\demo-data.js'
raw = open(p, 'rb').read().decode('utf-8')
n = raw.count('四态')
assert n == 26, 'demo-data 四态 %d 处，期望 26' % n
raw = raw.replace('四态', '状态')
assert '状态统计 + 资产轨迹' in raw and '（按库存状态' not in raw  # 纯字符级，无此形态
assert raw.count('状态口径管理') == 10
open(p, 'wb').write(raw.encode('utf-8'))
print('✓ _data/demo-data.js（26 处 四态→状态）')
# 4. F01 导航图：5 处五态
patch(r'P3-R01-F01-业务流程导航图.html', [
    ('库存缓冲 · 五态统计', '库存缓冲 · 状态统计', 1),
    ('库存查询（五态）', '库存查询', 1),
    ('五态口径：', '库存状态口径：', 1),
    ('(在库·五态)', '(在库)', 1),
    ('在库 · 五态', '在库', 1),
], expect_zero=('五态',))
# 5. A04 流程链标注数据
patch(r'P3-R01-A04-流程链标注数据.json', [
    ('库存缓冲（五态）', '库存缓冲', 1),
], expect_zero=('五态',))
# 6. 采购入库列表 内联 pin 文案
patch(r'采购管理/采购入库列表.html', [
    ('库存缓冲（五态）', '库存缓冲', 1),
], expect_zero=('五态',))
# 7. A03 标注数据 selector 同步新标题（保持 contains 匹配有效）
patch(r'P3-R01-A03-标注数据.json', [
    ('<h3 class=\\"card-title\\">库存四态查询</h3>', '<h3 class=\\"card-title\\">库存状态查询</h3>', 1),
], expect_zero=())
print('全部完成')
