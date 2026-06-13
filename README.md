# Codex 查经项目包

这是一个可以放到 GitHub 分享的 Codex 查经项目包。第一版只服务 Codex：安装后，你可以让 Codex 帮你做读经前背景、读经后总结与试卷、指定牧师讲道整理、小组转写稿总结、分享前短提纲，并把历史保存在本地。

## 费用

项目本身 0 元。GitHub 公开仓库通常 0 元。使用 Codex、付费圣经资料、服务器、域名或外部 AI API 时，费用按对应平台为准。

## 安装

在这个项目根目录运行：

```bash
bash scripts/install.sh
```

安装完成后，重启 Codex。之后可以这样说：

```text
用 $bible-study-codex 帮我做约翰福音3:16-21的读经前背景。
```

如果你只想在这个项目里试用，也可以直接用 Codex 打开本文件夹。仓库里的 `.agents/skills/bible-study-codex` 已经是可读的 Skill。

## 常用方式

读经前：

```text
用 $bible-study-codex 做马可福音4:35-41的读经前背景，给历史背景、上下文、重要地名和简易路线图。
```

读经后：

```text
用 $bible-study-codex 总结罗马书8:1-17，并出一份Markdown试卷。
```

指定牧师讲道：

```text
用 $bible-study-codex 查我偏好的牧师有没有讲过路加福音15章。我的牧师名单是：名字1、名字2。
```

小组讨论：

```text
用 $bible-study-codex 总结下面这份Get笔记转写稿，按成员观点和后续问题整理。
```

分享前：

```text
用 $bible-study-codex 帮我把这段经文整理成一个短提纲。先问我几个真实经历问题，再写。
```

## 项目内容

- `.agents/skills/bible-study-codex/`：Codex Skill。
- `scripts/install.sh`：安装脚本。
- `templates/`：读经背景、试卷、小组总结、分享提纲、历史记录模板。
- `guides/get-note.md`：Get笔记使用教学。
- `sources/`：偏好牧师名单模板。
- `examples/`：示例提示词。
- `history/`：本地私有历史保存处。

## 重要规则

- 默认经文译本是和合本 CUV。
- 不把整本圣经打包进项目。
- 历史、地理、讲道信息需要联网核对。
- 查不到来源就不要硬说。
- 讲道整理只处理用户指定的牧师，不随机推荐名单外牧师。
- `history/` 默认不上传 GitHub，也不自动备份。

## 历史保存

私人查经记录请放在 `history/`。这个目录默认只保留说明文件，具体查经记录会被 Git 忽略，避免你把小组内容或个人感受误传到公开仓库。

如果将来想备份历史，可以自己复制到网盘或另建私有仓库。第一版不做自动备份。
