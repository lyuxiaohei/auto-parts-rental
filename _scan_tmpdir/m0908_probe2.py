# -*- coding: utf-8 -*-
# 第二轮：可疑项上下文定性
import pathlib, re
PROT = pathlib.Path('P3-R01-包装租赁管理后台原型')
OUT = []
def p(s=''): OUT.append(str(s))
def ctx(fname, word, n=3, span=70):
    t = (PROT/fname).read_text(encoding='utf-8', errors='replace') if (PROT/fname).exists() else ''
    if not t: return [f'<文件不存在 {fname}>']
    out = []
    idx = 0
    for _ in range(n):
        i = t.find(word, idx)
        if i < 0: break
        seg = re.sub(r'\s+', ' ', t[max(0,i-span):i+len(word)+span])
        out.append('…'+seg+'…')
        idx = i + len(word)
    return out or ['0命中']

# 1. 退租申请残留语境
for f, w in [('P3-R01-F01-业务流程导航图.html','退租申请'), ('仓储作业/库存查询.html','退租申请'), ('租赁管理/租赁单列表.html','退租申请')]:
    p(f'== 退租申请 @ {f} ==')
    for c in ctx(f, w, 2): p('   '+c)

# 2. 库存查询 组装 语境（形态归类）
p('\n== 库存查询「组装」全部形态 ==')
t = (PROT/'仓储作业/库存查询.html').read_text(encoding='utf-8', errors='replace')
forms = {}
for m in re.finditer(r'.{0,25}组装.{0,25}', t):
    s = re.sub(r'\s+',' ', m.group(0))
    forms[s] = forms.get(s, 0) + 1
for k, v in sorted(forms.items(), key=lambda x:-x[1])[:12]: p(f'   [{v}] {k}')

# 3. 客户转租形态 + 菜单是否有入口
p('\n== 客户转租 @ 库存查询 形态 ==')
forms = {}
for m in re.finditer(r'.{0,20}客户转租.{0,20}', t):
    s = re.sub(r'\s+',' ', m.group(0)); forms[s] = forms.get(s,0)+1
for k, v in sorted(forms.items(), key=lambda x:-x[1])[:10]: p(f'   [{v}] {k}')
p('   mobile/库存查询 语境:')
for c in ctx('mobile/库存查询.html','客户转租',2): p('   '+c)
# 菜单入口：业务页侧边栏是否有 转租 字样（所有业务页都带菜单）
p('   全站 grep 转租(仅文件名层面看是否有独立页):')
for f in sorted(PROT.rglob('*.html')):
    if 'backup' in f.as_posix(): continue
    if '转租' in f.name: p('   独立页: '+f.as_posix())
menu_hit = [f.as_posix() for f in sorted(PROT.rglob('*.html')) if 'backup' not in f.as_posix() and '租赁管理/组合出库列表.html'==f.as_posix()]
mt = (PROT/'租赁管理/组合出库列表.html').read_text(encoding='utf-8', errors='replace')
p('   组合出库列表页侧边栏含 转租: '+str('转租' in mt))

# 4. 租赁单新建：含税/未税标签加粗 + 换算交互
p('\n== 租赁单新建弹窗 三件套/加粗/换算 ==')
lr = (PROT/'租赁管理/弹窗/租赁单新建.html').read_text(encoding='utf-8', errors='replace')
for w in ['未税单价','税率','含税单价','换算','oninput','bold','font-weight']:
    i = lr.find(w)
    p(f'   {w}: {"有" if i>=0 else "无"}')
    if i>=0 and w in ('未税单价','含税单价','换算','oninput'):
        p('      '+re.sub(r'\s+',' ',lr[max(0,i-80):i+120]))
# 含税/未税 label 是否加粗（找含税紧邻标签的class）
for m in re.finditer(r'<(th|label|td)[^>]{0,120}>(\s*(?:<[^>]+>\s*)*)(未税|含税)[^<]*', lr):
    p('   标签形态: '+re.sub(r'\s+',' ',m.group(0))[:160])

# 5. 租入单新建：计费方式与日租金
p('\n== 租入单新建 计费方式/日租金 ==')
zi = (PROT/'租赁管理/弹窗/租入单新建.html').read_text(encoding='utf-8', errors='replace')
for c in ctx('租赁管理/弹窗/租入单新建.html','日租金',2): p('   '+c)
i = zi.find('计费')
if i>=0: p('   计费段: '+re.sub(r'\s+',' ',zi[i-50:i+300]))
p('   租入单列表 日租金语境:')
for c in ctx('租赁管理/租入单列表.html','日租金',3): p('   '+c)
p('   数据字典 日租金: ' + str(ctx('系统管理/数据字典.html','日租金',1)))

# 6. 应付账单列头 + 剩余金额替代词
p('\n== 应付账单列头/三金额 ==')
yf = (PROT/'财务协同/应付账单.html').read_text(encoding='utf-8', errors='replace')
ths = re.findall(r'<th[^>]*>([^<]+)</th>', yf)
p('   th 列头: '+str(ths))
for w in ['未付金额','待付金额','未付','待付','剩余']:
    p(f'   {w}: {yf.count(w)}')

# 7. 付款登记新建：分期互算交互
p('\n== 付款登记新建 分期互算 ==')
fk = (PROT/'财务协同/弹窗/付款登记新建.html').read_text(encoding='utf-8', errors='replace')
i = fk.find('分期')
if i>=0: p('   分期段: '+re.sub(r'\s+',' ',fk[max(0,i-100):i+500]))
for w in ['oninput','比例','自动算']:
    p(f'   {w}: {fk.count(w)}')
for c in ctx('财务协同/弹窗/付款登记新建.html','超出',1,100): p('   超出语境: '+c)

# 8. 归还单独立页
p('\n== 租赁管理 目录文件 ==')
for f in sorted((PROT/'租赁管理').glob('*.html')): p('   '+f.name)
p('   归还单关键词:')
for f in sorted((PROT/'租赁管理').glob('*.html')):
    t2 = f.read_text(encoding='utf-8', errors='replace')
    if '归还单' in f.name or ('归还' in t2 and f.name.endswith('列表.html')):
        pass
gt = None
for f in sorted(PROT.rglob('*.html')):
    if 'backup' in f.as_posix(): continue
    if '归还' in f.name: p('   独立归还页: '+f.as_posix())

# 9. 赔偿单残留语境（应收账单4处+F01）
p('\n== 赔偿单 语境 ==')
for c in ctx('财务协同/应收账单.html','赔偿单',3): p('   应收: '+c)
for c in ctx('P3-R01-F01-业务流程导航图.html','赔偿单',2): p('   F01: '+c)

# 10. 库存不足提示语境（租赁单新建）
p('\n== 租赁单新建 库存不足提示 ==')
for c in ctx('租赁管理/弹窗/租赁单新建.html','库存不足',2,90): p('   '+c)

# 11. 租赁单新建 产品下拉
p('\n== 租赁单新建 产品字段形态 ==')
sels = re.findall(r'<select[^>]*>(.*?)</select>', lr, re.S)
p(f'   select 总数 {len(sels)}')
for i, s in enumerate(sels):
    opts = re.findall(r'<option[^>]*>([^<]+)', s)
    p(f'   select[{i}] options: {opts[:6]}')

out = ROOT if (ROOT:=pathlib.Path('.')).exists() else pathlib.Path('.')
(pathlib.Path('_scan_tmpdir')/'m0908_ctx2.txt').write_text('\n'.join(OUT), encoding='utf-8')
print('written', len(OUT))
