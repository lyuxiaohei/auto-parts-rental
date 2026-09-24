# -*- coding: utf-8 -*-
"""G56 acceptance - static checks: (1) structure (2) href (3) grep (5) F02<->F01 reconciliation"""
import sys, os, re, json
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁"
F01  = os.path.join(ROOT, r"P3-R01-包装租赁管理后台原型\P3-R01-F01-业务流程导航图.html")
F02  = os.path.join(ROOT, r"P1-R03\P1-R03-F02-业务流程导航图绘图信息.md")
F01_DIR = os.path.dirname(F01)

html = open(F01, encoding='utf-8').read()
f02  = open(F02, encoding='utf-8').read()
res = {}

# ---------- (1) structure gate ----------
TAGS = ['svg','a','g','text','rect','line','path']
tag_report = {}
for t in TAGS:
    opens = re.findall(r'<'+t+r'(?:\s|>)', html)
    selfc = re.findall(r'<'+t+r'(?:\s[^>]*?)?/>', html)
    closes = re.findall(r'</'+t+r'>', html)
    n_open_all = len(opens)
    n_selfc = len(selfc)
    n_close = len(closes)
    balanced = (n_open_all - n_selfc) == n_close
    tag_report[t] = dict(open_total=n_open_all, self_close=n_selfc, close=n_close, balanced=balanced)
res['tag_balance'] = tag_report

viewboxes = re.findall(r'<svg[^>]*viewBox="([^"]+)"', html)
res['viewboxes'] = viewboxes
res['viewbox_ok'] = (viewboxes == ['0 0 880 2484', '0 0 880 944'])

def svg_spans(html):
    """return list of (viewbox, start_idx, end_idx) for each <svg>...</svg>"""
    out = []
    for m in re.finditer(r'<svg[^>]*viewBox="([^"]+)"', html):
        start = m.start()
        end = html.index('</svg>', start)
        out.append((m.group(1), start, end))
    return out

spans = svg_spans(html)

def path_max_y(d):
    toks = re.findall(r'([MLHVQCSTAZmlhqvqcstaz])|(-?\d+(?:\.\d+)?)', d)
    seq = []
    for cmd, num in toks:
        if cmd: seq.append((cmd, []))
        else:
            if not seq: seq.append(('M', []))
            seq[-1][1].append(float(num))
    maxy = None
    for cmd, nums in seq:
        c = cmd.upper()
        if c in ('M','L','T'):
            for i in range(1, len(nums), 2):
                y = nums[i]; maxy = y if maxy is None or y > maxy else maxy
        elif c == 'V':
            for n in nums:
                maxy = n if maxy is None or n > maxy else maxy
        elif c in ('Q','S'):
            for i in range(1, len(nums), 4):
                for y in (nums[i], nums[i+3] if i+3 < len(nums) else nums[i]):
                    maxy = y if maxy is None or y > maxy else maxy
            # end point y at offset 3
            for i in range(3, len(nums), 4):
                y = nums[i]; maxy = y if maxy is None or y > maxy else maxy
        elif c == 'C':
            for i in range(1, len(nums), 6):
                y = nums[i]; maxy = y if maxy is None or y > maxy else maxy
            for i in range(3, len(nums), 6):
                y = nums[i]; maxy = y if maxy is None or y > maxy else maxy
            for i in range(5, len(nums), 6):
                y = nums[i]; maxy = y if maxy is None or y > maxy else maxy
        elif c == 'H' or c == 'Z':
            pass
        elif c == 'A':
            for i in range(6, len(nums), 7):
                y = nums[i]; maxy = y if maxy is None or y > maxy else maxy
    return maxy

def region_max_y(seg):
    mx = 0; detail = {}
    # text y
    for m in re.finditer(r'\by="(-?\d+(?:\.\d+)?)"', seg):
        y = float(m.group(1)); mx = max(mx, y); detail.setdefault('text_y', []).append(y)
    # rect y and y+height
    for m in re.finditer(r'<rect\b[^>]*>', seg):
        rm = re.search(r'\by="(-?\d+(?:\.\d+)?)"', m.group(0))
        hm = re.search(r'\bheight="(-?\d+(?:\.\d+)?)"', m.group(0))
        if rm:
            y = float(rm.group(1)) + (float(hm.group(1)) if hm else 0)
            mx = max(mx, y); detail.setdefault('rect_bottom', []).append(y)
    # line y1/y2
    for m in re.finditer(r'\b(y1|y2)="(-?\d+(?:\.\d+)?)"', seg):
        y = float(m.group(2)); mx = max(mx, y); detail.setdefault('line_y', []).append(y)
    # path d
    for m in re.finditer(r'\bd="([^"]+)"', seg):
        y = path_max_y(m.group(1))
        if y is not None:
            mx = max(mx, y); detail.setdefault('path_y', []).append(y)
    return mx, {k: max(v) for k, v in detail.items()}

struct_regions = {}
for vb, s, e in spans:
    seg = html[s:e]
    mx, detail = region_max_y(seg)
    limit = 2468 if vb == '0 0 880 2484' else 928
    struct_regions[vb] = dict(maxY=mx, limit=limit, ok=mx <= limit, detail=detail)
