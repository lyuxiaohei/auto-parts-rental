# diagram-design 版本管理

> 通用规则见 [VERSIONING.md](../VERSIONING.md)

**注意：** diagram-design 为第三方技能，版本格式 `V1.0`（非 V0.XY），遵循其原有规范。

---

## 当前版本

**V1.01**

---

## 版本历史

| 版本 | 日期 | 变更说明 | 变更文件 | 来源 |
|------|------|---------|---------|------|
| V1.01 | 2026-05-25 | 新增箭头连接规则：§9 自检清单增加 7 项箭头连接检查；type-flowchart.md 新增箭头连接规则段（错误对照表、边坐标公式、行过渡指南、逐箭头自检） | SKILL.md, references/type-flowchart.md | lyuxiaohei/diagram-design |
| V1.0 | — | 初始安装版本，14 种图表类型，编辑级设计系统 | — | cathrynlavery/diagram-design |

---

## 子文件版本

| 文件 | 当前版本 | 说明 |
|------|---------|------|
| references/type-flowchart.md | V1.01 | 流程图布局规范 + 箭头连接规则 |
| references/type-architecture.md | V1.0 | 架构图规范 |
| references/type-sequence.md | V1.0 | 时序图规范 |
| references/type-state.md | V1.0 | 状态机规范 |
| references/type-er.md | V1.0 | ER / 数据模型规范 |
| references/type-timeline.md | V1.0 | 时间线规范 |
| references/type-swimlane.md | V1.0 | 泳道图规范 |
| references/type-quadrant.md | V1.0 | 象限图规范 |
| references/type-nested.md | V1.0 | 嵌套图规范 |
| references/type-tree.md | V1.0 | 树形图规范 |
| references/type-org-chart.md | V1.0 | 组织架构图规范 |
| references/type-layers.md | V1.0 | 层叠图规范 |
| references/type-venn.md | V1.0 | 韦恩图规范 |
| references/type-pyramid.md | V1.0 | 金字塔/漏斗图规范 |
| references/style-guide.md | V1.0 | 设计系统令牌 |
| references/onboarding.md | V1.0 | 首次运行品牌提取 |
| references/primitive-annotation.md | V1.0 | 标注图元 |
| references/primitive-sketchy.md | V1.0 | 手绘变体 |

---

## 在技能链中的角色

diagram-design 是**辅助技能**，被以下技能调用：

| 调用方 | 调用场景 |
|--------|----------|
| logic-list-spec Extract | 页面操作流程图、状态流转图 |
| prd-auto-generator | 全流程图、校验流程图、状态流转图 |

### 调用规则

- **优先级 1**：调用 `/diagram-design` 生成 HTML（需已安装）
- **优先级 2**：回退到 Mermaid 代码块 + SVG 渲染（未安装时）
- 回退时向用户提示安装路径

### 检测方式

检查 `~/.claude/skills/diagram-design/` 目录存在且含 `SKILL.md`。

---

## 输出文档版本

### 命名规则

diagram-design 本身不决定输出路径，由调用方指定：

| 调用方 | 输出路径 |
|--------|---------|
| logic-list-spec | `doc/V{版本}/diagrams/{页面名}_flow.html` |
| prd-auto-generator | `PRD/diagrams/{流程名}.html` |

### 输出格式

单个自包含 `.html` 文件：内联 SVG + CSS，引用 Google Fonts CDN，无 JavaScript 依赖。

### 安装地址

- **上游**：`https://github.com/cathrynlavery/diagram-design`
- **Fork**：`https://github.com/lyuxiaohei/diagram-design`
