# PS5 Garlic Save Recovery — Codex Skill

通过现有局域网 Garlic Manager，指导 Codex 备份、检查、重新绑定并验证自有 PS5 存档。

这是恢复工作流程和只读校验工具，不是一键恢复程序。游戏、管理器版本与存档格式需要分别核实；管理器导入成功不能替代主机上的加载、保存、完全退出及重载测试。包内验证案例说明了已确认的范围，不代表所有游戏或固件都兼容。

## 目录约定

- `ps5-garlic-save-recovery/`：可安装的 skill，只含操作说明、界面元数据、参考资料和只读校验脚本。
- 本 README：分享包用途、安装和使用说明。
- `CREDITS.md`：上游作者、项目来源和授权边界。
- `.gitignore`：阻止把临时文件、存档和运行日志误加入仓库。

此目录作为独立分享副本维护。不存放游戏存档、恢复输出、账户信息或实际主机地址；不自动清理。发布用 ZIP、文件清单及本地检查结果放在此目录外。

## 安装

1. 解压分享包，将整个 `ps5-garlic-save-recovery` 文件夹复制到自己的 Codex skills 目录。
2. 默认用户目录通常为 `~/.codex/skills/`；Windows 可在文件资源管理器中使用 `%USERPROFILE%\.codex\skills\`。如果自定义了 CODEX_HOME，则使用该目录下的 `skills/`。
3. 最终结构必须为 `<skills-directory>/ps5-garlic-save-recovery/SKILL.md`，同级保留 `agents/`、`references/` 和 `scripts/`。
4. 如果 Codex 当前会话未发现新 skill，重新打开 Codex 后再使用。

## 使用

在 Codex 中明确调用 `$ps5-garlic-save-recovery`，提供自己的 Garlic Manager 地址、原始备份位置、游戏编号、已验证可用的新存档，以及游戏是否完全关闭。

示例：

> 使用 $ps5-garlic-save-recovery。请通过我的局域网 Garlic Manager 检查这个游戏的跨账户存档。先备份全部当前存档，再验证一个旧进度；我会在主机上完成加载、保存和重载测试。

处理存档时，源文件与恢复结果保留在用户自己的本地目录。此分享包不包含主机连接凭据、实际存档或针对某台主机硬编码的写入脚本。

## 本地校验工具

`scripts/inspect_recovery.py` 使用 Python 3 标准库，不需要额外安装第三方依赖；只检查本地 ZIP 完整性或备份文件长度、SHA-256，不连接主机、不上传或修改存档。

在 skill 文件夹中运行：

    python scripts/inspect_recovery.py --archive <your-save-backup.zip>
    python scripts/inspect_recovery.py --backup-dir <snapshot-directory> --manifest <manifest.json>

备份清单使用 `Save`、`Length`、`SHA256` 字段。ZIP 校验通过不证明镜像内部游戏进度有效。

## 功能边界和来源

不安装漏洞或新有效载荷，不改变固件、网络或账号配置；遇到无效元数据或验证失败时停止写入。Garlic Manager 协议依据是其安装版本的界面与匹配的上游实现：

https://github.com/earthonion/garlic-savemgr

此包只包含 skill 文档和本地校验脚本，不打包 Garlic Manager、游戏文件、上游有效载荷或存档备份。
## Credit / 来源致谢

本 skill 是独立维护的第三方配套工具。存档管理、解密/加密及重新绑定功能来自 [Garlic SaveMgr for PS5](https://github.com/earthonion/garlic-savemgr)，credit 归属 [earthonion](https://github.com/earthonion) 及该项目贡献者。

本仓库维护操作流程、验证要求和本地只读校验脚本；通过链接引用上游项目。详细来源和核对范围见 [CREDITS.md](CREDITS.md)。

2026-10-08 检查的上游版本未声明许可证。本分享包不附带或重新授权 Garlic SaveMgr 的源码、二进制或有效载荷。若未来需要修改和分发上游实现，应先核实其授权；这时 fork 用于保留项目历史，仍需遵守许可要求。
