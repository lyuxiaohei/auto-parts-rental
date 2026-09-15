---
name: admin-ui-spec
description: 01. 自研系统原型-当前版本（供应链管理后台 / 商城运营后台）HTML 页面的 UI 开发规范。新建或修改这两个系统的后台页面时使用，保证顶栏、侧边栏菜单、左下角系统切换、配色与交互在全部页面一致。
---

# 后台页面 UI 规范

页面为纯 HTML/CSS/JS 单文件，样式与脚本内联，必须兼容 `file://` 直接打开。

## 使用流程

1. 从 `references/common/page-skeleton.md` 搭骨架（顶栏 + 侧边栏 + 页签条 + 内容区）
2. 按目标系统从 `references/common/sidebar-menu.md` 复制**整份**侧边栏，只改 3 处状态（当前链路 `open`、当前页 `selected`、已有页面挂 `go()` 相对路径）
3. 从 `references/common/styles.md` 复制 CSS 变量与壳样式块
4. **先定交互载体**：按 `references/common/surface-selection.md` 判定本交互用页面还是弹窗（**默认页面**；弹窗只承担确认/提示/选择/拦截）
5. 按页面类型从 `references/components/` 取业务组件模板（见路由表）——**表单页一律分卡片**：一张卡＝一个业务段落（信息 / 明细 / 附件 / 计划），每卡带 `.card-head` + `.card-title` 标题（见 `references/components/form.md`）
6. 页面尾部引入 `references/common/interactions.md` 的统一脚本
7. **结构调整类改动**（拆卡片 / 搬段落 / 删弹窗块 / 加包裹层）改完按 `references/common/page-check.md` 自检——结构坏了浏览器会静默纠错，不做配平与几何体检看不出来

## 模板路由

**通用模板（每个页面必备）：**

| 文件 | 内容 |
|---|---|
| `references/common/page-skeleton.md` | 页面骨架、顶栏、页签条、两种滚动布局模式 |
| `references/common/sidebar-menu.md` | 两系统菜单数据（名称/图标/链接）+ 左下角系统切换块 |
| `references/common/styles.md` | 设计变量、顶栏/侧边栏/内容区卡片 CSS |
| `references/common/interactions.md` | 菜单折叠与系统切换的统一 JS |
| `references/common/page-check.md` | **页面结构自检**：标签配平、卡片体检、症状→根因对照、定位手法 |

**业务组件模板（按页面类型取用）：**

| 要什么 | 文件 | 内容 |
|---|---|---|
| 筛选区域 | `references/components/filter-bar.md` | 查询表单网格、收起/重置/查询、状态页签 |
| 列表 | `references/components/data-table.md` | 数据表格、固定操作列、状态标签、复选框 |
| 分页器 | `references/components/pagination.md` | 条数信息、页码、每页条数、跳转 |
| 表单 | `references/components/form.md` | 分卡片表单、必填星号、输入/单选/复选/下拉、校验反馈 |
| 弹窗 | `references/components/modal.md` | 模态框结构、开关 JS、按钮体系 |
| **载体选择** | `references/common/surface-selection.md` | **什么交互用页面、什么用弹窗**、判定三问、页面三骨架、迁移要点 |

典型组合：**列表页** = 通用 + filter-bar + data-table + pagination；**表单页 / 详情页 / 审核页** = 通用 + form（+ data-table）+ 提交条；**弹窗**仅用于确认 / 提示 / 选择 / 拦截。

## 硬性规则

- 所有按钮/操作链接必须绑定真实交互（开弹窗 / 页面跳转 / `window.print()` / 明确视觉态），**不允许裸元素无反馈**——静态原型同理
- **载体选择默认用页面**：新建 / 编辑 / 详情 / 审核一律做成页面；弹窗只承担确认、提示、选择、拦截四类轻交互（见 `references/common/surface-selection.md`）
- **表单页必须分卡片**：一张卡＝一个业务段落，卡片标题走 `.card-head` + `.card-title`（概括词，如「订单信息」「采购明细」）。**禁止**把明细段留在信息卡里用粗体小字当分隔标题；本卡动作（如「添加一行」）放卡头右侧 `.head-btns`，不要挂在表格下方做整宽按钮
- **卡片标题写法唯一**：一律 `<div class="card-head"><h3 class="card-title">…</h3></div>`；裸 `.card-title` 的下间距（20px）与卡头（14px）不一致，并排即露馅
- 同一系统的所有页面共用**同一份菜单**：名称、图标、顺序完全一致
- 顶栏 logo 纯文字无图标：供应链「一兆链采供应链管理后台」，商城「商城运营后台」
- 系统切换只出现在侧边栏左下角，点击直接跳转，无登录态、无遮罩
- 主色一律 `#1677ff`（`var(--primary)`），不要新造蓝色
- 样式基准页：`01. 自研系统原型-当前版本/供应链管理后台/商品管理/商品发布.html`
