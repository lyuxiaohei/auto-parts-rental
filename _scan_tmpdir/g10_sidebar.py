# -*- coding: utf-8 -*-
"""G10-B2: 38 页侧边栏 项目损益 移位+改名 财务看板（应收标签前插·href 不动）"""
import os, shutil, sys

ROOT = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型"
BK = r"D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-g10-20260910"

F1 = '<li><div class="sm-link" onclick="go(\'../财务协同/盈亏报表.html\')">项目损益</div></li>'
F2 = '<li><div class="sm-link" onclick="go(\'财务协同/盈亏报表.html\')">项目损益</div></li>'
F3 = '<li><div class="sm-link selected">项目损益</div></li>'
N1 = '<li><div class="sm-link" onclick="go(\'../财务协同/盈亏报表.html\')">财务看板</div></li>'
N2 = '<li><div class="sm-link" onclick="go(\'财务协同/盈亏报表.html\')">财务看板</div></li>'
N3 = '<li><div class="sm-link selected">财务看板</div></li>'
ANCHOR = '<li style="padding:4px 0 2px 48px;font-size:10px;color:#8c8c8c;letter-spacing:.08em;user-select:none;list-style:none">应收</li>'
FUDAI = '<li style="padding:4px 0 2px 48px;font-size:10px;color:#8c8c8c;letter-spacing:.08em;user-select:none;list-style:none">应付</li>'
OLD_ANY = '>项目损益</div>'
NEW_ANY = '>财务看板</div>'

def line_indent(s, pos):
    """pos 指向行内某串开头；返回 (indent_str, nl_pos)。indent 必须全空白否则报错。"""
    nl = s.rfind('\n', 0, pos)
    ind = s[nl+1:pos]
    assert ind and all(c in ' \t' for c in ind), f'非纯缩进行 indent={ind!r}'
    return ind, nl

pages, fails = [], []
for root, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ('弹窗', '_data') and not d.startswith('backup')]
    for f in files:
        if not f.endswith('.html'):
            continue
        p = os.path.join(root, f)
        s = open(p, encoding='utf-8').read()
        if OLD_ANY in s or NEW_ANY in s:
            pages.append(p)

print(f'pages with sidebar target: {len(pages)}')
assert len(pages) == 38, f'预期 38 页，实际 {len(pages)}'

ok = 0
for p in sorted(pages):
    rel = os.path.relpath(p, ROOT)
    try:
        s = open(p, encoding='utf-8').read()
        assert s.count(OLD_ANY) == 1, f'OLD_ANY count={s.count(OLD_ANY)}'
        assert s.count(NEW_ANY) == 0
        # 识别删除形态
        if F1 in s:
            old, new = F1, N1
        elif F2 in s:
            old, new = F2, N2
        elif F3 in s:
            old, new = F3, N3
        else:
            raise AssertionError('三种已知形态均未命中')
        assert s.count(old) == 1
        li_balance_before = (s.count('<li'), s.count('</li>'))
        # 备份
        dst = os.path.join(BK, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(p, dst)
        # 删除旧行（含前导换行+缩进）
        i = s.find(old)
        ind, nl = line_indent(s, i)
        s = s[:nl] + s[i+len(old):]
        # 在 应收 标签 li 前插入新行
        assert s.count(ANCHOR) == 1, f'应收锚 count={s.count(ANCHOR)}'
        j = s.find(ANCHOR)
        ind2, nl2 = line_indent(s, j)
        s = s[:j] + ind2 + new + '\n' + s[j:]
        # 写回
        open(p, 'w', encoding='utf-8', newline='').write(s)
        # 写后复核
        t = open(p, encoding='utf-8').read()
        assert t.count(OLD_ANY) == 0
        assert t.count(NEW_ANY) == 1
        p_fin = t.find(new)
        p_ys = t.find(ANCHOR)
        p_yf = t.find(FUDAI)
        assert 0 <= p_fin < p_ys < p_yf, f'顺序错 fin={p_fin} ys={p_ys} yf={p_yf}'
        assert li_balance_before == (t.count('<li'), t.count('</li>')), 'li 配平变化'
        ok += 1
        print(f'OK  {rel}')
    except Exception as e:
        fails.append((rel, str(e)))
        print(f'FAIL {rel}: {e}')

print(f'==== G10-B2: {ok}/38 ok, fails={len(fails)} ====')
sys.exit(1 if fails else 0)
