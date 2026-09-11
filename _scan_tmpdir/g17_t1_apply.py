# -*- coding: utf-8 -*-
"""G17 T1 八项合并替换：dry-run（默认）→ --apply（计数一致才写回）
铁律：精确字符串替换+assert 计数；替换串均带标签锚（URL 天然免疫）；
     词级替换仅限复合词（入库仓库等，URL 预检确认无文件名含词根）。"""
import pathlib, sys, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROT = ROOT / 'P3-R01-包装租赁管理后台原型'

# (项号, 文件相对路径, 旧串, 新串, 期望计数)
RULES = [
    # ===== 项1 物料类型 =====
    ('1', '仓储作业/库存查询.html', '<th>物料类别</th>', '<th>物料类型</th>', 1),
    ('1', '基础数据/BOM维护.html', '<th>来源</th><th>类型</th>', '<th>来源</th><th>物料类型</th>', 1),
    ('1', '采购管理/采购订单列表.html', '<span class="req">*</span>类别</span>', '<span class="req">*</span>物料类型</span>', 1),
    # ===== 项2 物料分类 =====
    ('2', '基础数据/产品档案.html', '<span class="ff-label">分类：</span>', '<span class="ff-label">物料分类：</span>', 1),
    ('2', '基础数据/产品档案.html', '<th>分类</th>', '<th>物料分类</th>', 2),
    ('2', '基础数据/产品档案.html', '<span class="form-label">分类</span>', '<span class="form-label">物料分类</span>', 1),
    ('2', '基础数据/产品档案.html', "{ label: '分类', field: 'cls' }", "{ label: '物料分类', field: 'cls' }", 1),
    ('2', '基础数据/弹窗/新建产品.html', '<span class="form-label">分类</span>', '<span class="form-label">物料分类</span>', 1),
    # ===== 项3 器具→物料 =====
    ('3', '租赁管理/租入单列表.html', '<span class="ff-label">器具：</span>', '<span class="ff-label">物料：</span>', 1),
    ('3', '租赁管理/租入单列表.html', '<th>器具</th>', '<th>物料</th>', 1),
    ('3', '租赁管理/租入单列表.html', "{ label: '器具', field: 'appliance' }", "{ label: '物料', field: 'appliance' }", 1),
    ('3', '租赁管理/租入入库列表.html', '<span class="ff-label">器具：</span>', '<span class="ff-label">物料：</span>', 1),
    ('3', '租赁管理/租入入库列表.html', '<th>器具</th>', '<th>物料</th>', 1),
    ('3', '租赁管理/租入入库列表.html', "{ label: '器具', field: 'appliance' }", "{ label: '物料', field: 'appliance' }", 1),
    ('3', '租赁管理/租入入库列表.html', '器具档案标记来源=租入', '物料档案标记来源=租入', 1),
    ('3', '租赁管理/租入归还列表.html', '<th>器具</th>', '<th>物料</th>', 1),
    ('3', '租赁管理/租入归还列表.html', '<span class="req">*</span>器具</span>', '<span class="req">*</span>物料</span>', 1),
    ('3', '租赁管理/租入归还列表.html', '归还器具出库至供应商', '归还物料出库至供应商', 1),
    ('3', '租赁管理/弹窗/租入归还新建.html', '<span class="req">*</span>器具</span>', '<span class="req">*</span>物料</span>', 1),
    ('3', '租赁管理/弹窗/租入入库确认.html', '器具档案标记来源=租入', '物料档案标记来源=租入', 1),
    ('3', '租赁管理/弹窗/租入归还审核.html', '归还器具出库至供应商', '归还物料出库至供应商', 1),
    ('3', '租赁管理/退租入库列表.html', '<th>退租器具名称</th>', '<th>退租物料名称</th>', 1),
    ('3', '采购管理/采购入库录单.html', '<th>零件号 / 器具编码</th>', '<th>零件号 / 物料编码</th>', 1),
    ('3', '基础数据/BOM维护.html', '<td>零件</td>', '<td>零部件</td>', 3),
    ('3', '基础数据/产品档案.html', '确认停用该器具（WBX-1210L）？', '确认停用该物料（WBX-1210L）？', 1),
    # ===== 项4 客商列头短名 =====
    ('4', '租赁管理/租赁单列表.html', '<th>客户名称</th>', '<th>客户</th>', 1),
    ('4', '租赁管理/租赁单列表.html', "{ label: '客户名称', field: 'customer' }", "{ label: '客户', field: 'customer' }", 1),
    ('4', '租赁管理/退租入库列表.html', '<th>客户名称</th>', '<th>客户</th>', 1),
    ('4', '租赁管理/退租入库列表.html', "{ label: '客户名称', field: 'customer' }", "{ label: '客户', field: 'customer' }", 1),
    ('4', '销售管理/销售出库列表.html', '<th>客户名称</th>', '<th>客户</th>', 1),
    ('4', '销售管理/销售出库列表.html', "{ label: '客户名称', field: 'customer' }", "{ label: '客户', field: 'customer' }", 1),
    ('4', '销售管理/销售订单列表.html', '<th>客户名称</th>', '<th>客户</th>', 1),
    ('4', '销售管理/销售订单列表.html', "{ label: '客户名称', field: 'customer' }", "{ label: '客户', field: 'customer' }", 1),
    ('4', '项目管理/项目档案.html', "{ label: '客户名称', field: 'customer' }", "{ label: '客户', field: 'customer' }", 1),
    ('4', '财务协同/付款登记.html', '<th>供应商名称</th>', '<th>供应商</th>', 1),
    ('4', '财务协同/付款登记.html', "{ label: '供应商名称', field: 'supplier' }", "{ label: '供应商', field: 'supplier' }", 1),
    ('4', '财务协同/应付账单.html', '<th>供应商名称</th>', '<th>供应商</th>', 1),
    ('4', '财务协同/应付账单.html', "{ label: '供应商名称', field: 'supplier' }", "{ label: '供应商', field: 'supplier' }", 1),
    ('4', '采购管理/采购订单列表.html', '<th>供应商名称</th>', '<th>供应商</th>', 1),
    ('4', '基础数据/客商管理.html', '<th>客商名称</th>', '<th>客商</th>', 1),
    ('4', '基础数据/客商管理.html', "{ label: '客商名称', field: 'name' }", "{ label: '客商', field: 'name' }", 1),
    # ===== 项5 单据编号 =====
    ('5', '仓储作业/其他入库列表.html', '<span class="ff-label">单号：</span>', '<span class="ff-label">单据编号：</span>', 1),
    ('5', '仓储作业/其他入库列表.html', '<th>单号</th>', '<th>单据编号</th>', 1),
    ('5', '仓储作业/其他入库列表.html', '按单号渲染', '按单据编号渲染', 1),
    ('5', '仓储作业/其他入库列表.html', '按行内单号渲染', '按行内单据编号渲染', 1),
    ('5', '仓储作业/其他入库列表.html', "{ label: '单号', field: '_key' }", "{ label: '单据编号', field: '_key' }", 1),
    ('5', '仓储作业/其他出库列表.html', '<span class="ff-label">单号：</span>', '<span class="ff-label">单据编号：</span>', 1),
    ('5', '仓储作业/其他出库列表.html', '<th>单号</th>', '<th>单据编号</th>', 1),
    ('5', '仓储作业/其他出库列表.html', '按单号渲染', '按单据编号渲染', 1),
    ('5', '仓储作业/其他出库列表.html', '按行内单号渲染', '按行内单据编号渲染', 1),
    ('5', '仓储作业/其他出库列表.html', "{ label: '单号', field: '_key' }", "{ label: '单据编号', field: '_key' }", 1),
    ('5', '我的待办.html', '<th>单据号</th>', '<th>单据编号</th>', 1),
    ('5', '我的待办.html', 'placeholder="单号 / 客户 / 项目 / 摘要"', 'placeholder="单据编号 / 客户 / 项目 / 摘要"', 1),
    # ===== 项6 状态 =====
    ('6', '基础数据/BOM.html', '<div class="dlabel">当前状态</div>', '<div class="dlabel">状态</div>', 1),
    ('6', '基础数据/产品档案.html', '<div class="dlabel">当前状态</div>', '<div class="dlabel">状态</div>', 1),
    ('6', '基础数据/库位档案.html', '<div class="dlabel">当前状态</div>', '<div class="dlabel">状态</div>', 1),
    ('6', '系统管理/数据字典.html', '<div class="dlabel">当前状态</div>', '<div class="dlabel">状态</div>', 1),
    ('6', '系统管理/用户权限.html', '<div class="dlabel">当前状态</div>', '<div class="dlabel">状态</div>', 2),
    ('6', '系统管理/弹窗/停用确认.html', '<div class="dlabel">当前状态</div>', '<div class="dlabel">状态</div>', 1),
    ('6', '基础数据/弹窗/停用确认.html', '<div class="dlabel">当前状态</div>', '<div class="dlabel">状态</div>', 1),
    ('6', '系统管理/弹窗/重置密码确认.html', '<div class="dlabel">当前状态</div>', '<div class="dlabel">状态</div>', 1),
    # ===== 项7 备注 =====
    ('7', '系统管理/用户权限.html', '<th>说明</th>', '<th>备注</th>', 1),
    ('7', '系统管理/角色管理.html', '<th>说明</th>', '<th>备注</th>', 1),
    ('7', '系统管理/弹窗/角色管理.html', '<th>说明</th>', '<th>备注</th>', 1),
    # ===== 项8 库房 =====
    ('8', '仓储作业/其他入库列表.html', '入库仓库', '入库库房', 4),
    ('8', '仓储作业/弹窗/其他入库新建.html', '入库仓库', '入库库房', 1),
    ('8', '租赁管理/退租入库列表.html', '入库仓库', '入库库房', 1),
    ('8', '仓储作业/其他出库列表.html', '出库仓库', '出库库房', 4),
    ('8', '仓储作业/弹窗/其他出库新建.html', '出库仓库', '出库库房', 1),
    ('8', '销售管理/销售出库列表.html', '出库仓库', '出库库房', 2),
    ('8', '销售管理/弹窗/销售出库新建.html', '出库仓库', '出库库房', 1),
    ('8', '仓储作业/库存调拨列表.html', '调出仓库', '调出库房', 4),
    ('8', '仓储作业/库存调拨列表.html', '调入仓库', '调入库房', 4),
    ('8', '仓储作业/弹窗/调拨新建.html', '调出仓库', '调出库房', 1),
    ('8', '仓储作业/弹窗/调拨新建.html', '调入仓库', '调入库房', 1),
    ('8', '仓储作业/盘点录入.html', '盘点仓库：', '盘点库房：', 1),
    ('8', '基础数据/库位档案.html', '<span class="ff-label">仓库：</span>', '<span class="ff-label">库房：</span>', 1),
    ('8', '基础数据/库位档案.html', '<th>仓库</th>', '<th>库房</th>', 1),
    ('8', '基础数据/库位档案.html', '<span class="req">*</span>仓库</span>', '<span class="req">*</span>库房</span>', 1),
    ('8', '基础数据/库位档案.html', "{ label: '仓库', field: 'wh' }", "{ label: '库房', field: 'wh' }", 1),
    ('8', '基础数据/弹窗/新建库位.html', '<span class="req">*</span>仓库</span>', '<span class="req">*</span>库房</span>', 1),
]

