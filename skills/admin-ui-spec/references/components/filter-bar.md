# 筛选区域（列表页查询区）

列表页第一块 `.filter-card`：**4 列网格**，每个筛选项是**一体框**（label 与控件包在同一个输入框内，非“label 裸露+控件框”分离式）。控件高 32px、字号 13px。超出首行的项挂 `.ff-row-extra`，卡片默认 `collapsed`（折叠只显首行）。

**按钮区 `.filter-actions` 是 grid 内一格（首行末列），不独占整行**——收起时首行 = 3 个筛选项 + 按钮占第 4 格。

## HTML（以包装租赁项目为基准）

```html
<div class="filter-card collapsed" id="filterCard">
  <div class="filter-grid">
    <div class="ff"><span class="ff-label">入库单号：</span><input placeholder="请输入入库单号"></div>

    <!-- 下拉选择：必须真 <select>（禁 div 假下拉），首项「全部」占位，选项 ≥2，右侧叠加箭头 -->
    <div class="ff"><span class="ff-label">供应商：</span>
      <select><option value="">全部</option><option>宁波华塑包装制品有限公司</option><option>苏州联恒五金制品有限公司</option></select>
      <svg class="ff-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
    </div>

    <!-- 时间范围：双 input + 分隔符 -->
    <div class="ff"><span class="ff-label">入库时间：</span><input placeholder="开始日期"><span class="ff-sep">→</span><input placeholder="结束日期"></div>

    <!-- 超出首行的项挂 ff-row-extra（折叠行） -->
    <div class="ff ff-row-extra"><span class="ff-label">业务类型：</span>
      <select><option value="">全部</option><option>零部件采购</option><option>器具采购</option></select>
      <svg class="ff-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
    </div>

    <!-- 按钮区：grid 末列 -->
    <div class="filter-actions">
      <button class="link-collapse" onclick="var f=document.getElementById('filterCard');f.classList.toggle('collapsed');this.querySelector('span').textContent=f.classList.contains('collapsed')?'展开':'收起'"><span>展开</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></button>
      <button class="btn btn-default" id="btnReset">重置</button>
      <button class="btn btn-primary">查询</button>
    </div>
  </div>
</div>
```

## CSS

```css
.filter-card { background:#fff; border-radius:8px; padding:16px 18px; margin:0 0 12px; box-shadow:0 1px 3px rgba(0,0,0,0.05); }
.filter-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; }

/* 一体框筛选项：label+控件同框 */
.ff { display:flex; align-items:center; border:1px solid #d9d9d9; border-radius:6px; padding:0 10px; height:32px; background:#fff; transition:border-color .2s; }
.ff:focus-within { border-color:var(--primary); }
.ff-label { flex-shrink:0; font-size:13px; color:#262626; margin-right:6px; white-space:nowrap; }
.ff input { flex:1; min-width:0; border:none; outline:none; height:100%; font-size:13px; color:#262626; background:transparent; font-family:inherit; }
.ff input::placeholder { color:var(--placeholder); }

/* 真 select：去原生箭头，叠 svg 箭头 */
.ff select { flex:1; min-width:0; border:none; outline:none; height:100%; font-size:13px; color:#262626; background:transparent; font-family:inherit; appearance:none; -webkit-appearance:none; cursor:pointer; }
.ff select option[value=""] { color:var(--placeholder); }
.ff-chev { width:12px; height:12px; color:var(--text-3); flex:none; pointer-events:none; margin-left:4px; }
.ff-sep { color:var(--text-3); margin:0 4px; flex:none; }

/* 按钮区：grid 末列右对齐 */
.filter-actions { display:flex; align-items:center; justify-content:flex-end; gap:8px; }
.link-collapse { border:none; background:none; color:var(--primary); font-size:12px; cursor:pointer; display:inline-flex; align-items:center; gap:3px; font-family:inherit; padding:0 4px; }
.filter-card:not(.collapsed) .link-collapse svg { transform:rotate(180deg); }

/* 折叠：默认收起，extra 行隐藏 */
.collapsed .filter-grid .ff-row-extra { display:none; }

.btn { height:30px; padding:0 15px; border-radius:4px; font-size:12px; cursor:pointer; font-family:inherit; display:inline-flex; align-items:center; justify-content:center; gap:4px; }
.btn-default { border:1px solid var(--input-border); background:#fff; color:rgba(0,0,0,.85); }
.btn-default:hover { color:var(--primary); border-color:var(--primary); }
.btn-primary { border:1px solid var(--primary); background:var(--primary); color:#fff; }
```

## 重置清空 JS（全站统一，原样复制——重置必须真清空）

```html
<script>
(function () {
  var btn = document.getElementById('btnReset');
  if (!btn) return;
  var card = btn.closest('.filter-card');
  btn.addEventListener('click', function () {
    card.querySelectorAll('input').forEach(function (i) { i.value = ''; });
    card.querySelectorAll('select').forEach(function (s) { s.selectedIndex = 0; });
  });
})();
</script>
```

> 收起/展开用 HTML 内联 onclick（见上模板），不加独立脚本。

## 配套：状态页签（可选，筛选卡与表格之间）

带计数徽标，当前项 `.active`：

```html
<div class="stabs">
  <span class="stab active">全部<span class="stab-count">325</span></span>
  <span class="stab">待发货<span class="stab-count">18</span></span>
  <span class="stab">已发货<span class="stab-count">300</span></span>
</div>
```

```css
.stabs { display:flex; padding:10px 16px 0; border-bottom:1px solid var(--border); gap:24px; background:#fff; }
.stab { padding:0 2px 10px; font-size:13px; color:rgba(0,0,0,.65); cursor:pointer; border-bottom:2px solid transparent; margin-bottom:-1px; user-select:none; }
.stab:hover { color:var(--primary); }
.stab.active { color:var(--primary); border-bottom-color:var(--primary); font-weight:500; }
.stab-count { font-size:12px; color:var(--text-3); margin-left:4px; }
```

页签切换 JS（全站统一写法——页签必须有可切换交互，不允许只有样式无绑定）：

```html
<script>
(function () {
  document.querySelectorAll('.stab').forEach(function (t) {
    t.addEventListener('click', function () {
      document.querySelectorAll('.stab').forEach(function (x) { x.classList.remove('active'); });
      t.classList.add('active');
    });
  });
})();
</script>
```

## 硬性要求（来自包装租赁项目全站审计口径）

- **下拉一律真 `<select>`**：div+文字+箭头的假下拉（无选项、不可交互）曾造成 180 处交互缺陷，禁止再出现
- **select 选项 ≥2**：含「全部」占位（`<option value="">全部</option>`），空下拉或单选项视为缺陷
- **重置必须真清空**：重置点击后本卡片所有 `input` 清值、所有 `select` 恢复首项——只做视觉态不清值视为假重置
- **input 必带 placeholder**；**查询/重置按钮必须绑行为**（至少视觉反馈+清空），不允许裸按钮
