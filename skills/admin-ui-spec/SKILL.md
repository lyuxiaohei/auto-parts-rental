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
4. 按页面类型从 `references/components/` 取业务组件模板（见路由表）
5. 页面尾部引入 `references/common/interactions.md` 的统一脚本

## 模板路由

**通用模板（每个页面必备）：**

| 文件 | 内容 |
|---|---|
| `references/common/page-skeleton.md` | 页面骨架、顶栏、页签条、两种滚动布局模式 |
| `references/common/sidebar-menu.md` | 两系统菜单数据（名称/图标/链接）+ 左下角系统切换块 |
| `references/common/styles.md` | 设计变量、顶栏/侧边栏/内容区卡片 CSS |
| `references/common/interactions.md` | 菜单折叠与系统切换的统一 JS |

**业务组件模板（按页面类型取用）：**

| 要什么 | 文件 | 内容 |
|---|---|---|
| 筛选区域 | `references/components/filter-bar.md` | 查询表单网格、收起/重置/查询、状态页签 |
| 列表 | `references/components/data-table.md` | 数据表格、固定操作列、状态标签、复选框 |
| 分页器 | `references/components/pagination.md` | 条数信息、页码、每页条数、跳转 |
| 表单 | `references/components/form.md` | 分卡片表单、必填星号、输入/单选/复选/下拉、校验反馈 |
| 弹窗 | `references/components/modal.md` | 模态框结构、开关 JS、按钮体系 |

典型组合：**列表页** = 通用 + filter-bar + data-table + pagination；**表单页** = 通用 + form +（可选）modal。

## 硬性规则

- 所有按钮/操作链接必须绑定真实交互（开弹窗 / 页面跳转 / `window.print()` / 明确视觉态），**不允许裸元素无反馈**——静态原型同理
- 同一系统的所有页面共用**同一份菜单**：名称、图标、顺序完全一致
- 顶栏 logo 纯文字无图标：供应链「一兆链采供应链管理后台」，商城「商城运营后台」
- 系统切换只出现在侧边栏左下角，点击直接跳转，无登录态、无遮罩
- 主色一律 `#1677ff`（`var(--primary)`），不要新造蓝色
- 样式基准页：`01. 自研系统原型-当前版本/供应链管理后台/商品管理/商品发布.html`
