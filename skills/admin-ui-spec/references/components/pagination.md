# 分页器

表格卡片底部右对齐：条数信息 + 页码 + 每页条数 + 跳转。控件高 30px、字号 12px。

## HTML

```html
<div class="pager">
  <span class="pg-info">第 1-10 条/总共 10383 条</span>
  <span class="pg-btn">‹</span>
  <span class="pg-btn cur">1</span>
  <span class="pg-btn">2</span>
  <span class="pg-btn">3</span>
  <span class="pg-btn">4</span>
  <span class="pg-btn">5</span>
  <span class="pg-ellipsis">…</span>
  <span class="pg-btn">1034</span>
  <span class="pg-btn">›</span>
  <span class="pg-size">10 条/页
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
  </span>
  <span class="pg-jump">跳至 <input value=""> 页</span>
</div>
```

## CSS

```css
.pager { display:flex; align-items:center; justify-content:flex-end; gap:8px; padding:14px 16px; font-size:12px; color:rgba(0,0,0,.85); flex-wrap:wrap; }
.pg-info { margin-right:8px; }
.pg-btn { min-width:30px; height:30px; padding:0 6px; border:1px solid var(--input-border); border-radius:4px; background:#fff; display:inline-flex; align-items:center; justify-content:center; cursor:pointer; color:rgba(0,0,0,.85); font-size:12px; user-select:none; }
.pg-btn:hover { color:var(--primary); border-color:var(--primary); }
.pg-btn.cur { background:var(--primary); border-color:var(--primary); color:#fff; }
.pg-ellipsis { color:rgba(0,0,0,.45); padding:0 2px; }
.pg-size { height:30px; border:1px solid var(--input-border); border-radius:4px; padding:0 8px; display:inline-flex; align-items:center; gap:6px; cursor:pointer; background:#fff; }
.pg-size svg { width:11px; height:11px; color:rgba(0,0,0,.35); }
.pg-jump { display:inline-flex; align-items:center; gap:6px; }
.pg-jump input { width:44px; height:30px; border:1px solid var(--input-border); border-radius:4px; text-align:center; font-size:12px; outline:none; font-family:inherit; }
.pg-jump input:focus { border-color:var(--primary); }
```

## 要点

- 页码超过 7 个时按 `1 2 3 4 5 … 末页` 折叠，当前页 `.cur`
- 原型无需真实翻页逻辑，页码静态展示即可；交互页可给 `.pg-btn` 挂点击切换 `.cur`
