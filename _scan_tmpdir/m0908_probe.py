# -*- coding: utf-8 -*-
# 09-08 最终版纪要 → 原型落实情况探针（只读；供应商税率项对照提交态 e45fac0）
import pathlib, re, subprocess
ROOT = pathlib.Path('.')
PROT = ROOT/'P3-R01-包装租赁管理后台原型'
OUT = []
def p(s=''): OUT.append(str(s))

files = sorted(f for f in PROT.rglob('*.html') if 'backup' not in f.as_posix())
texts = {f.as_posix(): f.read_text(encoding='utf-8', errors='replace') for f in files}

def grep(word, limit=8, glob_pat=None):
    res = []
    for k, t in texts.items():
        if glob_pat and not re.search(glob_pat, k): continue
        n = t.count(word)
        if n: res.append(f'{k}({n})')
    return res[:limit] if res else ['0 命中']

def item(no, desc, *lines):
    p(f'\n[{no}] {desc}')
    for l in lines: p('   ' + ' | '.join(l) if isinstance(l, tuple) else l)

p('== 09-08 纪要拍板项 vs 原型实测 ==')
p(f'受检 HTML: {len(files)} 个（不含 backup）')

# --- 菜单/模块 ---
item('1', '退租申请 模块级移除（M5）', f"grep 退租申请: {grep('退租申请')}")
item('2', '组装/拆卸 移除（M6）', f"grep 组装: {grep('组装', 6)}", f"grep 拆卸: {grep('拆卸', 6)}")
item('3', '运营商角色去掉（L6）', f"grep 运营商: {grep('运营商')}")
item('4', '客户转租 单独菜单+拉表改状态（八.5）', f"grep 客户转租: {grep('客户转租', 10)}")
item('5', '打印按钮=「打印出货单」（L9）', f"打印出货单: {grep('打印出货单', 6)}", f"旧词残留 打印出库单: {grep('打印出库单')}", f"旧词残留 打印拣货单: {grep('打印拣货单')}")

# --- 表单字段 ---
item('6', '明细三件套 未税/税率/含税 双向换算+标签加粗（三.3/七.2.4）',
     f"未税单价: {grep('未税单价', 10)}",
     f"含税单价: {grep('含税单价', 10)}",
     f"换算: {grep('换算', 8)}",
     "标签加粗证据: " + str(grep('font-weight', 3, '租赁管理')))
item('7', '明细产品字段=下拉框 数据源产品档案（L11）',
     "弹窗内产品码 WBX-1210L: " + str(grep('WBX-1210L', 12)))
# select 明细抽查
for pat in ['新建销售订单', '新建采购订单', '新建租赁单', '新建租入单']:
    hit = [k for k in texts if pat in pathlib.Path(k).stem]
    for k in hit[:2]:
        t = texts[k]
        sels = re.findall(r'<select[^>]*>(.*?)</select>', t, re.S)
        prod_sel = [i for i, s in enumerate(sels) if 'WBX' in s or '围板箱' in s]
        p(f'   {k}: select 总数 {len(sels)}, 含产品选项的下标 {prod_sel}')

# --- 财务 ---
item('8', '应收 4 来源（含对供应商应收）/应付 4 来源（含对客户应付）（M8）',
     f"丢损赔偿: {grep('丢损赔偿', 10)}",
     f"供应商赔付: {grep('供应商赔付', 6)}",
     f"客户赔付: {grep('客户赔付', 6)}",
     f"赔付客户/我方赔付: {grep('赔付客户', 4)} {grep('我方赔付', 4)}")
item('9', '赔偿不走独立赔偿单（L2）', f"grep 赔偿单: {grep('赔偿单')}")
item('10', '付款分期 比例⇄金额互算（M2）', f"分期: {grep('分期', 8)}", f"比例: {grep('比例', 8)}")
item('11', '账单 账单/已付/剩余金额+超额拦截（四.5）',
     f"已付金额: {grep('已付金额', 6)}", f"剩余金额: {grep('剩余金额', 6)}",
     f"超额: {grep('超额', 6)}", f"超出: {grep('超出', 6)}")
