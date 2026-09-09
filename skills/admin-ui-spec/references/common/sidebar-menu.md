# 侧边栏：菜单数据 + 系统切换

同一系统的所有页面**原样共用**对应模板，每页只改 3 处：

1. 当前页面所在链路的 `sm-item has-sub` 加 `open`（最多展开一条链路；三级页同时展开其父级二级链路）
2. 当前页面对应的叶子 `.sm-link` 加 `selected`，并去掉其 `onclick`
3. 已有真实页面的菜单项挂 `onclick="go('相对路径')"`；无页面的项不挂
4. `.sys-pop` 为**三系统**（供应链 / 商城 / WMS）：本系统项为 `current`（带 ✓），另两系统项挂 `go()` 指向其首页

已有页面（互链路径以此为准）：

- 供应链：`全量订单/订单列表.html`、`全量订单/订单策略.html`、`全量订单/异常订单.html`、`全量订单/异常分类设置.html`、`一件代发订单/订单列表.html`、`一件代发订单/退单列表.html`、`商品管理/商品发布.html`、`订单管理/自动合单.html`、`订单管理/发货仓库策略.html`、`订单管理/订单分析报表.html`、`仓储管理/到货通知单.html`、`仓储管理/入库单.html`、`仓储管理/出库作业单.html`、`仓储管理/其它出库.html`、`仓储管理/直发发货登记.html`、`仓储管理/库存简表查询.html`、`库存管理/库存台账.html`、`库存管理/库存移动.html`、`库存管理/库存冻结.html`、`库存管理/库存调整.html`、`库存管理/调拨单.html`、`库存管理/盘点单.html`、`仓内作业/波次管理.html`、`仓内作业/拣货作业.html`、`仓内作业/复核作业.html`、`仓内作业/出库拦截.html`、`仓内作业/打包作业.html`、`仓内作业/称重作业.html`、`仓内作业/发货作业.html`、`仓内作业/交接管理.html`、`仓内作业/PDA作业.html`、`采购管理/采购订单.html`、`退换货管理/销售退货通知.html`、`退换货管理/销售退货入库.html`、`退换货管理/采购退货通知.html`、`退换货管理/采购退货出库.html`、`退换货管理/更换商品.html`、`退换货管理/二次配送.html`、`退换货管理/退款单.html`、`报表中心/查询中心.html`、`基础数据/仓库管理.html`、`基础数据/货区货位.html`、`基础数据/承运商管理.html`、`设置/取消交易类型.html`
- 商城：`订单与售后/订单列表.html`、`订单与售后/售后监控.html`
- WMS（老系统对照，独立目录）：`WMS仓储管理/{入库管理,出库管理,退货管理}/*.html`

## 结构规则

- 一级项：`li.sm-item`（有子级加 `.has-sub`）> `.sm-link`（`.sm-ico` 图标 + 名称 + 子级加 `.sm-arrow`）
- 子级：`ul.sm-sub`，二级缩进 48px、三级缩进 64px（CSS 已处理）
- 图标统一 14px（商城模板历史上用 16px，新页面一律 14px）、`stroke="currentColor"`；**同名菜单项跨页图标必须逐字符一致**，从本文件模板复制
- 菜单数据缺页时先补占位（不挂 `go()`），不要改名或调序

## 供应链管理后台模板

