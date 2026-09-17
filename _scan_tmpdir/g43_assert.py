# -*- coding: utf-8 -*-
"""
G43 验证门 3 · 逐组断言：页面运行时 option 文本集合 = 运行时字典/实体值集合。
期望值由页面 evaluate 内独立遍历 DEMO_DATA 计算（不经 SSEL 函数·避免自证）。
白名单：全部 / 其他（演示） / 其他终端用户。输出逐行 [PASS/FAIL]。
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent / "P3-R01-包装租赁管理后台原型"

# 独立期望计算 JS（页面上下文·遍历 DEMO_DATA 原始结构）
JS_EXPECT = r"""
(mode, a, b, c) => {
  const D = window.DEMO_DATA || {};
  const out = [];
  if (mode === 'dict') { // a=组名 b=only 子集(可空)
    const it = D.dictItems || {};
    Object.keys(it).filter(k => {
      const f = (it[k].row || {}).fields || {};
      return f.category === a && f.status !== '停用';
    }).sort().forEach(k => {
      const n = ((it[k].row || {}).fields || {}).name;
      if (n && (!b || b.indexOf(n) > -1)) out.push(n);
    });
  } else if (mode === 'field') { // a=实体 b=字段 c=排除子串(可空)
    const ent = D[a] || {};
    const seen = {};
    Object.keys(ent).forEach(k => {
      const v = ((ent[k].row || {}).fields || {})[b];
      if (v == null || v === '' || v === '—' || seen[v]) return;
      if (c && String(v).indexOf(c) > -1) return;
      seen[v] = 1; out.push(v);
    });
  } else if (mode === 'rows') { // a=实体数组 b=过滤js c=label js
    const ents = Array.isArray(a) ? a : [a];
    const keys = [];
    ents.forEach(e => { const en = D[e] || {}; Object.keys(en).forEach(k => keys.push([k, en])); });
    const fl = b ? new Function('k', 'f', 'return ' + b) : null;
    if (fl) { for (let i = keys.length - 1; i >= 0; i--) { const f = (keys[i][1][keys[i][0]].row || {}).fields || {}; if (!fl(keys[i][0], f)) keys.splice(i, 1); } }
    keys.sort((x, y) => (x[0] < y[0] ? -1 : x[0] > y[0] ? 1 : 0)).reverse();
    keys.slice(0, 30).forEach(p => {
      const f = (p[1][p[0]].row || {}).fields || {};
      const lb = new Function('k', 'f', 'return ' + c);
      out.push(lb(p[0], f));
    });
  } else if (mode === 'partners') { // a=类型
    const ent = D.partners || {};
    Object.keys(ent).sort().forEach(k => {
      const f = (ent[k].row || {}).fields || {};
      if (f.type === a) out.push(f.name);
    });
  } else if (mode === 'projects') { // a='keys'|'active' b=label形态
    const ent = D.projects || {};
    Object.keys(ent).sort().forEach(k => {
      const f = (ent[k].row || {}).fields || {};
      if (a === 'active' && f.status === '已完结') return;
      out.push(b === 'full' ? (k + ' ' + (f.name || '')) : k);
    });
  } else if (mode === 'wh') {
    const ent = D.locations || {};
    const seen = {};
    Object.keys(ent).forEach(k => {
      const v = ((ent[k].row || {}).fields || {}).wh;
      if (v && !seen[v]) { seen[v] = 1; out.push(v); }
    });
  } else if (mode === 'users') {
    const ent = D.users || {};
    const seen = {};
    Object.keys(ent).forEach(k => {
      const s = ((ent[k].row || {}).fields || {}).search || '';
      const n = s.split(' ').slice(1).join(' ');
      if (n && !seen[n]) { seen[n] = 1; out.push(n); }
    });
  } else if (mode === 'cats') {
    const ent = D.dictItems || {};
    const seen = {};
    Object.keys(ent).forEach(k => {
      const v = ((ent[k].row || {}).fields || {}).category;
      if (v && !seen[v]) { seen[v] = 1; out.push(v); }
    });
  } else if (mode === 'periods') {
    const d = new Date(); let y = d.getFullYear(), m = d.getMonth() + 1;
    for (let i = 0; i < a; i++) { out.push(y + '-' + ('0' + m).slice(-2)); m--; if (m === 0) { m = 12; y--; } }
  }
  return out;
}
"""

JS_LOCATE = r"""
(kind, a) => {
  let r = null;
  if (kind === 'id') r = document.getElementById(a);
  else if (kind === 'ff') {
    const els = document.querySelectorAll('.ff');
    for (const el of els) {
      const lb = el.querySelector('.ff-label');
      if (lb && lb.textContent.replace(/[:：]\s*$/, '') === a) { r = el.querySelector('select'); break; }
    }
  } else if (kind === 'form') {
    const norm = t => String(t).replace(/[\s\*]/g, '').replace(/[:：]$/, '');
    const els = document.querySelectorAll('.form-label');
    for (const el of els) {
      if (norm(el.textContent) !== norm(a)) continue;
      const row = el.closest('.form-row') || el.parentElement;
      if (row) { r = row.querySelector('select'); break; }
    }
  } else if (kind === 'qsa') r = [...document.querySelectorAll(a)];
  if (!r) return null;
  const list = Array.isArray(r) ? r : [r];
  return list.map(s => [...s.options].map(o => (o.textContent || '').replace(/\s+/g, ' ').trim()));
}
"""

WHITELIST = {'全部', '其他（演示）', '其他终端用户', '其他终端用户（手输）', '＋ 其他（手工录入）'}

# (页, 定位kind, 定位arg, 期望mode, 期望参数...)
CASES = [
    # ---- B 类字典 ----
    ("仓储作业/其他入库列表.html", 'ff', '入库类型', 'dict', ('入库类型',)),
    ("仓储作业/其他出库列表.html", 'ff', '出库类型', 'dict', ('出库类型',)),
    ("仓储作业/库存查询.html", 'ff', '库存状态', 'dict', ('库存状态',)),
    ("仓储作业/盘点列表.html", 'ff', '盘点口径', 'dict', ('盘点口径',)),
    ("基础数据/产品档案.html", 'ff', '物料类型', 'dict', ('物料类型',)),
    ("我的待办.html", 'id', 'todoType', 'dict', ('待办单据类型',)),
    ("系统管理/角色新建.html", 'form', '数据权限范围', 'dict', ('数据权限范围',)),
    ("系统管理/角色管理.html", 'ff', '数据权限', 'dict', ('数据权限范围',)),
    ("财务协同/付款新建.html", 'form', '付款方式', 'dict', ('支付方式',)),
    ("财务协同/应付新建.html", 'form', '费用分类', 'dict', ('费用分类',)),
    ("财务协同/退款新建.html", 'id', 'refundTypeSel', 'dict', ('退款类型',)),
    ("财务协同/退款登记.html", 'ff', '退款类型', 'dict', ('退款类型',)),
    ("采购管理/采购退货单列表.html", 'ff', '退货类型', 'dict', ('退货类型',)),
    ("销售管理/销售退货单列表.html", 'ff', '退货类型', 'dict', ('退货类型',)),
    ("财务协同/应收账单.html", 'ff', '账单类型', 'dict', ('应收账单类型',)),
    ("财务协同/应付账单.html", 'ff', '账单类型', 'dict', ('应付账单类型',)),
    ("财务协同/开票登记.html", 'ff', '发票类型', 'dict', ('发票类型',)),
    ("财务协同/开票新建.html", 'form', '发票类型', 'dict', ('发票类型',)),
    ("财务协同/应付新建.html", 'id', 'cmBtype', 'dict', ('应付账单类型',)),
    ("财务协同/应收生成.html", 'id', 'cmBtype', 'dict', ('应收账单类型',
        ['租赁费', '销售费', '丢损赔偿', '供应商应收', '押金', '预收'])),
    # ---- A 类·客商 ----
    ("租赁管理/租赁单列表.html", 'ff', '客户名称', 'partners', ('客户',)),
    ("租赁管理/租赁出库列表.html", 'ff', '客户', 'partners', ('客户',)),
    ("租赁管理/退租入库列表.html", 'ff', '客户名称', 'partners', ('客户',)),
    ("财务协同/应收账单.html", 'ff', '客户', 'partners', ('客户',)),
    ("财务协同/收款登记.html", 'ff', '客户', 'partners', ('客户',)),
    ("销售管理/销售订单列表.html", 'ff', '客户名称', 'partners', ('客户',)),
    ("销售管理/销售出库列表.html", 'ff', '客户名称', 'partners', ('客户',)),
    ("销售管理/销售退货单列表.html", 'ff', '客户名称', 'partners', ('客户',)),
    ("财务协同/付款登记.html", 'ff', '供应商名称', 'partners', ('供应商',)),
    ("财务协同/应付账单.html", 'ff', '供应商名称', 'partners', ('供应商',)),
    ("采购管理/采购订单列表.html", 'ff', '供应商', 'partners', ('供应商',)),
    ("采购管理/采购入库列表.html", 'ff', '供应商', 'partners', ('供应商',)),
    ("采购管理/采购退货单列表.html", 'ff', '供应商', 'partners', ('供应商',)),
    ("租赁管理/租赁单新建.html", 'form', '客户', 'partners', ('客户',)),
    ("销售管理/销售订单新建.html", 'form', '客户', 'partners', ('客户',)),
    ("销售管理/销售退货新建.html", 'form', '客户', 'partners', ('客户',)),
    ("财务协同/收款新建.html", 'form', '客户', 'partners', ('客户',)),
    ("财务协同/开票新建.html", 'form', '购方名称（客户）', 'partners', ('客户',)),
    ("项目管理/项目新建.html", 'id', 'prjCust', 'partners', ('客户',)),
    ("财务协同/付款新建.html", 'form', '供应商', 'partners', ('供应商',)),
    ("采购管理/采购退货新建.html", 'form', '供应商', 'partners', ('供应商',)),
    # ---- A 类·租入域筛选（实体字段） ----
    ("租入管理/租入入库列表.html", 'ff', '供应商', 'field', ('rentInbounds', 'operator', '待选')),
    ("租入管理/租入入库列表.html", 'ff', '物料', 'field', ('rentInbounds', 'appliance', None)),
    ("租入管理/租入单列表.html", 'ff', '供应商', 'field', ('rentInOrders', 'operator', '待选')),
    ("租入管理/租入单列表.html", 'ff', '物料', 'field', ('rentInOrders', 'appliance', None)),
    ("租入管理/租入归还列表.html", 'ff', '供应商', 'field', ('rentInReturns', 'operator', '待选')),
    # ---- A 类·仓储域筛选 ----
    ("仓储作业/其他入库列表.html", 'ff', '入库库房', 'field', ('otherInbounds', 'warehouse', None)),
    ("仓储作业/其他出库列表.html", 'ff', '出库库房', 'field', ('otherOutbounds', 'warehouse', None)),
    ("仓储作业/库存调拨列表.html", 'ff', '调出库房', 'field', ('transfers', 'frm', None)),
    ("仓储作业/库存调拨列表.html", 'ff', '调入库房', 'field', ('transfers', 'to', None)),
    ("仓储作业/盘点列表.html", 'ff', '盘点范围', 'field', ('stocktakes', 'scope', None)),
    ("仓储作业/盘点列表.html", 'ff', '盘点人', 'field', ('stocktakes', 'checker', None)),
    ("仓储作业/库存查询.html", 'ff', '库位', 'field', ('stockFlows', 'loc', None)),
    ("基础数据/库位档案.html", 'ff', '仓库', 'wh', ()),
    # ---- A 类·项目 ----
    ("租赁管理/租赁单列表.html", 'ff', '所属项目', 'projects', ('keys',)),
    ("租赁管理/租赁出库列表.html", 'ff', '所属项目', 'projects', ('keys',)),
    ("租赁管理/退租入库列表.html", 'ff', '所属项目', 'projects', ('keys',)),
    ("财务协同/应收账单.html", 'ff', '所属项目', 'projects', ('keys',)),
    ("财务协同/损益报表.html", 'ff', '所属项目', 'projects', ('keys',)),
    ("销售管理/销售订单列表.html", 'ff', '所属项目', 'projects', ('keys',)),
    ("销售管理/销售出库列表.html", 'ff', '所属项目', 'projects', ('keys',)),
    ("采购管理/采购入库列表.html", 'ff', '所属项目', 'projects', ('keys',)),
    ("采购管理/采购订单列表.html", 'ff', '所属项目', 'projects', ('keys',)),
    ("仓储作业/库存查询.html", 'ff', '项目', 'projects', ('keys',)),
    ("租入管理/租入单新建.html", 'id', 'cmProject', 'projects', ('active', 'full')),
    ("采购管理/采购订单新建.html", 'id', 'cmProject', 'projects', ('active', 'full')),
    ("租赁管理/租赁单新建.html", 'form', '所属项目', 'projects', ('active', 'full')),
    ("销售管理/销售订单新建.html", 'form', '所属项目', 'projects', ('active', 'full')),
    ("财务协同/应收生成.html", 'form', '所属项目', 'projects', ('active', 'full')),
    # ---- A 类·人名/角色 ----
    ("我的待办.html", 'id', 'todoAuditor', 'field', ('todoItems', 'auditor', None)),
    ("系统管理/操作日志.html", 'ff', '操作人', 'field', ('opLogs', 'user', None)),
    ("项目管理/项目档案.html", 'ff', '项目负责人', 'field', ('projects', 'owner', None)),
    ("系统管理/用户权限.html", 'ff', '角色', 'rows', ('roles', None, "(f.name||'')")),
    ("系统管理/用户新建.html", 'form', '角色', 'rows', ('roles', None, "(f.name||'')")),
    ("采购管理/采购入库录单.html", 'form', '仓管员', 'users', ()),
    ("仓储作业/盘点录入.html", 'form', '盘点人', 'users', ()),
    ("仓储作业/盘点录入.html", 'form', '复盘人', 'users', ()),
    # ---- A 类·库房表单（locations） ----
    ("仓储作业/其他入库新建.html", 'form', '入库库房', 'wh', ()),
    ("仓储作业/其他出库新建.html", 'form', '出库库房', 'wh', ()),
    ("仓储作业/调拨新建.html", 'form', '调出库房', 'wh', ()),
    ("仓储作业/调拨新建.html", 'form', '调入库房', 'wh', ()),
    ("销售管理/销售出库新建.html", 'form', '出库库房', 'wh', ()),
    ("仓储作业/盘点录入.html", 'form', '盘点库房', 'wh', ()),
    ("项目管理/上下游绑定.html", 'id', 'bindWh', 'wh', ()),
    # ---- A 类·物料明细 ----
    ("仓储作业/其他入库新建.html", 'form', '物料', 'rows', ('products', None, "(k+' '+(f.name||''))")),
    ("仓储作业/其他出库新建.html", 'form', '物料', 'rows', ('products', None, "(k+' '+(f.name||''))")),
    ("仓储作业/调拨新建.html", 'form', '物料', 'rows', ('products', None, "(k+' '+(f.name||''))")),
    ("销售管理/销售订单新建.html", 'qsa', '.edit-tbl td select[data-tax="prod"]', 'rows', ('products', None, "(k+' '+(f.name||''))")),
    ("销售管理/销售出库新建.html", 'qsa', '.edit-tbl td select[data-tax="prod"]', 'rows', ('products', None, "(k+' '+(f.name||''))")),
    ("租入管理/租入单新建.html", 'qsa', '.edit-tbl td select.g39mat', 'rows', ('products', None, "(k+' '+(f.name||''))")),
    ("租赁管理/租赁单新建.html", 'qsa', '.edit-tbl td select.g39mat', 'rows', (['products', 'bomList'], None, "(k+' '+(f.name||''))")),
    # ---- A 类·关联单号 ----
    ("租入管理/租入归还新建.html", 'id', 'riSelect', 'rows', ('rentInOrders', "f.status!=='新建(草稿)'", "(k+' · '+(f.operator||'')+' · '+(f.status||''))")),
    ("销售管理/销售出库新建.html", 'form', '关联销售订单', 'rows', ('salesOrders', None, "(k+' · '+(f.summary||f.customer||''))")),
    ("财务协同/开票新建.html", 'form', '关联应收账单', 'rows', ('receivableBills', None, "(k+' · '+(f.customer||'')+' · '+(f.period||''))")),
    ("财务协同/收款新建.html", 'form', '关联应收账单', 'rows', ('receivableBills', None, "(k+' · '+(f.customer||'')+' · '+(f.period||''))")),
    ("财务协同/付款新建.html", 'form', '关联应付账单', 'rows', ('payableBills', None, "(k+' · '+(f.supplier||''))")),
    ("采购管理/采购入库录单.html", 'form', '关联采购订单号', 'rows', ('purchaseOrders', None, "(k+' · '+(f.summary||''))")),
    ("采购管理/采购退货新建.html", 'form', '关联原单', 'rows', ('purchaseInbounds', None, "(k+' · '+(f.supplier||''))")),
    ("销售管理/销售退货新建.html", 'form', '关联原单', 'rows', ('salesOutbounds', None, "(k+' · '+(f.summary||''))")),
    # ---- A 类·其他 ----
    ("系统管理/字典项新建.html", 'form', '字典分类', 'cats', ()),
    ("系统管理/用户新建.html", 'form', '数据权限范围', 'dict', ('数据权限范围',)),
    ("财务协同/应收账单.html", 'ff', '账期', 'periods', (12,)),
    ("财务协同/损益报表.html", 'ff', '账期', 'periods', (12,)),
]

def main():
    npass = nfail = 0
    fails = []
    with sync_playwright() as pw:
        br = pw.chromium.launch(headless=True)
        pg = br.new_page()
        pg.on("pageerror", lambda e: None)
        for page, kind, loc, mode, args in CASES:
            f = ROOT / page
            try:
                pg.goto(f.as_uri(), wait_until="load", timeout=15000)
                pg.wait_for_timeout(200)
                sels = pg.evaluate("([k,a]) => (%s)(k, a)" % JS_LOCATE, [kind, loc])
                if not sels:
                    raise Exception("定位失败")
                exp = pg.evaluate("(m) => (%s)(m[0], m[1], m[2], m[3])" % JS_EXPECT, [mode] + list(args[:3]))
                exp_set = [x for x in exp if x not in WHITELIST]
                from collections import Counter
                exp_c = Counter(exp_set)
                ok_all = True
                detail = ""
                for got in sels:
                    got = [o for o in got if o not in WHITELIST]
                    got_c = Counter(got)
                    if got_c != exp_c:
                        ok_all = False
                        detail = "缺=%s 多=%s" % (sorted((exp_c - got_c).elements())[:4], sorted((got_c - exp_c).elements())[:4])
                        break
                if ok_all:
                    npass += 1
                    print(f"[PASS] {page} · {loc} ({len(exp_set)} 项)")
                else:
                    nfail += 1
                    fails.append((page, loc, detail))
                    print(f"[FAIL] {page} · {loc} {detail}")
            except Exception as e:
                nfail += 1
                fails.append((page, loc, str(e)[:80]))
                print(f"[FAIL] {page} · {loc} 异常: {str(e)[:80]}")
        br.close()
    print(f"\n总判定：{npass} PASS / {nfail} FAIL")
    sys.exit(1 if nfail else 0)

main()
