# -*- coding: utf-8 -*-
"""G36 优化：按 admin-ui-spec/form.md 参照 采购管理/采购订单新建.html 规范化 20 个表单页 + 17 个审核页

T1 标签 <span class="form-label"> → <div class="form-label"> 并补全角冒号
T2 下拉箭头 <span class="caret"><svg…></svg></span> → <span class="caret">▾</span>
T3 备注行 → 样板形态（.input-box 外壳 + textarea min-height:72px + 顶部对齐；位置归到表单卡末尾）
T4 控件宽内联化：补 width:380px，删页级 <style>.form-row .input-box{width:380px;}</style> 覆盖
T5 日期字段 → <input type="date">（带 value）
T6 170px 日期控件归一为 380（起租日期单控件 / 合同起止复合 380 框）
T7 审核页删顶部「返回列表」（提交条「取消」已承担返回）
"""
import io, os, re, sys

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

FORM_PAGES = [
    '采购管理/采购退货新建.html',
    '销售管理/销售订单新建.html', '销售管理/销售出库新建.html', '销售管理/销售退货新建.html',
    '租赁管理/租赁单新建.html', '租赁管理/退租入库新建.html',
    '租入管理/租入单新建.html', '租入管理/租入归还新建.html',
    '仓储作业/其他入库新建.html', '仓储作业/其他出库新建.html', '仓储作业/调拨新建.html',
    '财务协同/付款新建.html', '财务协同/应付新建.html', '财务协同/应收生成.html',
    '财务协同/开票新建.html', '财务协同/收款新建.html', '财务协同/退款新建.html',
    '系统管理/字典项新建.html', '系统管理/用户新建.html', '系统管理/角色新建.html',
]
AUDIT_PAGES = [
    '采购管理/采购订单审核.html', '采购管理/采购入库审核.html', '采购管理/采购退货审核.html',
    '销售管理/销售订单审核.html', '销售管理/销售出库审核.html', '销售管理/销售退货审核.html',
    '租赁管理/租赁单审核.html', '租赁管理/租赁出库确认.html', '租赁管理/退租入库审核.html',
    '租入管理/租入单审核.html', '租入管理/租入入库确认.html', '租入管理/租入归还审核.html',
    '仓储作业/其他入库审核.html', '仓储作业/其他出库审核.html', '仓储作业/盘点审核.html', '仓储作业/调拨审核.html',
    '财务协同/付款确认.html',
]
# 备注字段 label 文本（保留业务语义）
DATE_MINUS = ['2026-09-03', '2027-09-02']  # 起租日期/框架起止示例值

def rd(p):
    return io.open(os.path.join(ROOT, p), encoding='utf-8', newline='').read()

def wr(p, s):
    io.open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='').write(s)

def row_spans(s):
    """返回所有 <div class="form-row"…>…</div> 的 (start, end)（深度扫描）"""
    out = []
    for m in re.finditer(r'<div class="form-row"', s):
        i = m.start(); depth = 0; j = i
        while j < len(s):
            mo = re.compile(r'<div\b|</div>').search(s, j)
            if not mo:
                break
            if mo.group(0) == '</div>':
                depth -= 1
                if depth == 0:
                    out.append((i, mo.end()))
                    break
            else:
                depth += 1
            j = mo.end()
    return out

def label_text(block):
    m = re.search(r'<(?:span|div) class="form-label"[^>]*>((?:<span[^>]*>[^<]*</span>|[^<])*)</(?:span|div)>', block)
    if not m:
        return ''
    return re.sub(r'<[^>]+>', '', m.group(1)).strip()

NOTE_TPL = ('<div class="form-row" style="align-items:flex-start;">\r\n'
            '        <div class="form-label" style="padding-top:6px;">{label}</div>\r\n'
            '        <div>\r\n'
            '          <div class="input-box" style="width:380px;height:auto;padding:6px 11px;"><textarea placeholder="{ph}" style="width:100%;border:none;outline:none;background:transparent;font:inherit;color:inherit;resize:vertical;min-height:72px;line-height:1.6;"></textarea></div>\r\n'
            '        </div>\r\n'
            '      </div>')

