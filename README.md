# gh-stars

输入一个 GitHub 用户名，输出他所有仓库按 star 排序的表格，并存成 CSV。

## 安装

需要 Python 3.13+ 和 [uv](https://docs.astral.sh/uv/)。

```bash
git clone git@github.com:qinwang499/gh-stars.git
cd gh-stars
uv sync
```

### 配置 Token（可选）

不带 token 也能用，但 GitHub 限制匿名请求每小时 60 次；带 token 可提高到 5000 次。

在项目根目录建 `.env` 文件：

```
GITHUB_TOKEN=你的token
```

Token 在 https://github.com/settings/tokens 生成，勾选 `public_repo` 即可。`.env` 已被 `.gitignore` 忽略，不会提交。

## 用法

```bash
# 查看帮助
uv run python -m gh_stars --help

# 查询某个用户，显示前 10 个仓库
uv run python -m gh_stars --user octocat

# 只看前 5 个，存到 my.csv
uv run python -m gh_stars --user octocat --top 5 --output my.csv

# 显示调试日志
uv run python -m gh_stars --user octocat -v
```

| 参数 | 说明 | 默认值 |
|---|---|---|
| `--user` / `-u` | GitHub 用户名（必填） | — |
| `--top` / `-t` | 只显示前 N 个仓库 | 10 |
| `--output` / `-o` | CSV 输出路径 | `stars.csv` |
| `--verbose` / `-v` | 显示调试日志 | 关闭 |

## 我要它能做什么

- [x] 项目骨架（config / core / cli 三层）
- [x] 命令行入口 `python -m gh_stars`
- [x] 命令行传入用户名：`--user octocat`
- [x] 拉取该用户所有仓库（处理分页）
- [x] 每个仓库保留四个字段：名字、star 数、语言、最后更新时间
- [x] 按 star 从高到低排序
- [x] 终端打印成表格
- [x] 存成 `stars.csv`，Excel 能直接打开
- [x] 出错时给人话，不甩一堆红色 traceback

## 示例输出

```bash
$ uv run python -m gh_stars --user torvalds --top 5
查询用户：torvalds

排名   仓库名                         STARS  语言          更新
---------------------------------------------------------------
1      linux                         255610  C             2026-11-14
2      AudioNoise                      4533  C             2026-11-12
3      GuitarPedal                     2496  C             2026-11-13
4      uemacs                          2200  C             2026-11-14
5      test-tlb                        1085  C             2026-11-13

已保存到 stars.csv
```

出错时：

```bash
$ uv run python -m gh_stars --user this-user-does-not-exist
查询用户：this-user-does-not-exist
错误：找不到用户 this-user-does-not-exist
程序结束
```

## 项目结构

```
src/gh_stars/
├── __init__.py        版本号
├── __main__.py        入口（python -m gh_stars）
├── api.py             GitHub API 调用、分页
├── cli.py             命令行参数解析（argparse）
├── config.py          常量与 .env 读取
├── core.py            主流程：校验 → 拉取 → 清洗 → 排序 → 输出
├── errors.py          自定义异常
├── logging_setup.py   日志配置（控制台 + 文件）
└── render.py          表格打印与 CSV 导出
```

## 说明

- 日志写入 `gh-stars.log`：控制台显示 INFO 以上，文件记录 DEBUG 以上。
- CSV 使用 `utf-8-sig` 编码，Excel 打开中文不乱码。
- `stars.csv` 和 `gh-stars.log` 均为运行产物，已加入 `.gitignore`。
