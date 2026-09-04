# -*- coding: utf-8 -*-
# C批：采购入库录单补关联采购订单号；销售出库新建补库存可用量；新建采购订单物料类型级联+话术弱化
# 纪律：精确字符串替换 + assert 计数； newline='' 保持原行尾；列表页内嵌 modal 与弹窗模板同步改
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

def edit(path, old, new, n=1):
    s = io.open(path, encoding='utf-8', newline='').read()
    c = s.count(old)
    assert c == n, '%s 匹配数异常 expect=%d got=%d : %r' % (path, n, c, old[:60])
    s = s.replace(old, new)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)
    print('OK %s (%d处)' % (path.split('\\')[-1], c))

# ---------- C1 采购入库录单.html：供应商后插「关联采购订单号」必填（CRLF 文件） ----------
p1 = BASE + r'\仓储作业\采购入库录单.html'
old = '  <div class="form-row">\r\n    <div class="form-label"><span class="req">*</span>到货日期：</div>\r\n'
new = ('  <div class="form-row">\r\n'
       '    <div class="form-label"><span class="req">*</span>关联采购订单号：</div>\r\n'
       '    <div>\r\n'
       '      <div class="input-box select-box" style="width:380px;"><select style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"><option selected>PO-20260902-018（苏州联恒 · 零部件 · 锁扣组件/铰链）</option><option>PO-20260828-015（苏州联恒 · 零部件 · 箱盖）</option></select><span class="caret">▾</span></div>\r\n'
       '      <div style="margin-top:6px;font-size:12px;color:#8c8c8c;">凭单验收：到货数量须与采购订单明细匹配，方可提交验收（无单不入库）</div>\r\n'
       '    </div>\r\n'
       '  </div>\r\n') + old
edit(p1, old, new)

# ---------- C2 销售出库新建：关联销售订单后插「库存可用量」提示（模板 LF + 列表页内嵌 CRLF 同步） ----------
old_tpl = ('  </div><div class="form-row">\n'
           '    <span class="form-label"><span class="req">*</span>出库仓库</span>')
hint = ('  </div><div class="form-row">\n'
        '    <span class="form-label"></span>\n'
        '    <div style="font-size:12px;color:#8c8c8c;line-height:1.7;">库存可用量：内衬 EPE 珍珠棉（LJ-F600）在库 <b style="color:#1677ff;">1,520</b> 件 · 原料区 RA —— 按库存可用量发货，超量需先入库</div>\n'
        '  </div><div class="form-row">\n'
        '    <span class="form-label"><span class="req">*</span>出库仓库</span>')
edit(BASE + r'\仓储作业\弹窗\销售出库新建.html', old_tpl, hint)
edit(BASE + r'\仓储作业\销售出库列表.html', old_tpl.replace('\n', '\r\n'), hint.replace('\n', '\r\n'))

# ---------- C3 新建采购订单：物料类型两级级联 + 关联销售订单话术弱化（模板 LF + 列表页内嵌 CRLF） ----------
SEL = 'style="flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;"'
CARET = '<span class="caret"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>'

old_type = ('<span class="form-label"><span class="req">*</span>物料类型</span>\n'
            '    <div class="input-box select-box" style="width:350px;"><select ' + SEL + '><option selected>零部件</option><option>WBX-1210L 围板箱</option><option>PLT-1210P 塑料托盘</option><option>BTC-6040 料箱</option><option>LJ-A100 护角</option></select>')
new_type = ('<span class="form-label"><span class="req">*</span>物料类型</span>\n'
            '    <div class="input-box select-box" style="width:350px;"><select onchange="var r=document.getElementById(\'poQjRow\');if(r)r.style.display=(this.options[this.selectedIndex].text==\'器具\')?\'flex\':\'none\'" ' + SEL + '><option selected>零部件</option><option>器具</option></select>')

old_next = ('  </div><div class="form-row">\n'
            '    <span class="form-label">关联销售订单号</span>\n'
            '    <div class="input-box" style="width:350px;"><input placeholder="选填，先销后采时自动带出"></div>\n'
            '  </div>')
new_next = ('  </div><div class="form-row" id="poQjRow" style="display:none;">\n'
            '    <span class="form-label"><span class="req">*</span>器具档案</span>\n'
            '    <div class="input-box select-box" style="width:350px;"><select ' + SEL + '><option selected>WBX-1210L 围板箱</option><option>PLT-1210P 塑料托盘</option><option>BTC-6040 料箱</option></select>' + CARET + '</div>\n'
            '  </div><div class="form-row">\n'
            '    <span class="form-label">关联销售订单号</span>\n'
            '    <div class="input-box" style="width:350px;"><input placeholder="选填 · 仅参考关联（非以销定采）"></div>\n'
            '  </div>')

edit(BASE + r'\采购管理\弹窗\新建采购订单.html', old_type, new_type)
edit(BASE + r'\采购管理\弹窗\新建采购订单.html', old_next, new_next)
edit(BASE + r'\采购管理\采购订单列表.html', old_type.replace('\n', '\r\n'), new_type.replace('\n', '\r\n'))
edit(BASE + r'\采购管理\采购订单列表.html', old_next.replace('\n', '\r\n'), new_next.replace('\n', '\r\n'))

# ---------- 校验 ----------
import re
for f, checks in [
    (p1, [('关联采购订单号', 1), ('PO-20260902-018', 1), ('无单不入库', 1)]),
    (BASE + r'\仓储作业\弹窗\销售出库新建.html', [('库存可用量', 1), ('1,520', 1)]),
    (BASE + r'\仓储作业\销售出库列表.html', [('库存可用量', 1)]),
    (BASE + r'\采购管理\弹窗\新建采购订单.html', [('poQjRow', 2), ('非以销定采', 1), ('<option>器具</option>', 1), ('WBX-1210L 围板箱</option>', 1)]),
    (BASE + r'\采购管理\采购订单列表.html', [('poQjRow', 2), ('非以销定采', 1), ('先销后采时自动带出', 0)]),
]:
    s = io.open(f, encoding='utf-8', newline='').read()
    for kw, n in checks:
        c = s.count(kw)
        assert c == n, '%s 校验失败 %s expect=%d got=%d' % (f, kw, n, c)
    print('校验通过', f.split('\\')[-1])
print('C批页面修改完成')
