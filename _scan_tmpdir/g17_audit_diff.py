# -*- coding: utf-8 -*-
"""G17 验证门（基线滚动版）：audit 复跑（113 页）vs g17baseline（108 页）逐键 diff
判定：①post=113 页 ②既有 108 页 problems 逐键新增 0 ③全站死链 0 ④JS 错 0（F01 ERR_CONNECTION_CLOSED 断网豁免沿 G13 预注）⑤mobile 5 页各自 死链0/JS0"""
import io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
# G22 跨机归一（沿本脚本 G21 页键归一先例）：OUT 改按脚本位置解析，双机通用
OUT = Path(__file__).resolve().parent
base = json.load(open(OUT / 'audit_results_g17baseline.json', encoding='utf-8'))
post = json.load(open(OUT / 'audit_results.json', encoding='utf-8'))

def pkey(p):
    w = p.get('where') or {}
    return '|'.join([str(p.get('cat','')), str(p.get('type','')), str(w.get('tag','')), str(w.get('id','')), str(w.get('row',''))[:24], str(w.get('text',''))[:16], str(p.get('detail',''))[:24]])

# G22：4 页改名映射（基线旧键 → 现行键）；改名页问题键文本含「租赁出库」须归一回「组合出库」比对
RENAMES = {
  '租赁管理/组合出库列表.html': '租赁管理/租赁出库列表.html',
  '租赁管理/组合出库录单.html': '租赁管理/租赁出库录单.html',
  '租赁管理/弹窗/组合出库单详情.html': '租赁管理/弹窗/租赁出库单详情.html',
  '租赁管理/弹窗/组合出库确认.html': '租赁管理/弹窗/租赁出库确认.html',
}
legacy_page = {v: k for k, v in RENAMES.items()}

basemap = {}
for r in base:
    basemap.setdefault(r['page'].replace('\\', '/'), set()).update(pkey(p) for p in r['problems'])

new_probs, new_dl, new_js, exempt = [], [], [], []
tot_dl = tot_js = 0
mobile = [r for r in post if r['page'].replace('/', '\\').startswith('mobile\\')]
pc = [r for r in post if not r['page'].replace('/', '\\').startswith('mobile\\')]

for r in post:
    page = r['page'].replace('\\', '/')  # G21：跨机页键归一（基线 Windows \ 与副机 / 等价）
    basekey = legacy_page.get(page, page)  # G22：改名页按基线旧键比对
    for p in r['problems']:
        k = pkey(p)
        if k not in basemap.get(basekey, set()) and k.replace('租赁出库', '组合出库') not in basemap.get(basekey, set()):
            new_probs.append((page, k))
    tot_dl += len(r['dead_links'])
    new_dl += [(page, d) for d in r['dead_links']]
    for e in r['js_errors']:
        tot_js += 1
        if 'ERR_CONNECTION_' in e.get('text',''):  # G20 扩：断网变体 CLOSED/RESET/ABORTED 全豁免
            exempt.append((page, e['text'][:80]))
        else:
            new_js.append((page, e['text'][:100]))

print(f"基线页数: {len(base)} ｜ post 页数: {len(post)}（PC {len(pc)} + mobile {len(mobile)}）")
print(f"全站死链合计: {tot_dl}")
print(f"全站 JS 错合计: {tot_js}（豁免 F01 外链断网 {len(exempt)} 条；其余 {len(new_js)}）")
for pg, t in exempt[:5]: print("  [豁免]", pg, t)
for pg, t in new_js[:10]: print("  [JS新增]", pg, t)
print(f"既有页 problems 逐键新增: {len(new_probs)}")
for pg, k in new_probs[:20]: print("  [新增]", pg, '|', k)

print("\n---- mobile 5 页逐页（死链/JS/问题/审计异常）----")
for r in mobile:
    print(f"  {r['page']}  死链:{len(r['dead_links'])}  JS错:{len(r['js_errors'])}  问题:{len(r['problems'])}  异常:{r.get('audit_error','无')[:60]}  nav_anomaly:{r.get('nav_anomaly') is not None}")
    for p in r['problems'][:5]: print("     ·", pkey(p))

# G22：页键改名对账——基线消失键=4 改名旧键+G20 角色模板下线；post 新增键=4 改名新键+G16a/G19b/G20 三新页；改名页三项≤基线水平
base_keys = {r['page'].replace('\\', '/') for r in base}
post_keys = {r['page'].replace('\\', '/') for r in post}
disappeared = base_keys - post_keys
appeared = post_keys - base_keys
expect_disappear = set(RENAMES) | {'系统管理/弹窗/角色管理.html'}
expect_appear = set(RENAMES.values()) | {'P3-R01-A06-实体关系与状态机.html', '登录.html', '租赁管理/弹窗/退租入库新建.html'}
rename_ok = disappeared == expect_disappear and appeared == expect_appear
postcnt = {r['page'].replace('\\', '/'): r for r in post}
for oldk, newk in RENAMES.items():
    b = next(r for r in base if r['page'].replace('\\', '/') == oldk)
    if len(postcnt[newk]['problems']) > len(b['problems']):
        rename_ok = False
        print(f"  [改名页超基线] {newk}: post {len(postcnt[newk]['problems'])} > base {len(b['problems'])}")
print(f"页键对账: 消失 {sorted(disappeared)}")
print(f"页键对账: 新增 {sorted(appeared)}")
print(f"页键改名对账: {'PASS（4 对改名+既有增删页与 G16a/G19b/G20 沿革一致）' if rename_ok else 'FAIL'}")

mobile_ok = len(mobile) == 5 and all(len(r['dead_links']) == 0 and len(r['js_errors']) == 0 for r in mobile)
ok = len(post) == 115 and len(base) == 113 and tot_dl == 0 and len(new_js) == 0 and len(new_probs) == 0 and mobile_ok and rename_ok
print('\n==== audit 门：', 'PASS（115 页·死链0·JS0·diff 新增 0·mobile 5 页各自 0/0）====' if ok else 'FAIL ====')
sys.exit(0 if ok else 1)
