#!/usr/bin/env bash
# 项目编码一致性检查（在项目根目录运行：bash check_consistency.sh [项目根目录]）
# 三项检查：裸写缩写 / 相对链接磁盘存在性 / 附录清单↔实际文件（第三项人工核对）
set -uo pipefail
cd "${1:-.}" || exit 1

echo "== 1. 裸写缩写检查（应为 0；排除全码内的 -X0N；豁免：附录清单行内缩略、更名历史条目）=="
grep -rnoE --include='*.md' --exclude-dir={.prompts,agent-handoff,99-归档} "(^|[^-A-Za-z0-9/])[ADF]0[0-9]" . || echo "OK: 无裸写缩写"

echo
echo "== 2. 相对链接磁盘存在性（含子文件夹，路径相对文件所在目录解析）=="
found=0
while IFS= read -r -d '' f; do
  while IFS= read -r p; do
    p="${p#](./}"
    p="${p%)}"
    [ -e "$(dirname "$f")/$p" ] || { echo "缺失: $f -> $p"; found=1; }
  done < <(grep -o '](\./[^)]*)' "$f" || true)
done < <(find . -name '*.md' -not -path './.prompts/*' -not -path './99-归档/*' -print0)
[ "$found" -eq 0 ] && echo "OK: 链接全部存在"

echo
echo "== 3. 附录清单 10.2 ↔ 实际文件双向核对（人工，对照主文档附录）=="
echo "提示: 打开各 R01 附录 10.2，核对每个编码的路径列与磁盘文件一一对应"

# 教训：批量 sed 展开裸写缩写时，范围缩写（~F06、/F02）会按所在文件阶段错误展开跨阶段引用；
# 展开后必须逐条人工核对语义；历史条目（更名日志）应回写当时原貌，不被全局替换污染。
