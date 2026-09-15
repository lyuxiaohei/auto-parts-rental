# -*- coding: utf-8 -*-
"""G35 验证门：audit 复跑 vs g34baseline 逐键 diff（脱敏文本归一版）
判定：①post=128 页 ②既有页 problems 逐键新增 0（基线键先过 G35 替换映射归一——脱敏改文本不改问题性质）③死链 0 ④JS 0（F01 断网豁免沿例）
"""
import io, sys, json
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
OUT = Path(__file__).resolve().parent
base = json.load(open(OUT / 'audit_results_g34baseline.json', encoding='utf-8'))
post = json.load(open(OUT / 'audit_results.json', encoding='utf-8'))

# G35 脱敏映射（与 g35_t4_desensitize.py 一致·长度降序）——用于基线问题键文本归一
MAP = [
    ('一汽解放汽车有限公司', '华骏重卡汽车有限公司'), ('上汽大众汽车有限公司宁波分公司', '东海商用汽车有限公司宁波分公司'),
    ('小鹏汽车科技有限公司', '星途新能源汽车科技有限公司'), ('东风本田汽车有限公司', '长风汽车制造有限公司'),
    ('路凯包装运营（上海）有限公司', '环通循环包装运营（上海）有限公司'), ('宁波华塑包装制品有限公司', '甬城塑业包装制品有限公司'),
    ('苏州联恒五金制品有限公司', '吴越联合五金制品有限公司'), ('常州正大塑料托盘厂', '延陵塑料托盘厂'),
    ('上汽大众汽车有限公司', '东海商用汽车有限公司'), ('一汽大众汽车有限公司', '北方商用汽车有限公司'),
    ('东风锂电科技', '长丰锂电科技'), ('上汽通用五菱', '南方汽造'), ('吉利汽车', '星河汽车'),
    ('一汽解放', '华骏重卡'), ('上汽大众', '东海商用'), ('一汽大众', '北方商用'),
    ('小鹏汽车', '星途新能源'), ('东风本田', '长风汽制'), ('东风锂电', '长丰锂电'),
    ('苏州联恒', '吴越联合'), ('常州正大', '延陵托盘'), ('宁波华塑', '甬城塑业'),
    ('王琳总', '沈总'), ('袁丽晶', '严丽'), ('李国栋', '林国栋'), ('王志远', '周志远'), ('吕道远', '陆鸣'),
    ('路凯', '环通'), ('华塑', '甬城塑业'), ('联恒', '吴越'), ('正大', '延陵'), ('袁工', '严工'), ('徐蔚', '徐文'),
    ('王琳', '沈婷'), ('王强', '江强'), ('陈金', '陈锋'), ('赵磊', '邵磊'), ('何静', '何雅'), ('李静', '李婧'),
    ('袁明', '严明'), ('张伟', '张帆'), ('林芳', '林岚'), ('孙建军', '孙建平'), ('吴海涛', '吴海川'), ('郑卫东', '郑卫平'),
    ('吉客云', '捷科云'), ('小鹏', '星途'), ('道远', '陆鸣'), ('一汽解…', '华骏重卡…'),
]
MAP.sort(key=lambda x: len(x[0]), reverse=True)

def norm(s):
    for a, b in MAP:
        if a in s:
            s = s.replace(a, b)
    return s

def pkey(p):
    w = p.get('where') or {}
    return '|'.join([str(p.get('cat','')), str(p.get('type','')), str(w.get('tag','')), str(w.get('id','')),
                     str(w.get('row',''))[:24], str(w.get('text',''))[:16], str(p.get('detail',''))[:24]])

basemap = {}
for r in base:
    basemap.setdefault(r['page'].replace('\\', '/'), set()).update(norm(pkey(p)) for p in r['problems'])

new_probs, new_dl, new_js, exempt = [], [], [], []
tot_dl = tot_js = 0
mobile = [r for r in post if r['page'].replace('/', '\\').startswith('mobile\\')]
pc = [r for r in post if not r['page'].replace('/', '\\').startswith('mobile\\')]

for r in post:
    page = r['page'].replace('\\', '/')
    for p in r['problems']:
        k = norm(pkey(p))
        if k not in basemap.get(page, set()):
            new_probs.append((page, k))
    tot_dl += len(r['dead_links'])
    new_dl += [(page, d) for d in r['dead_links']]
    for e in r['js_errors']:
        tot_js += 1
        if 'ERR_CONNECTION_' in e.get('text', ''):
            exempt.append((page, e['text'][:80]))
        else:
            new_js.append((page, e['text'][:100]))

print(f"基线页数: {len(base)} ｜ post 页数: {len(post)}（PC {len(pc)} + mobile {len(mobile)}）")
print(f"全站死链合计: {tot_dl}")
print(f"全站 JS 错合计: {tot_js}（豁免断网 {len(exempt)} 条；其余 {len(new_js)}）")
for pg, t in exempt[:5]: print("  [豁免]", pg, t)
for pg, t in new_js[:10]: print("  [JS]", pg, t)
print(f"既有页 problems 逐键新增（脱敏归一后）: {len(new_probs)}")
for pg, k in new_probs[:30]: print("  [新增]", pg, '|', k)
verdict = (len(post) == 128 and tot_dl == 0 and len(new_js) == 0 and len(new_probs) == 0)
print("G35 AUDIT VERDICT:", "PASS" if verdict else "FAIL")
