# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
F = Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型\_data\demo-data.js")
s = F.read_bytes().decode('utf-8')
NL = '\r\n' if '\r\n' in s else '\n'
i = s.index('salesOrders: {'); j = s.index('purchaseInbounds: {', i)
sec = s[i:j]
pat = re.compile(r"(\{\s*'label': '状态',\s*'tag': '[^']+'\s*\},)")
sec2, k = pat.subn(lambda mm: mm.group(1) + NL + "        {'label': '订单附件', 'text': 'PO-2601-围板箱采购合同.pdf · 客户下单确认邮件截图.png（新建可上传/删除，演示）'},", sec)
assert k == 8, f"附件 info 锚 {k} 处（期望 8）"
s = s[:i] + sec2 + s[j:]
F.write_bytes(s.encode('utf-8'))
print("demo-data.js OK：salesOrders 订单附件 info 行 ×8")
