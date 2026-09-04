# -*- coding: utf-8 -*-
"""R5a：同 id modal-overlay 去重。
规则：① 标题「新建项目」的 createModal 为构建期污染，非项目档案页一律删除
     ② 组合出库列表 auditModal x3：出库确认份改 id=exitConfirmModal，末份删，首份保留
     ③ 其余同 id 组保留内容最长份，删其余
校验：处理后各页 modal id 唯一。"""
import io, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
MRE = re.compile(r'<div class="modal-overlay[^"]*" id="([a-zA-Z]+)"')

def find_close(s, start):
    depth = 0
    for m in re.finditer(r'<div\b|</div>', s[start:]):
        if m.group(0) == '</div>':
            depth -= 1
            if depth == 0: return start + m.end()
        else: depth += 1
    return -1

total_del, total_mod = 0, 0
for p in sorted(glob.glob(f'{BASE}/**/*.html', recursive=True)):
    if '弹窗' in p: continue
    rel = p.replace(BASE + '\\', '')
    s = io.open(p, encoding='utf-8', newline='').read()
    groups = {}
    for m in MRE.finditer(s):
        end = find_close(s, m.start())
        if end < 0: continue
        t = re.search(r'modal-title">([^<]*)', s[m.start():end])
        groups.setdefault(m.group(1), []).append([m.start(), end, (t.group(1).strip() if t else '?')])
    dups = {k: v for k, v in groups.items() if len(v) > 1}
    if not dups: continue
    drop_spans, renames = [], []
    for mid, lst in dups.items():
        if rel == '仓储作业\\组合出库列表.html' and mid == 'auditModal':
            # 份2(出库确认,1460) 改 id；份3(1367) 删；份1 保留
            lst.sort(key=lambda x: x[0])
            drop_spans.append((lst[2][0], lst[2][1]))
            renames.append((lst[1][0], lst[1][1]))
            continue
        proj = [x for x in lst if x[2] == '新建项目']
        if proj and len(lst) > 1 and rel != '项目管理\\项目档案.html':
            for x in proj: drop_spans.append((x[0], x[1]))
            rest = [x for x in lst if x not in proj]
            if len(rest) > 1:  # 剩余仍重复，保最长
                keep = max(rest, key=lambda x: x[1] - x[0])
                for x in rest:
                    if x is not keep: drop_spans.append((x[0], x[1]))
        else:
            keep = max(lst, key=lambda x: x[1] - x[0])
            for x in lst:
                if x is not keep: drop_spans.append((x[0], x[1]))
    if not drop_spans and not renames: continue
    # 逆序删除（防位移）
    out, cuts = s, sorted(drop_spans, reverse=True)
    div_in_cuts = sum(s[a:b].count('<div') for a, b in cuts)
    for a, b in cuts:
        out = out[:a] + out[b:]
        total_del += 1
    # 改 id（出库确认份）
    if rel == '仓储作业\\组合出库列表.html':
        m = re.search(r'<div class="modal-overlay[^"]*" id="auditModal">(?:(?!</div>\s*<div class="modal-overlay).)*?出库确认', out, re.S)
        if m:
            out = out[:m.start()] + out[m.start():m.end()].replace('id="auditModal"', 'id="exitConfirmModal"', 1) + out[m.end():]
            total_mod += 1
    # 校验唯一
    ids = MRE.findall(out)
    assert len(ids) == len(set(ids)), (rel, ids)
    # 标签配平
    assert out.count('<div') == s.count('<div') - div_in_cuts, rel
    io.open(p, 'w', encoding='utf-8', newline='').write(out)
    print(f'{rel}: 删 {len(cuts)} 份' + ('，出库确认改 id=exitConfirmModal' if renames else ''), '| 保留:', {k: 1 for k in dups})
print(f'=== R5a 完成：共删 {total_del} 份，改 id {total_mod} 处 ===')
