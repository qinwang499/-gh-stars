# gh-stars

输入一个 GitHub 用户名，输出他所有仓库按 star 排序的表格，并存成 CSV。

## 安装

需要 Python 3.13+ 和 [uv](https://docs.astral.sh/uv/)。

```bash
git clone git@github.com:qinwang499/-gh-stars.git
cd gh-stars
uv sync
```

## 用法

```bash
uv run python -m gh_stars
```

## 我要它能做什么

- [x] 项目骨架（config / core / cli 三层）
- [x] 命令行入口 `python -m gh_stars`
- [ ] 命令行传入用户名：`--user octocat`
- [ ] 拉取该用户所有仓库（处理分页）
- [ ] 每个仓库保留四个字段：名字、star 数、语言、最后更新时间
- [ ] 按 star 从高到低排序
- [ ] 终端打印成表格
- [ ] 存成 `stars.csv`，Excel 能直接打开
- [ ] 出错时给人话，不甩一堆红色 traceback

## 示例输出

（等有了再补）