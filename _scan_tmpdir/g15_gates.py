# -*- coding: utf-8 -*-
"""G15 T5 · 机器门自检（4 门）· 只读
门1 grep 残留：max-width:880px=1 / 主viewBox 0 0 880 2184=1 / 支viewBox 0 0 880 846=1 / x2=1240=0 / x=1112=0
门2 内容零丢失：href 列表一致 + text 全文拼接（去空白）一致 + Mermaid/script 尾部逐字节一致
门3 溢出：两 SVG 全元素 bbox 右缘 ≤880（text 估宽：全角=font-size、半角=0.6×font-size；anchor 折算）
门4 支线重叠：支 SVG rect×rect 相交=0
"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

ROOT = Path(r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁')
CUR = ROOT / 'P3-R01-包装租赁管理后台原型' / 'P3-R01-F01-业务流程导航图.html'
OLD = ROOT / 'backup-f01-20260911' / 'P3-R01-包装租赁管理后台原型' / 'P3-R01-F01-业务流程导航图.html'
cur = open(CUR, encoding='utf-8', newline='').read()
old = open(OLD, encoding='utf-8', newline='').read()
fails = []

# ---------- 门1 grep 残留 ----------
print('== 门1 grep 残留 ==')
g = [
    ('max-width:880px', cur.count('max-width:880px'), 1),
    ('viewBox 0 0 880 2184', cur.count('viewBox="0 0 880 2184"'), 1),
    ('viewBox 0 0 880 846', cur.count('viewBox="0 0 880 846"'), 1),
    ('x2="1240" 残留', cur.count('x2="1240"'), 0),
    ('x="1112" 残留', cur.count('x="1112"'), 0),
    ('x="1240" 残留', cur.count('x="1240"'), 0),
]
for name, got, want in g:
    ok = got == want
    print(f'  {"PASS" if ok else "FAIL"} {name}: {got}（期望 {want}）')
    if not ok: fails.append(f'门1 {name}')

# ---------- 门2 内容零丢失 ----------
print('== 门2 内容零丢失 ==')
h_old = re.findall(r'href="([^"]+)"', old)
h_cur = re.findall(r'href="([^"]+)"', cur)
ok = h_old == h_cur
print(f'  {"PASS" if ok else "FAIL"} href 列表一致（改前 {len(h_old)} 条 = 改后 {len(h_cur)} 条）')
if not ok: fails.append('门2 href')

def texts(s):
    out = []
    for m in re.finditer(r'<text\b[^>]*>(.*?)</text>', s, re.S):
        inner = re.sub(r'<[^>]+>', '', m.group(1))
        out.append(re.sub(r'\s+', '', inner))
    return ''.join(out)
t_old, t_cur = texts(old), texts(cur)
ok = t_old == t_cur
print(f'  {"PASS" if ok else "FAIL"} text 全文拼接一致（去空白 {len(t_old)} 字 = {len(t_cur)} 字）')
if not ok:
    fails.append('门2 text')
    for i, (a, b) in enumerate(zip(t_old, t_cur)):
        if a != b:
            print(f'    首个分歧 @{i}: 旧…{t_old[max(0,i-30):i+30]}… 新…{t_cur[max(0,i-30):i+30]}…')
            break

tail_mark = '<!-- ============ Mermaid'
ok = old[old.index(tail_mark):] == cur[cur.index(tail_mark):]
print(f'  {"PASS" if ok else "FAIL"} Mermaid/script/footer 尾部逐字节一致')
if not ok: fails.append('门2 尾部')

# ---------- 门3 溢出 ----------
print('== 门3 溢出（bbox 右缘 ≤880） ==')
def est_w(s, fs):
    w = 0.0
    for ch in s:
        o = ord(ch)
        if o >= 0x2E80 or o in (0x2190, 0x2192, 0x21C4):
            w += fs * (2 if o >= 0x1F000 else 1)
        else:
            w += fs * 0.6
    return w

def path_max_x(d):
    xs = []
    for m in re.finditer(r'([MHVQ])\s*([\d\s.]+)', d):
        cmd, nums = m.group(1), [float(v) for v in m.group(2).split()]
        if cmd in ('M', 'Q'):
            xs += nums[0::2]
        elif cmd == 'H':
            xs += nums
    return max(xs) if xs else 0

over = []
for svg_i, sm in enumerate(re.finditer(r'<svg viewBox="0 0 (\d+) (\d+)"(.*?)</svg>', cur, re.S), 1):
    vbw, body = int(sm.group(1)), sm.group(3)
    for m in re.finditer(r'<rect\b([^>]*)/>', body):
        a = m.group(1)
        x = float(re.search(r'x="([\d.]+)"', a).group(1)); w = float(re.search(r'width="([\d.]+)"', a).group(1))
        if x + w > vbw: over.append((svg_i, 'rect', x + w, a.strip()[:60]))
    for m in re.finditer(r'<line\b([^>]*)/>', body):
        a = m.group(1)
        x2 = max(float(re.search(r'x1="([\d.]+)"', a).group(1)), float(re.search(r'x2="([\d.]+)"', a).group(1)))
        if 'marker-end' in a: x2 += 2
        if x2 > vbw: over.append((svg_i, 'line', x2, a.strip()[:60]))
    for m in re.finditer(r'<path\b([^>]*)/>', body):
        a = m.group(1)
        x2 = path_max_x(re.search(r'd="([^"]+)"', a).group(1)) + 2
        if x2 > vbw: over.append((svg_i, 'path', x2, a.strip()[:60]))
    for m in re.finditer(r'<text\b([^>]*)>(.*?)</text>', body, re.S):
        a, inner = m.group(1), m.group(2)
        x = float(re.search(r'x="([\d.]+)"', a).group(1))
        fs = float(re.search(r'font-size="([\d.]+)"', a).group(1))
        anchor = (re.search(r'text-anchor="(\w+)"', a) or [None, 'start'])[1]
        # tspan 自带 fill 但随宿主字号；全文计
        txt = re.sub(r'<[^>]+>', '', inner)
        w = est_w(txt, fs)
        right = x + (w / 2 if anchor == 'middle' else 0 if anchor == 'end' else w)
        if right > vbw + 0.5: over.append((svg_i, 'text', round(right, 1), txt[:30]))
print(f'  溢出元素 {len(over)}')
for o in over[:20]:
    print(f'    SVG{o[0]} {o[1]} 右缘={o[2]} {o[3]}')
if over: fails.append(f'门3 溢出{len(over)}')

# ---------- 门4 支线重叠 ----------
print('== 门4 支线重叠（支 SVG rect×rect） ==')
sub = list(re.finditer(r'<svg viewBox="0 0 (\d+) (\d+)"(.*?)</svg>', cur, re.S))[1]
rects = []
for m in re.finditer(r'<rect\b([^>]*)/>', sub.group(3)):
    a = m.group(1)
    x = float(re.search(r'x="([\d.]+)"', a).group(1)); y = float(re.search(r'y="([\d.]+)"', a).group(1))
    w = float(re.search(r'width="([\d.]+)"', a).group(1)); h = float(re.search(r'height="([\d.]+)"', a).group(1))
    rects.append((x, y, x + w, y + h, a.strip()[:50]))
hits = 0
for i in range(len(rects)):
    for j in range(i + 1, len(rects)):
        a, b = rects[i], rects[j]
        if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
            hits += 1
            print(f'    重叠: [{a[4]}] × [{b[4]}]')
print(f'  rect 重叠对 {hits}')
if hits: fails.append(f'门4 重叠{hits}')

print()
print('总结:', 'ALL PASS' if not fails else f'FAIL: {fails}')
sys.exit(0 if not fails else 1)
