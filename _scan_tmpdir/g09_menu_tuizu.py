# -*- coding: utf-8 -*-
"""G09: 菜单 v3.4——退租入库移入「租赁」小标签（租赁出库之下），取消「退租」小标签
38 页侧边栏：删退租标签 li ×1 + 退租入库 li 移至租赁出库 li 之后 ×1（逐文件 assert）
"""
import shutil
from pathlib import Path

PROTO = Path(r'P3-R01-包装租赁管理后台原型')
BACKUP = Path(r'_scan_tmpdir/backup-g09-20260910')

TAG = '   <li style="padding:4px 0 2px 48px;font-size:10px;color:#8c8c8c;letter-spacing:.08em;user-select:none;list-style:none">退租</li>'
ITEM_FORMS = [
    '   <li><div class="sm-link" onclick="go(\'../租赁管理/退租入库列表.html\')">退租入库</div></li>',
    '   <li><div class="sm-link" onclick="go(\'租赁管理/退租入库列表.html\')">退租入库</div></li>',
    '   <li><div class="sm-link selected">退租入库</div></li>',
]
ANCHOR_FORMS = [
    '   <li><div class="sm-link" onclick="go(\'../租赁管理/组合出库列表.html\')">租赁出库</div></li>',
    '   <li><div class="sm-link" onclick="go(\'租赁管理/组合出库列表.html\')">租赁出库</div></li>',
    '   <li><div class="sm-link selected">租赁出库</div></li>',
]

files = sorted(p for p in PROTO.rglob('*.html') if TAG in p.read_text(encoding='utf-8'))
assert len(files) == 38, f'命中 {len(files)} (expect 38)'

for f in files:
    rel = f.relative_to(PROTO)
    s = f.read_text(encoding='utf-8')
    nl = '\r\n' if '\r\n' in s else '\n'
    assert s.count(TAG) == 1, f'{rel}: 退租标签 count != 1'
    item = next((it for it in ITEM_FORMS if s.count(it) == 1), None)
    assert item, f'{rel}: 退租入库项未唯一命中'
    anchor = next((a for a in ANCHOR_FORMS if s.count(a) == 1), None)
    assert anchor, f'{rel}: 租赁出库锚未唯一命中'
    # 备份
    bf = BACKUP / rel
    bf.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(f, bf)
    # 删标签行 + 剪出退租入库项 + 插到租赁出库之后
    s = s.replace(TAG + nl, '')
    s = s.replace(item + nl, '')
    s = s.replace(anchor + nl, anchor + nl + item + nl)
    # 顺序断言：租赁出库 < 退租入库 < 租入标签
    i_out = s.index('>租赁出库</div>')
    i_tz = s.index('>退租入库</div>')
    i_zr = s.index('list-style:none">租入</li>')
    assert i_out < i_tz < i_zr, f'{rel}: 顺序异常 {i_out} {i_tz} {i_zr}'
    f.write_text(s, encoding='utf-8', newline='')

print('OK · 38 页侧边栏：退租入库 → 租赁标签（租赁出库之下），退租小标签移除')
