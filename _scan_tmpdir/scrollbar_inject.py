# -*- coding: utf-8 -*-
"""任务三·全站滚动条浅色改造（2026-09-08）：每页首个 style 块末尾注入四行（固定规范）
幂等：页内已有 -webkit-scrollbar 则跳过记录；排除 99-归档 与 BOM.html；备份按原相对路径
"""
import sys, io, re, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / 'P3-R01-包装租赁管理后台原型'
BAK = ROOT / '_scan_tmpdir' / 'backup-scrollbar-20260908'

CSS = ('::-webkit-scrollbar{width:6px;height:6px}\n'
       '::-webkit-scrollbar-thumb{background:#d9d9d9;border-radius:3px}\n'
       '::-webkit-scrollbar-thumb:hover{background:#c4c4c4}\n'
       '::-webkit-scrollbar-track{background:transparent}\n')

EXCLUDE = {'BOM.html'}  # 道远既有裁定不动（默认决策表）

pages = sorted(p for p in PROTO.rglob('*.html')
               if '99-归档' not in str(p) and p.name not in EXCLUDE)
print(f'目标页数: {len(pages)}')

inj, skip_have, skip_nostyle, fail = [], [], [], []
for p in pages:
    try:
        raw = p.read_bytes()
        crlf = raw.count(b'\r\n') * 2 > raw.count(b'\n')
        nl = '\r\n' if crlf else '\n'
        txt = raw.decode('utf-8')
        if '-webkit-scrollbar' in txt:
            skip_have.append(p.relative_to(PROTO)); continue
        m = re.search(r'</style>', txt)
        assert m, '无 style 块'
        # 首个 </style> 前 = 首个 style 块末尾
        ins = CSS.replace('\n', nl)
        txt = txt[:m.start()] + ins + txt[m.start():]
        dst = BAK / p.relative_to(PROTO)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dst)
        p.write_bytes(txt.encode('utf-8'))
        # 标签配平自检
        t2 = p.read_bytes().decode('utf-8')
        assert t2.count('<style') == t2.count('</style>'), 'style 标签不配平'
        inj.append(p.relative_to(PROTO))
    except Exception as e:
        fail.append((str(p.relative_to(PROTO)), str(e)[:80]))

print(f'注入 {len(inj)} / 已有跳过 {len(skip_have)} / 无style跳过 {len(skip_nostyle)} / 失败 {len(fail)}')
for f in fail: print('  FAIL:', f)
for s in skip_have: print('  已有(跳过):', s)
if len(inj) + len(skip_have) != len(pages):
    print('!! 计数不符'); sys.exit(1)
print('OK')
