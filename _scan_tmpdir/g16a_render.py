# -*- coding: utf-8 -*-
"""G16a-2：A06 md 全文渲染为 HTML（道远 2026-09-11 点名：内容全转 html，不然无法阅读）
轻量 md 解析（标题/表格/mermaid/引用/列表/粗体/行内码）+ 内嵌 mermaid 离线自包含 + 左侧 TOC
重跑=从最新 md 重新生成（md 仍是真值源）
"""
import pathlib, re, html as H

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROT = ROOT / 'P3-R01-包装租赁管理后台原型'
MD = (PROT / 'P3-R01-A06-实体关系与状态机.md').read_text(encoding='utf-8')
MM = (ROOT / '_scan_tmpdir/mermaid.min.js').read_text(encoding='utf-8')

# ---------- 行内格式 ----------
def inline(t):
    t = H.escape(t, quote=False)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'~~([^~]+)~~', r'<del>\1</del>', t)
    return t

# ---------- 块级解析 ----------
lines = MD.splitlines()
out, toc = [], []
i, n = 0, len(lines)
in_code, code_buf, code_kind = False, [], ''
while i < n:
    ln = lines[i]
    # 代码块
    if ln.startswith('```'):
        if not in_code:
            in_code, code_buf, code_kind = True, [], ln[3:].strip()
        else:
            in_code = False
            body = '\n'.join(code_buf).strip()
            if code_kind == 'mermaid':
                out.append('<pre class="mermaid">' + H.escape(body, quote=False) + '</pre>')
            else:
                out.append('<pre class="rawcode"><code>' + H.escape(body, quote=False) + '</code></pre>')
        i += 1; continue
    if in_code:
        code_buf.append(ln); i += 1; continue
    # 空行
    if not ln.strip():
        i += 1; continue
    # 标题
    m = re.match(r'^(#{1,4})\s+(.*)', ln)
    if m:
        lv = len(m.group(1)); txt = m.group(2).strip()
        aid = re.sub(r'[^\w一-鿿·．.-]+', '_', txt)[:40]
        if lv == 1:
            out.append(f'<h1 id="{aid}">{inline(txt)}</h1>')
        else:
            out.append(f'<h{lv} id="{aid}">{inline(txt)}</h{lv}>')
            if lv == 2:
                toc.append((2, aid, txt))
            elif lv == 3:
                toc.append((3, aid, txt))
        i += 1; continue
    # 引用块
    if ln.startswith('>'):
        buf = []
        while i < n and lines[i].startswith('>'):
            buf.append(lines[i].lstrip('> ').rstrip()); i += 1
        out.append('<blockquote>' + '<br>'.join(inline(b) for b in buf if b) + '</blockquote>')
        continue
    # 表格
    if ln.startswith('|') and i + 1 < n and re.match(r'^\|[\s:|-]+\|?$', lines[i+1]):
        head = [c.strip() for c in ln.strip().strip('|').split('|')]
        i += 2
        rows = []
        while i < n and lines[i].startswith('|'):
            rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]); i += 1
        t = ['<div class="tbl-wrap"><table><thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in head) + '</tr></thead><tbody>']
        for r in rows:
            t.append('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>')
        t.append('</tbody></table></div>')
        out.append(''.join(t))
        continue
    # 无序列表
    if re.match(r'^[-*]\s+', ln):
        buf = []
        while i < n and re.match(r'^[-*]\s+', lines[i]):
            buf.append(re.sub(r'^[-*]\s+', '', lines[i]).strip()); i += 1
        out.append('<ul>' + ''.join(f'<li>{inline(b)}</li>' for b in buf) + '</ul>')
        continue
    # 有序列表
    if re.match(r'^\d+[.、]\s*', ln):
        buf = []
        while i < n and re.match(r'^\d+[.、]\s*', lines[i]):
            buf.append(re.sub(r'^\d+[.、]\s*', '', lines[i]).strip()); i += 1
        out.append('<ol>' + ''.join(f'<li>{inline(b)}</li>' for b in buf) + '</ol>')
        continue
    # 普通段落
    buf = [ln.strip()]
    i += 1
    while i < n and lines[i].strip() and not re.match(r'^(#{1,4}\s|>|\||```|[-*]\s|\d+[.、])', lines[i]):
        buf.append(lines[i].strip()); i += 1
    out.append('<p>' + ' '.join(inline(b) for b in buf) + '</p>')

# ---------- TOC ----------
toc_html = ['<nav class="toc"><div class="toc-title">目录</div>']
for lv, aid, txt in toc:
    short = re.sub(r'^\d+\.\s*', '', txt)[:18]
    toc_html.append(f'<a class="lv{lv}" href="#{aid}">{H.escape(short)}</a>')
toc_html.append('</nav>')
toc_html = ''.join(toc_html)

CSS = '''
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:"Microsoft YaHei","PingFang SC",sans-serif; background:#f5f7fa; color:#1f2329; }
.layout { display:flex; max-width:1380px; margin:0 auto; align-items:flex-start; }
.toc { position:sticky; top:0; width:212px; flex:none; height:100vh; overflow-y:auto; padding:28px 10px 40px 18px; font-size:13px; }
.toc-title { font-weight:700; color:#1677ff; margin-bottom:10px; font-size:14px; }
.toc a { display:block; padding:5px 8px; color:#595959; text-decoration:none; border-left:2px solid transparent; border-radius:0 6px 6px 0; }
.toc a.lv3 { padding-left:20px; font-size:12.5px; }
.toc a:hover { color:#1677ff; background:#e8f1ff; border-left-color:#1677ff; }
.main { flex:1; min-width:0; padding:32px 26px 72px; }
h1 { font-size:23px; color:#1677ff; margin:6px 0 10px; }
h2 { font-size:18px; color:#1677ff; margin:30px 0 10px; padding-bottom:6px; border-bottom:2px solid #e8f1ff; }
h3 { font-size:15.5px; color:#1f2329; margin:20px 0 8px; }
h4 { font-size:14px; margin:14px 0 6px; }
p { font-size:13.5px; line-height:1.85; margin:8px 0; color:#333; }
blockquote { background:#f0f7ff; border-left:4px solid #1677ff; border-radius:6px; padding:10px 14px; font-size:12.8px; color:#4a5568; line-height:1.8; margin:10px 0; }
code { background:#eef1f5; border-radius:4px; padding:1px 5px; font-size:12.3px; font-family:Consolas,Menlo,monospace; color:#c7254e; }
strong { color:#1f2329; }
.tbl-wrap { overflow-x:auto; margin:10px 0 16px; border-radius:8px; box-shadow:0 1px 3px rgba(0,0,0,.06); }
table { border-collapse:collapse; width:100%; background:#fff; font-size:12.8px; }
th { background:#1677ff; color:#fff; font-weight:600; padding:8px 10px; text-align:left; white-space:nowrap; position:sticky; top:0; }
td { padding:7px 10px; border-bottom:1px solid #eef1f5; line-height:1.6; vertical-align:top; }
tbody tr:nth-child(even) { background:#fafbfd; }
tbody tr:hover { background:#f0f7ff; }
.mermaid { display:flex; justify-content:center; overflow-x:auto; background:#fff; border-radius:8px; padding:14px 8px; margin:10px 0 18px; box-shadow:0 1px 3px rgba(0,0,0,.06); }
.rawcode { background:#1f2329; color:#e8eaed; border-radius:8px; padding:14px; overflow-x:auto; font-size:12.5px; margin:10px 0; }
ul, ol { margin:8px 0 8px 22px; font-size:13.5px; line-height:1.9; color:#333; }
.footer { text-align:center; font-size:12px; color:#bfbfbf; margin-top:36px; }
@media (max-width:900px){ .toc{ display:none; } .main{ padding:20px 12px 60px; } }
'''
HTML_DOC = '\n'.join([
'<!DOCTYPE html>', '<html lang="zh-CN">', '<head>', '<meta charset="UTF-8">',
'<meta name="viewport" content="width=device-width, initial-scale=1">',
'<title>A06 实体关系与状态机 - 包装租赁管理后台</title>',
f'<style>{CSS}</style>', '</head>', '<body>',
'<div class="layout">', toc_html, '<div class="main">'] + out +
['<div class="footer">P3-R01-包装租赁管理后台原型 · A06 全文渲染版 · 真值源=同名 .md · mermaid 10.9 内嵌（file:// 离线可用）· 重跑脚本 _scan_tmpdir/g16a_render.py</div>',
'</div></div>', '<script>', MM, '</script>',
'<script>mermaid.initialize({startOnLoad:true, theme:"base", themeVariables:{primaryColor:"#e8f1ff", primaryBorderColor:"#1677ff", primaryTextColor:"#1f2329", lineColor:"#8c8c8c", fontSize:"14px"}, flowchart:{curve:"basis", htmlLabels:true}});</script>',
'</body>', '</html>'])
out_path = PROT / 'P3-R01-A06-实体关系与状态机.html'
out_path.write_text(HTML_DOC, encoding='utf-8')
print('HTML 全文版 written:', out_path.stat().st_size, 'bytes; blocks:', len(out), '; toc:', len(toc))
