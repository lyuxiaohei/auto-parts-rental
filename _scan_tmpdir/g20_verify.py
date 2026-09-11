# -*- coding: utf-8 -*-
"""G20 验证门 1：全量断言（F01 v3.6 / T2a 退租入库新建 / T2b 待办 15 类 / T2c 角色旧模板 / T5 日租金口径）。"""
import pathlib, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROT = ROOT/'P3-R01-包装租赁管理后台原型'
results = []

def chk(name, cond, detail=''):
    results.append(('PASS' if cond else 'FAIL', name, detail))

# ---------- F01 ----------
f01 = (PROT/'P3-R01-F01-业务流程导航图.html').read_text(encoding='utf-8')
chk('F01 租赁出库录单=2(chip1+Mermaid源1)', f01.count('租赁出库录单') == 2, f'={f01.count("租赁出库录单")}')
chk('F01 退租入库新建 chip=1', f01.count('>退租入库新建</text>') == 1, f'={f01.count(">退租入库新建</text>")}')
chk('F01 chip href 正确', '租赁管理/弹窗/退租入库新建.html' in f01)
chk('F01 租入归还新建 chip=1', f01.count('>租入归还新建</text>') == 1, f'={f01.count(">租入归还新建</text>")}')
chk('F01 弹窗/角色管理.html=0', '系统管理/弹窗/角色管理.html' not in f01)
chk('F01 五类应收来源=1', f01.count('五类应收来源') == 1)
chk('F01 五类应付来源=1', f01.count('五类应付来源') == 1)
chk('F01 「4 来源」仅历史沿革保留', f01.count('4 来源') == 1 and '各 4 来源' in f01, f'={f01.count("4 来源")}')
chk('F01 「四类应收来源」=0', '四类应收来源' not in f01)
chk('F01 「四类应付来源」=0', '四类应付来源' not in f01)
chk('F01 v3.6>=3', f01.count('v3.6') >= 3, f'={f01.count("v3.6")}')
chk('F01 旧五态副标=0', '在库/在途/客户/退租/租入' not in f01)
chk('F01 新五态副标=1', f01.count('在库/客户/转租/退租/租入') == 1)
chk('F01 S1 注记五态全称', '在库/在客户（租出）/客户转租出/退租在途/租入在库' in f01)
chk('F01 S1 新增注记行', '在途＝应入库未入库' in f01)
chk('F01 角色管理改链独立页', '系统管理/角色管理.html' in f01)

# ---------- T2a 退租入库新建 ----------
tpl = PROT/'租赁管理'/'弹窗'/'退租入库新建.html'
chk('T2a 新模板存在', tpl.exists())
lst = (PROT/'租赁管理'/'退租入库列表.html').read_text(encoding='utf-8')
chk('T2a 列表「新建退租入库单」=2(按钮+弹窗标题)', lst.count('新建退租入库单') == 2, f'={lst.count("新建退租入库单")}')
chk('T2a 列表 createModal=1', lst.count('id="createModal"') == 1)
chk('T2a 弹窗字段：关联租赁单 select', '关联租赁单' in lst)
chk('T2a 弹窗字段：明细 3 行', all(k in lst for k in ['WBX-1210L', 'GB-800', '锁扣组件']))
chk('T2a 弹窗字段：缺损 3', '退回 86' in lst or '86' in lst)
# div 配平与备份差值对比（固有 JS 模板假象豁免）
bk_lst = (ROOT/'backup-g20-20260911'/'P3-R01-包装租赁管理后台原型'/'租赁管理'/'退租入库列表.html').read_text(encoding='utf-8')
diff_now = len(re.findall(r'<div[ >]', lst)) - lst.count('</div>')
diff_bk = len(re.findall(r'<div[ >]', bk_lst)) - bk_lst.count('</div>')
chk('T2a 列表 div 配平差值与备份一致', diff_now == diff_bk, f'{diff_now}/{diff_bk}')
for f, name in [((tpl.read_text(encoding='utf-8') if tpl.exists() else ''), '退租入库新建模板')]:
    for tag in ['div', 'table', 'form']:
        o = len(re.findall(f'<{tag}[ >]', f)); c = f.count(f'</{tag}>')
        chk(f'T2a {name} <{tag}> 配平', o == c, f'{o}/{c}')