```html
<aside class="sidebar">
  <ul class="side-menu">
    <li class="sm-item">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></span>首页</div>
    </li>
    <li class="sm-item has-sub">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l1.5-5h15L21 9M3 9v11a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1V9M3 9h18M9 21v-6h6v6"/></svg></span>供应商管理<span class="sm-arrow"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
      <ul class="sm-sub">
        <li><div class="sm-link">供应商列表</div></li>
        <li><div class="sm-link">企业认证</div></li>
      </ul>
    </li>
    <li class="sm-item has-sub">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg></span>商品管理<span class="sm-arrow"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
      <ul class="sm-sub">
        <li><div class="sm-link">商品列表</div></li>
        <li><div class="sm-link" onclick="go('../商品管理/商品发布.html')">商品发布</div></li>
        <li><div class="sm-link">草稿列表</div></li>
        <li><div class="sm-link">待审核商品</div></li>
        <li><div class="sm-link">商品类目</div></li>
        <li><div class="sm-link">商品品牌</div></li>
        <li><div class="sm-link">物流模板</div></li>
      </ul>
    </li>
    <li class="sm-item has-sub">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></span>订单管理<span class="sm-arrow"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
      <ul class="sm-sub">
        <li class="sm-item has-sub">
          <div class="sm-link">全量订单<span class="sm-arrow"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
          <ul class="sm-sub">
            <li><div class="sm-link" onclick="go('../全量订单/订单列表.html')">订单列表</div></li>
            <li><div class="sm-link" onclick="go('../全量订单/订单策略.html')">订单策略</div></li>
            <li><div class="sm-link" onclick="go('../全量订单/异常订单.html')">异常订单</div></li>
            <li><div class="sm-link" onclick="go('../全量订单/异常分类设置.html')">异常分类设置</div></li>
          </ul>
        </li>
        <li class="sm-item has-sub">
          <div class="sm-link">一件代发订单<span class="sm-arrow"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
          <ul class="sm-sub">
            <li><div class="sm-link" onclick="go('../一件代发订单/订单列表.html')">订单列表</div></li>
            <li><div class="sm-link" onclick="go('../一件代发订单/退单列表.html')">退单列表</div></li>
          </ul>
        </li>
        <li><div class="sm-link" onclick="go('../订单管理/自动合单.html')">自动合单</div></li>
        <li><div class="sm-link" onclick="go('../订单管理/发货仓库策略.html')">发货仓库策略</div></li>
        <li><div class="sm-link" onclick="go('../订单管理/订单分析报表.html')">订单分析报表</div></li>
      </ul>
    </li>
    <li class="sm-item has-sub">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="21 8 21 21 3 21 3 8"/><rect x="1" y="3" width="22" height="5"/><line x1="10" y1="12" x2="14" y2="12"/></svg></span>仓储管理<span class="sm-arrow"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
      <ul class="sm-sub">
        <li><div class="sm-link" onclick="go('../仓储管理/到货通知单.html')">到货通知单</div></li>
        <li><div class="sm-link" onclick="go('../仓储管理/入库单.html')">入库单</div></li>
        <li><div class="sm-link" onclick="go('../仓储管理/出库作业单.html')">出库作业单</div></li>
        <li><div class="sm-link" onclick="go('../仓储管理/其它出库.html')">其它出库</div></li>
        <li><div class="sm-link" onclick="go('../仓储管理/直发发货登记.html')">直发发货登记</div></li>
        <li><div class="sm-link" onclick="go('../仓储管理/库存简表查询.html')">库存简表查询</div></li>
      </ul>
    </li>
    <li class="sm-item has-sub">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg></span>库存管理<span class="sm-arrow"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
      <ul class="sm-sub">
        <li><div class="sm-link" onclick="go('../库存管理/库存台账.html')">库存台账</div></li>
        <li><div class="sm-link" onclick="go('../库存管理/库存移动.html')">库存移动</div></li>
        <li><div class="sm-link" onclick="go('../库存管理/库存冻结.html')">库存冻结</div></li>
        <li><div class="sm-link" onclick="go('../库存管理/库存调整.html')">库存调整</div></li>
        <li><div class="sm-link" onclick="go('../库存管理/调拨单.html')">调拨单</div></li>
        <li><div class="sm-link" onclick="go('../库存管理/盘点单.html')">盘点单</div></li>
      </ul>
    </li>
    <li class="sm-item has-sub">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></span>仓内作业<span class="sm-arrow"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
      <ul class="sm-sub">
        <li><div class="sm-link" onclick="go('../仓内作业/波次管理.html')">波次管理</div></li>
        <li><div class="sm-link" onclick="go('../仓内作业/拣货作业.html')">拣货作业</div></li>
        <li><div class="sm-link" onclick="go('../仓内作业/复核作业.html')">复核作业</div></li>
        <li><div class="sm-link" onclick="go('../仓内作业/出库拦截.html')">出库拦截</div></li>
        <li><div class="sm-link" onclick="go('../仓内作业/打包作业.html')">打包作业</div></li>
        <li><div class="sm-link" onclick="go('../仓内作业/称重作业.html')">称重作业</div></li>
        <li><div class="sm-link" onclick="go('../仓内作业/发货作业.html')">发货作业</div></li>
        <li><div class="sm-link" onclick="go('../仓内作业/交接管理.html')">交接管理</div></li>
        <li><div class="sm-link" onclick="go('../仓内作业/PDA作业.html')">PDA作业</div></li>
      </ul>
    </li>
    <li class="sm-item has-sub">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg></span>采购管理<span class="sm-arrow"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
      <ul class="sm-sub">
        <li><div class="sm-link" onclick="go('../采购管理/采购订单.html')">采购订单</div></li>
      </ul>
    </li>
    <li class="sm-item has-sub">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg></span>退换货管理<span class="sm-arrow"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
      <ul class="sm-sub">
        <li><div class="sm-link" onclick="go('../退换货管理/销售退货通知.html')">销售退货通知</div></li>
        <li><div class="sm-link" onclick="go('../退换货管理/销售退货入库.html')">销售退货入库</div></li>
        <li><div class="sm-link" onclick="go('../退换货管理/采购退货通知.html')">采购退货通知</div></li>
        <li><div class="sm-link" onclick="go('../退换货管理/采购退货出库.html')">采购退货出库</div></li>
        <li><div class="sm-link" onclick="go('../退换货管理/更换商品.html')">更换商品</div></li>
        <li><div class="sm-link" onclick="go('../退换货管理/二次配送.html')">二次配送</div></li>
        <li><div class="sm-link" onclick="go('../退换货管理/退款单.html')">退款单</div></li>
      </ul>
    </li>
    <li class="sm-item has-sub">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/></svg></span>报表中心<span class="sm-arrow"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
      <ul class="sm-sub">
        <li><div class="sm-link" onclick="go('../报表中心/查询中心.html')">查询中心</div></li>
      </ul>
    </li>
    <li class="sm-item">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/></svg></span>客服管理</div>
    </li>
    <li class="sm-item">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/><path d="M6 15h4"/></svg></span>结算管理</div>
    </li>
    <li class="sm-item has-sub">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg></span>基础数据<span class="sm-arrow"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
      <ul class="sm-sub">
        <li><div class="sm-link" onclick="go('../基础数据/仓库管理.html')">仓库管理</div></li>
        <li><div class="sm-link" onclick="go('../基础数据/货区货位.html')">货区货位</div></li>
        <li><div class="sm-link" onclick="go('../基础数据/承运商管理.html')">承运商管理</div></li>
      </ul>
    </li>
    <li class="sm-item has-sub">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09a1.65 1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33h.01a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51h.01a1.65 1.65 0 0 0 1.82.33l.06-.06a2 2 0 1 1 2.83-2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82v.01a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg></span>设置<span class="sm-arrow"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
      <ul class="sm-sub">
        <li><div class="sm-link" onclick="go('../设置/取消交易类型.html')">取消交易类型</div></li>
      </ul>
    </li>
  </ul>
  <div class="side-foot">
    <div class="sys-cur" id="sysSwitchBtn" title="切换系统">
      <span class="sys-badge">供</span>
      <span class="sys-name">供应链管理后台</span>
      <span class="sys-swap"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg></span>
    </div>
    <div class="sys-pop" id="sysPop">
      <div class="sys-pop-title">切换系统</div>
      <div class="sys-item current">一兆链采供应链管理后台<span class="check">✓</span></div>
      <div class="sys-item" onclick="go('../../商城运营后台/订单与售后/订单列表.html')">商城运营后台</div>
      <div class="sys-item" onclick="go('../../WMS仓储管理/入库管理/到货通知单.html')">一兆链采WMS仓储管理</div>
    </div>
  </div>
</aside>
```

