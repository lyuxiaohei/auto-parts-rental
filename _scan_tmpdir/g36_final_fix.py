# -*- coding: utf-8 -*-
import io, json, re, sys, os
sys.path.insert(0, '_scan_tmpdir')
from g36_factory import rd, wr

# 1) 越界 ../../ 修复（内部链接降级为 ../）
for p in ['租入管理/租入单新建.html', '租入管理/租入归还新建.html', '租赁管理/租赁单新建.html', '系统管理/权限配置.html', '销售管理/销售订单新建.html']:
    s = rd(p)
    n = s.count('../../')
    s = s.replace('../../', '../')
    wr(p, s)
    print(p, ': ../../ x%d -> ../' % n)

# 2) 新页 readonly 预填输入 → 可编辑＋灰底样式
r = json.load(io.open('_scan_tmpdir/audit_results.json', encoding='utf-8'))
pages = r if isinstance(r, list) else r.get('pages', r)
if isinstance(pages, dict):
    pages = list(pages.values())
targets = {}
for pg in pages:
    for q in pg.get('problems', []):
        if q.get('type') == 'input-not-editable':
            k = pg['page'].replace(os.sep, '/')
            targets[k] = targets.get(k, 0) + 1
print('readonly 问题页:', targets)
total = 0
for p in targets:
    s = rd(p)
    out = []
    pos = 0
    for m in re.finditer(r'<input[^>]*>', s):
        tag = m.group(0)
        if 'readonly' in tag or 'readOnly' in tag:
            total += 1
            tag = tag.replace(' readonly', '').replace('readonly ', '').replace(' readOnly', '').replace('readOnly ', '')
            if 'style="' in tag:
                tag = tag.replace('style="', 'style="background:#fafafa;color:#8c8c8c;', 1)
            else:
                tag = tag.replace('<input', '<input style="background:#fafafa;color:#8c8c8c;"', 1)
        out.append(s[pos:m.start()])
        out.append(tag)
        pos = m.end()
    out.append(s[pos:])
    wr(p, ''.join(out))
    print(p, ': readonly 转换 ✓')
print('共转换 %d 个 readonly 输入' % total)