APPLY = '--apply' in sys.argv

# ---- URL 免疫预检：全站 URL 语境内不得含任何替换词根 ----
URL_PAT = re.compile(r'(?:go|openDetail|location\.href\s*=|href\s*=)\s*\(?[\'"]([^\'"]+\.html)[\'"]')
WORD_ROOTS = ['仓库', '分类', '器具', '单号', '单据号', '说明', '类型', '类别', '零件',
              '客户名称', '供应商名称', '客商名称', '当前状态', '物料类别', '退租器具', '该器具']
url_hits = []
for f in sorted(PROT.rglob('*.html')):
    p = f.as_posix()
    if 'backup' in p or 'mobile' in p:
        continue
    s = f.read_text(encoding='utf-8')
    for m in URL_PAT.finditer(s):
        for root in WORD_ROOTS:
            if root in m.group(1):
                url_hits.append(f"{p}: URL={m.group(1)} 含词根 {root}")
if url_hits:
    print('!! URL 免疫预检失败：')
    for h in url_hits:
        print('  ', h)
    sys.exit(2)
print(f"URL 免疫预检 PASS（全站 URL 参数 0 含替换词根）")

# ---- dry-run / apply ----
results, mismatches, total = [], [], 0
for item, rel, old, new, expect in RULES:
    f = PROT / rel
    s = f.read_text(encoding='utf-8')
    actual = s.count(old)
    ok = (actual == expect)
    if not ok:
        mismatches.append((item, rel, old[:30], expect, actual))
    results.append(f"{'OK ' if ok else 'MIS'} 项{item} {rel} [{old[:34]}] 期望{expect} 实际{actual}")
    total += actual

