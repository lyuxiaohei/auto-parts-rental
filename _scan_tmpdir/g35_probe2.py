# -*- coding: utf-8 -*-
import io, re
ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
txt = io.open(ROOT + r'\_data\demo-data.js', encoding='utf-8').read()
print('demo-data CRLF:', '\r\n' in txt)
# opLogs rows: print each row's key + fields line + cells line (truncated)
i = txt.find('  opLogs: {')
j = txt.find('\n  },', i)
seg = txt[i:j]
print('=== opLogs block len:', len(seg), '===')
PAT = re.compile(r"'(OP-[0-9-]+|[A-Z][A-Z0-9-]+)': \{ 'row': \{..fields..: (\{[^\n]*?\})\}, ..cells..: (\[[^\n]*?\])".replace('..', chr(34)))
for m in PAT.finditer(seg):
    print(m.group(1), '|', m.group(2)[:160])
    print('   cells:', m.group(3)[:360])
print()
i = txt.find('  purchaseInbounds: {')
j = txt.find('\n  },', i)
seg = txt[i:j]
print('=== purchaseInbounds block len:', len(seg), '===')
for m in PAT.finditer(seg):
    print(m.group(1), '|', m.group(2)[:150])
    print('   cells:', m.group(3)[:400])
