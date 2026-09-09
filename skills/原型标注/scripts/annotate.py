#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""原型标注注入器：给 HTML 原型页面注入可开关的注释层（数字角标 + 侧边说明面板）。

用法:
  python annotate.py --pages <原型目录> --data annotations.json            # 全量注入
  python annotate.py --pages <原型目录> --data annotations.json --only 仓储作业/小组装列表.html
  python annotate.py --pages <原型目录> --data annotations.json --remove   # 移除注入

标注数据格式见 references/annotation-format.md。
幂等：重复注入自动清理旧注入块后重注。selector 建议用元素开标签前缀（如 <button class="btn"），
完整元素（如 <th>名称</th>）也支持——属性自动插入其开标签。
"""
import argparse, json, pathlib, re, sys

STYLE = '''<style id="proto-notes-style">
body.proto-notes-on [data-note]{position:relative}
body.proto-notes-on [data-note]::after{content:attr(data-note);position:absolute;top:1px;right:1px;min-width:16px;height:16px;padding:0 3px;border-radius:3px;background:#722ed1;color:#fff;font-size:10px;line-height:16px;text-align:center;font-weight:600;box-shadow:0 0 0 1.5px #fff;cursor:pointer;opacity:.75;transition:opacity .15s}
body.proto-notes-on [data-note]:hover::after{opacity:1}
@keyframes pn-blink{0%{box-shadow:0 0 0 2px #722ed1}25%{box-shadow:0 0 0 5px rgba(114,46,209,.35)}100%{box-shadow:0 0 0 2px transparent}}
.proto-pin{display:none;position:absolute;width:300px;background:#fff;border:1px solid #f0f0f0;border-top:2px solid #722ed1;border-radius:6px;box-shadow:0 4px 14px rgba(0,0,0,.13);z-index:890;padding:10px 12px;font-family:-apple-system,'Segoe UI','Microsoft YaHei',sans-serif;font-size:12px;color:#262626}
body.proto-notes-on .proto-pin.pn-open{display:block}
.proto-pin .pnp-close{position:absolute;top:6px;right:8px;cursor:pointer;color:#8c8c8c;font-size:14px;line-height:1;padding:2px}
.proto-pin .pnp-close:hover{color:#262626}
.proto-pin .pnp-t{display:flex;align-items:center;gap:6px;font-weight:600;font-size:13px;color:#262626;padding-right:16px}
.proto-pin .pnp-n{flex:none;min-width:16px;height:16px;padding:0 3px;border-radius:3px;background:#722ed1;color:#fff;font-size:10px;line-height:16px;text-align:center;font-weight:600}
.proto-pin .pnp-d{margin-top:5px;color:#595959;line-height:1.6}
.proto-pin .pnp-b{margin-top:6px;display:flex;gap:4px;flex-wrap:wrap}
.proto-pin .pnp-tag{background:#f9f0ff;color:#722ed1;border-radius:3px;padding:0 6px;font-size:11px;line-height:20px}
.proto-pin .pnp-src{margin-top:8px;padding-top:7px;border-top:1px dashed #e5dff0;font-size:11px;color:#595959;line-height:1.65}
.proto-pin .pnp-src b{color:#722ed1;font-weight:600}
.pn-fab{position:fixed;right:12px;bottom:12px;z-index:880;display:flex;align-items:center;gap:5px;height:24px;padding:0 10px;border-radius:4px;background:#fff;border:1px solid #ddd0ec;color:#722ed1;font-size:11px;font-family:-apple-system,'Segoe UI','Microsoft YaHei',sans-serif;cursor:pointer;box-shadow:0 1px 4px rgba(0,0,0,.06);opacity:.6;transition:opacity .15s}
.pn-fab:hover{opacity:1;border-color:#722ed1}
body.proto-notes-on .pn-fab{background:#f9f0ff;border-color:#722ed1;opacity:.95}
.pn-fab .pn-fab-n{font-family:Consolas,monospace;font-weight:600}
</style>'''

JS = '''<script id="proto-notes-js">
(function(){
  var KEY='proto-notes-on';
  function on(){return location.search.indexOf('notes=1')>-1||localStorage.getItem(KEY)==='1'}
  function apply(){
    document.body.classList.toggle('proto-notes-on',on());
    var fab=document.getElementById('protoNotesFab');
    if(fab){fab.innerHTML=on()?'收起':'标注 <span class="pn-fab-n">'+(document.querySelectorAll('[data-note]').length)+'</span>';fab.title=on()?'收起标注（Alt+N）':'显示标注（Alt+N）'}
  }
  function toggle(){var v=!on();localStorage.setItem(KEY,v?'1':'0');apply()}
  document.addEventListener('keydown',function(e){if(e.altKey&&(e.key==='n'||e.key==='N')){e.preventDefault();toggle()}});
  function place(el,pin){
    var r=el.getBoundingClientRect(),sx=window.scrollX||0,sy=window.scrollY||0;
    var w=pin.offsetWidth||248,h=pin.offsetHeight||90,vw=document.documentElement.clientWidth;
    var x=r.right+sx+12;
    if(x+w>sx+vw-8){var xl=r.left+sx-w-12;x=xl>=sx+8?xl:(sx+vw-w-8)}
    var y=r.top+sy;
    if(y+h>sy+document.documentElement.clientHeight-8)y=Math.max(sy+52,r.bottom+sy-h);
    pin.style.left=x+'px';pin.style.top=y+'px';
  }
  document.addEventListener('click',function(e){
    if(!on())return;
    var tgt=e.target.closest?e.target.closest('[data-note]'):null;
    if(tgt){
      var r=tgt.getBoundingClientRect();
      if(e.clientX>r.right-24&&e.clientY<r.top+22){
        e.stopPropagation();e.preventDefault();
        var pin=document.getElementById('proto-pin-'+tgt.getAttribute('data-note'));
        if(pin){
          if(pin.classList.contains('pn-open')){pin.classList.remove('pn-open')}
          else{pin.classList.add('pn-open');place(tgt,pin)}
        }
      }
    }
  },true);
  document.addEventListener('click',function(e){
    var t=e.target;
    var fab=t.closest?t.closest('.pn-fab'):null;
    if(fab){toggle();return}
    var pc=t.closest?t.closest('.proto-pin'):null;
    if(pc){
      if(t.classList&&t.classList.contains('pnp-close'))pc.classList.remove('pn-open');
      return;
    }
  });
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',apply);else apply();
})();
</script>'''


def find_block_end(html, start, tag):
    pat = re.compile(r'<' + tag + r'\b|</' + tag + r'\s*>', re.I)
    d, p = 0, start
    while True:
        m = pat.search(html, p)
        if m is None:
            return html.find('>', start) + 1
        d += 1 if not m.group(0).startswith('</') else -1
        p = m.end()
        if d == 0:
            return p


def strip_injected(html):
    for tag, marker in (('style', 'id="proto-notes-style"'), ('div', 'id="proto-pins"'), ('script', 'id="proto-notes-js"')):
        while marker in html:
            i = html.find(marker)
            s = html.rfind('<' + tag, 0, i)
            e = find_block_end(html, s, tag)
            html = html[:s] + html[e:]
    html = re.sub(r'\s*data-note="\d+"', '', html)
    html = re.sub(r'\s*pn-flash(?=["\s>])', '', html)
    return html


def mount(html, sel, nid):
    """挂载结果：'ok' / 'miss' / ('ambiguous', n) / 'replaced'（替换元素，::after 不渲染）"""
    n = html.count(sel)
    if n == 0:
        return html, 'miss'
    if re.match(r'<(input|img|br|hr|textarea)\b', sel, re.I):
        return html, 'replaced'
    if n > 1:
        return mount_at(html, sel, nid), ('ambiguous', n)
    return mount_at(html, sel, nid), 'ok'


def mount_at(html, sel, nid):
    i = html.find(sel)
    m = re.match(r'<(\w+)', sel)
    tag = m.group(1)
    open_start = html.rfind('<' + tag, 0, i + m.end())
    open_end = html.find('>', open_start)
    seg = html[open_start:open_end]
    insert = open_end - 1 if seg.rstrip().endswith('/') else open_end
    html = html[:insert] + ' data-note="' + str(nid) + '"' + html[insert:]
    return html


def build_pins(items, codes=None):
    """codes: {'FP3-02': {'name': '小组装单', 'desc': '...'}}，来自 annotations.json 的 _meta.codes。
    有映射时标签显示「编码 · 名称」，便签底部附出处块（编码全称+要点说明），避免裸代号不可读。"""
    pins = []
    for it in items:
        tags, srcs = [], []
        for t in (it.get('fp'), it.get('req')):
            if not t:
                continue
            c = (codes or {}).get(t)
            if c:
                tags.append('<span class="pnp-tag">' + t + ' · ' + c['name'] + '</span>')
                srcs.append('<div class="src-item"><b>' + t + ' ' + c['name'] + '</b>：' + c.get('desc', '') + '</div>')
            else:
                tags.append('<span class="pnp-tag">' + t + '</span>')
        note = (it.get('note') or '').replace('\n', '<br>')
        pins.append('<div class="proto-pin" id="proto-pin-' + str(it['id']) + '">'
                    '<span class="pnp-close">×</span>'
                    '<div class="pnp-t"><span class="pnp-n">' + str(it['id']) + '</span>' + it['title'] + '</div>'
                    + ('<div class="pnp-d">' + note + '</div>' if note else '')
                    + ('<div class="pnp-b">' + ''.join(tags) + '</div>' if tags else '')
                    + ('<div class="pnp-src">' + ''.join(srcs) + '</div>' if srcs else '') + '</div>')
    fab = ('<div class="pn-fab" id="protoNotesFab">标注</div>')
    return '<div id="proto-pins">' + '\n'.join(pins) + '\n' + fab + '</div>'


def inject(page_path, items, codes=None):
    html = strip_injected(page_path.read_text(encoding='utf-8'))
    hit, miss = 0, []
    for it in items:
        html, st = mount(html, it['selector'], it['id'])
        if st == 'ok':
            hit += 1
        elif st == 'miss':
            miss.append('#' + str(it['id']) + ' selector 未命中: ' + it['selector'])
        elif st == 'replaced':
            miss.append('#' + str(it['id']) + ' 替换元素(input/img等)无 ::after，请改挂父级容器: ' + it['selector'])
        else:
            hit += 1
            miss.append('!! #' + str(it['id']) + ' selector 有 ' + str(st[1]) + ' 处匹配，默认挂首个，请消歧: ' + it['selector'])
    pins = build_pins(items, codes)
    html = html.replace('</body>', STYLE + '\n' + pins + '\n' + JS + '\n</body>')
    page_path.write_text(html, encoding='utf-8')
    return hit, miss


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pages', required=True, help='原型根目录')
    ap.add_argument('--data', required=True, help='annotations.json 路径')
    ap.add_argument('--only', help='仅处理指定页面（相对路径）')
    ap.add_argument('--remove', action='store_true', help='仅移除注入')
    a = ap.parse_args()
    root, data = pathlib.Path(a.pages), json.loads(pathlib.Path(a.data).read_text(encoding='utf-8'))
    codes = (data.get('_meta') or {}).get('codes') or {}
    pages = {k: v for k, v in data.items() if not k.startswith('_')}
    todo = {a.only: pages[a.only]} if a.only and a.only in pages else pages
    for rel, items in sorted(todo.items()):
        p = root / rel
        if not p.exists():
            print('!! 页面不存在: ' + rel)
            continue
        if a.remove:
            p.write_text(strip_injected(p.read_text(encoding='utf-8')), encoding='utf-8')
            print('-- 已移除注入: ' + rel)
            continue
        hit, miss = inject(p, items, codes)
        print('OK ' + rel + ': 标注 %d/%d' % (hit, len(items)) + ('；未命中 -> ' + '; '.join(miss) if miss else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
