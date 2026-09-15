# -*- coding: utf-8 -*-
# 以归档0914为底版重建0915：功能点表右移对齐0906（J=评估人）+ 重放全部数据改动 + 汇总
import shutil, datetime
from copy import copy
from openpyxl import load_workbook

SRC = '99-归档/P1-R03-工期评估表-20260914.xlsx'
DST = 'P1-R03-工期评估表-20260915.xlsx'
shutil.copy(SRC, DST)
wb = load_workbook(DST)
fp = wb['功能点评估（全栈）']; hs = wb['汇总']
D = lambda m, d: datetime.datetime(2026, m, d)
fail = []
def chk(c, m):
    if not c: fail.append(m)

# ---------- A. 数据右移对齐 0906：J=吕道远，K=开始，L=结束，M=状态+风险合并 ----------
for r in range(4, 65):
    j = fp.cell(row=r, column=10).value   # 开始(0914错位)
    k = fp.cell(row=r, column=11).value   # 结束
    l = fp.cell(row=r, column=12).value   # 状态注记
    m = fp.cell(row=r, column=13).value   # 风险注记
    fp.cell(row=r, column=10).value = '吕道远'
    fp.cell(row=r, column=11).value = j
    fp.cell(row=r, column=12).value = k
    note = ''
    if isinstance(l, str) and l.strip(): note = l.strip()
    if isinstance(m, str) and m.strip():
        note = (note + '；' + m.strip()) if note else m.strip()
    fp.cell(row=r, column=13).value = note if note else None
chk(fp.cell(row=4, column=10).value == '吕道远' and isinstance(fp.cell(row=4, column=11).value, datetime.datetime), '右移后行4异常')

# ---------- B. 既有行内容更新（K/L=日期、M=合并注记） ----------
UPD = {
 4:  dict(D='原型走查与字段确认（四轮评审·第 2~4 次沟通 09-02~09-14）', K=D(9,2),  L=D(9,14), M='✅ 已完成（09-02 第 2 次沟通起·09-14 第 4 次沟通收口）；依赖 #2 #3：账号或全套截图；走查结论直接落到 PRD'),
 5:  dict(D='计费规则与单据流程确认（09-11 三段式→09-15 改定：按时间周期直录日租金/按次次单价·按持有量计租）', L=D(9,15), M='✅ 已定案（09-15·D-145；「无日租金」口径由 G39 修订）；依赖 #1 #5：合同/报价单、单据样例'),
 7:  dict(L=D(9,18), M='⏳ 09-18（本周五）范围冻结（拍板台账滚动至 09-15·D-145 待归并）；客户确认后冻结范围，原型同步定稿'),
 8:  dict(K=D(9,14), L=D(9,18), M='G31~G39 改造包进行中（弹窗页面化/转移出库/字段口径/按天计租）·09-18 定稿；v2.8 已交付，仅评修订量'),
 9:  dict(K=D(9,18), L=D(9,18), M='⏳ 09-18（本周五）定稿收口（需求期 09-02~09-18·吕道远）；与 PRD 冻结同节点收口'),
 17: dict(D='产品档案：物料类型一级 10 值（WB/T 1058 行业口径·D-96/G38）+四参考价按物料类型通用+供应商税率+三段式仅参考价（D-145）'),
 19: dict(D='库位档案：仓库→库位两级（区层已删·G31）·客户虚拟仓不维护（D-006）'),
 24: dict(D='我的待办：19 类待办聚合入口', M='19 类=可审矩阵 19 项同值源（G33 扩）；审核人筛选；V1.0 无采购订单时先手工入库，V1.0 内衔接 FP8-03 凭单发起'),
 25: dict(M='凭采购订单验收；入库计量以物料基本单位（托层删·G38）；BOM 结果导向·出库按组合扣减'),
 36: dict(D='计费与租价管理：单据侧直录日租金（按时间周期）/次单价（按次）·三段式仅档案参考价·计费方式随料带出（含组合件补字段）', H=3.5, M='计费定案 09-15（D-145）：按持有量×天数计租；G20「无日租金」口径由 G39 修订；FP 码待补'),
 43: dict(D='应收账单：六来源（租赁费/销售费/丢损赔偿/供应商应收/押金/预收）自动汇总+手填＋按持有量×天数期段化（起租/止租/天数/日单价/小计·G39）', H=3.5),
 46: dict(D='银行回单核销（原水单·D-142 更名）：导入勾对 + 部分核销 + 对账联调', F='银行回单核销（D-142 更名）', M='#5 银行回单（原水单）样例；#6 结算格式待路凯方提供'),
 48: dict(H=3.0, M='押金退还（D-82）；预付退款同口径（D-83）；租入侧对称按天计租（G39）·退款登记独立页（G33）；依赖 #8 开票主体信息'),
 50: dict(D='组织与权限：6 角色（系统管理员/财务/商务/物流/采购/项目经理·D-143）+可审单据矩阵 19 类（G33 扩）+数据权限三档（客户/供应商账号本版不做）', M='roles 7→6（D-143·D-89 沿革）；矩阵 16→19 类（G33）；现状缺失环节；依赖 #5 水单样例'),
 52: dict(D='数据字典：28 组 141 项业务字典配置（枚举值域统一管理·物料类型 10 值行业口径 WB/T 1058）', M='G30 13 组→G34 后 28 组 141 项；G38 物料类型 6→10 值；REQ-21；V1.1 简化版，完整核销流 V2.0'),
}
COL = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':10,'K':11,'L':12,'M':13}
for r, d in UPD.items():
    for k, v in d.items():
        fp.cell(row=r, column=COL[k]).value = v

