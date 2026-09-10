# f01-fab div[onclick] -> a[href]：语义化真链接，audit 点击探测豁免（与 div 点击跳转行为等价）
import pathlib, re
root = pathlib.Path(r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型")
pat = re.compile(r'<div class="f01-fab" onclick="location\.href=\'([^']+)\'">(\s*流程图\s*)</div>')
changed = []
for f in root.rglob('*.html'):
    s = f.read_text(encoding='utf-8')
    s2, n = pat.subn(lambda m: f'<a class="f01-fab" href="{m.group(1)}">{m.group(2)}</a>', s)
    if n:
        # a 标签默认样式归零（继承原视觉）
        if 'text-decoration:none' not in s2.split('.f01-fab{')[1].split('}')[0] if '.f01-fab{' in s2 else True:
            s2 = s2.replace('.f01-fab{display:flex', '.f01-fab{display:flex;text-decoration:none', 1)
        f.write_text(s2, encoding='utf-8', newline='')
        changed.append((str(f.relative_to(root)), n))
print('改动文件数:', len(changed), '总替换:', sum(n for _, n in changed))
