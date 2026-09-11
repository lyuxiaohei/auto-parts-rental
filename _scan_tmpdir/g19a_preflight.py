import pathlib, time
p1 = pathlib.Path(r'agent-handoff/20260911-G19a-移动端H5规范化.md')
print('[1] task file exists:', p1.exists())
idx = pathlib.Path(r'agent-handoff/_索引.md').read_text(encoding='utf-8')
for line in idx.splitlines():
    if 'G16' in line or 'G19a' in line:
        print('[2] idx line:', line.strip()[:110])
mob = pathlib.Path(r'P3-R01-包装租赁管理后台原型/mobile')
now = time.time()
all_ok = True
for f in sorted(mob.iterdir()):
    age_min = (now - f.stat().st_mtime) / 60
    ok = age_min >= 30
    all_ok = all_ok and ok
    print('[3]', f.name, f'{age_min:.0f}min', 'OK' if ok else 'FRESH!!!')
print('PREFLIGHT3 all >=30min:', all_ok)