res['maxY'] = struct_regions

# ---------- (2) href gate ----------
hrefs = re.findall(r'href="([^"]+\.html)"', html)
uniq = sorted(set(hrefs))
missing = [h for h in uniq if not os.path.exists(os.path.join(F01_DIR, h))]
new3 = ['采购管理/采购退货单列表.html','销售管理/销售退货单列表.html','财务协同/退款登记.html']
res['href'] = dict(
    total_href_occurrences=len(hrefs),
    unique_targets=len(uniq),
    missing=missing,
    new3={t: os.path.exists(os.path.join(F01_DIR, t)) for t in new3},
    unique_sorted=uniq,
)

# ---------- (3) grep gate ----------
grep_terms = {
    'v3.9': ('ge', 4),
    'v3.8 原型业务流程导航': ('eq', 0),
    '直发': ('ge', 5),
    '背靠背': ('ge', 2),
    'XNC-ZF': ('ge', 1),
    '采购退货': ('ge', 2),
    '销售退货': ('ge', 2),
    '退款': ('ge', 3),
    '67 个弹窗': ('eq', 0),
    '38 个页面': ('eq', 0),
    'Geist': ('eq', 0),
}
grep_report = {}
for term, (op, want) in grep_terms.items():
    n = html.count(term)
    ok = (n >= want) if op == 'ge' else (n == want)
    grep_report[term] = dict(count=n, rule=f"{op} {want}", ok=ok)
res['grep'] = grep_report

# ---------- (5) F02 <-> F01 reconciliation ----------
# spans: [0]=main, [1]=branch (viewbox asserted above)
main_seg = html[spans[0][1]:spans[0][2]]
branch_seg = html[spans[1][1]:spans[1][2]]

node_box_re = re.compile(r'<a href="[^"]*">\s*<rect\b')
main_nodes = len(node_box_re.findall(main_seg))
branch_nodes = len(node_box_re.findall(branch_seg))

a_total = len(re.findall(r'<a(?:\s|>)', html))

def uniq_targets(seg):
    return set(re.findall(r'href="([^"]+\.html)"', seg))
mu, bu = uniq_targets(main_seg), uniq_targets(branch_seg)
inter = sorted(mu & bu)

# SRC_DATA keys
src_m = re.search(r'var SRC_DATA\s*=\s*\{(.*?)\n\};', html, re.S)
src_body = src_m.group(1)
# top-level keys: lines starting with two-space indent then key:
src_keys = re.findall(r'^\s{2}([A-Za-z0-9_]+)\s*:\s*\{head:', src_body, re.M)

# 16px titles
main16 = len(re.findall(r'font-size="16"', main_seg))
branch16 = len(re.findall(r'font-size="16"', branch_seg))

# inline (non-node-box) <a> count = total - node boxes
inline_a = a_total - (main_nodes + branch_nodes)

f02_check = {
    'node_boxes': dict(main=main_nodes, branch=branch_nodes, total=main_nodes+branch_nodes,
                       f02_claim=(58,31,89)),
    'a_total': dict(actual=a_total, f02_claim=102),
    'inline_a': dict(actual=inline_a, f02_claim=13),
    'unique_targets': dict(main=len(mu), branch=len(bu), union=len(mu|bu), intersection=inter,
                           f02_claim=(25,30,49,6)),
    'src_data_keys': dict(actual=src_keys, f02_claim=['b1','l1','l2','l3','l4','t1','t2','fin']),
    'titles_16px': dict(main=main16, branch=branch16, total=main16+branch16,
                        f02_claim=(8,7,15)),
}
res['f02_reconcile'] = f02_check

# F02 forbidden strings outside section 8 (evolution history)
idx8 = f02.find('## 8.')
f02_before8 = f02[:idx8 if idx8 >= 0 else len(f02)]
f02_after8 = f02[idx8:] if idx8 >= 0 else ''
forbidden = ['组合出库列表','租赁管理/租入','租赁管理/归还','银行水单','盈亏报表','1280','v3.3']
res['f02_forbidden_outside_s8'] = {
    t: dict(count=f02_before8.count(t), ok=f02_before8.count(t)==0) for t in forbidden
}
res['f02_s8_found'] = idx8 >= 0
# sanity: also confirm forbidden words only live inside s8
res['f02_forbidden_inside_s8'] = {t: f02_after8.count(t) for t in forbidden}

# also verify F02 documents the claimed numbers itself (quotes present)
f02_claims_present = {
    '102 处 <a>': '102 处 `<a>`' in f02,
    '89 (58+31)': ('89' in f02 and '58＋支线 31' in f02),
    '唯一目标 49 (25+30·6)': ('唯一目标 49' in f02 and '主线区 25＋支线区 30' in f02),
    'viewBox 2484': '0 0 880 2484' in f02,
    'viewBox 944': '0 0 880 944' in f02,
    'SRC_DATA 8 键': 'SRC_DATA` 共 **8 键**' in f02,
    '16px 15 (8+7)': ('16' in f02 and '泳道/支线标题' in f02),
}
res['f02_claims_text'] = f02_claims_present

print(json.dumps(res, ensure_ascii=False, indent=1, default=str))
