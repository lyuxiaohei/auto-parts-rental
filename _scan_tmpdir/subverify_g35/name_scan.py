# -*- coding: utf-8 -*-
"""G35 独立验收·真名清零扫描：任务书第四节全部 36 个真名词 + 碎片词，在原型目录全部文本文件逐词 str.count。"""
import io
from pathlib import Path

ROOT = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型')
EXTS = {'.html', '.js', '.md', '.json', '.css'}

WORDS = [
    # 企业名 21
    '一汽解放汽车有限公司', '一汽解放',
    '上汽大众汽车有限公司宁波分公司', '上汽大众',
    '小鹏汽车科技有限公司', '小鹏汽车',
    '东风本田汽车有限公司', '东风本田',
    '东风锂电科技', '上汽通用五菱', '吉利汽车',
    '路凯包装运营（上海）有限公司', '路凯',
    '宁波华塑包装制品有限公司', '华塑',
    '苏州联恒五金制品有限公司', '苏州联恒', '联恒',
    '常州正大塑料托盘厂', '常州正大', '正大',
    # 人名 15
    '王琳', '王琳总', '袁丽晶', '袁工', '吕道远', '徐蔚', '李国栋',
    '王强', '陈金', '赵磊', '何静', '李静', '王志远', '袁明', '张伟',
]
FRAGS = ['一汽', '上汽', '东风', '本田', '小鹏', '吉利', '五菱', 'FAW']

counts = {w: 0 for w in WORDS + FRAGS}
files_scanned = 0
hits = []

for f in ROOT.rglob('*'):
    if not f.is_file() or f.suffix.lower() not in EXTS:
        continue
    files_scanned += 1
    try:
        t = io.open(f, encoding='utf-8').read()
    except Exception as e:
        print('READ_FAIL', f, e)
        continue
    for w in WORDS + FRAGS:
        c = t.count(w)
        if c:
            counts[w] += c
            hits.append((str(f.relative_to(ROOT)), w, c))

print('files_scanned:', files_scanned)
print('--- 36 词计数 ---')
bad = 0
for w in WORDS:
    print('%s = %d' % (w, counts[w]))
    if counts[w]:
        bad += 1
print('--- 碎片词计数 ---')
for w in FRAGS:
    print('%s = %d' % (w, counts[w]))
    if counts[w]:
        bad += 1
print('--- 残留命中明细（应为空）---')
for h in hits:
    print(h)
print('NONZERO_WORDS:', bad)
