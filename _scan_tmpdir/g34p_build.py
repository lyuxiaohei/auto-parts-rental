# -*- coding: utf-8 -*-
"""G34 试点：把「新建采购订单」弹窗改造为表单页 采购管理/采购订单新建.html

以 采购管理/采购入库录单.html 为骨架（CSS+壳+统一脚本），
移植 弹窗/新建采购订单.html 的表单字段与关联销售订单搜索脚本。
"""
import io, os, re

PROTO = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
A_P = os.path.join(PROTO, r'采购管理\采购入库录单.html')        # 表单页样板（骨架源）
B_P = os.path.join(PROTO, r'采购管理\弹窗\新建采购订单.html')   # 弹窗模板（内容源）
OUT = os.path.join(PROTO, r'采购管理\采购订单新建.html')

A = io.open(A_P, encoding='utf-8', newline='').read().replace('\r\n', '\n')
B = io.open(B_P, encoding='utf-8', newline='').read().replace('\r\n', '\n')
assert not os.path.exists(OUT), '目标已存在，停止'

print(f'骨架源 A: {len(A)} 字符 | 内容源 B: {len(B)} 字符')
print(f'A 自身配平: <div={A.count("<div")} </div>={A.count("</div>")} 差={A.count("<div")-A.count("</div>")}')

# ---------- 1. head + CSS（改 title） ----------
i_top = A.index('<header class="topbar">')
head = A[:i_top]
head_new = re.sub(r'<title>.*?</title>', '<title>新建采购订单 - 包装租赁管理后台</title>', head, count=1)
assert head_new != head and '新建采购订单 - 包装租赁管理后台' in head_new
head = head_new
print('[1] head/CSS 就绪，title 已改')

# ---------- 2. 壳（topbar + sidebar + main-col + tabs） ----------
i_content = A.index('<div class="content submit-pad">')
shell = A[i_top:i_content]

t1 = '<span class="tab">采购入库 <span class="close">×</span></span>'
t2 = '<span class="tab active">采购入库录单 <span class="close">×</span></span>'
assert shell.count(t1) == 1 and shell.count(t2) == 1, 'tabs 锚点异常'
shell = shell.replace(t1, '<span class="tab">采购订单 <span class="close">×</span></span>')
shell = shell.replace(t2, '<span class="tab active">新建采购订单 <span class="close">×</span></span>')

sel_old = """   <li><div class="sm-link" onclick="go('../采购管理/采购订单列表.html')">采购订单</div></li>
   <li><div class="sm-link selected">采购入库</div></li>"""
sel_new = """   <li><div class="sm-link selected">采购订单</div></li>
   <li><div class="sm-link" onclick="go('../采购管理/采购入库列表.html')">采购入库</div></li>"""
assert shell.count(sel_old) == 1, 'sidebar selected 锚点异常'
shell = shell.replace(sel_old, sel_new)
print('[2] 壳就绪：tabs 改「新建采购订单」，sidebar 选中项改「采购订单」')

# ---------- 3. content（表单页三卡） ----------
SEL_STYLE = 'style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"'
CARET = '<span class="caret">▾</span>'
PROD_OPTS = ('<option>WBX-1210L 围板箱 1200×1000×970</option><option>WBX-1210M 围板箱 1200×1000×590</option>'
             '<option>PLT-1210W 木托盘 1200×1000</option><option>PLT-1210P 塑料托盘 1200×1000</option>'
             '<option>BTC-6040 料箱 600×400×340</option><option selected>LJ-A100 锁扣组件</option>'
             '<option>LJ-C300 围板</option><option>LJ-D400 箱盖</option><option>LJ-F600 内衬</option>')

