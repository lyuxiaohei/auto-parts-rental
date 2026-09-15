# -*- coding: utf-8 -*-
# P1-R03 0915 增补估算（按 0906 口径·产品侧初估，开发后续重估）：新行人日+版本小计+里程碑+按月负载
import datetime
from openpyxl import load_workbook

F = 'P1-R03-工期评估表-20260914.xlsx'
wb = load_workbook(F)
fp = wb['功能点评估（全栈）']; hs = wb['汇总']
D = lambda d: datetime.datetime(2026, d[0], d[1])
fail = []
def chk(c, m):
    if not c: fail.append(m)

# ---- 1. 新行与改动行人日/日期（0906 口径类比：全栈人日含概设+编码+自测） ----
ROWS = {
 36: (2.5, (9,25), (9,28)),   # 库存事件流水（类比：库存查询3/调拨1.5 → 2.5）
 40: (2.0, (10,26),(10,28)),  # 转移出库单（类比：租赁出库2/租赁单3 → 2）
 41: (2.5, (10,29),(11,2)),   # 按持有量计租引擎（类比：计费管理3·无页面纯引擎 → 2.5）
 46: (1.5, (10,1), (10,2)),   # 销售退货单（类比：其他出库1.5 → 1.5）
 54: (1.0, (11,3), (11,4)),   # 退款登记（单页双向，类比：付款登记1.5·无分期 → 1）
 62: (1.5, (9,29), (9,30)),   # 采购退货单（类比：其他入库1.5 → 1.5）
}
for r,(h,j,k) in ROWS.items():
    chk(fp.cell(row=r,column=8).value is None, '行%d 人日已有值'%r)
    fp.cell(row=r,column=8).value = h
    fp.cell(row=r,column=10).value = D(j)
    fp.cell(row=r,column=11).value = D(k)
ADJ = [(37,3,3.5),(43,3,3.5),(52,2.5,3.0)]  # FP4-03/FP6-01/FP6-06 计费口径改动
for r,old,new in ADJ:
    chk(fp.cell(row=r,column=8).value==old, '行%d 人日 %r≠%r'%(r,fp.cell(row=r,column=8).value,old))
    fp.cell(row=r,column=8).value = new

# 总量自检：141.25 + (2.5+2+2.5+1.5+1+1.5) + 1.5 = 153.75
tot = sum(fp.cell(row=r,column=8).value for r in range(4,71) if isinstance(fp.cell(row=r,column=8).value,(int,float)))
chk(abs(tot-153.75)<1e-9, '功能点人日合计 %.2f ≠ 153.75'%tot)

# ---- 2. 版本里程碑区（硬值人日 + 节点 + 无AI 对照） ----
hs['D23'] = 41; hs['D24'] = 34.5          # 35+6 / 28+6.5；前置12.75·V2.0 20.5·各版45 不变 → 合计153.75
MS = [
 (23,'★ 10-16 上线','★ 10-20 上线（09-15 增补·初估）',(9,10),(10,1),'无AI 10-30','无AI 11-03'),
 (24,'★ 11-17 上线','★ 11-24 上线（初估）',(9,17),(11,12),'无AI 12-10','无AI 12-17'),
 (25,'★ 12-07 上线','★ 12-14 上线（初估）',(11,13),(11,30),'无AI 01-15','无AI 01-22'),
 (26,'12-25 前后','01-08 前后（初估）',None,None,'无AI 2027-01-31','无AI 2027-02-05'),
 (27,'10-08 / 11-09 / 12-01 启动','10-13 / 11-16 / 12-08 启动（初估）',(10,13),(12,25),'—','—'),
]
for r,bold,bnew,f,g,hold,hnew in MS:
    chk(hs.cell(row=r,column=2).value==bold, 'B%d=%r'%(r,hs.cell(row=r,column=2).value))
    hs.cell(row=r,column=2).value = bnew
    if f: hs.cell(row=r,column=6).value = D(f)
    if g: hs.cell(row=r,column=7).value = D(g)
    if hold!='—': hs.cell(row=r,column=8).value = hnew
c26 = hs['C26'].value; chk('年内验收' in c26, 'C26 异常')
hs['C26'] = c26.replace('年内验收','01-08 前验收')

# ---- 3. 按月负载（含缓冲合计 153.75×1.15=176.81；44+48.5+46+38.31） ----
chk(isinstance(hs['F31'].value,(str,int,float)) , 'F31=%r'%hs['F31'].value)
MON = [
 (31,45,'需求 09-18 冻结；底座+V1.0 全量开发（09-15 起）＋采购/销售退货单与库存事件流水并入'),
 (32,48.5,'10-13~20 轮1：集成测试/UAT/主数据迁移/部署；★10-20 V1.0 上线（09-15 增补口径·初估）'),
 (33,46,'V1.1 开发完成（含移动端 H5＋转移出库＋按天计租引擎＋退款登记）；11-16~23 轮2；★11-24 V1.1 上线'),
 (34,38.31,'12-08~11 轮3（租入在途迁移/部署）；★12-14 V2.0 全量上线（128+ 页口径）；01-08 前验收'),
]
for r,d,g in MON:
    hs.cell(row=r,column=4).value = d
    hs.cell(row=r,column=7).value = g
s = sum(x[1] for x in MON)
chk(abs(s-176.81)<1e-9, '按月合计 %.2f ≠ 176.81'%s)

# ---- 4. 口径注记 ----
note = fp.cell(row=2,column=1).value
chk('人日留空待开发重估' in note, '行2 注记异常')
fp.cell(row=2,column=1).value = note.replace('新行人日留空待开发重估','新行人日 09-15 已按 0906 口径产品侧初估填入（+12.5 人日·开发重估后滚动刷新）')

wb.save(F)
print('失败项 %d 条' % len(fail))
for x in fail: print('  ' + x)
print('功能点合计 = %.2f（141.25+12.5）｜按月含缓冲合计 = %.2f' % (tot, s))
