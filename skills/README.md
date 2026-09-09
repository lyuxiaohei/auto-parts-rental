# skills/ · 项目常用技能分发副本

> **用途**：随 git 仓库分发本项目常用技能，供**新电脑**一键安装。**本机日常调用不走此目录**——Claude Code 读的是 `~/.claude/skills/`（用户级），此处仅为分发快照，不会被加载（刻意不放在 `.claude/skills/` 以免与本机用户级技能双载冲突）。

## 技能清单（2026-09-09 快照，共 5 个）

| 技能 | 用途 | 版本注记 |
|---|---|---|
| goal-creator | 生成无人值守 /goal 命令（三道保险+双层路由） | v7（2026-09-09） |
| 原型标注 | HTML 原型注释层注入/重注/角标维护（A04 体系） | 含 annotate 脚本 |
| admin-ui-spec | 自研后台原型 UI 规范（表格/弹窗/筛选栏/tag 语义） | 含本项目实战回填（sticky-op/弹窗两档/四段式详情） |
| 文件名编码管理 | 工作台目录/项目文档 Pn 编码/归档规则 | |
| humanizer-zh | 中文文案去 AI 味 | |

## 新电脑安装（二选一）

```powershell
# PowerShell
Copy-Item -Path skills\* -Destination "$env:USERPROFILE\.claude\skills\" -Recurse -Force
```

```bash
# Git Bash
cp -r skills/* ~/.claude/skills/
```

安装后重启 Claude Code 会话即生效（`/技能名` 或语义触发）。

## 更新惯例

- 日常改进只改 `~/.claude/skills/` 内的原件
- 需要重新分发时：把对应技能文件夹重新复制覆盖到本目录，随 git 提交（保持 README 快照日期同步）
