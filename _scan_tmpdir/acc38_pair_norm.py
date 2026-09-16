# -*- coding: utf-8 -*-
# acc38 独立验收·第11项：diff 行配对归一比较（fields.cls + cells 内 tag 徽标文本归一）
import io, re
t = io.open('acc38_demo_diff.txt', encoding='utf-8').read().splitlines()
mrows = [l[1:] for l in t if l.startswith('-') and not l.startswith('---') and "'row':" in l and '"cls"' in l]
prows = [l[1:] for l in t if l.startswith('+') and not l.startswith('+++') and "'row':" in l and '"cls"' in l]
re_cls = re.compile(r'("cls": ")[^"]*(")')
# 源文本中 tag 徽标形如 <span class=\"tag tag-blue\">TEXT</span>（引号带反斜杠转义）
re_tag = re.compile(r'(tag tag-\w+\\">)[^<]*(</span>)')
def norm(s):
    s = re_cls.sub(r'\1*\2', s)
    s = re_tag.sub(r'\1*\2', s)
    return s.strip()
ok = bad = 0
for i in range(min(len(mrows), len(prows))):
    a, b = norm(mrows[i]), norm(prows[i])
    if a == b:
        ok += 1
    else:
        bad += 1
        for j in range(min(len(a), len(b))):
            if a[j] != b[j]:
                print('第%d对 差异@%d:' % (i+1, j))
                print('  A:', a[max(0, j-70):j+70])
                print('  B:', b[max(0, j-70):j+70])
                break
        else:
            print('第%d对 长度不同 %d/%d' % (i+1, len(a), len(b)))
            print('  A尾:', a[-110:])
            print('  B尾:', b[-110:])
print('cls+tag徽标 归一后逐对全同 = %d / %d（不同 = %d）' % (ok, len(mrows), bad))
print('== done ==')
