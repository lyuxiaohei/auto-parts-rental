# -*- coding: utf-8 -*-
"""深度曲线对比：不平衡页 vs 平衡同族页，定位缺失闭合位置"""
import io, re, os

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
PAIRS = [('仓储作业/其他入库列表.html', '仓储作业/盘点列表.html'),
         ('财务协同/退款登记.html', '财务协同/开票登记.html')]

for bad, good in PAIRS:
    for name in (bad, good):
        fp = os.path.join(ROOT, name.replace('/', os.sep))
        s = io.open(fp, encoding='utf-8', newline='').read()
        lines = s.split('\n')
        d = 0
        marks = []
        for i, ln in enumerate(lines, start=1):
            o = len(re.findall(r'<div(?:\s[^>]*)?>', ln))
            c = len(re.findall(r'</div>', ln))
            d += o - c
            marks.append((i, d, o, c, ln.strip()[:80]))
        # 找到最后一个 </table> 行作为锚，打印其后 30 行
        anchor = None
        for i, ln in enumerate(lines, start=1):
            if '</table>' in ln:
                anchor = i
        print('=' * 32, name, '| 末尾深度 =', d, '| 最后 </table> 行 =', anchor)
        if anchor:
            for (i, dd, o, c, t) in marks:
                if anchor - 2 <= i <= anchor + 26 and t:
                    print('%4d d=%-3d (+%d/-%d) %s' % (i, dd, o, c, t))
        print()
