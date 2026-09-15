# -*- coding: utf-8 -*-
"""G33 T3: 菜单 v4 -> v5 全站侧边栏同步（幂等）
新增三项：采购退货（采购管理组·采购入库后）/销售退货（销售管理组·销售出库后）/退款登记（财务管理组·付款登记后）
"""
import io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # _scan_tmpdir 的上级 = 项目根
PROTO = os.path.join(ROOT, 'P3-R01-包装租赁管理后台原型')

NEW_ITEMS = [
    # (锚点判别子串[含 onclick 版], 锚点判别子串[selected 版], 新行)
    (
        "onclick=\"go('../采购管理/采购入库列表.html')\">采购入库",
        'class="sm-link selected">采购入库</div>',
        '<li><div class="sm-link" onclick="go(\'../采购管理/采购退货单列表.html\')">采购退货</div></li>',
    ),
    (
        "onclick=\"go('../销售管理/销售出库列表.html')\">销售出库",
        'class="sm-link selected">销售出库</div>',
        '<li><div class="sm-link" onclick="go(\'../销售管理/销售退货单列表.html\')">销售退货</div></li>',
    ),
    (
        "onclick=\"go('../财务协同/付款登记.html')\">付款登记",
        'class="sm-link selected">付款登记</div>',
        '<li><div class="sm-link" onclick="go(\'../财务协同/退款登记.html\')">退款登记</div></li>',
    ),
]
NEW_KEYS = ['采购退货单列表.html', '销售退货单列表.html', '退款登记.html']

changed_files = []
total_ins = {k: 0 for k in NEW_KEYS}

for dirpath, dirnames, filenames in os.walk(PROTO):
    rel = os.path.relpath(dirpath, PROTO)
    if rel.startswith('_data') or rel.startswith('mobile'):
        continue
    for fn in filenames:
        if not fn.endswith('.html'):
            continue
        fp = os.path.join(dirpath, fn)
        with io.open(fp, 'r', encoding='utf-8', newline='') as f:
            src = f.read()
        if 'class="sm-link' not in src:
            continue
        out = src
        touched = False
        for (a_onclick, a_selected, newline), nkey in zip(NEW_ITEMS, NEW_KEYS):
            # 幂等：新菜单行（onclick 引用新页）已存在则跳过
            if ("go('../" + nkey) in out:
                continue
            lines = out.split('\n')
            newlines = []
            ins = 0
            for ln in lines:
                newlines.append(ln)
                if (a_onclick in ln) or (a_selected in ln):
                    newlines.append(newline)
                    ins += 1
            if ins == 0:
                continue
            assert ins == 1, 'G33 菜单锚点命中 %d 次(应 1): %s / %s' % (ins, fp, nkey)
            out = '\n'.join(newlines)
            touched = True
            total_ins[nkey] += ins
        if touched:
            # 标签配平自检：li 数量配平（新增行自带闭合）
            assert out.count('<li>') >= src.count('<li>'), 'li 计数异常: ' + fp
            with io.open(fp, 'w', encoding='utf-8', newline='') as f:
                f.write(out)
            changed_files.append(os.path.relpath(fp, PROTO))

print('=== G33 T3 菜单 v5 同步 ===')
print('改动文件数: %d' % len(changed_files))
for k in NEW_KEYS:
    print('新项 %s 插入次数: %d' % (k, total_ins[k]))
for c in sorted(changed_files):
    print('  ' + c)
