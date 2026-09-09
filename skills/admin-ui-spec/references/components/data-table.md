# 列表（数据表格）

表格放在独立 `.card` 中，字号 12px，表头 `#fafafa` 底，行 hover 浅蓝。列多时外层加横向滚动，「操作」列固定在右侧（`.sticky-op`）。单号、商品名等可点文字用 `.lk`，状态用 `.tag`。

## HTML

```html
<div class="card">
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th style="width:36px"><input type="checkbox" class="cb"></th>
          <th>主订单号</th>
          <th>商品名称</th>
          <th>数量</th>
          <th>订单状态</th>
          <th class="sticky-op">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><input type="checkbox" class="cb"></td>
          <td><span class="lk">SJ2026080714360812597368797</span></td>
          <td>北鼎电器 AUY HY501W 电动牙刷</td>
          <td>1</td>
          <td><span class="tag tag-green">已发货</span></td>
          <td class="sticky-op ops"><a>详情</a><a>发货</a></td>
        </tr>
      </tbody>
    </table>
  </div>
  <!-- 分页器：见 pagination.md -->
</div>
```

## CSS

```css
.table-wrap { overflow-x:auto; }
table { width:100%; border-collapse:collapse; font-size:12px; white-space:nowrap; }
thead th { background:var(--thead-bg); font-weight:600; color:rgba(0,0,0,.85); text-align:left; padding:10px 12px; border-bottom:1px solid var(--border); }
tbody td { padding:9px 12px; border-bottom:1px solid var(--border); color:rgba(0,0,0,.85); }
tbody tr:hover td { background:#f5faff; }

/* 操作列固定右侧 */
th.sticky-op, td.sticky-op { position:sticky; right:0; background:#fff; box-shadow:-6px 0 8px -6px rgba(0,0,0,.12); }
thead th.sticky-op { background:var(--thead-bg); }
tbody tr:hover td.sticky-op { background:#f5faff; }

/* 链接文字 / 操作列 */
.lk { color:var(--primary); cursor:pointer; display:inline-flex; align-items:center; gap:3px; }
.lk svg { width:11px; height:11px; flex:none; }
.ops a { color:var(--primary); cursor:pointer; margin-right:10px; }
.ops a:last-child { margin-right:0; }

/* 状态标签——色彩语义（新类型复用现有色，不新造）：
   green=成功/已发货/已出库 · orange=待处理/异常/盘亏 · blue=信息类（如赔偿核销）
   red=报废/风险/失败 · gray=已关闭/历史 */
.tag { display:inline-block; padding:0 7px; height:22px; line-height:20px; font-size:12px; border-radius:2px; border:1px solid transparent; }
.tag-green { color:#52c41a; background:#f6ffed; border-color:#b7eb8f; }
.tag-orange { color:#fa8c16; background:#fff7e6; border-color:#ffd591; }
.tag-blue { color:var(--primary); background:var(--primary-bg); border-color:var(--primary); }
.tag-red { color:var(--danger); background:#fff1f0; border-color:#ffa39e; }
.tag-gray { color:var(--text-3); background:#fafafa; border-color:var(--border); }

/* 复选框 */
.cb { width:13px; height:13px; accent-color:var(--primary); cursor:pointer; vertical-align:middle; }
```

## 要点

- 数字、金额列右对齐（`style="text-align:right"` 或加类），时间列保持 `nowrap`
- 空数据态：`<tbody>` 内放一行跨列居中的「暂无数据」
- 表格上方如需批量操作，放一行按钮（`.btn .btn-default`，如「批量导出」），位置在状态页签之下、表格之上
- **操作列冻结验收**：视口收窄出横向滚动后，操作列（th/td 均挂 `.sticky-op`）必须仍贴容器右缘——Playwright 断言 `getBoundingClientRect().right ≈ wrap.right`（滚动前后各测一次）
- **业务口径注记条**：列表底部（分页器之下）用 `.pn-hint` 灰字条写单据联动/业务口径说明（如「审核通过后自动生成××单」），供演示时指读，不散落各处
- **示例数据规范**：单号前缀按单据类型严格区分（如 PO=采购订单 / CGRK=采购入库 / QTCK=其他出库），禁止跨类混用；日期用近月；新增示例行每页 1-2 行；状态列值与 tag 色语义一致