# ---------- C. V2.0 行日期 +7 天；C1-C3 行新轮次日期 ----------
n2 = 0
for r in range(4, 65):
    if fp.cell(row=r, column=7).value == 'V2.0':
        for c in (11, 12):
            v = fp.cell(row=r, column=c).value
            if isinstance(v, datetime.datetime): fp.cell(row=r, column=c).value = v + datetime.timedelta(days=7)
        n2 += 1
chk(n2 == 10, 'V2.0 行 %d≠10' % n2)
CD = {57:(D(10,13),D(12,11)),58:(D(10,19),D(12,14)),59:(D(10,13),D(12,9)),60:(D(10,16),D(12,10)),61:(D(10,19),D(12,11)),62:(D(10,19),D(12,11)),63:(D(10,20),D(12,14)),64:(D(10,20),D(12,25))}
for r,(a,b) in CD.items():
    chk(fp.cell(row=r, column=1).value in ('C1','C2','C3'), '行%d 非 C 行'%r)
    fp.cell(row=r, column=11).value = a; fp.cell(row=r, column=12).value = b

# ---------- D. 插入 6 新行（对齐布局·样式抄邻行·自下而上） ----------
NEW = [
 (57, 53, ('B8','采购管理','（待补）','采购退货单：收货拒收/入库后退货·可退上限·关联采购入库','全栈','采购退货单列表+新建弹窗','V1.0',1.5,D(9,29),D(9,30),'G33·D-123（方案 B）→应付退款（对供应商）；人日待开发重估')),
 (50, 48, ('B6','财务协同','（待补）','退款登记（一页双向）：应付退款（对供应商）/应收退款（对客户）·关联退货单','全栈','退款登记','V1.1',1.0,D(11,3),D(11,4),'G33·D-123；TKD- 前缀；人日待开发重估')),
 (43, 39, ('B5','销售管理','（待补）','销售退货单：收货拒收/入库后退货·可退上限·关联销售出库','全栈','销售退货单列表+新建弹窗','V1.0',1.5,D(9,23),D(9,24),'G33·D-123（方案 B）→应收退款（对客户）；人日待开发重估')),
 (39, 38, ('B4','租赁管理','（待补）','转移出库单：列表+录单+详情+终止转移；结算方式两值（按租出/按终端·项目档案带出可覆盖）；库存状态「客户转租出」由审核驱动','全栈','转移出库列表+新建/详情弹窗','V1.1',2.0,D(10,26),D(10,28),'G37·D-106+D-132+D-137（转租登记退场·D-78 被替代）；人日待开发重估')),
 (39, 38, ('B4','租赁管理','（待补）','按持有量计租引擎：Σ(每日在租量×日租金)·天数=max(2,止−起+1)·单价相同合并总量·不勾稽原单','全栈','应收/应付账单明细（期段行）','V1.1',2.5,D(10,29),D(11,2),'G39·D-145；三段式仅档案参考价；人日待开发重估')),
 (36, 35, ('B3','仓储作业 ★核心','（待补）','库存事件流水与每日在租量：出库/退租/归还/调拨事件＋任意区间每日余额复算（按天计租数据基座）','全栈','库存查询（事件派生）＋各单据明细','V1.0',2.5,D(9,25),D(9,28),'G39·D-145；不勾稽（D-106·退租入库不关联租赁单）；人日待开发重估')),
]
final_rows = {}
for pos, src, (a,b,c,d_,e,f,g,h,k,l,m) in NEW:
    styles = [copy(fp.cell(row=src, column=cc)._style) for cc in range(1, 14)]
    fp.insert_rows(pos, 1)
    for cc, st in enumerate(styles, 1):
        fp.cell(row=pos, column=cc)._style = st
    vals = {1:a,2:b,3:c,4:d_,5:e,6:f,7:g,8:h,9:'=H%d*(1+汇总!$C$46)'%pos,10:'吕道远',11:k,12:l,13:m}
    for cc, v in vals.items(): fp.cell(row=pos, column=cc).value = v
    final_rows[d_[:4]] = pos
for rr in NEW:  # 记录最终行号（后面的插入使前面的行号+1）
    pass
# 重算最终行号：自下而上插入后，先插的在更下位置不变，后插的(数组倒序为底->顶)…直接按任务名定位
def find_row(prefix):
    for r in range(4, 75):
        if str(fp.cell(row=r, column=4).value or '').startswith(prefix): return r
    return None
locs = {k: find_row(k) for k in ['库存事件流水','转移出库单','按持有量计租','销售退货单','退款登记（','采购退货单']}
chk(all(locs.values()), '新行定位失败: %s' % locs)

