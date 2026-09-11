# G19a T1 差距清单（miniprogram-components ↔ _m.css 现状）

> 2026-09-11 · 留档不改文件 · 配色按 D1：结构取规范、颜色留项目（#1677ff+#07c160）
> 规范源：`C:\Users\Administrator\.claude\skills\prototype-design\components\miniprogram-components.md` + `templates\miniprogram-template.md`

## 一、不适用·跳过（骨架件，D2：企微 H5 原生承载）

| 组件 | 规范要求 | 判定 |
|---|---|---|
| phone-frame 手机外框 | 375px 容器 | 不引入——m-page max-width 480 居中已覆盖桌面预览 |
| status-bar 状态栏 | 44px 预留+09:41 | 不引入——企微 App 原生状态栏 |
| capsule-btn 胶囊按钮 | 右上角胶囊 | 不引入——企微原生 |
| nav-bar 小程序导航栏 | 44px 白底+back-btn 居中 | 不引入——保留 m-header 蓝底轻标题条（现状形态，仅对齐字号/间距） |
| 商品网格 2 列卡片 | product-grid aspect-ratio:1 | 不适用——本项目无商品网格场景 |
| 价格红 #ee0a24 | 价格数字 | 不适用——电商红零混入（验证门断言） |

## 二、适用差距（组件/规范要求/现状/动作）

| # | 组件 | 规范要求 | 现状 | 动作 |
|---|---|---|---|---|
| 1 | CSS 变量体系 | --primary/--card-bg/--bg-color 等变量命名 | 全部硬编码色值 | 重写：:root 落变量块（值=项目色板），组件全部改引变量 |
| 2 | 卡片 | 圆角 12px、白底、阴影 | m-card/m-item/m-stat 圆角 10px | 对齐 12px |
| 3 | 按钮 | 全圆角胶囊 22px、padding 10 24、字号 14-16、600、:active opacity .85 | m-btn 圆角 8px 方角 | 对齐胶囊 22px（微信生态通用形态；height 44 时 22=正圆） |
| 4 | 底部 Tab | 56px 高、tab-item flex column gap 2、字号 10、#999、active 主色+600 字重、**仅纯文字/SVG 禁 Emoji** | padding 6 0 8、字号 11、active 只变色、**图标=Emoji（☑📦👤）** | 重写 tabbar 样式 + 三页 HTML 换 inline SVG 线性图标（stroke currentColor） |
| 5 | Tab badge | 圆角 7 全圆、9px、红底 | 无 badge 场景 | 不新增（无数据源，避免假功能） |
| 6 | chips 筛选 | padding 6 14、圆角 18、border #ddd、selected 主色边+浅底+600 | padding 6 12、圆角 14、#e5e6eb、selected 达标 | 对齐 padding/圆角 |
| 7 | 搜索框 | （规范无独立定义，参照表单） | 18px 全圆角+icon | 保留，仅引变量 |
| 8 | 表单输入 | 高 44、圆角 8、focus 态 | m-field 高 44 圆角 8 focus 蓝 | 达标，仅引变量 |
| 9 | 徽标 badge | 全圆角（7px 参考） | 圆角 4px | 对齐全圆（≥高度/2） |
| 10 | 空状态 | （规范未单列组件） | m-empty 纯文字 13px | 增强：SVG 图标+主文案+副文案三层结构（提升观感，D4 截图人审） |
| 11 | 底部弹窗 | 圆角 16 16 0 0、translateY 动画、overlay .5 | 五页无弹窗场景 | 不新增（无业务需要，T2 注记） |
| 12 | 居中弹窗 | max-width 320、圆角 16 | 无场景 | 不新增（同上） |
| 13 | 左滑删除 | 触屏手势 | 无场景 | 不新增（同上） |
| 14 | 单选圆 | 18px、border 2px、checked 主色 | 无场景 | 不新增（同上） |
| 15 | m-header | （保留形态）字号 17/600 已达标 | padding 14 16 12 | 仅微调：统一高度结构 44px、副标 12px 保留 |
| 16 | 内容区底部预留 | padding-bottom 60px | m-body 76px | 达标（>60，含 safe-area），保留 |
| 17 | tabbar 固定 | position fixed/absolute bottom | fixed+safe-area | 达标，保留 |
| 18 | 纯文字纪律 | 检查清单：Tab/按钮/菜单仅纯文字禁 Emoji | 我的页 m-cell 前缀 Emoji（📷🗄🖥ℹ️） | 去 Emoji 换 SVG 小图标（cell 菜单类） |
| 19 | 返回按钮 | 规范 back-btn 32px SVG | 审批详情用文字字符 ‹ | 换 SVG chevron-left 24px |
| 20 | toast | （规范无定义） | m-toast 已有 | 保留，仅引变量 |
| 21 | 文本可读性 | 状态栏文字白/黑切换 | 不适用（骨架件） | 跳过 |

## 三、T2 施工范围汇总

1. `_m.css` 整文件重写（D5）：变量块+圆角/胶囊/间距对齐+tabbar 56px 重做+empty 增强；类名 m- 前缀全保留；max-width 480/375 视口保留；#1677ff/#07c160 不变
2. HTML 五页（读取-精确替换+assert）：
   - 待办审批/库存查询/我的：tabbar Emoji → inline SVG（待办=list-check、库存=box、我的=user）
   - 我的：m-cell Emoji → SVG 小图标（企微/数据/PC/版本）；退出按钮保留文字
   - 审批详情：返回 ‹ → SVG chevron；m-empty 调用处不变（样式由 css 层增强，innerHTML 的空态结构在 JS 字符串里——D8 禁改 _m.js，页面内联 script 非共享件可改，但空态文案结构简单，css 层增强足够，不动 JS 字符串）
   - 登录：hero 保留纯文字 logo（合规）；按钮自动获胶囊样式（css 层）；无 m-header/tabbar（登录页无导航，达标）
3. 不改：_m.js、底部 Tab 三项构成（D3）、业务功能、demo-data 消费、文件名、URL/onclick 语境
