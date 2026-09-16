#!/usr/bin/env python3
# G42 T7a: partners 8 家补 invoiceTaxNo + info2 开票资料段；detail-generic.js 扩 info2 可选段
import io, re, sys

ROOT = '/Users/bailey/Desktop/xiaohei-workplace/auto-parts-rental/P3-R01-包装租赁管理后台原型'
DD = ROOT + '/_data/demo-data.js'
DG = ROOT + '/_data/detail-generic.js'

# ---- 编造规范（任务书 T7a）：18 位：'9' + '1' + '131015'(3~8位) + 'MA1F'+序号大写字母数字(9~17位) + 末位数字(mod10) ----
def taxno(seq):
    body = '9' + '1' + '131015' + 'MA1F' + seq          # 17 位
    chk = sum(ord(c) for c in body) % 10                # 末位数字（可复算）
    return body + str(chk)

PARTNERS = [
    # key, seq(5位大写字母数字), 发票类型, 开户行, 账号, 结算周期
    ('DW-0001', 'A0001', '增值税专票 13%', '工商银行长春汽车厂支行',   '0800221109100123456', '月结'),
    ('DW-0002', 'A0002', '增值税专票 13%', '建设银行宁波分行',         '6217001230056689',    '月结'),
    ('DW-0003', 'A0003', '增值税专票 13%', '中国银行合肥滨湖支行',     '3411222009887',       '发票后 30 天'),
    ('DW-0004', 'A0004', '增值税专票 13%', '农业银行西安经开区支行',   '1020681209966',       '月结'),
    ('DW-0101', 'A0005', '增值税专票 13%', '宁波银行鄞州支行',         '3102010099876',       '月结'),
    ('DW-0102', 'A0006', '增值税专票 13%', '招商银行苏州分行',         '5129066012213',       '发票后 30 天'),
    ('DW-0103', 'A0007', '增值税专票 13%', '江苏银行常州新北支行',     '3204109001120',       '货到付款'),
    ('DW-0201', 'A0008', '增值税专票 13%', '建设银行上海分行',         '3100156820005001234', '预付'),
]

s = io.open(DD, encoding='utf-8').read()

for key, seq, invtype, bank, acct, settle in PARTNERS:
    tax = taxno(seq)
    # 1) fields 行插 invoiceTaxNo（锚：该键块内 'row': {"fields": 行的 "contact": "<v>",）
    m_key = s.index("    '%s': {" % key)
    m_row = s.index("'row': {\"fields\":", m_key)
    m_line_end = s.index('\n', m_row)
    rowline = s[m_row:m_line_end]
    m_contact = re.search(r'"contact": "([^"]+)",', rowline)
    assert m_contact, key + ' contact anchor missing'
    assert 'invoiceTaxNo' not in rowline, key + ' already has invoiceTaxNo'
    newline = rowline.replace(m_contact.group(0), m_contact.group(0)[:-1] + ' "invoiceTaxNo": "%s",' % tax, 1)
    s = s[:m_row] + newline + s[m_line_end:]
    # 2) info2 段插在 'feeSecTitle' 行前（该键块内首个）
    m_key = s.index("    '%s': {" % key)
    m_fee = s.index("      'feeSecTitle':", m_key)
    info2 = (
        "      'info2Title': '开票资料',\n"
        "      'info2': [\n"
        "        {\n          'label': '发票类型',\n          'text': '%s'\n        },\n"
        "        {\n          'label': '纳税人识别号',\n          'text': '%s'\n        },\n"
        "        {\n          'label': '开户行',\n          'text': '%s'\n        },\n"
        "        {\n          'label': '账号',\n          'text': '%s'\n        },\n"
        "        {\n          'label': '结算周期',\n          'text': '%s'\n        }\n"
        "      ],\n"
    ) % (invtype, tax, bank, acct, settle)
    s = s[:m_fee] + info2 + s[m_fee:]

assert s.count('invoiceTaxNo') == 8, s.count('invoiceTaxNo')
assert s.count("'info2Title': '开票资料'") == 8
io.open(DD, 'w', encoding='utf-8').write(s)
print('demo-data.js: 8x invoiceTaxNo + 8x info2 injected')
for key, seq, *_ in PARTNERS:
    print(' ', key, taxno(seq))

# ---- detail-generic.js：info 段后扩可选 info2 段（守卫式，其他页零影响） ----
g = io.open(DG, encoding='utf-8').read()
anchor = "      h1 += '</div>';\n\n    if (rec.feeCols && rec.fees) {"
assert g.count(anchor) == 1, 'detail-generic anchor count=' + str(g.count(anchor))
inject = """      h1 += '</div>';

    /* G42 T7a：可选第二信息段（如客商详情·开票资料）——无 info2 键的页面零影响 */
    if (rec.info2) {
      h1 += '<div class="dt-sec">' + (rec.info2Title || '更多信息') + '</div><div class="dgrid c3">';
      rec.info2.forEach(function (f) {
        var v;
        if (f.tag) v = '<span class="tag ' + (STATUS_CLS[f.tag] || 'tag-gray') + '">' + f.tag + '</span>';
        else v = lk(f.text, f.url, base);
        h1 += drow(f.label, v, f.full);
      });
      h1 += '</div>';
    }

    if (rec.feeCols && rec.fees) {"""
g = g.replace(anchor, inject)
io.open(DG, 'w', encoding='utf-8').write(g)
print('detail-generic.js: info2 section support added')
