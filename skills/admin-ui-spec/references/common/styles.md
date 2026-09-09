# 样式规范

整页 CSS 内联在 `<style>` 中。以下三块原样复制，业务样式另起段落追加。

## 1. 设计变量与基础

```css
:root {
  --primary: #1677ff;
  --primary-bg: #e6f4ff;   /* 选中菜单底 */
  --strip-bg: #e6f7ff;     /* 浅蓝信息条 / 激活页签 */
  --page-bg: #f5f5f5;
  --side-bg: #fafafa;
  --thead-bg: #fafafa;
  --border: #f0f0f0;
  --input-border: #d9d9d9;
  --text: #262626;
  --text-2: #595959;
  --text-3: #8c8c8c;
  --placeholder: #bfbfbf;
  --danger: #ff4d4f;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  background: var(--page-bg);
  color: var(--text);
  font-size: 13px;
  line-height: 1.5715;
  min-width: 1200px;
  margin: 0;
}
```

## 2. 壳样式（顶栏 + 布局 + 页签条）

```css
/* 顶栏 */
.topbar { height:44px; background:#fff; border-bottom:1px solid var(--border); display:flex; align-items:center; }
.topbar .logo { width:208px; flex-shrink:0; padding-left:24px; color:var(--primary); font-size:16px; font-weight:700; letter-spacing:.5px; white-space:nowrap; }
.topbar .tools { margin-left:auto; display:flex; align-items:center; gap:18px; padding-right:20px; color:var(--text-2); }
.topbar .tools .ico-btn { cursor:pointer; display:inline-flex; align-items:center; }
.topbar .manual { color:var(--primary); font-size:13px; display:inline-flex; align-items:center; gap:4px; cursor:pointer; }
.topbar .avatar { width:28px; height:28px; border-radius:50%; background:var(--primary); display:inline-flex; align-items:center; justify-content:center; cursor:pointer; }

/* 主体：侧边栏 + 右侧（模式 A 整窗滚动；模式 B 见 page-skeleton.md） */
.body { display:flex; align-items:stretch; }
.sidebar { width:208px; flex-shrink:0; background:var(--side-bg); border-right:1px solid var(--border); display:flex; flex-direction:column; min-height:calc(100vh - 44px); }
.main-col { flex:1; min-width:0; display:flex; flex-direction:column; }

/* 页签条 */
.tabs { background:#fff; border-bottom:1px solid var(--border); padding:8px 16px 0; display:flex; gap:6px; overflow-x:auto; }
.tab { height:28px; display:inline-flex; align-items:center; gap:6px; padding:0 10px; border:1px solid var(--border); border-radius:4px; background:#fff; color:var(--text); font-size:13px; white-space:nowrap; cursor:pointer; }
.tab .close { color:var(--text-3); font-size:12px; line-height:1; }
.tab .close:hover { color:var(--text); }
.tab.active { background:var(--strip-bg); border-color:transparent; color:var(--primary); }
```

## 3. 侧边栏菜单 + 系统切换

```css
.side-menu { flex:1; padding:8px 0; overflow-y:auto; list-style:none; margin:0; }
.side-menu ul { list-style:none; margin:0; padding:0; }
.sm-ico { width:16px; height:16px; flex:none; margin-right:10px; display:inline-flex; align-items:center; justify-content:center; }
.sm-link { height:40px; display:flex; align-items:center; padding:0 24px; font-size:14px; color:#262626; cursor:pointer; white-space:nowrap; }
.sm-link:hover { color:#1677ff; }
.sm-arrow { margin-left:auto; display:inline-flex; color:#8c8c8c; transition:transform .2s; }
.sm-item:not(.open) > .sm-sub { display:none; }
.sm-item.has-sub.open > .sm-link { color:#1677ff; }
.sm-item.has-sub.open > .sm-link .sm-arrow { transform:rotate(180deg); color:#1677ff; }
.sm-sub .sm-link { padding-left:48px; }
.sm-sub .sm-sub .sm-link { padding-left:64px; }
.sm-link.selected { background:#e6f4ff; color:#1677ff; border-right:3px solid #1677ff; }

.side-foot { position:relative; flex:none; border-top:1px solid #f0f0f0; padding:8px; }
.sys-cur { display:flex; align-items:center; gap:8px; height:36px; padding:0 8px; border-radius:6px; cursor:pointer; color:#262626; }
.sys-cur:hover { background:#f0f0f0; }
.sys-badge { width:24px; height:24px; border-radius:6px; background:#1677ff; color:#fff; font-size:12px; font-weight:600; display:inline-flex; align-items:center; justify-content:center; flex:none; }
.sys-name { flex:1; min-width:0; font-size:13px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.sys-swap { color:#8c8c8c; display:inline-flex; flex:none; }
.sys-pop { position:absolute; bottom:calc(100% + 4px); left:8px; right:8px; background:#fff; border:1px solid #f0f0f0; border-radius:8px; box-shadow:0 6px 16px rgba(0,0,0,.12); padding:6px; display:none; z-index:1000; }
.sys-pop.show { display:block; }
.sys-pop-title { font-size:12px; color:#8c8c8c; padding:6px 10px 8px; border-bottom:1px solid #f0f0f0; margin-bottom:4px; }
.sys-item { display:flex; align-items:center; padding:8px 10px; font-size:13px; color:#262626; border-radius:4px; cursor:pointer; }
.sys-item:hover { background:#f5f5f5; color:#1677ff; }
.sys-item.current { color:#1677ff; background:#e6f4ff; font-weight:600; cursor:default; }
.sys-item .check { margin-left:auto; }
```

## 4. 模式 A 必带补丁（整窗滚动页）

```css
/* 整窗滚动布局：系统切换块固定到视口左下角 */
.side-foot { position:fixed; left:0; bottom:0; width:208px; background:var(--side-bg, #fff); z-index:30; }
.side-menu { padding-bottom:64px; }
```

## 5. 内容区卡片约定

```css
.content { padding:16px 20px 32px; }
.card { background:#fff; border-radius:8px; padding:20px 24px; margin-bottom:16px; box-shadow:0 1px 2px rgba(0,0,0,.03); }
.card-title { font-size:16px; font-weight:600; color:#1a1a1a; margin-bottom:20px; }
```

## 要点

- 主色一律 `#1677ff`，选中底 `#e6f4ff`，不要新造蓝色
- 组件规范自带色不算新造蓝色：表格行 hover `#f5faff`（data-table.md）、按钮 hover `#4096ff`（modal.md）
- 菜单/页签/表格等 hover 文字色用 `var(--primary)`
- 侧栏宽 208px 固定；顶栏 44px 固定；正文 13px，菜单 14px，卡片标题 16px
- 状态色：成功/通过 `#52c41a` 系、失败/驳回 `var(--danger)`、警示橙 `#fa8c16` 系（与已有页面标签一致）
