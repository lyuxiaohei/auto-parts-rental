# -*- coding: utf-8 -*-
# P1-R03-F01 阶梯图 HTML：0906 口径 → 0915 增补口径（153.75 人日·10-20/11-24/12-14·49 页）
import io
F = 'P1-R03/P1-R03-F01-版本业务能力阶梯图.html'
s = io.open(F, encoding='utf-8', newline='').read()

REPL = [
 # 页眉 / 副题
 ('<span class="docno">DOC · 2026-09-07 · 对应工期表 20260906</span>',
  '<span class="docno">DOC · 2026-09-15 · 对应工期表 20260914（09-15 增补）</span>'),
 ('2026 年内全量交付、两套旧系统停用',
  '12-14 全量上线、两套旧系统停用，验收顺至 01-08'),
 # 前置柱
 ('<div class="ver">前置</div><div class="date">09-07 ~ 09-11</div>',
  '<div class="ver">前置</div><div class="date">09-02 ~ 09-18</div>'),
 ('<div>需求走查45页</div>', '<div>需求四轮走查（09-02~09-14）</div>'),
 ('<div>PRD 冻结</div>', '<div>PRD 冻结（09-18）</div>'),
 # V1.0
 ('<div class="date">买卖版 · 10-16 上线</div>', '<div class="date">买卖版 · 10-20 上线</div>'),
 ('<div>· 按项目归集，权限分级</div>',
  '<div>· 按项目归集，权限分级（6 角色）</div>\n              <div>· 退货闭环起步：采购/销售退货单＋库存事件流水</div>'),
 ('<div class="pages">+17 页</div>', '<div class="pages">+19 页</div>'),
 # V1.1
 ('<div class="date">租赁版 · 11-17 上线</div>', '<div class="date">租赁版 · 11-24 上线</div>'),
 ('<div>· 对供应商：应付登记 + 付款 · 我的待办</div>',
  '<div>· 转移出库＋按天计租（直录日租金）· 退款登记</div>'),
 ('<div class="pages">+20 页 · 累计 37</div>', '<div class="pages">+22 页 · 累计 41</div>'),
 # V2.0
 ('<div class="date">深化版 · 12-07 上线</div>', '<div class="date">深化版 · 12-14 上线</div>'),
 ('<div class="d">12-25 前项目验收 · 年内交付收口 · 富余产能启动 2027 增强</div>',
  '<div class="d">01-08 前项目验收 · 12-14 全量上线收口 · 富余产能启动 2027 增强</div>'),
 ('<span class="star">★ 45 页全量</span>', '<span class="star">★ 49 页全量</span>'),
 ('<div>· 财务收口：开票登记 + 银行水单核销</div>',
  '<div>· 财务收口：开票登记 + 银行回单核销</div>'),
 ('<div class="pages">+8 页 · 45 页全量</div>', '<div class="pages">+8 页 · 49 页全量</div>'),
 # 时间轴
 ('<div class="tick pre-t">09-07</div>', '<div class="tick pre-t">09-02</div>'),
 ('<div class="tick vt"><span class="dot"></span>10-16</div>', '<div class="tick vt"><span class="dot"></span>10-20</div>'),
 ('<div class="tick vt"><span class="dot"></span>11-17</div>', '<div class="tick vt"><span class="dot"></span>11-24</div>'),
 ('<div class="tick vt"><span class="dot"></span>12-07<span style="float:right;color:var(--soft)">12-25 验收</span></div>',
  '<div class="tick vt"><span class="dot"></span>12-14<span style="float:right;color:var(--soft)">01-08 验收</span></div>'),
 # KPI 条
 ('<div class="val">149 <small>人日</small></div><div class="note">3 全栈 + Claude Code 提速口径（无 AI 对照 212）</div>',
  '<div class="val">153.75 <small>人日</small></div><div class="note">3 全栈 + Claude Code 提速口径（无 AI 约 219 · 含 09-15 增补 +12.5）</div>'),
 ('<div class="val">171.35 <small>人日</small></div>', '<div class="val">176.81 <small>人日</small></div>'),
 ('<div class="val">09-07 → 12-25</div><div class="note">约 3.6 个月 · 80 个工作日 · 年内验收收口</div>',
  '<div class="val">09-02 → 01-08</div><div class="note">约 4.4 个月 · 92 个工作日 · 12-14 全量上线（09-15 增补初估）</div>'),
 ('<div class="note">10-16 买卖版 · 11-17 租赁版 · 12-07 全量</div>',
  '<div class="note">10-20 买卖版 · 11-24 租赁版 · 12-14 全量</div>'),
 # 底部三卡
 ('有 AI 149 人日 vs 无 AI 212 人日（工期表「方案 2.0 vs 方案 1」），已按月负载排定（9~11 月负载 0.96~1.0 满负荷）。',
  '有 AI 153.75 人日 vs 无 AI 约 219 人日（工期表「方案 2.0 vs 方案 1」·09-15 增补 +12.5），已按月负载排定（9~10 月负载 0.85~0.99 满负荷）。'),
 ('15% 缓冲已含在 171.35 人日内；AI 磨合不顺可回退无 AI 口径（工期上浮至 212 人日、里程碑顺延约 1.3 个月），已列 R1~R5 风险跟踪。',
  '15% 缓冲已含在 176.81 人日内；AI 磨合不顺可回退无 AI 口径（工期上浮至约 219 人日、里程碑顺延约 1.3 个月），已列 R1~R5 风险跟踪。'),
 ('#1 计费规则与合同/报价单 · #5 水单与台账样例',
  '#1 计费规则（09-15 已定按天计租）· #5 银行回单与台账样例'),
 # 页脚
 ('<span>SOURCE · P1-R03-工期评估表-20260906.xlsx（汇总 · 版本里程碑 / 按月负载区）</span>',
  '<span>SOURCE · P1-R03-工期评估表-20260914.xlsx（汇总 · 版本里程碑 / 按月负载区 · 09-15 增补初估）</span>'),
 ('<span>P1-R03-F01 · 2026-09-07</span>', '<span>P1-R03-F01 · 2026-09-15</span>'),
]
fail = []
for old, new in REPL:
    n = s.count(old)
    if n != 1:
        fail.append('命中 %d 次: %s' % (n, old[:40]))
        continue
    s = s.replace(old, new)
io.open(F, 'w', encoding='utf-8', newline='').write(s)
print('替换 %d/%d 成功' % (len(REPL) - len(fail), len(REPL)))
for x in fail: print('  ' + x)
