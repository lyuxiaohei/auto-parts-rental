# -*- coding: utf-8 -*-
# ============================================================
# [脚本登记] 时期：2026-09-02 ~ 09-03 v2原型改造期
# 状态：已完成（GLM检查期校验）
# 归档于 2026-09-03。9/2 与 9/3 两次覆盖事故后，全部页面写入源
# 已清零：原型此后只能逐页手工维护，禁止任何脚本整页覆盖。
# ============================================================
"""GLM 修复终验：9 项验证"""
import os, re, glob, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
PROTO = 'P3-R01-包装租赁管理后台原型'
R = lambda rel: open(os.path.join(PROTO, rel), encoding='utf-8').read()

# 1. 采购入库列表「关联采购订单号」列
h = R('仓储作业/采购入库列表.html')
ok1 = '<th>关联采购订单号</th>' in h and 'PO-20260902-018' in h and h.index('<th>供应商</th>') < h.index('<th>关联采购订单号</th>') < h.index('<th>业务类型</th>')
print('【1】采购入库列表-关联采购订单号列（位于供应商与业务类型之间，7 行有值）:', '✅' if ok1 and h.count('<span class="lk">PO-') >= 7 else '❌')

# 2. 应收账单「销售费」行
h = R('财务协同/应收账单.html')
n_xs = h.count('销售费（按销售出库自动汇总）')
print(f'【2】应收账单-销售费类型行: {"✅" if n_xs >= 3 else "❌"}（{n_xs} 处，含弹窗提示）')

# 3. 组合出库「关联租赁单号」列 + 租赁单「出库」入口
h = R('仓储作业/组合出库列表.html')
ok3a = '<th>关联租赁单号</th>' in h and 'ZL-20260610-015' in h
h2 = R('包装管理/租赁单列表.html')
n_out = h2.count(">出库</a>")
ok3b = n_out >= 4 and "go('../仓储作业/组合出库列表.html')" in h2
print(f'【3】组合出库-关联租赁单号列: {"✅" if ok3a else "❌"} ｜ 租赁单行内出库链接: {"✅" if ok3b else "❌"}（{n_out} 处）')

# 4. 页面底部无游离表单残留
def modal_spans(html):
    spans = []
    for m in re.finditer(r'<div class="modal-overlay"', html):
        depth = 1
        for mm in re.finditer(r'<div|</div>', html[m.end():]):
            depth += 1 if mm.group(0) == '<div' else -1
            if depth == 0:
                spans.append((m.start(), m.end() + mm.end())); break
    return spans
stray_total = 0
for p in glob.glob(os.path.join(PROTO, '*', '*.html')):
    if os.sep + '弹窗' + os.sep in p: continue
    html = open(p, encoding='utf-8').read()
    spans = modal_spans(html)
    for mm in re.finditer(r'<div class="(form-row|modal-footer|dgrid)"', html):
        # 表单页的 form-row 是正常内容：排除 录单/录入/维护/BOM维护 页面
        rel = os.path.relpath(p, PROTO)
        if any(k in rel for k in ['录单', '录入', '维护']):
            continue
        if not any(s <= mm.start() < e for s, e in spans):
            stray_total += 1
            print(f'   ❌ 游离元素: {rel} 行{html.count(chr(10), 0, mm.start())+1}')
print(f'【4】页面无游离表单残留: {"✅" if stray_total == 0 else "❌"}（{stray_total} 处）')

# 5. 弹窗示例单号格式与列表一致
h = R('财务协同/开票登记.html') + R('财务协同/回款登记.html')
old_fmt = 'AR-202608-001' in h
new_fmt = 'AR-2026-08-PRJ2601' in h
print(f'【5】弹窗示例格式: {"✅" if (not old_fmt and new_fmt) else "❌"}（旧格式残留={old_fmt}，新格式存在={new_fmt}）')

# 6. 拆卸弹窗配比 = BOM（围板箱×1+围板×4+箱盖×1+锁扣×4+铰链×2）
h = R('仓储作业/拆卸管理列表.html')
bom = R('基础数据/BOM.html')
modal_seg = h[h.find('id="createModal"'):]
pairs = {'WBX-1210L': '1', 'LJ-C300': '4', 'LJ-D400': '1', 'LJ-A100': '4', 'LJ-B200': '2'}
ok6 = all(re.search(re.escape(code) + r'</span></td><td><span class="auto-cell">[^<]+</span></td><td><span class="auto-cell">[^<]+</span></td><td><span class="auto-cell">' + qty + r'</span>', modal_seg) for code, qty in pairs.items())
ok6b = '围板箱×1 + 围板×4 + 箱盖×1 + 锁扣×4 + 铰链×2' in bom
print(f'【6】拆卸弹窗配比=BOM（围板箱1/围板4/箱盖1/锁扣4/铰链2）: {"✅" if ok6 and ok6b else "❌"}')

# 7-9. 菜单一致性 / 死链 / 幽灵弹窗
pages = [p for p in glob.glob(os.path.join(PROTO, '*', '*.html')) if os.sep + '弹窗' + os.sep not in p]
seqs = set()
dead = 0
for p in pages:
    html = open(p, encoding='utf-8').read()
    m = re.search(r'<ul class="side-menu">(.*?)</ul>\s*<div class="side-foot">', html, re.S)
    seg = re.sub(r'<svg.*?</svg>', '', m.group(1), flags=re.S)
    seqs.add('|'.join(t.strip() for t in re.findall(r'>([^<>]+)<', seg) if t.strip()))
    for mm in re.finditer(r'''go\(\s*['"]([^'"]+)['"]''', html):
        u = mm.group(1)
        if not u.startswith(('http', '#')) and not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(p), u))):
            dead += 1
ghost = 0
for p in pages:
    html = open(p, encoding='utf-8').read()
    defs = set(re.findall(r'<div class="modal-overlay" id="([^"]+)"', html))
    refs = set(re.findall(r"openModal\('([^']+)'\)", html))
    ghost += len(refs - defs)
print(f'【7】菜单一致性: {"✅" if len(seqs) == 1 else "❌"}（唯一值 {len(seqs)}）')
print(f'【8】死链: {"✅" if dead == 0 else "❌"}（{dead}）')
print(f'【9】幽灵弹窗: {"✅" if ghost == 0 else "❌"}（{ghost}）')
