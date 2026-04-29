---
name: 证券查找
description: 查询市场全部上市证券列表,以及港股市场参与者(经纪商 ID 与名字字典)。当用户询问某市场总共有多少只股票、列出全部 X 市场股票、按代码反查名字、经纪商 ID 翻译等场景必须使用此技能。返回原始字典,不做筛选。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
---

# 证券查找 使用指南

## 版本

`1.0.0`

## 技能概述

元数据查找:

- **securities**:某市场全部证券列表(symbol + name_en + name_cn)
- **participants**:港股经纪商参与者字典(broker_id + name)

数据来源:**长桥证券**(https://longbridge.com)

注意:数据量大(港股 ~2.5k 条,A 股 ~5k+),不要把全部 datas 贴给用户,用 count 回答总数,具体股票名字反查取用户关心的子集。

## 何时使用本技能

- "港股一共有多少只股票" / "美股 listed 数量"
- "经纪商 ID 9000 是谁" / "0001 是哪家券商"
- "列出 A 股全部股票"(LLM 应反问范围)
- "翻译一下经纪商列表"(→ participants)

## 核心处理流程

### 步骤 1:决定子命令

| 用户语义 | 子命令 |
|---|---|
| "X 市场多少股票 / listed / 总数" | securities |
| "经纪商 ID xxx 是谁" / "完整经纪商列表" | participants |

### 步骤 2:市场识别

`securities` 的 `--market`:
- "美股 / US / 纳斯达克" → US
- "港股 / HK" → HK
- "A 股 / 沪深 / SH / SZ" → CN
- "新加坡 / SG" → SG

### 步骤 3:调用工具(securities 优先 MCP,participants CLI 优先)

**路径选择**:
- `participants` → cli.py 默认(本机更快)
- `securities` → **优先走 MCP**(`mcp__longbridge__security_list`),原因:CLI 当前版本对 security-list 偶发后端 param_error,MCP 走 SDK 直连绕过 CLI 中间层
- 本机无 CLI / `binary_not_found` → 全部改 MCP

```bash
# participants 默认走 cli.py
python3 scripts/cli.py participants

# securities 数据量大,如果调用失败优先改走 MCP
python3 scripts/cli.py securities --market HK --timeout 60
python3 scripts/cli.py participants
```

数据量大,securities 用 `--timeout 60`(默认 30s 可能不够)。

### 步骤 4:回答规范

| 用户问的 | 回答策略 |
|---|---|
| "X 市场多少股票" | 用 count 直接回答,不展示 datas 全部 |
| "经纪商 ID xxx 是谁" | 在 datas 里 grep,只回该条 |
| "完整经纪商列表" | 列表 ≤ 100 条可全展示;否则回总数并建议按 ID 反查 |
| "列出全部股票" | 反问"想找哪只 / 哪个行业",引导到行情查询 skill |

- **必须**强调"数据来源于长桥证券"

## CLI 接口文档

```
python3 cli.py securities    [--market HK|US|CN|SG]
python3 cli.py participants
```

通用参数:`--longbridge-bin / --format json / --timeout 30`(securities 建议 `--timeout 60`)。

退出码:`0` 业务成功 / `1` 业务错 / `2` 系统错。

## 输出 JSON Schema

securities:`market / count / datas`(数组,每条 `{symbol, name_en, name_cn}`)

participants:`datas`(数组,每条 `{broker_id, name_en, name_cn}`)

## 数据来源标注

- 引用任何证券或经纪商列表数据时,**必须**强调"数据来源于长桥证券"

## 错误处理

| `error_kind` | 用户侧话术 |
|---|---|
| `binary_not_found` | "长桥 CLI 工具未安装" |
| `auth_expired` | "长桥登录态过期了,请跑 `longbridge login`" |
| `subprocess_failed` | "查询失败:<details.stderr>。可能是数据量大超时,试着加 --timeout 60。" |
| `no_input` | "请告诉我要查什么:securities / participants" |
| `invalid_input_format` | "市场不支持。可选 HK / US / CN / SG" |

## MCP 备选

| cli.py 子命令 | 等效 MCP 工具 |
|---|---|
| `securities` | `mcp__longbridge__security_list` |
| `participants` | `mcp__longbridge__participants` |

由于 cli.py 在 `securities` 上偶发后端 param_error(longbridge-terminal 当前版本的已知问题),如果失败,**优先**改用 `mcp__longbridge__security_list` —— MCP 走的是直接 SDK 调用,不受 CLI 中间层影响。

## 代码结构

```
证券查找/
├── SKILL.md
└── scripts/
    ├── cli.py
    └── test_cli.py
```