## 商城运营后台模板

```html
<aside class="sidebar">
  <ul class="side-menu">
    <li class="sm-item">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></span>首页</div>
    </li>
    <li class="sm-item">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg></span>选品管理</div>
    </li>
    <li class="sm-item">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg></span>运营配置</div>
    </li>
    <li class="sm-item">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg></span>商城装修</div>
    </li>
    <li class="sm-item">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg></span>活动卡券</div>
    </li>
    <li class="sm-item">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 12 20 22 4 22 4 12"/><rect x="2" y="7" width="20" height="5"/><line x1="12" y1="22" x2="12" y2="7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/></svg></span>积分管理</div>
    </li>
    <li class="sm-item has-sub">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="16" y2="17"/></svg></span>订单与售后<span class="sm-arrow"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span></div>
      <ul class="sm-sub">
        <li><div class="sm-link">订单配置</div></li>
        <li><div class="sm-link" onclick="go('订单列表.html')">订单列表</div></li>
        <li><div class="sm-link" onclick="go('售后监控.html')">售后监控</div></li>
      </ul>
    </li>
    <li class="sm-item">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg></span>渠道管理</div>
    </li>
    <li class="sm-item">
      <div class="sm-link"><span class="sm-ico"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09a1.65 1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33h.01a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51h.01a1.65 1.65 0 0 0 1.82.33l.06-.06a2 2 0 1 1 2.83-2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82v.01a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg></span>系统设置</div>
    </li>
  </ul>
  <div class="side-foot">
    <div class="sys-cur" id="sysSwitchBtn" title="切换系统">
      <span class="sys-badge">商</span>
      <span class="sys-name">商城运营后台</span>
      <span class="sys-swap"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg></span>
    </div>
    <div class="sys-pop" id="sysPop">
      <div class="sys-pop-title">切换系统</div>
      <div class="sys-item current">商城运营后台<span class="check">✓</span></div>
      <div class="sys-item" onclick="go('../../供应链管理后台/全量订单/订单列表.html')">一兆链采供应链管理后台</div>
      <div class="sys-item" onclick="go('../../WMS仓储管理/入库管理/到货通知单.html')">一兆链采WMS仓储管理</div>
    </div>
  </div>
</aside>
```