CONTENT = '''<div class="content submit-pad">
<div class="card">
  <div class="card-head">
    <h3 class="card-title">订单信息</h3>
    <div class="head-btns"><button class="btn btn-default btn-sm" onclick="go('../采购管理/采购订单列表.html')">返回列表</button></div>
  </div>
  <div class="form-row">
    <div class="form-label"><span class="req">*</span>所属项目：</div>
    <div>
      <div class="input-box select-box" style="width:380px;"><select id="cmProject" ''' + SEL_STYLE + '''><option value="PRJ-2601" selected>PRJ-2601 一汽解放·长春基地 围板箱租赁</option><option value="PRJ-2602">PRJ-2602 一汽解放·青岛基地 料架租赁</option><option value="PRJ-2603">PRJ-2603 东风锂电·电池包周转箱</option><option value="PRJ-2604">PRJ-2604 上汽通用五菱·座椅周转箱（试点）</option><option value="PRJ-2605">PRJ-2605 一汽解放·蔚山基地 扩建</option><option value="PRJ-2606">PRJ-2606 东风锂电·二期扩容</option></select>''' + CARET + '''</div>
    </div>
  </div>
  <div class="form-row">
    <div class="form-label"><span class="req">*</span>供应商：</div>
    <div>
      <div class="input-box select-box" style="width:380px;"><select id="cmSupplier" ''' + SEL_STYLE + '''><option>路凯包装运营（上海）有限公司</option><option selected>苏州联恒五金制品有限公司</option><option>宁波华塑包装制品有限公司</option><option>常州正大塑料托盘厂</option></select>''' + CARET + '''</div>
    </div>
  </div>
  <div class="form-row">
    <div class="form-label"><span class="req">*</span>类别：</div>
    <div>
      <div class="input-box select-box" style="width:380px;"><select onchange="poToggleQj(this)" ''' + SEL_STYLE + '''><option selected>零部件</option><option>器具</option></select>''' + CARET + '''</div>
    </div>
  </div>
  <div class="form-row" id="poQjRow" style="display:none;">
    <div class="form-label"><span class="req">*</span>物料档案：</div>
    <div>
      <div class="input-box select-box" style="width:380px;"><select ''' + SEL_STYLE + '''><option selected>WBX-1210L 围板箱</option><option>PLT-1210P 塑料托盘</option><option>BTC-6040 料箱</option></select>''' + CARET + '''</div>
    </div>
  </div>
  <div class="form-row">
    <div class="form-label">关联销售订单号：</div>
    <div>
      <div class="input-box" style="width:380px;position:relative;"><input id="poSoInput" placeholder="输入单号/客户搜索 · 选填 · 可直接手输" oninput="poSoSearch(this.value)" onfocus="poSoSearch(this.value)" autocomplete="off"><div id="poSoDrop" style="display:none;position:absolute;top:36px;left:0;width:100%;background:#fff;border:1px solid var(--border);border-radius:6px;box-shadow:0 4px 12px rgba(0,0,0,.08);z-index:30;max-height:220px;overflow:auto;font-size:12.5px;"></div></div>
      <div class="pn-hint">关联后可带出客户与销售明细（以销定采 · 采购与销售并行，不强制关联）。</div>
    </div>
  </div>
  <div class="form-row" id="poSoCustRow" style="display:none;">
    <div class="form-label">客户（带出）：</div>
    <div>
      <div class="input-box" style="width:380px;"><input id="poSoCust" readonly class="auto"></div>
    </div>
  </div>
  <div class="form-row">
    <div class="form-label">预计到货日期：</div>
    <div>
      <div class="input-box" style="width:180px;"><input type="text" value="2026-09-15" placeholder="请输入"></div>
    </div>
  </div>
</div>

<div class="card">
  <div class="card-head">
    <h3 class="card-title">采购明细</h3>
    <div class="head-btns"><button class="btn btn-dashed btn-sm" onclick="addDetailRow(this)">添加一行</button></div>
  </div>
  <div class="table-wrap edit-tbl">
    <table>
      <thead><tr><th style="width:44px;">序号</th><th>物料编码</th><th>物料名称</th><th>规格</th><th>单位</th><th style="width:90px;">数量</th><th style="font-size:13.5px;font-weight:700;">未税单价(元)</th><th style="font-size:13.5px;font-weight:700;">税率</th><th style="font-size:13.5px;font-weight:700;">含税单价(元)</th><th>含税金额(元)</th><th class="sticky-op">操作</th></tr></thead>
      <tbody>
        <tr>
          <td>1</td>
          <td><select data-tax="prod" style="width:100%;min-width:130px;border:1px solid #d9d9d9;border-radius:4px;padding:2px 4px;font:inherit;background:#fff;cursor:pointer;">''' + PROD_OPTS + '''</select></td>
          <td><input value="锁扣组件"></td>
          <td><input value="不锈钢 304"></td>
          <td><input value="件"></td>
          <td class="td-num"><input data-tax="qty" value="5,000"></td>
          <td class="td-num"><input data-tax="excl" value="1.28"></td>
          <td><input data-tax="rate" value="13%" style="width:56px;"></td>
          <td class="td-num"><input data-tax="incl" value="1.45"></td>
          <td class="td-num"><input data-tax="amt" class="auto" value="7,250.00" readonly></td>
          <td class="ops sticky-op"><a>删除</a></td>
        </tr>
        <tr>
          <td>2</td>
          <td><select data-tax="prod" style="width:100%;min-width:130px;border:1px solid #d9d9d9;border-radius:4px;padding:2px 4px;font:inherit;background:#fff;cursor:pointer;"><option selected>LJ-B200</option>''' + PROD_OPTS + '''</select></td>
          <td><input value="铰链"></td>
          <td><input value="锌合金 65mm"></td>
          <td><input value="件"></td>
          <td class="td-num"><input data-tax="qty" value="2,000"></td>
          <td class="td-num"><input data-tax="excl" value="1.65"></td>
          <td><input data-tax="rate" value="13%" style="width:56px;"></td>
          <td class="td-num"><input data-tax="incl" value="1.86"></td>
          <td class="td-num"><input data-tax="amt" class="auto" value="3,720.00" readonly></td>
          <td class="ops sticky-op"><a>删除</a></td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<div class="card">
  <h3 class="card-title">随附信息</h3>
  <div class="form-row">
    <div class="form-label">备注：</div>
    <div>
      <div class="input-box" style="width:520px;"><input type="text" value="" placeholder="选填"></div>
    </div>
  </div>
</div>
'''
print(f'[3] content 就绪（三卡：订单信息 / 采购明细 / 随附信息），{len(CONTENT)} 字符')

