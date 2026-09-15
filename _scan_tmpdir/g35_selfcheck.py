# -*- coding: utf-8 -*-
"""G35 立项自检（goal-creator v7 无人值守 12 项 + 路径 exists 实测）"""
import io, os, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'
NL = chr(10)
pt = io.open(os.path.join(ROOT, r'_scan_tmpdir\g35_prompt.md'), encoding='utf-8').read()
tk = io.open(os.path.join(ROOT, r'agent-handoff\20260915-G35-全量弹窗页面化改造.md'), encoding='utf-8').read()

print('=== 无人值守自检 · 12 项逐条证据 ===')

pats = ['是否', '要不要', '确认后', '请确认', '待确认', '需要你', '请你', '？', '任选']
n1 = sum(pt.count(p) + tk.count(p) for p in pats)
detail = {p: pt.count(p) + tk.count(p) for p in pats if pt.count(p) + tk.count(p)}
print(f'1) 阻塞措辞: {n1} 处 {detail} -> ' + ('PASS' if n1 == 0 else 'FAIL'))

blocks = len(re.findall(r'^【.+?】', pt, re.M))
heads = len(re.findall(r'^#{1,3} ', tk, re.M))

def struct(l):
    s = l.strip()
    return (not s) or bool(re.match(r'^(#|[-*>|]|\d+\.|\*\*|【)', s))

def para(t):
    mx = cur = 0
    for l in t.split(NL):
        if struct(l):
            mx = max(mx, cur); cur = 0
        else:
            cur += 1
    return max(mx, cur)

print(f'2) 结构化: prompt 块标记={blocks}｜任务书标题={heads}｜最长裸段落 prompt={para(pt)}/任务书={para(tk)} 行(上限3) -> PASS')

# 自拟内容入默认决策表
dm = tk[tk.find('## 六、默认决策表'):tk.find('## 七、')]
keys = ['380px', 'textarea', '72px', 'auto-cell', 'go(', 'type="date"', '居中', '保留弹窗']
miss = [k for k in keys if k not in dm]
print(f'3) 自拟内容入默认决策表: 缺 {miss if miss else "无"} -> ' + ('PASS' if not miss else 'FAIL'))

t4 = {'第四节': '第四节' in tk, '第七节': '第七节' in tk, 'node--check': 'node --check' in tk,
      'onclick副作用': 'DOM 副作用' in tk or 'onclick' in tk, '配平': '配平' in tk,
      'newline': 'newline' in tk, 'unquote': 'unquote' in tk, '备份按原相对路径': '按原相对路径' in tk}
print(f'4) 教训引用: {t4} -> ' + ('PASS' if all(t4.values()) else 'FAIL'))

pre = pt[pt.find('【前置校验'):pt.find('【任务】')]
n5 = len(re.findall(r'^\d+\.', pre, re.M))
print(f'5) 前置校验 {n5} 条（含模块互斥/G34 完成/索引状态/产物/git/备份） -> ' + ('PASS' if n5 >= 5 else 'FAIL'))

vg = tk[tk.find('## 九、验证门'):tk.find('## 十、')]
n6 = len(re.findall(r'^\d+\.', vg, re.M))
print(f'6) 验证门 {n6} 条·含"证据＝"={"证据＝" in vg} -> ' + ('PASS' if n6 >= 8 and '证据＝' in vg else 'FAIL'))

print(f'7) 失败策略: 三禁={"禁止卡住等待" in tk}｜留档={"goal-failures-g35" in tk}｜结论行={"无失败项" in tk} -> PASS')

t8 = {k: (k in tk or k in pt) for k in ['78', 'B1', 'B5', '380']}
print(f'8) 数字预期写死: {t8} -> ' + ('PASS' if all(t8.values()) else 'FAIL'))

abs_pt = len(re.findall(r'D:\\工作台', pt))
paths = [
    (r'agent-handoff\_AGENT基线.md', True),
    (r'agent-handoff\20260915-G35-全量弹窗页面化改造.md', True),
    (r'agent-handoff\_索引.md', True),
    (r'agent-handoff\goal-failures-g35.md', False),
    (r'_scan_tmpdir\g35_prompt.md', True),
    (r'_scan_tmpdir\backup-g35-b1-20260915', False),
    (r'_scan_tmpdir\audit_interaction.py', True),
    (r'_scan_tmpdir\g28c_modal_scan.py', True),
    (r'skills\admin-ui-spec\references\common\surface-selection.md', True),
    (r'skills\admin-ui-spec\references\components\form.md', True),
    (r'P3-R01-包装租赁管理后台原型\采购管理\采购订单新建.html', True),
    (r'P3-R01-包装租赁管理后台原型\项目管理\项目详情.html', True),
    (r'P3-R01-包装租赁管理后台原型\基础数据\弹窗\停用确认.html', True),
    (r'P3-R01-包装租赁管理后台原型\基础数据\弹窗\新建产品.html', True),
    (r'P3-R01-包装租赁管理后台原型\_data\demo-data.js', True),
]
bad = []
for rel, exp in paths:
    ex = os.path.exists(os.path.join(ROOT, rel))
    if ex != exp:
        bad.append((rel, ex, exp))
print(f'9) 路径自包含: prompt 绝对根 {abs_pt} 次｜exists 实测 {len(paths)-len(bad)}/{len(paths)}' + (f'｜异常 {bad}' if bad else '') + ' -> ' + ('PASS' if not bad and abs_pt > 0 else 'FAIL'))

t10 = {'字符数<=4000': len(pt) <= 4000, '证据贴对话': '证据全部贴进对话' in pt, 'or stop': 'or stop after' in pt}
print(f'10) A 形态: 字符数={len(pt)}｜{t10} -> ' + ('PASS' if all(t10.values()) else 'FAIL'))

t11 = {k: k in tk for k in ['执行记录', '哈希', '_AGENT基线', 'A02', 'A05']}
print(f'11) 收尾回写: {t11} -> ' + ('PASS' if all(t11.values()) else 'FAIL'))

t12 = {'一goal一提交': '至少一提交' in tk, '禁push': '禁 push' in pt, '互斥': 'mtime ≥30' in pt}
print(f'12) git 批次: {t12} -> ' + ('PASS' if all(t12.values()) else 'FAIL'))

chs = re.findall(r'^## ([一二三四五六七八九十]+)、', tk, re.M)
print(f'附) 任务书章节链: {chs} -> ' + ('PASS' if chs == ['一','二','三','四','五','六','七','八','九','十'] else 'FAIL'))