print('\n'.join(results))
print(f"\n合计匹配 {total} 处 / {len(RULES)} 条规则；不符 {len(mismatches)} 条")
if mismatches:
    print("!! 存在计数不符，未写回任何文件（dry-run 安全退出）")
    sys.exit(3)

if APPLY:
    import shutil
    BK = ROOT / '_scan_tmpdir' / 'backup-g17-20260911' / 'P3-R01-包装租赁管理后台原型'
    changed = 0
    for item, rel, old, new, expect in RULES:
        f = PROT / rel
        s = f.read_text(encoding='utf-8')
        assert s.count(old) == expect, f"apply 阶段计数漂移: {rel}"
        # 备份双保险（逐文件首改时再备份一次原态，防 T0 后有变）
        bkp = BK / rel
        if not bkp.exists():
            bkp.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, bkp)
        f.write_text(s.replace(old, new), encoding='utf-8')
        changed += 1
    print(f"APPLY 完成：{changed} 条规则全部写回")
    # 写回后逐条复检：旧串残留=0 新串在
    for item, rel, old, new, expect in RULES:
        s = (PROT / rel).read_text(encoding='utf-8')
        assert s.count(old) == 0, f"写回后旧串残留: {rel} [{old[:30]}]"
        assert s.count(new) >= expect, f"写回后新串不足: {rel}"
    print("写回复检 PASS：旧串残留 0 / 新串全在")
else:
    print("dry-run 模式（未写回）。加 --apply 执行。")
