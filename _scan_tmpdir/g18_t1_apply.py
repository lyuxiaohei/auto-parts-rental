# -*- coding: utf-8 -*-
"""G18 T1：A 类 10 条说明文字清理（页面本体删行）+ A03 加标注条目。
用法：python g18_t1_apply.py           # dry-run（assert 计数）
      python g18_t1_apply.py --apply   # 写回
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROT = ROOT/'P3-R01-包装租赁管理后台原型'
A03 = PROT/'P3-R01-A03-标注数据.json'
APPLY = '--apply' in sys.argv

# ---------- 1) 页面本体删除（精确替换，各 1 次） ----------
NOTE_UPDOWN = '<div style="font-size:12px;color:#8c8c8c;margin:10px 0 0;line-height:1.7;">上下游支持一对多/多对多（2026-09-08 王总提出，2026-09-11 落地）：单项目可绑定多家供应商（勾选，含租入/采购角色），新建租入单/采购订单时按项目带出候选供应商。</div>'
NOTE_AUDIT = '<div style="font-size:12px;color:#8c8c8c;padding-top:6px;line-height:1.7;">勾选该角色可审核的单据类型；各审核弹窗「审核人（按角色匹配）」据此匹配（G13 · 纪要十.1）。</div>'

DELS = [
    # (文件, 旧串, 新串)
    ('仓储作业/库存调拨列表.html',
     '</div><div class="pn-hint" style="padding:0 4px;">第一期仅支持同仓群内的库位调拨，不做调拨在途管理；调拨审核通过后即时完成库存转移。</div>',
     '</div>'),
    ('财务协同/银行水单核销.html',
     '    <div class="mini-note">单据金额取自应收账单 / 丢损赔偿单；勾选两侧后点击「生成核销记录」，系统按回单未核销金额与单据未核销金额取小核销。</div>\n',
     ''),
    ('财务协同/应付账单.html',
     '</div><div class="pn-hint" style="padding:0 4px;">应付账单可由采购入库单审核后自动生成（第一期支持手动创建）；租入业务（路凯）按周期生成应付账单。</div>',
     '</div>'),
    ('项目管理/项目档案.html', '    ' + NOTE_UPDOWN + '\n', ''),
    ('项目管理/项目详情.html', '    ' + NOTE_UPDOWN + '\n', ''),
    ('项目管理/弹窗/上下游绑定.html', '    ' + NOTE_UPDOWN + '\n', ''),
    ('系统管理/角色管理.html', '      ' + NOTE_AUDIT + '\n', ''),
    ('系统管理/弹窗/权限配置.html', '      ' + NOTE_AUDIT + '\n', ''),
    ('租赁管理/弹窗/租入单新建.html',
     '  <div style="margin-top:6px;font-size:12px;color:#8c8c8c;">计费＝月租金 + 按套数单价（无日租金，2026-09-08 会议）；应付生成方式取决于租入单模式（静态租入 / 背靠背）。</div>\n',
     ''),
    ('租赁管理/弹窗/租赁单新建.html',
     '  <div class="form-row">\n    <span class="form-label"></span>\n    <div style="font-size:12px;color:#8c8c8c;line-height:1.7;">押金为设计预留字段——两次会议均未涉及，收退与计价商务口径待客户确认（F01 财务通道注记同步）</div>\n  </div><div class="form-row">',
     '  <div class="form-row">'),
]

# ---------- 2) A03 新增条目 ----------
def E(id, sel, title, note, fp, req):
    return {'id': id, 'selector': sel, 'title': title, 'note': note, 'fp': fp, 'req': req}

SEL_UPDOWN = '<h3 class="modal-title">项目上下游绑定</h3>'
SEL_ROLE = '<h3 class="modal-title"><span id="rolePermTitle">权限配置 · 系统管理员</span></h3>'
N_UPDOWN = '上下游支持一对多/多对多（2026-09-08 王总提出，2026-09-11 落地）：单项目可绑定多家供应商（勾选，含租入/采购角色），新建租入单/采购订单时按项目带出候选供应商。'
N_AUDIT = '勾选该角色可审核的单据类型；各审核弹窗「审核人（按角色匹配）」据此匹配（G13 · 纪要十.1）。'
ADDS = {
    '仓储作业/库存调拨列表.html': [E(1, '<h3 class="card-title">库存调拨单</h3>', '调拨范围与生效口径',
        '第一期仅支持同仓群内的库位调拨，不做调拨在途管理；调拨审核通过后即时完成库存转移。', 'FP3-06', 'REQ-06')],
    '财务协同/银行水单核销.html': [E(4, '<h3 class="card-title">② 待核销单据</h3>', '核销金额口径',
        '单据金额取自应收账单 / 丢损赔偿单；勾选两侧后点击「生成核销记录」，系统按回单未核销金额与单据未核销金额取小核销。', 'FP6-04', 'REQ-09')],
    '财务协同/应付账单.html': [E(1, '<h3 class="card-title">应付账单</h3>', '应付账单生成方式',
        '应付账单可由采购入库单审核后自动生成（第一期支持手动创建）；租入业务（路凯）按周期生成应付账单。', 'FP4-02', 'REQ-03')],
    '项目管理/项目档案.html': [E(4, SEL_UPDOWN, '上下游绑定关系口径', N_UPDOWN, 'FP2-02', 'REQ-01')],
    '项目管理/项目详情.html': [E(3, SEL_UPDOWN, '上下游绑定关系口径', N_UPDOWN, 'FP2-02', 'REQ-01')],
    '项目管理/弹窗/上下游绑定.html': [E(1, SEL_UPDOWN, '上下游绑定关系口径', N_UPDOWN, 'FP2-02', 'REQ-01')],
    '系统管理/角色管理.html': [E(1, SEL_ROLE, '可审单据与审核人匹配', N_AUDIT, 'FP7-01', 'REQ-01')],
    '系统管理/弹窗/权限配置.html': [E(1, SEL_ROLE, '可审单据与审核人匹配', N_AUDIT, 'FP7-01', 'REQ-01')],
    '租赁管理/弹窗/租入单新建.html': [E(1, '<th>计费方式</th>', '租入计费口径',
        '计费＝月租金 + 按套数单价（无日租金，2026-09-08 会议）；应付生成方式取决于租入单模式（静态租入 / 背靠背）。', 'FP4-02', 'REQ-03')],
    '租赁管理/弹窗/租赁单新建.html': [E(1, '<span class="form-label">押金(元)</span>', '押金=设计预留字段',
        '押金为设计预留字段——两次会议均未涉及，收退与计价商务口径待客户确认（F01 财务通道注记同步）', 'FP4-02', 'REQ-03')],
}

# ---------- 执行 ----------
fail = 0
print(f"=== T1 {'APPLY' if APPLY else 'DRY-RUN'} ===")
for f, old, new in DELS:
    p = PROT/f
    s = p.read_text(encoding='utf-8')
    n = s.count(old)
    ok = (n == 1)
    print(f"[{'PASS' if ok else 'FAIL'}] 删除 {f}: 命中 {n}/1")
    if not ok:
        fail += 1
        continue
    if APPLY:
        p.write_text(s.replace(old, new, 1), encoding='utf-8')

d = json.loads(A03.read_text(encoding='utf-8'))
for k, items in ADDS.items():
    cur = d.get(k, [])
    ids = [e['id'] for e in cur]
    dup = [e['id'] for e in items if e['id'] in ids]
    # selector 唯一性（在删除后的干净页面上）
    p = PROT/k
    s = p.read_text(encoding='utf-8') if p.exists() else ''
    for e in items:
        c = s.count(e['selector'])
        st = 'PASS' if c == 1 else 'FAIL'
        if c != 1:
            fail += 1
        print(f"[{st}] A03 {k} +id={e['id']} selector 命中 {c}/1: {e['selector'][:40]}")
    if not dup and APPLY:
        d[k] = cur + items
if APPLY and not fail:
    d['_meta']['date'] = d['_meta'].get('date', '') + '；2026-09-12 G18：A 类 10 处说明文字清理转标注层（页面本体删说明行，口径说明由标注便签承载）'
    A03.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    json.loads(A03.read_text(encoding='utf-8'))
    print('A03 写回 + json.load 校验 OK（条目总数=%d）' % sum(len(v) for k, v in d.items() if k != '_meta'))
# 标签配平自检（改后页面）
if APPLY:
    import re
    for f, _, _ in DELS:
        s = (PROT/f).read_text(encoding='utf-8')
        o, c = len(re.findall(r'<div\b', s)), len(re.findall(r'</div>', s))
        print(f"[{'PASS' if o == c else 'WARN'}] 配平 {f}: div {o}/{c}")
print(f"=== 结果: {'FAIL=' + str(fail) if fail else 'ALL PASS'} ===")
sys.exit(1 if fail else 0)
