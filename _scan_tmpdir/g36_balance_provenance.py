# -*- coding: utf-8 -*-
"""对比 G36 前备份 vs 当前：判定标签不平衡是否为本次改造引入"""
import io, os, re

ROOT = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'
BAKS = {
    '采购管理': r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-g36-b2-20260915\采购管理',
    '销售管理': r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-g36-b2-20260915\销售管理',
    '租赁管理': r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-g36-b3-20260915\租赁管理',
    '租入管理': r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-g36-b3-20260915\租入管理',
    '仓储作业': r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-g36-b3-20260915\仓储作业',
    '财务协同': r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\_scan_tmpdir\backup-g36-b5-20260915\财务协同',
}
FILES = ['采购管理/采购入库录单.html', '采购管理/采购订单列表.html', '销售管理/销售出库列表.html',
         '租赁管理/租赁单列表.html', '租赁管理/退租入库列表.html', '租入管理/租入入库列表.html',
         '租入管理/租入单列表.html', '租入管理/租入归还列表.html', '仓储作业/其他入库列表.html',
         '仓储作业/其他出库列表.html', '仓储作业/库存调拨列表.html', '财务协同/应付账单.html',
         '财务协同/退款登记.html', '财务协同/银行水单核销.html']


def bal(s):
    return (len(re.findall(r'<div(?:\s[^>]*)?>', s)), len(re.findall(r'</div>', s)))


def script_stripped(s):
    """去掉 <script>…</script> 与 <style>…</style> 后再计（判定是否为 JS 字符串造成）"""
    s = re.sub(r'<script[^>]*>.*?</script>', '', s, flags=re.S)
    s = re.sub(r'<style[^>]*>.*?</style>', '', s, flags=re.S)
    return s


print('%-28s %-18s %-18s %-18s' % ('文件', 'G36前备份', '当前(含JS)', '当前(去JS/style)'))
for rel in FILES:
    mod = rel.split('/')[0]
    cur = io.open(os.path.join(ROOT, rel), encoding='utf-8', errors='ignore').read()
    bakp = os.path.join(BAKS[mod], rel.split('/')[1])
    bak = io.open(bakp, encoding='utf-8', errors='ignore').read() if os.path.exists(bakp) else ''
    o1, c1 = bal(bak) if bak else (0, 0)
    o2, c2 = bal(cur)
    o3, c3 = bal(script_stripped(cur))
    print('%-28s %-18s %-18s %-18s' % (
        rel.split('/')[1],
        '%d/%d 差%d' % (o1, c1, o1 - c1) if bak else '(无备份)',
        '%d/%d 差%d' % (o2, c2, o2 - c2),
        '%d/%d 差%d' % (o3, c3, o3 - c3)))
