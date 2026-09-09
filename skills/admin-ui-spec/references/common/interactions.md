# 统一交互脚本

放在页面**最后一个** `<script>` 块（业务脚本之后），三行职责：跳转、菜单折叠、系统切换弹层。原样复制，不要改。

```html
<script>
/* ===== 菜单折叠 / 左下角系统切换（统一脚本） ===== */
function go(url) { location.href = url; }
document.querySelectorAll('.sm-item.has-sub > .sm-link').forEach(function (link) {
  link.addEventListener('click', function () { link.parentElement.classList.toggle('open'); });
});
(function () {
  var btn = document.getElementById('sysSwitchBtn');
  var pop = document.getElementById('sysPop');
  btn.addEventListener('click', function (e) { e.stopPropagation(); pop.classList.toggle('show'); });
  pop.addEventListener('click', function (e) { e.stopPropagation(); });
  document.addEventListener('click', function () { pop.classList.remove('show'); });
})();
</script>
```

## 行为约定

- `go(url)`：所有页面跳转唯一入口（菜单项、系统切换都用它），url 为相对路径
- 菜单折叠：点 `.has-sub` 的 `.sm-link` 切换父级 `open`；初始状态由 HTML 上的 `open` 类决定（当前页所在链路展开）
- 系统切换：点 `.sys-cur` 切换 `.sys-pop` 的 `show`；点弹层内部不冒泡；点页面任意处关闭
- 不做登录校验、不加遮罩层——原型默认已单点登录
- 存量页面存在「统一脚本三段与业务脚本合并在同一 `<script>` 块、且三段在块首」的写法，功能等效，视为合法；新页面仍按业务脚本在前、统一脚本三段垫底