item('12', '无订单保证金/预付 直接建单（M3）', f"保证金: {grep('保证金', 10)}", f"预付: {grep('预付', 8)}")

# --- 档案 ---
item('13', '器具+零部件合并产品档案 分类+归属权（二.1）', f"归属权: {grep('归属权', 8)}")
item('14', '产品档案挂供应商税率（二.2/三.4）——对照提交态 e45fac0',
     f"工作树 产品档案 供应商税率区: {'供应商税率' in texts.get('P3-R01-包装租赁管理后台原型/基础数据/产品档案.html','')}",
     f"工作树 新建产品弹窗含税率: {'税率' in texts.get('P3-R01-包装租赁管理后台原型/基础数据/弹窗/新建产品.html','')}")
def gitshow(path):
    r = subprocess.run(['git','show',f'e45fac0:{path}'], capture_output=True)
    return r.stdout.decode('utf-8', errors='replace') if r.returncode==0 else f'<git show 失败 {r.returncode}>'
for f in ['基础数据/产品档案.html', '基础数据/弹窗/新建产品.html', '基础数据/弹窗/编辑产品.html']:
    key = 'P3-R01-包装租赁管理后台原型/'+f
    c = gitshow(key)
    if not c.startswith('<git'):
        p(f'   提交态 {pathlib.Path(f).name}: 供应商={c.count("供应商")} 税率={c.count("税率")} select下拉={len(re.findall(chr(60)+"select", c))}')
    else:
        p(f'   提交态 {f}: {c[:60]}（可能文件名不同）')

# --- 流程 ---
item('15', '销售订单去关联采购（L1）/采购关联销售=选填（三.1）',
     f"关联采购: {grep('关联采购')}", f"关联销售订单: {grep('关联销售订单', 6)}", f"预计到货: {grep('预计到货', 6)}")
item('16', '租入单：背靠背类型+多货品明细+月租/按套+无日租金（7.1）',
     f"背靠背: {grep('背靠背', 10)}", f"日租金: {grep('日租金')}", f"按套: {grep('按套', 6)}", f"月租: {grep('月租', 6)}")
item('17', '租入归还单 关联+同步明细+分批（L3）', f"归还: {grep('归还', 12)}")
item('18', '租赁单去租期（L4）', f"租期: {grep('租期', 8)}")
item('19', '创建租赁单优先查库存 不足提示生成草稿（7.2.1）',
     f"库存不足: {grep('库存不足', 8)}", f"生成草稿: {grep('生成草稿', 6)}")
item('20', '组合出库 选组合/BOM 扣组件（7.2.5）', f"组合出库: {grep('组合出库', 8)}")
item('21', '库存两视角 单品+可组套数（九.3）', f"可组: {grep('可组', 8)}", f"可配: {grep('可配', 6)}")
item('22', '移动端 H5+企微+免二次登录（十.2/3）',
     f"mobile 文件: {[k for k in texts if 'mobile' in k][:8]}",
     f"m-auth: {grep('m-auth', 6, 'mobile')}", f"企微: {grep('企微', 6)}")
item('23', '审核按角色 财务/商务/物流（十.1）',
     f"用户权限页 财务: {grep('财务', 3, '用户权限')}", f"商务: {grep('商务', 3, '用户权限')}", f"物流: {grep('物流', 3, '用户权限')}")
item('24', '销售订单支持 PDF/邮件截图附件（五.2）', f"附件: {grep('附件', 10)}")

p('\n== demo-data 实体名 ==')
js = (PROT/'_data'/'demo-data.js').read_text(encoding='utf-8', errors='replace')
ents = re.findall(r'(?:const|var)\s+([A-Za-z_][\w]*)\s*=', js)
p(str(ents[:50]))
p(f"demo-data 含 背靠背: {js.count('背靠背')}, 税率: {js.count('税率')}, 客户转租: {js.count('客户转租')}, 归还: {js.count('归还')}")

out_path = ROOT/'_scan_tmpdir'/'m0908_fulfil_check.txt'
out_path.write_text('\n'.join(OUT), encoding='utf-8')
print('written', out_path, len(OUT), 'lines')
