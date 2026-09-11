# -*- coding: utf-8 -*-
"""G22 验证门 1：租赁出库称呼统一与杂项清理 · 逐项断言（2026-09-11 任务书验证门 1 写死口径）
用法：python g22_verify.py  → 逐行 PASS/FAIL，末行汇总
"""
import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.abspath(__file__)).rsplit(os.sep, 1)[0]
PROTO = os.path.join(ROOT, 'P3-R01-包装租赁管理后台原型')
DD = os.path.join(PROTO, '_data', 'demo-data.js')

results = []
def chk(name, ok, detail=''):
    results.append(ok)
    print(('PASS' if ok else 'FAIL'), '|', name, '|', detail)

def read(p): return open(p, encoding='utf-8', newline='').read()

# ── 1. 4 文件改名 ─────────────────────────────────────────
olds = ['租赁管理/组合出库列表.html', '租赁管理/组合出库录单.html',
        '租赁管理/弹窗/组合出库单详情.html', '租赁管理/弹窗/组合出库确认.html']
news = ['租赁管理/租赁出库列表.html', '租赁管理/租赁出库录单.html',
        '租赁管理/弹窗/租赁出库单详情.html', '租赁管理/弹窗/租赁出库确认.html']
chk('旧文件名 4 个全不存在', all(not os.path.exists(os.path.join(PROTO, o)) for o in olds), str(olds))
chk('新文件名 4 个全存在', all(os.path.exists(os.path.join(PROTO, n)) for n in news), str(news))

# ── 2. 旧文件名引用清零 + 菜单项存在 ──────────────────────
def scan_all(pred):
    hits = []
    for dp, dns, fns in os.walk(PROTO):
        for fn in fns:
            if not fn.endswith(('.html', '.js', '.json', '.md')): continue
            p = os.path.join(dp, fn)
            c = read(p).count(pred)
            if c: hits.append((p, c))
    return hits

chk('「组合出库列表.html」全站 0 命中', not scan_all('组合出库列表.html'), str(scan_all('组合出库列表.html')))
menu_hits = sum(read(os.path.join(PROTO, p)).count("go('租赁管理/租赁出库列表.html')")
                for p in ['我的待办.html', '首页/项目看板.html'])
chk("菜单项 go('租赁管理/租赁出库列表.html') 存在", menu_hits >= 1, f'根级页命中 {menu_hits}')

# ── 3. 「组合出库」可见字样（白名单=开发规则.md v3.5 沿革句 1 处） ──
whitelist = {'P3-R01-F01-业务流程导航图-开发规则.md'}
raw = scan_all('组合出库')
visible = [(p, c) for p, c in raw if os.path.relpath(p, PROTO) not in whitelist]
chk('原型目录「组合出库」可见=0（白名单豁免：开发规则.md 沿革句 ×1）', not visible,
    f'白名单内 {raw} 可见 {visible}')

# ── 4. dictItems 单据名 ───────────────────────────────────
dd = read(DD)
chk('dictItems 含 "name": "租赁出库单"', '"name": "租赁出库单"' in dd, 'CK 行')

# ── 5. todoItems 16 键 + 租赁出库类型 ─────────────────────
seg = dd[dd.find('todoItems:'):dd.find('projects:')]
keys = re.findall(r"^    '([^']+)': \{", seg, re.M)
chk('todoItems 键数=16', len(keys) == 16, f'{len(keys)} 键：…{keys[-2:]}')
chk('todoItems 含 type「租赁出库」', '"type": "租赁出库"' in seg, 'CK-20260910-022')
todo_html = read(os.path.join(PROTO, '我的待办.html'))
chk('我的待办 option 含「租赁出库」', '<option>租赁出库</option>' in todo_html, '插于租赁单后')
a04 = read(os.path.join(PROTO, 'P3-R01-A04-流程链标注数据.json'))
chk('A04「15 类」=0', '15 类' not in a04, '0')
chk('A04「16 类」≥1', a04.count('16 类') >= 1, f'{a04.count("16 类")} 处')

# ── 6. 操作日志 module 五旧名清零（option+demo-data module 值） ──
oplog = read(os.path.join(PROTO, '系统管理', '操作日志.html'))
banned = ['包装管理', '财务应收', '基础资料', '订单管理', '仓储作业']
opt_bad = [t for t in banned if f'<option>{t}</option>' in oplog]
mod_bad = [t for t in banned if f'"module": "{t}"' in dd]
cells_bad = [t for t in banned if f'"{t}"' in re.sub(r'"module": "[^"]*"', '', dd)]
chk('操作日志 option 无五旧名', not opt_bad, str(opt_bad))
chk('demo-data module 值无五旧名', not mod_bad, str(mod_bad))
chk('demo-data 双引号字符串无五旧名残留', not cells_bad, str(cells_bad))

# ── 7. 租入-路凯 全站 0 ──────────────────────────────────
lu = scan_all('租入-路凯')
chk('「租入-路凯」全站=0', not lu, str(lu))

# ── 8. 赔偿核销 radio 双层 ────────────────────────────────
tpl = read(os.path.join(PROTO, '仓储作业', '弹窗', '其他出库新建.html'))
lst = read(os.path.join(PROTO, '仓储作业', '其他出库列表.html'))
radio = '<span class="radio"><span class="dot"></span>赔偿核销</span>'
chk('其他出库新建弹窗含「赔偿核销」radio（模板+页内双层）', radio in tpl and radio in lst, '盘亏后·其他前')

# ── 9. 页数口径 ──────────────────────────────────────────
n_html = sum(1 for dp, dns, fns in os.walk(PROTO) for fn in fns if fn.endswith('.html'))
chk('原型 HTML 总数=115', n_html == 115, str(n_html))

n_pass = sum(results)
print(f'==== g22_verify：{n_pass}/{len(results)} PASS，失败 {len(results) - n_pass} 项 ====')
sys.exit(0 if n_pass == len(results) else 1)
