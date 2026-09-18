# -*- coding: utf-8 -*-
"""关联单据号搜索下拉铺开（2026-09-17·道远样板通过后全量）：11 页 12 字段"""
import io

B = "P3-R01-包装租赁管理后台原型/"

def load(p): return io.open(B + p, encoding="utf-8", newline="").read()
def save(p, s): io.open(B + p, "w", encoding="utf-8", newline="").write(s)

def wire(p, js):
    """页尾插入 mat-search 接线（页面未引共享件时补引）"""
    s = load(p)
    inc = '' if 'src="../_data/mat-search.js"' in s else '<script src="../_data/mat-search.js"></script>\r\n'
    assert inc or 'mat-search.js' in s, p + ' 无共享件引用'
    block = inc + '<script>\r\n' + js + '\r\n</script>\r\n'
    assert s.count('</body>') == 1
    s = s.replace('</body>', block + '</body>', 1)
    save(p, s)
    print('OK', p)

HDR = '/* 关联单据号搜索下拉（2026-09-17 道远指示·采购入库录单样板推广） */'

# 1 租入归还新建（riSelect 已有 SSEL 填充+data-key 联动）
wire('租入管理/租入归还新建.html',
     HDR + "\r\nMSEL.attach(document.getElementById('riSelect'), { placeholder: '输入单号搜索' });")

# 2 租赁出库录单（静态选项→SSEL 填充 salesOrders）
wire('租赁管理/租赁出库录单.html',
     HDR + "\r\nSSEL.fillEntity(SSEL.byFormLabel('关联销售订单'),'salesOrders',{desc:true,limit:30,label:function(k,f){return k+' · '+(f.summary||'');}});\r\n"
     "MSEL.attach(SSEL.byFormLabel('关联销售订单'), { placeholder: '输入单号/摘要搜索' });")

# 3-5 付款/收款/开票（SSEL 已就位·只挂组件）
for f, lab, ph in (
    ('财务协同/付款新建.html', '关联应付账单', '输入单号/供应商搜索'),
    ('财务协同/收款新建.html', '关联应收账单', '输入单号/客户搜索'),
    ('财务协同/开票新建.html', '关联应收账单', '输入单号/客户搜索'),
):
    wire(f, HDR + "\r\nMSEL.attach(SSEL.byFormLabel('" + lab + "'), { placeholder: '" + ph + "' });")

# 6 退款新建（静态选项→SSEL 双退货实体）
wire('财务协同/退款新建.html',
     HDR + "\r\nSSEL.fillEntity(SSEL.byFormLabel('关联退货单'),['purchaseReturns','salesReturns'],{desc:true,limit:30,label:function(k,f){return k+' · '+(f.supplier||f.customer||'');}});\r\n"
     "MSEL.attach(SSEL.byFormLabel('关联退货单'), { placeholder: '输入退货单号/单位搜索' });")

# 7-8 采购退货/销售退货（SSEL 已就位）
for f in ('采购管理/采购退货新建.html', '销售管理/销售退货新建.html'):
    wire(f, HDR + "\r\nMSEL.attach(SSEL.byFormLabel('关联原单'), { placeholder: '输入原单号/单位搜索' });")

# 9 销售出库新建（SSEL 已就位）
wire('销售管理/销售出库新建.html',
     HDR + "\r\nMSEL.attach(SSEL.byFormLabel('关联销售订单'), { placeholder: '输入单号/客户搜索' });")

# 10 应付新建：两个 input 转 select（保留行 id cmRefPo/cmRefRent·账单类型切换逻辑不受影响）
p = '财务协同/应付新建.html'
s = load(p)
old_po = '<div class="input-box" style="width:380px;"><input value="PO-20260901-017" placeholder="请输入"></div>'
new_po = ('<div class="input-box select-box" style="width:380px;"><select style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;">'
          '<option selected>PO-20260901-017</option></select><span class="caret">\u25be</span></div>')
assert s.count(old_po) == 1
s = s.replace(old_po, new_po)
old_rent = '<div class="input-box" style="width:380px;"><input placeholder="请输入"></div>'
assert s.count(old_rent) == 1
new_rent = ('<div class="input-box select-box" style="width:380px;"><select style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;">'
            '<option>（选择租入单）</option></select><span class="caret">\u25be</span></div>')
s = s.replace(old_rent, new_rent)
save(p, s)
print('OK 应付新建 两 input 转 select')
wire(p,
     HDR + "\r\nSSEL.fillEntity(SSEL.byFormLabel('关联采购订单号'),'purchaseOrders',{desc:true,limit:30,label:function(k,f){return k+' · '+(f.summary||'');}});\r\n"
     "SSEL.fillEntity(SSEL.byFormLabel('关联租入单号'),'rentInOrders',{desc:true,limit:30,label:function(k,f){return k+' · '+(f.matName||'');}});\r\n"
     "MSEL.attach(SSEL.byFormLabel('关联采购订单号'), { placeholder: '输入单号/摘要搜索' });\r\n"
     "MSEL.attach(SSEL.byFormLabel('关联租入单号'), { placeholder: '输入单号搜索' });")

print('\n全部完成')