# ---------- T2b 待办 15 类 ----------
d = (PROT/'_data'/'demo-data.js').read_text(encoding='utf-8')
ti = d[d.find('todoItems:'):]
ti = ti[:ti.find('\n  },')]
keys = re.findall(r"'[A-Z]+-\d{8}-\d{3,4}':\s*\{\s*'row'", ti)
chk('T2b todoItems 键数=15', len(keys) == 15, f'={len(keys)}')
chk("T2b type '租入库'=0", "'type': '租入库'" not in d and "'租入库',\n" not in d)
chk("T2b type '租入入库'>=1", "'租入入库'" in d)
chk('T2b 新增 3 键在', all(k in d for k in ['QTCK-20260904-003', 'DB-20260906-008', 'RZD-20260909-010']))
a4 = (PROT/'P3-R01-A04-流程链标注数据.json').read_text(encoding='utf-8')
chk('T2b A04「18 类」=0', '18 类' not in a4)
chk('T2b A04「15 类」>=1', '15 类' in a4)
todo = (PROT/'我的待办.html').read_text(encoding='utf-8')
chk('T2b 我的待办页「18 类」=0', '18 类' not in todo)
chk('T2b 我的待办页「15 类」>=1', '15 类' in todo)

# ---------- T2c 角色旧模板 ----------
chk('T2c 弹窗/角色管理.html 不存在', not (PROT/'系统管理'/'弹窗'/'角色管理.html').exists())
html_total = sum(1 for f in PROT.rglob('*.html'))
chk('T2c 原型 HTML 总数=115', html_total == 115, f'={html_total}')
up = (PROT/'系统管理'/'用户权限.html').read_text(encoding='utf-8')
chk('T2c 用户权限旧引用=0', '弹窗/角色管理.html' not in up)

# ---------- T5 日租金口径 ----------
zr = (PROT/'租赁管理'/'租入单列表.html').read_text(encoding='utf-8')
chk('T5 租入单列表「日租金(元)」=0', '日租金(元)' not in zr)
chk('T5 租入单列表 列头「租金」=1', '<th>租金</th>' in zr)
chk('T5 租入单列表「日租金 400」=0', '日租金 400' not in zr)
chk('T5 租入单列表「月租 45.00 元/只」>=1', '月租 45.00 元/只' in zr)
chk('T5 我的待办「日租金 1.20」=0', '日租金 1.20' not in todo)
chk('T5 我的待办「月租 12.00」>=1', '月租 12.00' in todo)
sh = (PROT/'租赁管理'/'弹窗'/'租入单审核.html').read_text(encoding='utf-8')
chk('T5 租入单审核「日租金」=0', '日租金' not in sh)
zd = (PROT/'系统管理'/'数据字典.html').read_text(encoding='utf-8')
chk('T5 数据字典「按天」=0', '<td>按天</td>' not in zd and '按天计租' not in zd)
chk('T5 数据字典「按月计租」>=1', '按月计租' in zd)
chk('T5 demo-data「元 / 日」=0', '元 / 日' not in d)
chk('T5 demo-data 否定式保留>=5', d.count('无日租金') >= 5, f'={d.count("无日租金")}')
chk('T5 demo-data BF-01 按月计租', '"abbr": "按月", "name": "按月计租"' in d)

npass = sum(1 for r in results if r[0] == 'PASS')
for st, name, detail in results:
    print(f'{st} {name}' + (f'  ({detail})' if detail and st == 'FAIL' else ''))
print(f'== {npass}/{len(results)} ==')
sys.exit(0 if npass == len(results) else 1)