tot = sum(fp.cell(row=r, column=8).value for r in range(4, 71) if isinstance(fp.cell(row=r, column=8).value, (int, float)))
chk(abs(tot-153.75) < 1e-9, '合计 %.2f≠153.75' % tot)

# ---------- E. 行2 口径 + 表头 M 列名 ----------
note = fp.cell(row=2, column=1).value
chk(note.startswith('口径：'), '行2 异常')
fp.cell(row=2, column=1).value = note + '｜2026-09-15 增补：需求期 09-02~09-18；新增功能点 6 行（转移出库/库存事件流水/按持有量计租/采购退货/销售退货/退款登记·G33/G37/G39）＋既有行口径刷新；新行人日按 0906 口径产品侧初估（+12.5 人日·开发重估后滚动刷新）'

# ---------- F. 汇总重放 ----------
for r in range(4, 18):
    f_ = hs.cell(row=r, column=3).value
    if isinstance(f_, str) and 'SUMIF' in f_:
        hs.cell(row=r, column=3).value = f_.replace('$A$4:$A$69','$A$4:$A$75').replace('$H$4:$H$69','$H$4:$H$75')
BLOCKS=[('A1',4,7),('A2',8,9),('B0',10,14),('B1',15,19),('B2',20,24),('B3',25,36),('B4',37,41),('B5',42,46),('B6',47,54),('B7',55,57),('B8',58,62),('C1',63,64),('C2',65,67),('C3',68,70)]
S="'功能点评估（全栈）'!"
for (w,a,b),r in zip(BLOCKS,range(4,18)):
    chk(hs.cell(row=r,column=1).value==w,'汇总行%d=%s'%(r,w))
    hs.cell(row=r,column=4).value='=IF(COUNT(%sK%d:K%d)=0,"",MIN(%sK%d:K%d))'%(S,a,b,S,a,b)
    hs.cell(row=r,column=5).value='=IF(COUNT(%sL%d:L%d)=0,"",MAX(%sL%d:L%d))'%(S,a,b,S,a,b)
hs['F10']='计费定案（09-15·D-145）：按时间周期直录日租金／按次次单价·按持有量计租·三段式仅档案参考价'
hs['B22']='09-02 ~ 09-18 定版'; hs['C22']='需求 09-02 起（第 2~4 次沟通＋09-15 拍板包）+ 计费定案（按天计租）+ PRD 冻结 + 芋道底座/编码规范'
hs['F22']=D(9,2); hs['G22']=D(9,18); hs['H22']='无AI 09-23'
hs['D23']=41; hs['B23']='★ 10-20 上线（09-15 增补·初估）'; hs['G23']=D(9,30); hs['H23']='无AI 11-03'
hs['D24']=34.5; hs['B24']='★ 11-24 上线（初估）'; hs['G24']=D(11,12); hs['H24']='无AI 12-17'
hs['B25']='★ 12-14 上线（初估）'; hs['F25']=D(11,13); hs['G25']=D(11,30); hs['H25']='无AI 01-22'
hs['B26']='01-08 前后（初估）'; hs['C26']=hs['C26'].value.replace('年内验收','01-08 前验收'); hs['H26']='无AI 2027-02-05'
hs['B27']='10-13 / 11-16 / 12-08 启动（初估）'; hs['F27']=D(10,13); hs['G27']=D(12,25)
c23=hs['C23'].value; chk(c23.startswith('买卖版'),'C23'); hs['C23']=c23+'；+库存事件流水/采购退货/销售退货（09-15 增·人日待评估）'
c24=hs['C24'].value; chk(c24.startswith('租赁版'),'C24'); hs['C24']=c24.replace('计费三段式','按天计租（直录日租金）')+'；+转移出库/按持有量计租/退款登记（09-15 增·人日待评估）'
c25=hs['C25'].value; chk('水单核销' in c25,'C25'); hs['C25']=c25.replace('水单核销','银行回单核销')
for r,(b,e) in {32:(46,'需求 09-18 冻结；底座+V1.0 全量开发（09-15 起）＋采购/销售退货单与库存事件流水并入'),33:(47.5,'10-13~20 轮1：集成测试/UAT/主数据迁移/部署；★10-20 V1.0 上线（09-15 增补口径·初估）'),34:(46,'V1.1 开发完成（含移动端 H5＋转移出库＋按天计租引擎＋退款登记）；11-16~23 轮2；★11-24 V1.1 上线'),35:(37.31,'12-08~11 轮3（租入在途迁移/部署）；★12-14 V2.0 全量上线（128+ 页口径）；01-08 前验收')}.items():
    hs.cell(row=r,column=2).value=b; hs.cell(row=r,column=5).value=e
hs['H21']=str(hs['H21'].value).replace('212人日','约219人日')
hs['B42']=hs['B42'].value.replace('212 人日','约 219 人日')

wb.save(DST)
print('失败 %d 条｜功能点合计=%.2f｜新行位置=%s' % (len(fail), tot, locs))
for x in fail: print('  ' + x)
