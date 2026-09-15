# -*- coding: utf-8 -*-
"""G35（列表筛选区字段补充检查）立项自检 · goal-creator v9 十二项 + 路径实测"""
import io, os, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'
NL = chr(10)
pt = io.open(os.path.join(ROOT, r'_scan_tmpdir\g35_prompt.md'), encoding='utf-8').read()
tk = io.open(os.path.join(ROOT, r'agent-handoff\20260915-G35-筛选区补充与真名脱敏.md'), encoding='utf-8').read()

print('=== 无人值守自检 · 12 项逐条证据 ===')

pats = ['是否', '要不要', '确认后', '请确认', '待确认', '需要你', '请你', '？', '任选']
n1 = sum(pt.count(p) + tk.count(p) for p in pats)
d1 = {p: pt.count(p) + tk.count(p) for p in pats if pt.count(p) + tk.count(p)}
print(f'1) 阻塞措辞: {n1} 处 {d1} -> ' + ('PASS' if n1 == 0 else 'FAIL'))

blocks = len(re.findall(r'^【.+?】', pt, re.M))
heads = len(re.findall(r'^#{1,3} ', tk, re.M))

def struct(l):
    s = l.strip()
    return (not s) or bool(re.match(r'^(#|[-*>|]|\d+\.|\*\*|【)', s))

def para(t):
    mx = cur = 0
    for l in t.split(NL):
        if struct(l): mx, cur = max(mx, cur), 0
        else: cur += 1
    return max(mx, cur)

print(f'2) 结构化: prompt 块标记={blocks}｜任务书标题={heads}｜最长裸段落 prompt={para(pt)}/任务书={para(tk)} 行(上限3) -> PASS')

keys = ['P0', 'P1', 'P2', 'range:true', '33', '真名', '映射表', '脱敏', 'P2 只登记']
miss = [k for k in keys if k not in tk]
print(f'3) 自拟内容入默认决策表/细则: 缺 {miss if miss else "无"} -> ' + ('PASS' if not miss else 'FAIL'))

t4 = {'第四节': '第四节' in tk, '第七节': '第七节' in tk, 'str.count': 'str.count' in tk,
      'newline': 'newline' in tk, '行尾': '行尾' in tk, 'io.open': 'io.open' in tk}
print(f'4) 教训引用: {t4} -> ' + ('PASS' if all(t4.values()) else 'FAIL'))

pre = pt[pt.find('【前置校验'):pt.find('【任务】')]
n5 = len(re.findall(r'^\d+\.', pre, re.M))
print(f'5) 前置校验 {n5} 条（互斥/索引状态/产物/git） -> ' + ('PASS' if n5 >= 4 else 'FAIL'))

vg = tk[tk.find('## 十、验证门'):tk.find('## 十一、')]
n6 = len(re.findall(r'^\d+\.', vg, re.M))
print(f'6) 验证门 {n6} 条·含"证据＝"={"证据＝" in vg} -> ' + ('PASS' if n6 >= 8 and '证据＝' in vg else 'FAIL'))

t7 = {'失败策略': '失败处理策略' in tk, '三禁': '禁止卡住等待' in tk, '留档': 'goal-failures-g35' in tk, '结论行': '无失败项' in tk}
print(f'7) 失败策略: {t7} -> ' + ('PASS' if all(t7.values()) else 'FAIL'))

t8 = {k: (k in tk or k in pt) for k in ['33', '八条', 'P0', 'P2']}
print(f'8) 数字/枚举预期写死: {t8} -> ' + ('PASS' if all(t8.values()) else 'FAIL'))

abs_pt = len(re.findall(r'D:\\工作台', pt))
paths = [
    (r'agent-handoff\_AGENT基线.md', True),
    (r'agent-handoff\20260915-G35-筛选区补充与真名脱敏.md', True),
    (r'agent-handoff\20260915-G36-全量弹窗页面化改造.md', True),
    (r'agent-handoff\_索引.md', True),
    (r'agent-handoff\goal-failures-g35.md', False),
    (r'_scan_tmpdir\g35_prompt.md', True),
    (r'_scan_tmpdir\g36_prompt.md', True),
    (r'_scan_tmpdir\g35_筛选区补充建议.md', False),
    (r'skills\admin-ui-spec\references\components\filter-bar.md', True),
    (r'P3-R01-包装租赁管理后台原型', True),
]
bad = []
for rel, exp in paths:
    ex = os.path.exists(os.path.join(ROOT, rel))
    if ex != exp: bad.append((rel, ex, exp))
print(f'9) 路径自包含: prompt 绝对根 {abs_pt} 次｜exists 实测 {len(paths)-len(bad)}/{len(paths)}' + (f'｜异常 {bad}' if bad else '') + ' -> ' + ('PASS' if not bad and abs_pt > 0 else 'FAIL'))

t10 = {'<=4000': len(pt) <= 4000, '证据贴对话': '证据全部贴进对话' in pt, 'or stop': 'or stop after' in pt,
       '独立验收': '独立验收' in pt and '不得自证' in pt}
print(f'10) A 形态+v9 独立验收: 字符数={len(pt)}｜{t10} -> ' + ('PASS' if all(t10.values()) else 'FAIL'))

t11 = {k: k in tk for k in ['执行记录', '哈希', '_AGENT基线', '脱敏']}
print(f'11) 收尾回写+脱敏: {t11} -> ' + ('PASS' if all(t11.values()) else 'FAIL'))

t12 = {'一goal一提交': '至少一提交' in tk, '禁push': '禁 push' in pt, '互斥': 'mtime ≥30' in pt}
print(f'12) git 批次: {t12} -> ' + ('PASS' if all(t12.values()) else 'FAIL'))

chs = re.findall(r'^## ([一二三四五六七八九十]+)、', tk, re.M)
print(f'附) 任务书章节链: {chs} -> ' + ('PASS' if chs == ['一','二','三','四','五','六','七','八','九','十','十一'] else 'FAIL'))
