# -*- coding: utf-8 -*-
"""G31 T1 菜单 v4：小标签取消 + 租入管理升一级
Transform: 38 sidebar files + 全站引用替换（.html/.js）
Discipline: 读取-精确替换 + assert 计数；io.open(newline='') 防行尾改写
"""
import io, os, re, sys

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
LABEL = r'<li style="padding:4px 0 2px 48px;font-size:10px;color:#8c8c8c;letter-spacing:\.08em;user-select:none;list-style:none">(LABELTXT)</li>'
RENTIN_GROUP = (
    '      <li class="sm-item has-sub%(OPEN)s">\r\n'
    '   <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 15 12 15 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg></span>租入管理<span class="sm-arrow"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>\r\n'
    '   <ul class="sm-sub">\r\n'
    '   <li><div class="sm-link%(SEL1)s" onclick="go(\'../租入管理/租入单列表.html\')">租入单</div></li>\r\n'
    '   <li><div class="sm-link%(SEL2)s" onclick="go(\'../租入管理/租入入库列表.html\')">租入入库</div></li>\r\n'
    '   <li><div class="sm-link%(SEL3)s" onclick="go(\'../租入管理/租入归还列表.html\')">租入归还</div></li>\r\n'
    '   </ul>\r\n'
    '      </li>\r\n'
)

def li_balance(s):
    return (len(re.findall(r'<li[\s>]', s)), len(re.findall(r'</li>', s)),
            len(re.findall(r'<ul[\s>]', s)), len(re.findall(r'</ul>', s)))

def transform_sidebar(path, is_rentin_page, rentin_idx):
    src = io.open(path, encoding='utf-8', newline='').read()
    if '>租入管理<' in src:
        return True  # 幂等：已改版
    orig = src
    b0 = li_balance(src)
    # B: 删 租入 小标签 + 3 项（含 selected 变体）
    pat_B = re.compile(r'\s*' + LABEL.replace('(LABELTXT)', '租入') + r'.*?租入归还</div></li>', re.S)
    src, nB = pat_B.subn('', src, count=1)
    assert nB == 1, f'B fail {path}'
    # A: 删 租赁 小标签
    pat_A = re.compile(r'\s*' + LABEL.replace('(LABELTXT)', '租赁'))
    src, nA = pat_A.subn('', src, count=1)
    assert nA == 1, f'A fail {path}'
    # C: 删 仓储组 3 小标签
    nC = 0
    for t in ('库存管理', '入库类', '出库类'):
        pat = re.compile(r'\s*' + LABEL.replace('(LABELTXT)', t))
        src, n = pat.subn('', src, count=1)
        nC += n
        assert n == 1, f'C[{t}] fail {path} n={n}'
    # E: 租入页——租赁组去 open
    if is_rentin_page:
        k = src.find('仓储管理<span')  # 仓储组定位先（D 前结构不变）
        li_start = src.rfind('<li class="sm-item', 0, src.find('租赁管理<span'))
        seg = src[li_start:li_start + 40]
        assert 'has-sub open' in seg, f'E open not found {path}: {seg}'
        src = src[:li_start] + seg.replace('has-sub open', 'has-sub', 1) + src[li_start + 40:]
    # D: 仓储组前插入 租入管理组
    fmt = dict(OPEN=' open' if is_rentin_page else '',
               SEL1=' selected' if rentin_idx == 1 else '',
               SEL2=' selected' if rentin_idx == 2 else '',
               SEL3=' selected' if rentin_idx == 3 else '')
    grp = RENTIN_GROUP % fmt
    anchor = src.rfind('<li class="sm-item', 0, src.find('仓储管理<span'))
    assert anchor > 0, f'D anchor fail {path}'
    src = src[:anchor] + grp + src[anchor:]
    # selected 项去掉 onclick（自页无跳转）
    if rentin_idx:
        src = re.sub(r'<div class="sm-link selected" onclick="go\(\'../租入管理/(租入[^.]+\.html)\'\)">',
                     lambda m: '<div class="sm-link selected">', src, count=1)
    b1 = li_balance(src)
    assert b1[0] == b1[1] and b1[2] == b1[3], f'balance fail {path}: {b1}'
    # 租入管理组恰好 1 个、菜单项 3 个
    assert src.count('租入管理<span') == 1, f'group count fail {path}'
    if rentin_idx == 0:
        assert src.count('../租入管理/租入单列表.html') == 1, f'item1 fail {path}'
    else:
        assert 'class="sm-link selected">租入' in src, f'selected fail {path}'
    if src != orig:
        io.open(path, 'w', encoding='utf-8', newline='').write(src)
    return True

def main():
    side_files = []
    for dp, dns, fns in os.walk(ROOT):
        if '.git' in dp or 'backup-' in dp: continue
        for fn in fns:
            if fn.endswith('.html'):
                p = os.path.join(dp, fn)
                if 'sm-item has-sub' in io.open(p, encoding='utf-8', errors='replace').read():
                    side_files.append(p)
    assert len(side_files) == 38, f'sidebar files={len(side_files)}'
    rentin_map = {os.path.join(ROOT, '租入管理', f): i for f, i in
                  [('租入单列表.html', 1), ('租入入库列表.html', 2), ('租入归还列表.html', 3)]}
    done = 0
    for p in sorted(side_files):
        is_rp = p in rentin_map
        transform_sidebar(p, is_rp, rentin_map.get(p, 0))
        done += 1
    print(f'T1 sidebar OK: {done}/38 transformed (租入页 open+selected ×3)')

    # 全站引用替换（.html/.js）
    expect = {'租赁管理/租入单列表.html': '租入管理/租入单列表.html',
              '租赁管理/租入入库列表.html': '租入管理/租入入库列表.html',
              '租赁管理/租入归还列表.html': '租入管理/租入归还列表.html'}
    totals = {k: 0 for k in expect}
    for dp, dns, fns in os.walk(ROOT):
        if '.git' in dp or 'backup-' in dp: continue
        for fn in fns:
            if not fn.endswith(('.html', '.js')): continue
            p = os.path.join(dp, fn)
            src = io.open(p, encoding='utf-8', newline='').read()
            orig = src
            for k, nk in expect.items():
                c = src.count(k)
                if c:
                    src = src.replace(k, nk)
                    totals[k] += c
            if src != orig:
                io.open(p, 'w', encoding='utf-8', newline='').write(src)
    for k, nk in expect.items():
        print(f'ref {k} -> {nk}: {totals[k]} 处')
        pass  # 幂等重入可为 0；以残留=0 为准
    # 残留检查
    resid = 0
    for dp, dns, fns in os.walk(ROOT):
        if '.git' in dp or 'backup-' in dp: continue
        for fn in fns:
            if not fn.endswith(('.html', '.js')): continue
            src = io.open(os.path.join(dp, fn), encoding='utf-8', errors='replace').read()
            resid += sum(src.count(k) for k in expect)
    assert resid == 0, f'残留 {resid}'
    print('T1 ref-replace OK: 残留 0')
    # .md 残留报告（不改，仅报）
    for dp, dns, fns in os.walk(ROOT):
        if '.git' in dp or 'backup-' in dp: continue
        for fn in fns:
            if fn.endswith('.md'):
                src = io.open(os.path.join(dp, fn), encoding='utf-8', errors='replace').read()
                c = sum(src.count(k) for k in expect)
                if c: print(f'MD-残留报告 {os.path.join(dp, fn)}: {c}')

if __name__ == '__main__':
    main()
