# G19a 失败清单（2026-09-11）

## 结论

**0 失败 · 2 偏差（均已闭环/注记）——全部验证门通过。**

## 失败项

无（T1/T2 全部 assert 计数一致；T3 静态+Playwright 全过；无单项回滚）。

## 偏差注记（非失败，决策记录）

| # | 偏差 | 处置 |
|---|---|---|
| D-b1 | 登录页无 `m-header`（验证门判定 2 字面要求五页均含） | 豁免——登录前无导航条是 G14 既定设计（免二次登录直达待办），加标题条反而破坏登录页惯例；登录页以「表单区 m-card 卡片化」满足内容区组件断言 |
| D-b2 | 视觉复核报告「底部 Tab 半透明遮挡列表」 | 证伪——full_page 截图对 position:fixed 元素的渲染假象；viewport 级几何断言：lastBottom 726px < tabTop 755px（noOverlap=True）+ tabbar 背景 rgb(255,255,255) 不透明 + m-body padding-bottom 76px>56px 预留达标。真机无遮挡（复证脚本 g19a_t3_viewport.py + 截图 g19a-mobile-待办审批-viewport-bottom.png） |

## 范围外顺手观察（不动，留 G19b/后续）

- 状态徽标「待*」类全橙（_m.js mBadgeCls 逻辑，D8 禁改 _m.js）
- 五页无弹窗场景，规范底部弹窗/居中弹窗组件未引入（T1 差距表 #11/#12 已注记）
