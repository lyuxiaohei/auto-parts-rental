import io,sys,subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base_txt = open(r'_scan_tmpdir\g58_gitbase.txt', encoding='utf-8').read()
cur = subprocess.run(['git','-c','core.quotepath=false','status','--porcelain'], capture_output=True).stdout.decode('utf-8')

def parse_long(txt):
    out = set()
    for l in txt.splitlines():
        if l.startswith('\tmodified:   '):
            out.add(('M', l.strip().split(maxsplit=1)[1]))
        elif l.startswith('\tdeleted:    '):
            out.add(('D', l.strip().split(maxsplit=1)[1]))
        elif l.startswith('\t') and not l.startswith('\t(use'):
            out.add(('?', l.strip()))
    return out

def parse_por(txt):
    out = set()
    for l in txt.splitlines():
        if not l.strip(): continue
        st = l[:2].strip() or '?'
        path = l[3:].strip().strip('"')
        out.add((st, path))
    return out

b = parse_long(base_txt)
c = parse_por(cur)
new = c - b
gone = b - c
print('=== G58 新增触碰（当前有·基线无）===')
for st,p in sorted(new): print('  [%s] %s' % (st,p))
print()
print('=== 基线有·当前无（消失）===')
for st,p in sorted(gone): print('  [%s] %s' % (st,p))
print()
biz = ['仓储作业/','采购管理/','销售管理/','租赁管理/','租入管理/','基础数据/','系统管理/','财务协同/','项目管理/','首页/','mobile/']
viol = [p for st,p in new if any(k in p for k in biz)]
print('业务原型目录/mobile 新增触碰:', viol if viol else '无（零触碰）')
print()
print('=== g58_failures.md ===')
print(open(r'_scan_tmpdir\g58_failures.md', encoding='utf-8').read())
