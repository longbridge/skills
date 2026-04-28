# Longbridge Skills

Anthropic Agent Skills 风格的长桥能力封装,基于本地 `longbridge` CLI(Rust,见 [longbridge-terminal](../longbridge-terminal))。

每个 skill 都是 `<中文名>/SKILL.md + scripts/cli.py` 的双文件结构,可直接 `cp -r` 到 `~/.claude/skills/` 在 Claude Code 内被自动调用。

## 全景(18 个 skill)

详见 [`docs/superpowers/specs/2026-04-28-skill-catalog.md`](docs/superpowers/specs/2026-04-28-skill-catalog.md)。共有工程范式见 [`2026-04-28-skill-platform-protocol.md`](docs/superpowers/specs/2026-04-28-skill-platform-protocol.md)。

### 读取层(13 个,wraps CLI/MCP,已实施 12 个 ✅)

| 类别 | Skills |
|---|---|
| 市场行情(只读) | 行情查询、K线查询、盘口深度、资金流向、市场情绪、期权与窝轮、证券查找 |
| 账户(只读,需登录) | 持仓查询、订单与成交、自选股 |
| 写入(需登录 + 二步确认) | 自选股管理、**股票交易** ⚠️(待实施) |
| 元能力 | 实时订阅 |

### 分析层(5 个,prompt-only,**强依赖 MCP**,已实施 5 个 ✅)

| Skill | 解锁的高频问句 |
|---|---|
| 估值分析 ✅ | "X 估值贵不贵 / 历史百分位" |
| 基本面分析 ✅ | "X 业绩怎么样 / 财务健康吗" |
| 同行对比 ✅ | "X 跟 Y 谁更值得买" |
| 投资组合分析 ✅ | "我账户表现 / 哪只股贡献最多"(需 trade scope) |
| 资讯舆情 ✅ | "X 最近新闻 / 市场怎么看" |

分析层前提:用户先 `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp`。

## 用法(只读 skill)

```bash
# 软链(推荐,便于本仓库内迭代;Claude Code 自动加载)
mkdir -p ~/.claude/skills
ln -s "$PWD/行情查询" "$HOME/.claude/skills/longbridge-quote"
```

实施时按 P0 → P1 → P2 → P3 顺序逐个 skill 上线,详见 catalog 末尾的"实施 plan 顺序"。

## ⚠️ 股票交易 skill(默认不安装)

`股票交易/` 会**实际下单到你的长桥账户**。批量 cp 默认不会装它,必须显式 symlink + 配置软上限。详见 [`skill-11-trading-risk-design.md`](docs/superpowers/specs/2026-04-28-skill-11-trading-risk-design.md)。

## 前置

- 已安装并登录 `longbridge` CLI:`longbridge login`
- `python3 --version` ≥ 3.8

## 设计/计划文档

- 设计:`docs/superpowers/specs/`(平台规约 + 13 个 skill 差异化稿)
- 实施计划:`docs/superpowers/plans/`(按优先级分批写)
