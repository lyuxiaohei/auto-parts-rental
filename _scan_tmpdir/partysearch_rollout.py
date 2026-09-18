# -*- coding: utf-8 -*-
"""主数据字段搜索下拉铺开（2026-09-17·道远采纳建议）：客户/供应商/所属项目/字典分类 15 处"""
import io, re

B = "P3-R01-包装租赁管理后台原型/"

FILL = {
    "客户": "SSEL.fillEntity(SSEL.byFormLabel('客户'),'partners',{label:'name',filter:function(k,f){return f.type==='客户';}});",
    "供应商": "SSEL.fillEntity(SSEL.byFormLabel('供应商'),'partners',{label:'name',filter:function(k,f){return f.type==='供应商';}});",
    "所属项目": "SSEL.fillEntity(SSEL.byFormLabel('所属项目'),'projects',{filter:function(k,f){return f.status!=='已完结';},label:function(k,f){return k+' '+(f.name||'');}});",
}
PH = {"客户": "输入名称搜索", "供应商": "输入名称搜索", "所属项目": "输入编码/名称搜索", "字典分类": "输入分类搜索"}

JOBS = [
    ("租入管理/租入单新建.html", ["供应商", "所属项目"]),
    ("租赁管理/租赁单新建.html", ["客户", "所属项目"]),
    ("租赁管理/退租入库新建.html", ["客户", "所属项目"]),
    ("财务协同/收款新建.html", ["客户"]),
    ("销售管理/销售订单新建.html", ["客户", "所属项目"]),
    ("销售管理/销售退货新建.html", ["客户"]),
    ("采购管理/采购退货新建.html", ["供应商"]),
    ("财务协同/付款新建.html", ["供应商"]),
    ("财务协同/应收生成.html", ["所属项目"]),
    ("系统管理/字典项新建.html", ["字典分类"]),
]

for path, labs in JOBS:
    s = io.open(B + path, encoding="utf-8", newline="").read()
    lines = [HDR] = ["/* 主数据字段搜索下拉（2026-09-17 道远采纳建议） */"]
    for lab in labs:
        ph = PH[lab]
        if lab in FILL:
            has = re.search(r"SSEL\.fillEntity\([^;]*byFormLabel\('" + lab + r"'\)[^;]*\);", s)
            if not has:
                lines.append(FILL[lab])
        lines.append("MSEL.attach(SSEL.byFormLabel('" + lab + "'), { placeholder: '" + ph + "' });")
    inc = '' if 'src="../_data/mat-search.js"' in s else '<script src="../_data/mat-search.js"></script>\r\n'
    block = inc + "<script>\r\n" + "\r\n".join(lines) + "\r\n</script>\r\n"
    assert s.count("</body>") == 1
    s = s.replace("</body>", block + "</body>", 1)
    io.open(B + path, "w", encoding="utf-8", newline="").write(s)
    print("OK", path, labs)

# 应付新建 cmParty（4v4 动态重建选项·挂组件＋类型切换后同步显示）
path = "财务协同/应付新建.html"
s = io.open(B + path, encoding="utf-8", newline="").read()
guard = ("/* 主数据字段搜索下拉（2026-09-17 道远采纳建议）：往来单位（4v4 按账单类型重建选项·切换后同步显示） */\r\n"
         "MSEL.attach(document.getElementById('cmParty'), { placeholder: '输入名称搜索' });\r\n"
         "document.addEventListener('change', function (e) { if (e.target && e.target.id === 'cmBtype') setTimeout(function () { MSEL.syncAll(); }, 0); });")
# 追加到既有 mat-search 接线块尾（该页已引入）
anchor = "MSEL.attach(SSEL.byFormLabel('关联租入单号'), { placeholder: '输入单号搜索' });"
assert s.count(anchor) == 1
s = s.replace(anchor, anchor + "\r\n" + guard)
io.open(B + path, "w", encoding="utf-8", newline="").write(s)
print("OK", path, ["供应商(cmParty·带4v4守卫)"])
