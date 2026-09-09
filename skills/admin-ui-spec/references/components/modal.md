# 弹窗（模态对话框）

全屏遮罩 `.modal-overlay`（默认 `display:none`，加 `.show` 弹出）+ 居中 `.modal`：头部标题与关闭 ×、内容区、底部右对齐按钮。**宽度两档**：审核/确认类 `.modal` **640px**、表单/详情类 `.modal-lg` **780px**，均加 `max-width:92vw` 自适应兜底；内容超 80vh 内部滚动。验收：无横向溢出、字段值不换行（见下 dgrid 三招）。

## HTML

```html
<div class="modal-overlay" id="resultModal">
  <div class="modal">
    <div class="modal-header">
      <h3 class="modal-title">提交校验结果</h3>
      <span class="modal-close">×</span>
    </div>
    <div class="modal-body">
      <!-- 弹窗内容 -->
    </div>
    <div class="modal-footer">
      <button class="btn btn-default">关 闭</button>
      <button class="btn">确 定</button>
    </div>
  </div>
</div>
```

## CSS

```css
.modal-overlay { position:fixed; inset:0; background:rgba(0,0,0,.45); display:none; align-items:center; justify-content:center; z-index:1000; }
.modal-overlay.show { display:flex; }
.modal { background:#fff; border-radius:8px; width:640px; max-width:92vw; max-height:80vh; overflow-y:auto; box-shadow:0 6px 16px rgba(0,0,0,.12); }
.modal-lg { width:780px; }
.modal-header { padding:16px 24px; border-bottom:1px solid var(--border); display:flex; justify-content:space-between; align-items:center; }
.modal-title { font-size:16px; font-weight:600; color:#1a1a1a; margin:0; }
.modal-close { cursor:pointer; font-size:20px; color:var(--text-3); line-height:1; }
.modal-close:hover { color:var(--text); }
.modal-body { padding:20px 24px; }
.modal-footer { padding:12px 24px; border-top:1px solid var(--border); display:flex; justify-content:flex-end; gap:10px; }
```

## 按钮体系（表单页通用）

```css
.btn { display:inline-flex; align-items:center; justify-content:center; height:30px; padding:0 14px; border-radius:6px; border:none; cursor:pointer; font-size:13px; background:var(--primary); color:#fff; white-space:nowrap; }
.btn:hover { background:#4096ff; }
.btn-sm { height:28px; padding:0 12px; font-size:12px; }
.btn-default { background:#fff; color:var(--text); border:1px solid var(--input-border); }
.btn-default:hover { border-color:#4096ff; color:#4096ff; background:#fff; }
.btn-dashed { background:#fff; color:var(--primary); border:1px dashed var(--primary); }
```

> 注意：列表页筛选区的按钮用 filter-bar.md 的 12px `.btn` 组（同名不同尺寸），同一页面只引入其中一套，或按作用域区分（如 `.filter .btn`）。

## 开关 JS

```js
function openModal() { document.getElementById('resultModal').classList.add('show'); }
function closeModal() { document.getElementById('resultModal').classList.remove('show'); }
// 点遮罩空白处关闭
document.getElementById('resultModal').addEventListener('click', function (e) { if (e.target === this) closeModal(); });
```

## 字段网格（审核/详情弹窗内 dgrid）——值不换行三招

```html
<div class="dgrid">
  <div class="drow"><div class="dlabel">单据编号</div><div class="dval">CGRK-20260827-009</div></div>
  <!-- 值超 22 字的字段，drow 跨全宽 -->
  <div class="drow" style="grid-column:1/-1;"><div class="dlabel">器具规格</div><div class="dval">WBX-1210L 围板箱 1200×1000×1200mm 加厚型带铰链</div></div>
</div>
```

```css
.dgrid { display:grid; grid-template-columns:repeat(2,1fr); gap:0 32px; }
.drow { display:flex; padding:8px 0; border-bottom:1px dashed var(--border); font-size:13px; min-width:0; }
.dlabel { flex:0 0 110px; color:var(--text-3); white-space:nowrap; }
.dval { flex:1; min-width:0; color:var(--text); overflow-wrap:break-word; }  /* 禁用 word-break:break-all */
```

三招：① 弹窗宽度按两档给足（640/780）② `.dval` 用 `overflow-wrap:break-word` 温和断行（单号/编码整串优先）③ 值 >22 字的 drow 加 `style="grid-column:1/-1;"` 跨全宽；>34 字的长说明文案（如「验收通过后…」提示语）天然允许换行，豁免。验收：Playwright 断言 `.dval` 渲染高度 ≤ 单行高。

## 详情弹窗四段式（成熟结构，单据类详情通用）

1. **单据头**：`dgrid` 字段网格（如上）
2. **物料明细**：小表格（表头 + 序号/零件号/规格/数量/金额行）
3. **关联单据互溯链**：`.chain` > `.node`（`.n-role` 角色名 + `.n-name` 单号可点 `.lk`），本单节点高亮（`border-color:#1677ff; background:#e6f4ff;`），节点间 `→`
4. **流转时间线**：`.tl` > `.tl-i`（`.tl-t` 时间 + 事件 + `.tl-who` 操作人），待发生项加 `off` 灰态

## 要点

- 一个页面可有多个弹窗，各自独立 `id` + 同一套类名
- 结果列表类内容：成功项绿 ✓（`#52c41a`）、失败项红 ✕（`var(--danger)`）
- **审核弹窗业务后果提示**：审核结论 radio（通过/驳回）+ 意见框之后，加一行橙字后果提示（`font-size:12px; color:#fa8c16`，如「通过后自动核销库存：缺失/报废件生成其他出库单」），承载单据联动口径
- **双层同步**：页面内嵌 modal 与 `弹窗/` 目录独立模板（同文件名包壳、打开即默认 show）双份维护；独立模板内相对路径多一级（`../../`），改一处必同步另一处（内嵌 `../` 版与独立 `../../` 版分锚替换）
