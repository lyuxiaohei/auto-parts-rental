# -*- coding: utf-8 -*-
"""R3+R1：全站注入 顶部.tab 切换绑定 + 死按钮全局反馈（重置清空筛选+按压视觉态）。幂等标记 ia-fix。"""
import io, sys, glob, os
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'D:\工作台-吕道远\5-【ACTIVE】汽车物流包装租赁\P3-R01-包装租赁管理后台原型'

BLOCK = '''<script>/*ia-fix: tab-switch + btn-feedback (2026-09-04)*/
/* R3 顶部页签切换（点击换 active；× 不做关闭跳转——原型不销毁页签） */
document.querySelectorAll('.tab').forEach(function (t) {
  t.addEventListener('click', function () {
    document.querySelectorAll('.tab').forEach(function (x) { x.classList.remove('active'); });
    t.classList.add('active');
  });
});
/* R1 死按钮全局反馈：无 onclick 的 button/a 给按压视觉态；「重置」清空所在筛选卡 */
(function () {
  document.addEventListener('click', function (e) {
    var el = e.target.closest ? e.target.closest('button, a, .sm-link') : null;
    if (!el) return;
    if (el.getAttribute('onclick')) return;
    var h = el.getAttribute('href');
    if (el.tagName === 'A' && h && h !== '#' && !/^javascript:/i.test(h)) return;
    if (el.disabled) return;
    var txt = (el.textContent || '').trim();
    if (txt === '重置') {
      var card = el.closest('.filter-card') || el.closest('.card');
      if (card) {
        card.querySelectorAll('input:not([type=checkbox]):not([type=radio])').forEach(function (i) { if (!i.readOnly && !i.disabled) i.value = ''; });
        card.querySelectorAll('select').forEach(function (s) { if (!s.disabled) s.selectedIndex = 0; });
      }
    }
    el.style.transition = 'transform .08s';
    el.style.transform = 'scale(.96)';
    setTimeout(function () { el.style.transform = ''; }, 160);
  }, true);
})();
</script>
'''

done, skip = 0, 0
for p in sorted(glob.glob(f'{BASE}/**/*.html', recursive=True)):
    s = io.open(p, encoding='utf-8', newline='').read()
    if '/*ia-fix: tab-switch' in s:
        skip += 1
        continue
    idx = s.rfind('</body>')
    assert idx > 0, p
    s2 = s[:idx] + BLOCK + s[idx:]
    assert s2.count('</body>') == s.count('</body>') and s2.count('<script') == s.count('<script') + 1
    io.open(p, 'w', encoding='utf-8', newline='').write(s2)
    done += 1
print(f'R3+R1 注入完成: {done} 页注入, {skip} 页幂等跳过')
