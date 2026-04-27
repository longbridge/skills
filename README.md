# Longbridge Skills

Anthropic Agent Skills 风格的长桥能力封装,基于本地 `longbridge` CLI(Rust,见 [longbridge-terminal](../longbridge-terminal))。

每个 skill 都是 `<中文名>/SKILL.md + scripts/cli.py` 的双文件结构,可直接 `cp -r` 到 `~/.claude/skills/` 在 Claude Code 内被自动调用。

## 当前 Skill

- `行情查询/` — 实时报价 + 静态参考(行业/市值/状态),支持港股/美股/A 股/新加坡

## 用法

```bash
# 一次性
cp -r 行情查询 ~/.claude/skills/longbridge-quote
# 或者软链(便于本仓库内迭代)
ln -s "$PWD/行情查询" ~/.claude/skills/longbridge-quote
```

## 前置

- 已安装并登录 `longbridge` CLI:`longbridge login`
- `python3 --version` ≥ 3.8

## 设计/计划文档

- 设计:`docs/superpowers/specs/`
- 实施计划:`docs/superpowers/plans/`