def fix_form_page(p):
    s = rd(p); log = []
    # ------ T1 标签 ------
    def _lbl(m):
        inner = m.group(1)
        txt = re.sub(r'<[^>]+>', '', inner).rstrip()
        if not txt.endswith('：') and not txt.endswith(':'):
            inner = inner + '：'
            return '<div class="form-label">' + inner + '</div>'
        return '<div class="form-label">' + inner + '</div>'
    n1 = len(re.findall(r'<span class="form-label">', s))
    s = re.sub(r'<span class="form-label">((?:<span[^>]*>[^<]*</span>|[^<])*)</span>', _lbl, s)
    assert '<span class="form-label">' not in s, p + ' 仍有 span 标签'
    log.append('标签 div 化+补冒号 ×%d' % n1)
    # ------ T2 箭头 ------
    n2 = len(re.findall(r'<span class="caret"><svg', s))
    s = re.sub(r'<span class="caret"><svg[^>]*>.*?</svg></span>', '<span class="caret">▾</span>', s, flags=re.S)
    log.append('箭头 svg→▾ ×%d' % n2)

    # ------ T5/T6 日期 ------
    n5 = 0
    spans = row_spans(s)
    for (a, b) in reversed(spans):
        blk = s[a:b]
        lbl = label_text(blk)
        if ('日期' not in lbl) and ('到期日' not in lbl) and ('合同起止' not in lbl) and ('起租' not in lbl):
            continue
        nb = blk
        # 170px 单独日期控件 → 380
        if 'width:170px' in nb and '合同起止' not in lbl:
            nb = re.sub(r'<div class="input-box" style="width:170px"><input[^>]*></div>',
                        '<div class="input-box" style="width:380px;"><input type="date" value="%s"></div>' % DATE_MINUS[0], nb)
        # 合同起止 两个 170 → 单个 380 复合框
        if '合同起止' in lbl and 'width:170px' in nb:
            nb = re.sub(r'<div style="display:flex;gap:10px">.*?</div>\s*</div>',
                        '<div class="input-box" style="width:380px;gap:8px;"><input type="date" value="%s"><span style="color:var(--text-3)">~</span><input type="date" value="%s"></div>' % (DATE_MINUS[0], DATE_MINUS[1]),
                        nb, flags=re.S)
        # 文本日期 input → type=date（去 placeholder、保 value）
        def _dt(mm):
            tag = mm.group(0)
            if 'type="date"' in tag:
                return tag
            tag2 = re.sub(r'\s+placeholder="[^"]*"', '', tag)
            return tag2.replace('<input', '<input type="date"', 1)
        nb2 = re.sub(r'<input[^>]*>', _dt, nb)
        if nb2 != blk:
            n5 += 1
            s = s[:a] + nb2 + s[b:]
    log.append('日期控件 type=date ×%d 行' % n5)

    # ------ T3 备注 ------
    spans = row_spans(s)
    note_idx = None
    for idx, (a, b) in enumerate(spans):
        if '备注' in label_text(s[a:b]):
            note_idx = idx
            break
    if note_idx is not None:
        a, b = spans[note_idx]
        blk = s[a:b]
        ph = '选填'
        m = re.search(r'placeholder="([^"]*)"', blk)
        if m:
            ph = m.group(1)
        lbl = label_text(blk)
        newrow = NOTE_TPL.format(label=lbl, ph=ph)
        s = s[:a] + s[a:a] + newrow + s[b:]  # 先原位替换
        # 位置：若后面仍有 form-row，则把备注行移到最后一个 form-row 之后
        spans2 = row_spans(s)
        cur = None
        for idx, (a2, b2) in enumerate(spans2):
            if '备注' in label_text(s[a2:b2]):
                cur = idx
                break
        if cur is not None and cur != len(spans2) - 1:
            a2, b2 = spans2[cur]
            row = s[a2:b2]
            s = s[:a2] + s[b2:]
            spans3 = row_spans(s)
            a3, b3 = spans3[-1]
            s = s[:b3] + '\r\n      ' + row.strip() + s[b3:]
            log.append('备注行移至表单卡末尾（原第 %d/%d 行）' % (cur + 1, len(spans2)))
        log.append('备注 → textarea 样板形态')

    # ------ T4 控件宽 ------
    def _w(m):
        cls, rest = m.group(1), m.group(2)
        if 'width:' in rest:
            return m.group(0)
        if 'style="' in rest:
            return '<div class="%s"%s>' % (cls, rest.replace('style="', 'style="width:380px;', 1))
        return '<div class="%s" style="width:380px;"%s>' % (cls, rest)
    n4 = len(re.findall(r'<div class="(?:select-box input-box|input-box(?: select-box)?)"[^>]*>', s))
    s = re.sub(r'<div class="(select-box input-box|input-box(?: select-box)?)"([^>]*)>', _w, s)
    # 类序归一为样板 input-box select-box
    s = s.replace('<div class="select-box input-box"', '<div class="input-box select-box"')
    # 删页级覆盖
    n4b = len(re.findall(r'<style>\.form-row \.input-box\{width:380px;\}</style>\r?\n?', s))
    s = re.sub(r'<style>\.form-row \.input-box\{width:380px;\}</style>\r?\n?', '', s)
    assert '.form-row .input-box{width:380px;}' not in s
    log.append('控件宽内联 ×%d（含 0 宽补）· 删页级覆盖 ×%d' % (n4, n4b))

    # 校验
    assert '<span class="caret"><svg' not in s
    assert 'width:170px' not in s, p + ' 仍有 170px 控件'
    wr(p, s)
    return log

def fix_audit_page(p):
    s = rd(p); log = []
    pat = r'\s*<div class="head-btns"><button class="btn btn-default btn-sm" onclick="go\(\'[^\']*\'\)">返回列表</button></div>'
    n = len(re.findall(pat, s))
    assert n == 1, '%s 返回列表数=%d' % (p, n)
    s = re.sub(pat, '', s)
    assert '返回列表' not in s, p + ' 仍有返回列表'
    wr(p, s)
    log.append('删顶部「返回列表」×1（提交条取消已承担返回）')
    return log

print('==== 表单页（20）====')
for p in FORM_PAGES:
    for l in fix_form_page(p):
        print('  %-28s %s' % (p.split('/')[-1], l))
print()
print('==== 审核页（17）====')
for p in AUDIT_PAGES:
    for l in fix_audit_page(p):
        print('  %-28s %s' % (p.split('/')[-1], l))
print()
print('DONE')
