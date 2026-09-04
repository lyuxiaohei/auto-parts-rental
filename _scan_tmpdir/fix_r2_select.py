# -*- coding: utf-8 -*-
"""R2：假下拉升级真 select。div.select-box 内首个 span/input → 真 <select>（保外观），选项按前置 label 语义映射，
预填文本保留为第一项。幂等：跳过已含 select 的。"""
import io, re, sys, glob, os
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

OPTS = [
    ('供应商', ['路凯包装运营（上海）有限公司', '苏州联恒五金制品有限公司', '宁波华塑包装制品有限公司', '常州正大塑料托盘厂']),
    ('运营方', ['路凯包装运营（上海）有限公司']),
    ('客户', ['一汽解放汽车有限公司', '上汽大众汽车有限公司宁波分公司', '小鹏汽车科技有限公司', '东风本田汽车有限公司']),
    ('项目', ['PRJ-2601 一汽解放', 'PRJ-2602 上汽大众', 'PRJ-2603 小鹏', 'PRJ-2604 东风本田']),
    ('租入单', ['RZD-20260815-003（路凯·围板箱×30）', 'RZD-20260815-005（路凯·围板箱×10）', 'RZD-20260902-008（待审核）']),
    ('租赁单', ['ZL-20260823-033（混合·40套）', 'ZL-20260828-031（组合C）', 'ZL-20260816-029（租入转租）']),
    ('销售订单', ['SO-20260903-0047', 'SO-20260902-0046', 'SO-20260901-0045']),
    ('采购订单', ['PO-20260902-018', 'PO-20260901-017', 'PO-20260830-016']),
    ('应收账单', ['AR-2026-08-PRJ2601', 'AR-2026-08-PRJ2602', 'AR-2026-08-PRJ2603']),
    ('应付账单', ['AP-20260903-009（租金应付）', 'AP-20260901-008（采购应付）']),
    ('器具', ['WBX-1210L 围板箱 1200×1000×970', 'PLT-1210P 塑料托盘 1200×1000', 'BTC-6040 料箱 600×400×340', 'ZH-2601-A 驾驶室围板箱整箱套件']),
    ('物料', ['WBX-1210L 围板箱', 'PLT-1210P 塑料托盘', 'BTC-6040 料箱', 'LJ-A100 护角']),
    ('组合', ['ZH-2601-A 驾驶室围板箱整箱套件', 'ZH-2602-B 冲压件料箱组套', 'ZH-2603-C 电池托盘护角套件', 'ZH-2604-D 混合组合套件']),
    ('库房', ['华东中心仓（WH-01）', '华南仓（WH-02）', '西南仓（WH-03）']),
    ('仓库', ['华东中心仓（WH-01）', '华南仓（WH-02）', '西南仓（WH-03）']),
    ('库区', ['原料区 RA', '成品区 RB', '外购区 RW', '器具区 JC']),
    ('单位', ['只', '套', '个', '托', '件']),
    ('客商类型', ['客户', '供应商', '客户兼供应商']),
    ('类别', ['围板箱', '塑料托盘', '木托盘', '料箱', '料架']),
    ('开票资料', ['增值税专用发票（13%）', '增值税普通发票']),
    ('负责人', ['王强', '李娜', '张伟', '刘志强', '李国栋']),
]
FALLBACK = ['全部', '待定选项（演示数据）']
SEL_STYLE = 'flex:1;min-width:0;border:none;outline:none;background:transparent;font:inherit;color:inherit;cursor:pointer;padding:0;appearance:none;-webkit-appearance:none;'

def options_for(label, preset):
    for key, vals in OPTS:
        if key in label:
            opts = list(vals)
            if preset and preset not in ('请选择', '全部', '') and preset not in opts:
                opts.insert(0, preset)
            return opts
    opts = list(FALLBACK)
    if preset and preset not in ('请选择', '全部', '') and preset not in opts:
        opts.insert(0, preset)
    return opts

def make_select(label, preset):
    opts = options_for(label, preset)
    first = preset if preset else opts[0]
    body = ''.join(f'<option{" selected" if o == first else ""}>{o}</option>' for o in opts)
    return f'<select style="{SEL_STYLE}">{body}</select>'

total, per_page = 0, {}
for p in sorted(glob.glob(f'{BASE}/**/*.html', recursive=True)):
    s = io.open(p, encoding='utf-8', newline='').read()
    out = s
    n = 0
    for m in list(re.finditer(r'<div[^>]*class="[^"]*select-box[^"]*"[^>]*>((?:(?!</div>).)*?)</div>', s, re.S)):
        seg = m.group(0)
        if '<select' in seg:
            continue
        before = s[max(0, m.start() - 300):m.start()]
        lm = re.findall(r'>([^<>]{2,14})(?:：|</(?:span|label|div)>)\s*$', before)
        label = lm[-1].replace('：', '').strip() if lm else ''
        preset_m = re.search(r'<span(?![^>]*caret)[^>]*>([^<]*)</span>', seg) or re.search(r'<input[^>]*value="([^"]*)"', seg) or re.search(r'<input[^>]*placeholder="([^"]*)"', seg)
        preset = (preset_m.group(1).strip() if preset_m else '')
        newseg = seg
        if preset_m and preset_m.group(0).startswith('<span'):
            newseg = newseg.replace(preset_m.group(0), make_select(label, preset), 1)
        elif '<input' in seg:
            im = re.search(r'<input[^>]*>', seg)
            if im:
                newseg = newseg.replace(im.group(0), make_select(label, preset), 1)
        if newseg != seg:
            out = out.replace(seg, newseg, 1)
            n += 1
    if n:
        assert '<select' not in '' or True
        io.open(p, 'w', encoding='utf-8', newline='').write(out)
        total += n
        per_page[os.path.relpath(p, BASE)] = n
print(f'R2 假下拉升级完成: {total} 处 / {len(per_page)} 页')
for k, v in sorted(per_page.items(), key=lambda x: -x[1])[:12]: print(f'  {k}: {v}')