# ---------- 4. submit-bar ----------
i_submit = A.index('<div class="submit-bar">')
tail = A[i_submit:]
sb_old = """<div class="submit-bar"><button class="btn btn-default" onclick="go('../采购管理/采购入库列表.html')">取 消</button><button class="btn btn-default">暂 存</button><button class="btn" data-note="2">提交验收</button></div>"""
assert tail.startswith(sb_old), 'submit-bar 锚点异常'
sb_new = """<div class="submit-bar"><button class="btn btn-default" onclick="go('../采购管理/采购订单列表.html')">取 消</button><button class="btn btn-default">保存草稿</button><button class="btn">提交审核</button></div>"""
tail = sb_new + tail[len(sb_old):]
print('[4] submit-bar 就绪：取消→采购订单列表 / 保存草稿 / 提交审核')

# ---------- 5. 关联销售订单搜索脚本（.modal → .content 迁移） ----------
i_s = B.index('<script>/* G31 T5')
i_e = B.index('</script>', i_s) + len('</script>')
po_js = B[i_s:i_e]
assert po_js.count("'.modal .edit-tbl tbody'") == 2, f'选择器锚点异常: {po_js.count(chr(39)+".modal")}'
po_js = po_js.replace("'.modal .edit-tbl tbody'", "'.content .edit-tbl tbody'")
print('[5] 关联销售订单搜索脚本已迁移（2 处 .modal → .content）')

# 插入到 addDetailRow 之后
anchor = "  rows.forEach(function (r, i) { r.cells[0].textContent = i + 1; });\n}\n</script>"
assert tail.count(anchor) == 1, 'addDetailRow 锚点异常'
tail = tail.replace(anchor, anchor + '\n' + po_js + '\n<script>\nfunction poToggleQj(sel) {\n  var r = document.getElementById("poQjRow");\n  if (r) r.style.display = (sel.options[sel.selectedIndex].text === "器具") ? "flex" : "none";\n}\n</script>')
print('[6] addDetailRow 保留 + 类别联动脚本已加')

# ---------- 6. 组装与自检 ----------
out = head + shell + CONTENT + tail

d_a = A.count('<div') - A.count('</div>')
d_o = out.count('<div') - out.count('</div>')
print(f'[7] 配平：骨架源差={d_a}，产物差={d_o}')
assert d_o == d_a == 0, f'配平异常 (A差={d_a} 产物差={d_o})'

out = out.replace('\r\n', '\n').replace('\n', '\r\n')   # 输出 CRLF：与项目既有页面一致
io.open(OUT, 'w', encoding='utf-8', newline='').write(out)
print(f'[8] 已写出 {OUT}（{len(out)} 字符）')
print(f'    校验：<div={out.count("<div")} </div>={out.count("</div>")} | 含 side-foot={"side-foot" in out} | 含 submit-bar={"submit-bar" in out}')
