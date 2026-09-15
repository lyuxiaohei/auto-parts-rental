# 页面结构自检（改完必跑）

页面结构出错时**页面照常能渲染**——浏览器会自动纠错，肉眼往往只看到「白底没了」「某个块窄得离谱」这类症状，看不出是标签嵌套坏了。所以结构调整类改动（拆卡片、搬段落、删弹窗块、加包裹层）一律按本文自检。

## 一、四道检查

| 检查 | 判据 | 手段 |
|---|---|---|
| **标签配平** | 每个标签开＝闭；末尾深度归零 | HTML 解析器深度扫描（见下）；**计数法不够用** |
| **卡片体检** | `.content` 的直接子元素只有 `.card` 与 `.submit-bar`；每张卡宽度正常（约等于内容区宽） | Playwright 取 `.content` 子元素几何量 |
| **提交条** | 是 `.content` 的子元素；`justify-content:center`；滚到底不与卡片重叠 | Playwright 取 `getBoundingClientRect` 比较 |
| **行尾** | 与宿主页主导行尾一致（插入块跟随，别引入另一种） | 二进制读计数 `\r\n` 与裸 `\n` |

## 二、症状 → 根因对照

| 症状 | 根因 | 定位 |
|---|---|---|
| 卡片只有几十像素宽、白底「消失」 | 上层容器被**提前闭合**，后续块掉进了外层 flex 壳（如 `.body`）被当成 flex item 压扁 | 取元素 DOM 祖先链，看它是否还在预期的 `.card` 内 |
| 文字/表格裸在灰底上 | 同上——原本包它们的 `.card` 没包住 | 同上 |
| 提交条跑到内容区外、或压在内容上 | `.content` 被提前闭合，或收尾闭合多了/少了 | 标志点深度对比（见下） |
| 解析器报「多余闭合在最后一行」 | 早先的多余 `</div>` 被上层元素「吸收」了，最后一行才露馅 | 标志点深度对比，别直接改最后一行 |
| 页面某区块整体错位、贴左/宽度异常 | 与「卡片塌陷」同源：flex 容器的直接子元素数量变了 | 数 `.content` 的直接子元素 |

## 三、手法

### 1) 解析器深度扫描（首选）

```python
import io
from html.parser import HTMLParser

VOID = {'br','hr','img','input','meta','link','area','base','col','embed','source','track','wbr'}

class Check(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.strays, self.lost = [], [], []
    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))
    def handle_endtag(self, tag):
        if tag in VOID: return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop(); return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                self.lost.append(([t for t, _ in self.stack[i+1:]], self.getpos()[0]))
                del self.stack[i:]; return
        self.strays.append((tag, self.getpos()[0]))

c = Check(); c.feed(io.open(path, encoding='utf-8', errors='ignore').read())
# 期望：c.stack == [] and not c.strays and not c.lost
```

- `c.strays`＝无主闭合（多了）；`c.lost`＝匹配到上层闭合时被丢弃的未闭合元素（少了）；`c.stack`＝文件末尾仍开着的
- **不要只看总数**：`开＝闭` 也可能是「多余闭合被上层吸收」的假平衡，必须看 `lost/strays`

### 2) 标志点深度对比（定位到行）

给页面里的稳定锚点（`.content` / `.card` / `.card-head` / `.submit-bar`）打深度戳，和**同族正常页**逐行对比，第一个分叉处就是病灶。比全文 diff 准，比手工数数快。

### 3) DOM 实测（结论以浏览器为准）

静态推断容易算错层级（容易漏掉 `tabs` 这类同层 div、或编辑器根那样的额外包裹层）。有疑问时直接问浏览器：

```js
// 元素祖先链——判断它到底在不在预期容器内
function chain(el) { var o = []; while (el && el !== document.documentElement) { o.unshift(el.tagName + '.' + (el.className||'').slice(0,16)); el = el.parentElement; } return o.join(' > '); }
// 内容区直接子元素 + 几何量
[...document.querySelector('.content').children].map(e => [e.className, Math.round(e.getBoundingClientRect().width)])
```

### 4) 修补口径

- **缺闭合**：补在对应结构收尾处；不确定位置时，补在 `</body>` 前（等价于浏览器隐式闭合，**渲染零变化**）
- **无主闭合**：按解析器给出的行号删掉（浏览器本就忽略它，删掉同样零变化）
- **修完必须复测**：拿改动前的备份渲染同一页，比对几何量（`scrollHeight` / 元素数 / 关键元素 rect），确认**逐项一致**

## 四、纪律

- **备份先行**：改前把涉及模块整目录复制到临时区（按原相对路径），改坏可整页还原
- **精确替换 + 断言**：每处替换前 `assert 命中数 == 1`，改完再断言旧串为 0；脚本写成可重复执行的（已处理则跳过）
- **别信推断，信实测**：涉及层级/宽度的结论一律用浏览器量一遍，静态数数只用来定位候选
- **改完跑三件套**：标签深度扫描 → 卡片几何体检 → 全站交互审计（死链 / JS 错误 / 按钮可达）
