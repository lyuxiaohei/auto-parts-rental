# -*- coding: utf-8 -*-
"""G33 T8a 修复：新页 4 项审计问题清零
1) 三新列表页 + demo-data：详情 ops 改 onclick openRetDetail（页内脚本含 openModal('detailModal') 字面量）
2) 退款登记 资金方向 readonly input → 非输入展示框（页+模板双层）
3) g17_audit_diff.py：页数 117→128 + expect_appear +11 新文件
"""
import io, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'P3-R01-包装租赁管理后台原型', *a)

def rd(fp):
    with io.open(P(*fp.split('/')), encoding='utf-8') as f:
        return f.read()

def wr(fp, s):
    with io.open(P(*fp.split('/')), 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(s)

WRAPPER = '''
<script>
/* G33 详情弹窗接线：onclick 直达（含 openModal 字面量·审计触发器可见） */
function openRetDetail(entity, key) {
  if (typeof openGenericDetail === 'function') openGenericDetail(entity, key);
  openModal('detailModal');
}
</script>
'''

# ---------- 1) demo-data ops：detail:true → act ----------
DD = P('_data', 'demo-data.js')
src = io.open(DD, encoding='utf-8', newline='').read()
ENT_KEYS = {
    'purchaseReturns': ['CGTH-20260914-001', 'CGTH-20260912-002', 'CGTH-20260910-003'],
    'salesReturns': ['XSTH-20260913-001', 'XSTH-20260912-002', 'XSTH-20260911-003'],
    'refunds': ['TKD-20260914-001', 'TKD-20260913-002', 'TKD-20260912-003'],
}
n_fix = 0
for ent, keys in ENT_KEYS.items():
    for k in keys:
        anchor = "'" + k + "': {"
        ent_i = src.index(ent + ': {')
        i = src.index(anchor, ent_i)
        j = src.index("'row': ", i)
        j2 = src.index(chr(10), j)  # row 为单行 JSON
        seg = src[i:j2]
        Q = chr(39)
        assert seg.count('{"t": "详情", "detail": true}') == 1, (ent, k, seg.count('{"t": "详情", "detail": true}'))
        seg2 = seg.replace('{"t": "详情", "detail": true}',
                           '{"t": "详情", "act": "openRetDetail(' + Q + ent + Q + ', ' + Q + k + Q + ')"}')
        src = src[:i] + seg2 + src[j2:]
        n_fix += 1
io.open(DD, 'w', encoding='utf-8', newline='').write(src)
print('demo-data ops 改写:', n_fix, '行')

# ---------- 2) 三新列表页：静态行 + 包装脚本 + （退款）只读输入 ----------
PAGE_KEY = {
    '采购管理/采购退货单列表.html': ('purchaseReturns', ['CGTH-20260914-001', 'CGTH-20260912-002', 'CGTH-20260910-003']),
    '销售管理/销售退货单列表.html': ('salesReturns', ['XSTH-20260913-001', 'XSTH-20260912-002', 'XSTH-20260911-003']),
    '财务协同/退款登记.html': ('refunds', ['TKD-20260914-001', 'TKD-20260913-002', 'TKD-20260912-003']),
}
for fp, (ent, keys) in PAGE_KEY.items():
    s = rd(fp)
    n0 = s.count("openModal('detailModal')")
    # 静态行：每行 详情 的 onclick 改 openRetDetail（按行内单号配对）
    for k in keys:
        old = '<a onclick="openModal(\'detailModal\')">详情</a>'
        # 定位该行片段（以单号 lk 起，向后 800 字符内的第一个 详情 链接）
        pos = s.index('<span class="lk">' + k + '</span>')
        seg_end = s.index('</tr>', pos)
        seg = s[pos:seg_end]
        assert seg.count(old) == 1, (fp, k, seg.count(old))
        seg2 = seg.replace(old, '<a onclick="openRetDetail(\'%s\', \'%s\')">详情</a>' % (ent, k))
        s = s[:pos] + seg2 + s[seg_end:]
    # 插入包装脚本（置于 ?audit=1 脚本之前）
    marker = '<script>\n/* ?audit=1 自动打开审核弹窗（我的待办跳转支持） */'
    assert s.count(marker) == 1, fp
    s = s.replace(marker, WRAPPER + '\n' + marker)
    wr(fp, s)
    print(fp, '静态行详情 onclick 改写 %d + 包装脚本注入（残留 openModal(detailModal) %d）' % (n0, s.count("openModal('detailModal')") - 1))

# 退款页只读输入 → 展示框（页 + 模板双层）
OLD_IN = '<div class="input-box" style="width:350px;"><input class="auto" value="收款（供应商退回）" readonly></div>'
NEW_IN = '<div class="input-box" style="width:350px;background:#fafafa;color:#595959;">收款（供应商退回）</div>'
for fp in ['财务协同/退款登记.html', '财务协同/弹窗/退款登记新建.html']:
    s = rd(fp)
    assert s.count(OLD_IN) == 1, fp
    s = s.replace(OLD_IN, NEW_IN)
    wr(fp, s)
    print(fp, '资金方向只读输入 → 展示框')

# ---------- 3) g17_audit_diff.py 更新 ----------
fp = os.path.join(ROOT, '_scan_tmpdir', 'g17_audit_diff.py')
s = io.open(fp, encoding='utf-8').read()
s = s.replace(
    "expect_appear = set(RENAMES.values()) | {'P3-R01-A06-实体关系与状态机.html', '登录.html', '租赁管理/弹窗/退租入库新建.html', '基础数据/弹窗/客商开票资料.html', '基础数据/弹窗/客商收货信息.html'}",
    "expect_appear = set(RENAMES.values()) | {'P3-R01-A06-实体关系与状态机.html', '登录.html', '租赁管理/弹窗/退租入库新建.html', '基础数据/弹窗/客商开票资料.html', '基础数据/弹窗/客商收货信息.html'\n"
    "    # G33：+3 列表页+8 弹窗模板（退货退款闭环）\n"
    "    | {'采购管理/采购退货单列表.html', '采购管理/弹窗/新建采购退货单.html', '采购管理/弹窗/采购退货审核.html', '采购管理/弹窗/采购退货单详情.html',\n"
    "       '销售管理/销售退货单列表.html', '销售管理/弹窗/新建销售退货单.html', '销售管理/弹窗/销售退货审核.html', '销售管理/弹窗/销售退货单详情.html',\n"
    "       '财务协同/退款登记.html', '财务协同/弹窗/退款登记新建.html', '财务协同/弹窗/退款登记详情.html'}")
s = s.replace("ok = len(post) == 117 and len(base) == 113 and tot_dl == 0 and len(new_js) == 0 and len(new_probs) == 0 and mobile_ok and rename_ok  # G31: 115→117（+客商开票/收货两模板·A06 渲染页计入 PC 112）",
              "ok = len(post) == 128 and len(base) == 113 and tot_dl == 0 and len(new_js) == 0 and len(new_probs) == 0 and mobile_ok and rename_ok  # G33: 117→128（+3 列表页+8 弹窗模板·PC 123）")
s = s.replace("print('\\n==== audit 门：', 'PASS（117 页·死链0·JS0·diff 新增 0·mobile 5 页各自 0/0）====' if ok else 'FAIL ====')",
              "print('\\n==== audit 门：', 'PASS（128 页·死链0·JS0·diff 新增 0·mobile 5 页各自 0/0）====' if ok else 'FAIL ====')")
io.open(fp, 'w', encoding='utf-8', newline='').write(s)
print('g17_audit_diff.py 更新（128 页+11 新键）')
print('=== G33 T8a 修复完成 ===')
