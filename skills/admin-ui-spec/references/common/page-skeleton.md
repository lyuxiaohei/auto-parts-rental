# 页面骨架

## 整体结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>页面名 - 系统名</title>
<style>/* 见 styles.md：:root 变量 + 壳样式 + 本页业务样式 */</style>
</head>
<body>
  <header class="topbar">…</header>
  <div class="body">
    <aside class="sidebar">…</aside>   <!-- 见 sidebar-menu.md -->
    <div class="main-col">
      <div class="tabs">…</div>        <!-- 页签条 -->
      <div class="content">…</div>     <!-- 业务内容，.card 卡片 -->
    </div>
  </div>
  <script>/* 业务脚本 */</script>
  <script>/* 统一脚本：见 interactions.md */</script>
</body>
</html>
```

## 顶栏（44px）

logo 纯文字，宽 208px 与侧边栏对齐；右侧工具依次为：刷新、通知、（全屏/下载可选）、操作手册、头像。

```html
<header class="topbar">
  <div class="logo">一兆链采供应链管理后台</div>   <!-- 商城页为：商城运营后台 -->
  <div class="tools">
    <span class="ico-btn" title="刷新"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-2.64-6.36"/><path d="M21 3v6h-6"/></svg></span>
    <span class="ico-btn" title="通知"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9a6 6 0 0 1 12 0c0 5 2 6 2 6H4s2-1 2-6"/><path d="M10 20a2 2 0 0 0 4 0"/></svg></span>
    <span class="manual">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M9.2 9a2.8 2.8 0 0 1 5.5.7c0 1.8-2.7 2.3-2.7 3.8"/><line x1="12" y1="17" x2="12" y2="17.01"/></svg>
      操作手册
    </span>
    <span class="avatar" title="账户"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="8" width="14" height="10" rx="3"/><circle cx="10" cy="13" r="0.6" fill="#fff"/><circle cx="14" cy="13" r="0.6" fill="#fff"/><path d="M12 8V4"/><circle cx="12" cy="3.4" r="0.8" fill="#fff"/></svg></span>
  </div>
</header>
```

## 页签条

模拟多页签工作台，当前页签加 `.active`，内容可按页面场景列举 3~6 个。

```html
<div class="tabs">
  <span class="tab">首页 <span class="close">×</span></span>
  <span class="tab">商品列表 <span class="close">×</span></span>
  <span class="tab active">当前页 <span class="close">×</span></span>
</div>
```

## 两种滚动布局模式

- **模式 A · 整窗滚动**（表单页等长内容）：`.body{display:flex;align-items:stretch}`，`.sidebar{min-height:calc(100vh - 44px)}`，窗口整体滚动。**必须**附带 side-foot 固定补丁（见 styles.md 末尾），否则左下角系统切换块会被内容顶到页面底部。
- **模式 B · 定高内滚动**（列表页）：`.body{display:flex;height:calc(100vh - 44px);overflow:hidden}`，侧边栏与内容区各自 `overflow-y:auto`，无需补丁。
  - 合法等效变体：`html,body{height:100%}` + `body{display:flex;flex-direction:column;overflow:hidden}` + `.body{flex:1;min-height:0;display:flex}` + `.sidebar{height:100%}`，行为与模式 B 相同，无需补丁。存量页面大量采用此写法，新页面两种均可。

拿不准时用模式 A + 补丁。
