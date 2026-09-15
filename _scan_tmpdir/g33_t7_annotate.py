# -*- coding: utf-8 -*-
"""G33 T7: 标注层与文档
- A03/A04 JSON 为三新页补键
- annotate.py 双轮重注入（A03 先→A04 后·G18 惯例），收集告警
- A02 对照表 v5 增订（菜单树/清单/弹窗统计/页数口径 117→128）
- A05 字段字典（头部统计+G33 登记块·三实体字段行）
"""
import io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'P3-R01-包装租赁管理后台原型')
ANN = r'C:\Users\Administrator\.zcode\skills\原型标注\scripts\annotate.py'

def rj(fp):
    with io.open(fp, encoding='utf-8') as f:
        return json.load(f)

def wj(fp, obj):
    with io.open(fp, 'w', encoding='utf-8', newline='') as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=2))
    # EOL 归一 CRLF（与仓库 HTML 一致）
    with io.open(fp, encoding='utf-8', newline='') as f:
        s = f.read()
    if '\r\n' not in s:
        with io.open(fp, 'w', encoding='utf-8', newline='') as f:
            f.write(s.replace('\n', '\r\n'))

# ================= A03 +3 键 =================
A3 = os.path.join(P, 'P3-R01-A03-标注数据.json')
a3 = rj(A3)
assert '采购管理/采购退货单列表.html' not in a3
a3['采购管理/采购退货单列表.html'] = [
    {"id": 1, "selector": "<h3 class=\"card-title\">采购退货单</h3>", "title": "采购退货单（方案 B）",
     "note": "双退货单之一：收货拒收（未入库直接退·不产生库存流水）／入库后退货（已入库再退·凭退货单自身冲减，不修改原入库单 D-109）。审核后可登记应付退款（对供应商）。",
     "fp": "", "req": ""},
    {"id": 2, "selector": "<button class=\"btn btn-sm\" onclick=\"openModal('createModal')\">新建退货单</button>", "title": "新建退货单",
     "note": "选择关联原单（采购入库单）自动带出物料行与可退上限；退货类型两值（THC 字典）。", "fp": "", "req": ""},
]
a3['销售管理/销售退货单列表.html'] = [
    {"id": 1, "selector": "<h3 class=\"card-title\">销售退货单</h3>", "title": "销售退货单（方案 B）",
     "note": "客户退货统一单据：收货拒收（客户未收货直接退回）／入库后退货（客户收货使用后退货回仓）。审核后可登记应收退款（对客户）。",
     "fp": "", "req": ""},
    {"id": 2, "selector": "<button class=\"btn btn-sm\" onclick=\"openModal('createModal')\">新建退货单</button>", "title": "新建退货单",
     "note": "选择关联销售出库单自动带出物料行与可退上限。", "fp": "", "req": ""},
]
a3['财务协同/退款登记.html'] = [
    {"id": 1, "selector": "<h3 class=\"card-title\">退款登记</h3>", "title": "退款登记（一页双向）",
     "note": "退款从核销散记升级为独立可查可审单据（G32-T1 方案 B·D-123）。方向映射固定：采购退货→应付退款（对供应商·收款）；销售退货→应收退款（对客户·付款）。「供应商应收」既有行（AR-20260904-015·赔付用途）不动。",
     "fp": "", "req": ""},
    {"id": 2, "selector": "<button class=\"btn btn-sm\" onclick=\"openModal('createModal')\">新建退款单</button>", "title": "新建退款单",
     "note": "退款类型（TKL 字典）决定往来单位方向与资金方向；关联退货单带出可退金额。", "fp": "", "req": ""},
]
wj(A3, a3)
print('A03 keys:', len(a3) - 1)

# ================= A04 +3 键 =================
A4 = os.path.join(P, 'P3-R01-A04-流程链标注数据.json')
a4 = rj(A4)
assert '采购管理/采购退货单列表.html' not in a4
a4['采购管理/采购退货单列表.html'] = [
    {"id": 1, "selector": "<td><span class=\"lk\">CGTH-20260912-002</span></td>",
     "title": "B1 采购线 · 退货支线（方案 B·D-123）",
     "note": "上一步 ← 采购入库（收货拒收行未入库直接退）。\n方向映射固定：采购退货 → 应付退款（对供应商·我方收款）。\n下一步 → 退款登记（TKD-）→ 到账确认。"},
]
a4['销售管理/销售退货单列表.html'] = [
    {"id": 1, "selector": "<td><span class=\"lk\">XSTH-20260913-001</span></td>",
     "title": "B2 销售线 · 退货支线（方案 B·D-123）",
     "note": "上一步 ← 销售出库（客户拒收或收货后退货回仓）。\n方向映射固定：销售退货 → 应收退款（对客户·我方付款）。\n下一步 → 退款登记（TKD-）→ 退款付讫。"},
]
a4['财务协同/退款登记.html'] = [
    {"id": 1, "selector": "<td><span class=\"lk\">TKD-20260914-001</span></td>",
     "title": "财务线 · 退款登记（方案 B 独立单据）",
     "note": "退货退款闭环的落账端：应付退款=收款（供应商退回）／应收退款=付款（退回客户）。\n与付款登记/收款确认按科目侧命名互不冲突（应付/应收各自成单）。"},
]
wj(A4, a4)
print('A04 keys:', len(a4) - 1)

# ================= 双轮注入 =================
for layer, jf in [('A03', A3), ('A04', A4)]:
    r = subprocess.run([sys.executable, ANN, '--pages', P, '--data', jf], capture_output=True, text=True, encoding='utf-8')
    out = (r.stdout or '') + (r.stderr or '')
    print('=== annotate %s exit %d ===' % (layer, r.returncode))
    print(out[-1500:] if len(out) > 1500 else out)
    assert r.returncode == 0, layer + ' 注入失败'

# 告警 0 自检（输出含 warn/未命中字样即失败）
combined = ''
for layer, jf in [('A03', A3), ('A04', A4)]:
    r = subprocess.run([sys.executable, ANN, '--pages', P, '--data', jf], capture_output=True, text=True, encoding='utf-8')
    combined += (r.stdout or '') + (r.stderr or '')
bad = [l for l in combined.splitlines() if ('warn' in l.lower() or '未命中' in l or 'miss' in l.lower())]
print('告警行数:', len(bad))
for l in bad[:10]:
    print('WARN:', l)

# 新页 pin 在位检查
for fp in ['采购管理/采购退货单列表.html', '销售管理/销售退货单列表.html', '财务协同/退款登记.html']:
    with io.open(os.path.join(P, *fp.split('/')), encoding='utf-8') as f:
        s = f.read()
    print(fp, 'data-note:', s.count('data-note='), '| proto-pin:', s.count('class="proto-pin"'), '| fab:', s.count('protoNotesFab'))
print('=== G33 T7 注入完成 ===')
