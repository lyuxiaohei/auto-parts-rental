# -*- coding: utf-8 -*-
"""G31 T2：税率区结算周期下拉化 + 物料型号/内部编码（双层）"""
import io, re, os

PROTO = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
Q = chr(39)  # '
D = chr(34)  # "

OLD_INPUT = ("+ '<span class=" + D + "tax-cell" + D + "><input class=" + D + "tax-in" + D + " value=" + D + "' + esc(cyc || '月结 30 天') + '" + D + "></span>'")
NEW_SEL = ("+ '<span class=" + D + "tax-cell" + D + "><select class=" + D + "tax-sel" + D + ">' + ['月结','发票后 30 天','发票后 60 天','发票后 90 天','发票后 120 天'].map(function(o){return '<option'+(o===(cyc||'月结')?' selected':'')+'>'+o+'</option>';}).join('') + '</select></span>'")

ADD = ('<div class="form-row">' + chr(10) +
       '    <span class="form-label">型号</span>' + chr(10) +
       '    <div class="input-box"><input placeholder="选填"></div>' + chr(10) +
       '  </div><div class="form-row">' + chr(10) +
       '    <span class="form-label">内部编码</span>' + chr(10) +
       '    <div class="input-box"><input placeholder="选填 · 供应商/客户方产品编码"></div>' + chr(10) +
       '  </div>')

def main():
    for rel in ['基础数据/产品档案.html', '基础数据/弹窗/新建产品.html']:
        p = os.path.join(PROTO, rel)
        s = io.open(p, encoding='utf-8', newline='').read()
        c = s.count(OLD_INPUT)
        assert c == 1, ('tax-input anchor', rel, c)
        s = s.replace(OLD_INPUT, NEW_SEL, 1)
        io.open(p, 'w', encoding='utf-8', newline='').write(s)
        print(rel, ': 税率区结算周期 手填→下拉 OK')
    for rel in ['基础数据/产品档案.html', '基础数据/弹窗/新建产品.html']:
        p = os.path.join(PROTO, rel)
        s = io.open(p, encoding='utf-8', newline='').read()
        m = re.search(r'(<div class="form-row">\s*<span class="form-label">(?:<span class="req">\*</span>)?物料编码</span>.*?</div>\s*</div>)', s, re.S)
        assert m, '物料编码 row not found ' + rel
        s = s.replace(m.group(1), m.group(1) + ADD, 1)
        io.open(p, 'w', encoding='utf-8', newline='').write(s)
        print(rel, ': +型号+内部编码 OK')

if __name__ == '__main__':
    main()
