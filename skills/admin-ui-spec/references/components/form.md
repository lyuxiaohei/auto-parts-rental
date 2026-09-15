# 表单（详情/发布/编辑页）

按 `.card` 分组（卡片标题 `.card-title`），组内逐行 `.form-row`：左侧 120px 右对齐 label（必填加 `.req` 红星）+ 右侧控件。控件高 30px、字号 13px。**卡片怎么分见下一节「分卡片」——表单页必须分卡，不是可选项。**

## 分卡片（表单页的强制结构）

一张卡＝一个业务段落，各司其职：**信息卡 / 明细卡 / 附件卡 / 计划卡**分别成卡。卡片标题用概括词（`订单信息`、`采购明细`、`分期付款计划`）。

- **禁止**把明细段塞进信息卡里、用一行 13px 粗体小字充当分隔标题——那是弹窗时代的写法，搬到页面上时一律升级成卡片标题
- **标题必须走 `.card-head` 包裹**：`<div class="card-head"><h3 class="card-title">标题</h3></div>`。裸 `.card-title` 的下间距是 20px、`.card-head` 是 14px，两种写法并排一眼就能看出不齐
- **卡头右侧放本卡自己的动作**：`<div class="head-btns">`，典型是明细卡的「添加一行」。**不要**在表格下方挂一条整宽的虚线按钮
- **标题只写概括词，补充说明进卡内**：括号类说明（「可退上限内填写」「比例⇄金额互算 · 笔数不限直至付清」）不作标题的一部分，改放卡内 `.pn-hint`
- **业务动作不进卡片**：提交 / 暂存 / 取消留在底部固定提交条

```html
<div class="content submit-pad">

  <div class="card">                       <!-- 信息卡：表单字段 -->
    <div class="card-head"><h3 class="card-title">订单信息</h3></div>
    <div class="form-row">…</div>
    <div class="form-row" style="align-items:flex-start;">备注行…</div>
  </div>

  <div class="card">                       <!-- 明细卡：表格 + 卡头动作 -->
    <div class="card-head">
      <h3 class="card-title">采购明细</h3>
      <div class="head-btns"><button class="btn btn-dashed btn-sm" onclick="addDetailRow(this)">添加一行</button></div>
    </div>
    <div class="table-wrap edit-tbl">…</div>
  </div>

  <div class="submit-bar">取消 / 保存草稿 / 提交审核</div>
</div>
```

> **改造已有页面时**：整页只包着一张卡、卡内混着表单与明细的，按上面的规则拆开；原卡内的粗体小标题提升为卡片标题，备注行归到信息卡末尾。

## HTML

```html
<div class="card">
  <div class="card-head"><h3 class="card-title">基础信息</h3></div>

  <!-- 文本输入（带清空 + 字数统计） -->
  <div class="form-row">
    <div class="form-label"><span class="req">*</span>产品名称：</div>
    <div class="input-box" style="width:380px;">
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
    <div class="input-box select-box" style="width:380px;">
      <span>彩虹</span><span class="caret">▾</span>
    </div>
  </div>
</div>
```

label 后需要说明图标时加 `.info-ico`（13px 圆圈 i）；输入框下方的固定说明用 `.pn-hint`，行内代码符号用 `<code>`。

## CSS

```css
.form-row { display:flex; align-items:center; margin-bottom:20px; }
.form-row:last-child { margin-bottom:0; }
.form-label { flex:0 0 120px; text-align:right; margin-right:8px; font-size:13px; color:var(--text); white-space:nowrap; }
.req { color:var(--danger); margin-right:4px; }
.info-ico { color:var(--text-3); margin:0 2px; display:inline-flex; vertical-align:middle; }

.input-box { width:380px; height:30px; border:1px solid var(--input-border); border-radius:6px; display:flex; align-items:center; padding:0 11px; background:#fff; font-size:13px; color:var(--text); }
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

- **页面底部固定提交条**：按钮组**居中**（`justify-content:center` + `padding:10px 24px`）——右对齐会与右下角常驻悬浮入口（流程图 / 标注等 fab）打架；实测右对齐时「提交」按钮被 fab 压住。提交条放**内容区内部**（`.content` 的直接子元素），配合 `.content.submit-pad`（`padding-bottom:72px`）保证滚到底不被遮挡
- 按钮体系见 modal.md 的 `.btn` 组（两模板共用）
- **控件宽度统一**：同一表单内所有控件同宽（推荐 **380px**），不要 180 / 520 混排；表格内控件按列分配宽度，避免整表超出容器产生横向滚动
- **日期字段用日期选择器**：`<input type="date">`，不要用文本输入框充当日期；日期框**必须带 `value`**（原型期给示例日期），空值的 date 控件在「不可输入」类校验里会被判死
- **自动生成 / 不可编辑字段用文本展示，不要用 `readonly` 输入框**：`<div class="input-box" style="width:380px;background:#fafafa;"><span style="color:#8c8c8c;">CGRK-20260831-007（自动生成 · 不可编辑）</span></div>`——`readonly` 输入框在没有豁免逻辑的项目里会被校验脚本报「不可编辑」（见下条）
- **备注**：并入所属表单卡片**末尾**（表单区最后一个字段），不单独成卡——除非同一张卡还有多个补充字段（如「质检要求 / 随货单据 / 备注」）。用文本域（`<textarea>`），**不是单行输入框**——遗漏时会退化成 28px 单行框，与样板的 72px 文本域一眼可辨。**外壳沿用 `.input-box`**（`height:auto;padding:6px 11px`）内嵌 `<textarea>`（`min-height:72px;resize:vertical`），这样边框、focus 高亮、placeholder 与表单其他控件完全一致；多行控件的 label 用顶部对齐（`align-items:flex-start` + label `padding-top:6px`）
- **返回入口不重复**：若提交条已有「取消」回列表，页面顶部**不再**另放「返回列表」按钮
- **字段取值优先走数据字典或主数据**：选项不写死——字典项取 `dictItems` 按 `category` 过滤，主数据取对应实体键（如物料档案）。**联动字段**（如物料编码 ↔ 物料名称）任一变更另一自动同步，并顺带带出可从主数据推导的相邻字段（规格 / 单位）；新增行与程序生成的行也要动态渲染下拉，不能只有初始行有
- **预填/自动计算字段**：加 `readonly` + `class="auto"`。⚠️ 是否被豁免取决于**各项目 audit 的实现**——没有豁免逻辑的项目（如包装租赁 `audit_interaction.py` 判据是 `el.disabled || el.readOnly`）里，只读输入框仍会被报「不可编辑」，此时改用**文本展示**（`<td class="td-num auto-cell">值</td>`），并让计算脚本兼容文本节点
