# 表单（详情/发布/编辑页）

按 `.card` 分组（卡片标题 `.card-title`），组内逐行 `.form-row`：左侧 120px 右对齐 label（必填加 `.req` 红星）+ 右侧控件。控件高 30px、字号 13px。

## HTML

```html
<section class="card">
  <h3 class="card-title">基础信息</h3>

  <!-- 文本输入（带清空 + 字数统计） -->
  <div class="form-row">
    <div class="form-label"><span class="req">*</span>产品名称：</div>
    <div class="input-box" style="width:350px;">
      <input type="text" autocomplete="off">
      <span class="suffix">
        <span class="clear-ico" title="清空">×</span>
        <span class="char-count">0 / 50</span>
      </span>
    </div>
  </div>

  <!-- 单选 -->
  <div class="form-row">
    <div class="form-label"><span class="req">*</span>是否有条形码：</div>
    <div>
      <span class="radio checked"><span class="dot"></span>是</span>
      <span class="radio"><span class="dot"></span>无条形码</span>
    </div>
  </div>

  <!-- 复选 -->
  <div class="form-row">
    <div class="form-label"><span class="req">*</span>供货方式：</div>
    <div>
      <span class="checkbox checked"><span class="box">✓</span>支持一件代发</span>
      <span class="checkbox"><span class="box"></span>支持集采</span>
    </div>
  </div>

  <!-- 下拉选择 -->
  <div class="form-row">
    <div class="form-label"><span class="req">*</span>商品品牌：</div>
    <div class="input-box select-box" style="width:350px;">
      <span>彩虹</span><span class="caret">▾</span>
    </div>
  </div>
</section>
```

label 后需要说明图标时加 `.info-ico`（13px 圆圈 i）；输入框下方的固定说明用 `.pn-hint`，行内代码符号用 `<code>`。

## CSS

```css
.form-row { display:flex; align-items:center; margin-bottom:20px; }
.form-row:last-child { margin-bottom:0; }
.form-label { flex:0 0 120px; text-align:right; margin-right:8px; font-size:13px; color:var(--text); white-space:nowrap; }
.req { color:var(--danger); margin-right:4px; }
.info-ico { color:var(--text-3); margin:0 2px; display:inline-flex; vertical-align:middle; }

.input-box { width:350px; height:30px; border:1px solid var(--input-border); border-radius:6px; display:flex; align-items:center; padding:0 11px; background:#fff; font-size:13px; color:var(--text); }
.input-box input { flex:1; min-width:0; height:100%; border:none; outline:none; background:transparent; font:inherit; color:inherit; padding:0; }
.input-box:focus-within { border-color:var(--primary); box-shadow:0 0 0 2px rgba(22,119,255,.1); }
.input-box .suffix { margin-left:auto; display:inline-flex; align-items:center; gap:6px; color:var(--text-3); font-size:12px; }
.input-box .clear-ico { display:inline-flex; cursor:pointer; }
.select-box { justify-content:space-between; cursor:pointer; }
.select-box .caret { color:var(--text-3); }

.radio, .checkbox { display:inline-flex; align-items:center; margin-right:24px; cursor:pointer; font-size:13px; color:var(--text); }
.radio .dot { width:16px; height:16px; border-radius:50%; border:1px solid var(--input-border); margin-right:6px; position:relative; background:#fff; }
.radio.checked .dot { border-color:var(--primary); }
.radio.checked .dot::after { content:''; position:absolute; inset:3px; border-radius:50%; background:var(--primary); }
.checkbox .box { width:16px; height:16px; border-radius:2px; border:1px solid var(--input-border); margin-right:6px; background:#fff; display:inline-flex; align-items:center; justify-content:center; color:#fff; font-size:11px; }
.checkbox.checked .box { background:var(--primary); border-color:var(--primary); }

.pn-hint { margin-top:6px; font-size:12px; color:var(--text-3); line-height:1.7; }
.pn-hint code { background:#fafafa; border:1px solid var(--border); border-radius:4px; padding:0 4px; margin:0 1px; color:#d4380d; font-family:Consolas,Monaco,monospace; font-size:11px; }
```

## 校验反馈（可选）

- 校验失败：输入框加 `.error`（`border-color:var(--danger); background:#fff1f0;`），下方输出 `.field-error` 列表；通过输出 `.field-ok`
- 字数超限：`.char-count` 加 `.over`（变红）

```css
.input-box.error { border-color:var(--danger); background:#fff1f0; }
.char-count.over { color:var(--danger); }
.field-error { margin-top:6px; font-size:12px; color:var(--danger); line-height:1.6; }
.field-ok { margin-top:6px; font-size:12px; color:#52c41a; }
```

## 要点

- 页面底部固定提交条：右对齐「取消（`.btn-default`）+ 提交（`.btn` 主色）」
- 按钮体系见 modal.md 的 `.btn` 组（两模板共用）
- **预填/自动计算字段**：加 `readonly class="auto"`（样式 `color:var(--text-3)`），扫描/审计工具按 `cls=auto` 识别为有意设计豁免，不算「不可编辑」问题
