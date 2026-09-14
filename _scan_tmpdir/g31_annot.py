# -*- coding: utf-8 -*-
"""G31 标注层：A03/A04 迁移路径同步 + pin 更新/新增 + 重注入（告警须 0）"""
import json, io, os, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁'
PROTO = os.path.join(ROOT, 'P3-R01-包装租赁管理后台原型')
ANN = os.path.join(PROTO, 'P3-R01-A03-标注数据.json')
ANN4 = os.path.join(PROTO, 'P3-R01-A04-流程链标注数据.json')
MOVES = {
    '租赁管理/租入单列表.html': '租入管理/租入单列表.html',
    '租赁管理/租入入库列表.html': '租入管理/租入入库列表.html',
    '租赁管理/租入归还列表.html': '租入管理/租入归还列表.html',
    '租赁管理/弹窗/租入库': '租入管理/弹窗/租入库',
}
MOVED_PAGES = [
    '租赁管理/租入单列表.html', '租赁管理/租入入库列表.html', '租赁管理/租入归还列表.html',
    '租赁管理/弹窗/租入单新建.html', '租赁管理/弹窗/租入归还新建.html',
]

def fix_paths(path):
    d = json.load(io.open(path, encoding='utf-8'))
    keys = [k for k in d.keys() if k != '_meta']
    moved = {}
    for k in keys:
        nk = k
        for a, b in MOVES.items():
            if k.startswith(a):
                nk = b + k[len(a):]
        if nk != k:
            moved[k] = nk
    for old, new in moved.items():
        d[new] = d.pop(old)
    io.open(path, 'w', encoding='utf-8', newline='').write(json.dumps(d, ensure_ascii=False, indent=2))
    print(os.path.basename(path), '路径迁移:', moved)
    return d

def add_pin(d, page, pin):
    d.setdefault(page, [])
    pin['id'] = len(d[page]) + 1
    d[page].append(pin)

def main():
    d = fix_paths(ANN)
    d4 = fix_paths(ANN4)
    # ① 库位档案 pin1 文本更新（三级→两级 D-102）
    p = d['基础数据/库位档案.html'][0]
    assert '三级' in p['note']
    p['note'] = '仓库/库位两级（D-102 去库区层级·2026-09-14 第4次沟通）：正品仓/次品仓按仓库层区分，实际损耗走次品仓锁定不参与拣货（D-101）；库区层级后续做大了再加'
    # ② 新增注记
    add_pin(d, '租入管理/租入入库列表.html', {
        'selector': '<span class="form-label">立即转租</span>', 'title': '立即转租（背靠背）',
        'note': 'D-105（2026-09-14 王琳总裁定）：租入入库登记同时可勾选立即转租——供应商直发终端客户，自动生成租赁出库单（自动带物料·免重复填单·租赁出库列表可查该单 CK-20260914-023）；自有+租入混合出库待袁工问领导；计费口径待 D-122 梳理拍板',
        'fp': 'FP2-01', 'req': 'REQ-02'})
    add_pin(d, '租入管理/弹窗/租入单新建.html', {
        'selector': '<span class="req">*</span>起租日期', 'title': '租期两层',
        'note': 'D-117（2026-09-14 拍板）：租期分两层——合同起止时间（框架合同一签两三年）与单据起止时间（只填开始时间·后续天数自算·无结束日期）；天数计费联动属 D-122 梳理域暂不落地',
        'fp': 'FP2-01', 'req': 'REQ-02'})
    add_pin(d, '租赁管理/弹窗/租赁单新建.html', {
        'selector': '<span class="req">*</span>计费方式', 'title': '免费借用形态',
        'note': 'D-115（2026-09-14 形态认可）：免费借用＝租赁/销售单价填 0 不结算，不加专门结构；财务合规口径袁工问财务待复',
        'fp': 'FP2-01', 'req': 'REQ-01'})
    add_pin(d, '基础数据/BOM维护.html', {
        'selector': '<div style="margin:4px 0 8px;font-size:13px;font-weight:600;color:#1a1a1a;">配方行', 'title': 'BOM 维护时点',
        'note': 'D-118（2026-09-14·以转写原文为准）：BOM 在物料建档后即可维护，采购前或采购后均可，按实际情况；损耗率字段已按 D-101 移除，实际损耗走库位（次品仓）区分',
        'fp': 'FP1-05', 'req': 'REQ-04'})
    add_pin(d, '仓储作业/盘点录入.html', {
        'selector': '<th class="sticky-op">操作</th>', 'title': '盘点行内生成其他出入库',
        'note': 'D-110（2026-09-14）：每物料行内按差异方向生成其他入库（盘盈）/其他出库（盘亏），跳创建页自动带物料；类型域已补「破损/自然损耗」（保留既有赔偿核销等值）',
        'fp': 'FP5-02', 'req': 'REQ-06'})
    io.open(ANN, 'w', encoding='utf-8', newline='').write(json.dumps(d, ensure_ascii=False, indent=2))
    io.open(ANN4, 'w', encoding='utf-8', newline='').write(json.dumps(d4, ensure_ascii=False, indent=2))
    print('A03 pin 更新 1 + 新增 5 OK')

    # ③ 重注入受影响页
    pages = ['基础数据/库位档案.html', '租入管理/租入入库列表.html', '租入管理/弹窗/租入单新建.html',
             '租入管理/弹窗/租入归还新建.html', '租赁管理/弹窗/租赁单新建.html', '基础数据/BOM维护.html',
             '仓储作业/盘点录入.html', '租赁管理/弹窗/租入单新建.html', '租赁管理/弹窗/租入库']
    # 租入库 前缀页（8 弹窗全重注）
    for f in os.listdir(os.path.join(PROTO, '租入管理/弹窗')):
        pages.append('租入管理/弹窗/' + f)
    for pg in dict.fromkeys(pages):
        fp = os.path.join(PROTO, pg)
        if not os.path.exists(fp):
            print('跳过（不存在）:', pg); continue
        r = subprocess.run([sys.executable, '-X', 'utf8', r'C:\Users\Administrator\.zcode\skills\原型标注\scripts\annotate.py',
                            '--pages', PROTO, '--data', ANN, '--only', pg], capture_output=True, text=True)
        out = (r.stdout + r.stderr).strip()
        if 'WARN' in out.upper() or r.returncode != 0:
            print('!!', pg, out[:300])
    print('重注入完成')

if __name__ == '__main__':
    main()
