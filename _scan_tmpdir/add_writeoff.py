# -*- coding: utf-8 -*-
"""A1-A5 赔偿减库存落地（09-05 王琳总需求，道远拍板：审核即核销；丢失件自客户态出账不走在库）
双层同步：页面内嵌 modal + 弹窗/ 独立模板。"""
import re
from pathlib import Path

ROOT = Path(r"P3-R01-包装租赁管理后台原型")

def edit(rel, pairs):
    p = ROOT / rel
    src = p.read_text(encoding="utf-8")
    done = [new for _, new in pairs if new in src]
    pairs = [(o, n) for o, n in pairs if n not in done]
    if not pairs:
        print(f"SKIP {rel}（幂等，已应用）"); return
    for old, new in pairs:
        c = src.count(old)
        assert c == 1, f"[{rel}] {c}!=1: {old[:50]!r}"
        src = src.replace(old, new)
    p.write_text(src, encoding="utf-8", newline="")
    print(f"OK {rel}（{len(pairs)} 处）")

def edit_re(rel, pat, repl, idem=None):
    p = ROOT / rel
    src = p.read_text(encoding="utf-8")
    if idem and idem in src:
        print(f"SKIP {rel}（幂等）"); return
    new, n = re.subn(pat, repl, src)
    assert n == 1, f"[{rel}] re {n}!=1"
    p.write_text(new, encoding="utf-8", newline="")
    print(f"OK {rel}（正则 1 处）")

TIP_HTML = '<div class="form-row"><span class="form-label"></span><div style="font-size:12px;color:#fa8c16;line-height:1.7;">通过后自动核销库存：缺失/报废件生成「其他出库单（赔偿核销）」账面扣减；丢失件自客户态直接出账，不回在库。</div></div>'
AUDIT_TIP_RE = (r'(placeholder="选填，驳回时建议填写原因"></div>\s*</div>)',
                lambda m: m.group(1) + '\n      ' + TIP_HTML)
CHAIN_TAIL = ('<div class="node"><div class="n-role">应付账单</div><div class="n-name"><span class="lk" onclick="go(\'../财务协同/应付账单.html\')">转应付（对运营方赔付）</span></div></div>',
              '<div class="node"><div class="n-role">应付账单</div><div class="n-name"><span class="lk" onclick="go(\'../财务协同/应付账单.html\')">转应付（对运营方赔付）</span></div></div><span class="link-arrow">→</span><div class="node"><div class="n-role">库存核销</div><div class="n-name"><span class="lk" onclick="go(\'../仓储作业/其他出库列表.html\')">其他出库 · 赔偿核销</span></div></div>')
TL_OFF = ('<div class="tl-i off"><span class="tl-t">—</span>待审核 · 通过后转应付账单（无中间结算环节）</div>',
          '<div class="tl-i off"><span class="tl-t">—</span>待审核 · 通过后转应付账单并自动核销库存（丢失/损失件出账 → 其他出库·赔偿核销）</div>')

# ── A1/A3 丢损赔偿单（内嵌）
edit_re("包装管理/丢损赔偿单.html", AUDIT_TIP_RE[0], AUDIT_TIP_RE[1], idem="通过后自动核销库存：缺失")
_p = ROOT / "包装管理/丢损赔偿单.html"
_s = _p.read_text(encoding="utf-8")
if '<div class="pn-hint">' not in _s:
    _m = _s.find('<div class="modal-overlay"')
    assert _m > 0
    _s = _s[:_m] + '<div class="pn-hint">赔偿单审核通过后自动核销库存——缺失/报废件生成「其他出库单（赔偿核销）」，账面同步扣减；丢失件自客户态直接出账（09-05 拍板：审核即核销）。</div>\n\n' + _s[_m:]
    _p.write_text(_s, encoding="utf-8", newline="")
    print("OK 包装管理/丢损赔偿单.html（pn-hint 插入）")
else:
    print("SKIP pn-hint（幂等）")
edit("包装管理/丢损赔偿单.html", [CHAIN_TAIL, TL_OFF])

# ── 双层同步：独立模板（相对路径多一级 ../../）
CHAIN_TAIL_M = (CHAIN_TAIL[0].replace("'../财务协同/", "'../../财务协同/"),
                CHAIN_TAIL[1].replace("'../财务协同/", "'../../财务协同/").replace("'../仓储作业/", "'../../仓储作业/"))
edit("包装管理/弹窗/丢损赔偿单详情.html", [CHAIN_TAIL_M, TL_OFF])
edit_re("包装管理/弹窗/丢损赔偿审核.html", AUDIT_TIP_RE[0], AUDIT_TIP_RE[1], idem="通过后自动核销库存：缺失")

# ── A2 其他出库列表：类型 + 示例行
edit("仓储作业/其他出库列表.html", [
    ('<option>报废</option><option>盘亏</option><option>其他</option>',
     '<option>报废</option><option>盘亏</option><option>赔偿核销</option><option>其他</option>'),
])
edit_re("仓储作业/其他出库列表.html", r'(\s*<tr>\s*<td><input type="checkbox" class="cb"></td>\s*<td><span class="lk">QTCK-20260901-004)',
        lambda m: '\n      <tr> <td><input type="checkbox" class="cb"></td> <td><span class="lk">QTCK-20260905-005</span></td> <td><span class="tag tag-blue">赔偿核销</span></td> <td>GB-800 隔板 · 关联赔偿单 <span class="lk">BS-20260902-010</span>（丢失 1 套自客户态出账）</td> <td><span class="td-num">1 套</span></td> <td>—</td> <td>2026-09-05</td> <td><span class="tag tag-green">已出库</span></td> <td><span class="ops"><a onclick="openModal(\'detailModal\')">详情</a></span></td> </tr>' + m.group(1),
        idem="QTCK-20260905-005")

# ── A4 F01：T1 赔偿支右注 + S4 注记
edit("P3-R01-F01-业务流程导航图.html", [
    ('自有 → 应收（客户赔）· 租入 → 应付（运营方赔）· 详见 S4',
     '自有 → 应收（客户赔）· 租入 → 应付（运营方赔）· 审核即核销库存 · 详见 S4'),
    ('口径：按对象直接转单据，无中间结算环节',
     '口径：按对象直接转单据，无中间结算环节；审核即核销库存（其他出库 · 赔偿核销，09-05 王琳总）'),
])

# ── A5 A04：赔偿 pin note 追加核销口径
p = ROOT / "P3-R01-A04-流程链标注数据.json"
j = p.read_text(encoding="utf-8")
old = '"note": "自有器具缺损：对客户的赔偿转应收账单（操作列「转应收」）。'
new = '"note": "自有器具缺损：对客户的赔偿转应收账单（操作列「转应收」）；审核通过自动核销库存（其他出库·赔偿核销，丢失件自客户态出账）。'
assert j.count(old) == 1
j = j.replace(old, new)
import json; json.loads(j)
p.write_text(j, encoding="utf-8", newline="")
print("OK A04 json")

# 自检：核心探针
for rel, probes in [
    ("包装管理/丢损赔偿单.html", ["审核即核销", "其他出库 · 赔偿核销", "库存核销"]),
    ("包装管理/弹窗/丢损赔偿单详情.html", ["库存核销", "赔偿核销）"]),
    ("仓储作业/其他出库列表.html", ["赔偿核销", "QTCK-20260905-005", "BS-20260902-010"]),
    ("P3-R01-F01-业务流程导航图.html", ["审核即核销库存"]),
]:
    s = (ROOT / rel).read_text(encoding="utf-8")
    for pr in probes:
        assert pr in s, (rel, pr)
print("全探针通过")
