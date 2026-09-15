# -*- coding: utf-8 -*-
"""修复 C2 脚本注入位置：从 renderListPage cfg 的 script 内部移出，插到该 script 块 </script> 之后"""
import io, os

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
FP = os.path.join(ROOT, '仓储作业', '库存查询.html')
s = io.open(FP, encoding='utf-8', newline='').read()

a = s.index('\n<script>\n/* G36 C2')
b = s.index('</script>', a) + len('</script>')
block = s[a:b]
assert 'qtyByProject' in block and 'recalcDrill' in block
s = s[:a] + s[b:]
print('移除内嵌误置块（%d 字符）' % len(block))

# 重新插入：cfg 所在 script 的 </script> 之后（独立块）
anchor = s.index("modalId: 'flowModal'")
end = s.index('</script>', anchor) + len('</script>')
# 吸收其后的换行
while end < len(s) and s[end] in '\r\n':
    end += 1
s = s[:end] + block + '\n' + s[end:]
io.open(FP, 'w', encoding='utf-8', newline='').write(s)
print('重插至 cfg script 块之后 ✓')
# 校验：块不在任何 <script> 内部——cfg </script> 之后紧跟 '<script>'
i = s.index(block)
prev_close = s.rfind('</script>', 0, i)
prev_open = s.rfind('<script', 0, i)
assert prev_close > prev_open, 'still inside a script block!'
print('位置校验通过（块前最近的标签是 </script>）')
