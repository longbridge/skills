---
name: 资金流向
description: 查询股票当日主力资金流向时序与大中小单分布(主力净流入、大单买卖、资金分布)。当用户询问主力资金、净流入、大单 / 中单 / 小单、资金分布、机构资金流等场景必须使用此技能。支持港股/美股/A 股/新加坡。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
---

# 资金流向 使用指南

## 版本

`1.0.0`

## 技能概述

本技能提供长桥证券当日主力资金流向查询能力,支持:
- **资金流向时序**(`capital-flow`):当日主力资金净流入/流出曲线,按时间点序列返回
- **资金分布快照**(`capital-dist`,可选):大单 / 中单 / 小单 / 超大单的截面分布(买入/卖出额)
- **多市场**:港股 `.HK`、美股 `.US`、A 股 `.SH`/`.SZ`、新加坡 `.SG`
- **单标的查询**:底层 `capital-flow` / `capital-dist` 都只接受单 symbol,本 skill 一次只查一只

数据来源:**长桥证券**(https://longbridge.com)

**限制**:
- 只查当日数据,不支持历史区间(用户问"过去 X 天资金流"时引导查 K 线 / 成交量)
- 不支持筛选(用户问"今天哪些股票主力大幅流入"时,告知本 skill 只能看单只,需用户提供具体标的)

## 何时使用本技能

当用户询问以下问题时,**必须**使用本技能:
- "今天 NVDA 主力净流入多少" / "茅台资金流向"
- "腾讯今日资金流入曲线"
- "看下 TSLA 大单分布" → 加 `--include-dist`
- "贵州茅台主力 / 大单 / 中单 / 小单" → 加 `--include-dist`
- "看一下 700 资金面" / "茅台资金面" → 加 `--include-dist`
- "今天哪些股票主力大幅流入"(本 skill 不支持筛选,引导用户提供具体标的)

## 核心处理流程

### 步骤 1:识别用户提到的标的

从用户问句里抽取股票名称或代码。可以是:
- 公司中文名(腾讯、贵州茅台、特斯拉)
- 英文 ticker(NVDA、AAPL、TSLA)
- 数字代码(700、600519、300750)

### 步骤 2:补全为 `<CODE>.<MARKET>` 格式

- 全大写英文字母 + 美国常见 ticker → 加 `.US`(NVDA → `NVDA.US`)
- 4 位数字 → 港股 `.HK`(700 → `700.HK`)
- 6 位数字以 `60` 开头 → 沪市 `.SH`(600519 → `600519.SH`)
- 6 位数字以 `00`/`30` 开头 → 深市 `.SZ`(300750 → `300750.SZ`)
- 中文公司名 → 知识映射(腾讯 → `700.HK`,贵州茅台 → `600519.SH`,特斯拉 → `TSLA.US`)
- 无法判断市场 → **必须反问用户确认**,不要瞎猜

### 步骤 3:决定子命令路由

| 用户语义 | flag |
|---|---|
| 时序 / 流向 / 净流入(随时间) | (默认,只 flow) |
| 大单 / 中单 / 小单 / 分布 / 截面 | `--include-dist` |
| 综合("看一下资金面") | `--include-dist` |

### 步骤 4:调用 CLI

```bash
# 默认:只查时序
python3 scripts/cli.py -s NVDA.US

# 同时查分布
python3 scripts/cli.py -s 600519.SH --include-dist
```

### 步骤 5:解析返回的 JSON

**默认**(只 capital-flow):

```json
{
  "success": true,
  "source": "longbridge",
  "skill": "资金流向",
  "skill_version": "1.0.0",
  "symbol": "TSLA.US",
  "datas": {
    "flow": [ /* 原 capital-flow 数组,时序 */ ]
  }
}
```

**`--include-dist`**:

```json
{
  "success": true,
  "source": "longbridge",
  "skill": "资金流向",
  "skill_version": "1.0.0",
  "symbol": "TSLA.US",
  "datas": {
    "flow": [ ... ],
    "distribution": { /* 原 capital-dist 对象 */ }
  }
}
```

错误时:

```json
{
  "success": false,
  "source": "longbridge",
  "skill": "资金流向",
  "skill_version": "1.0.0",
  "error_kind": "auth_expired" | "binary_not_found" | "subprocess_failed" | "no_input" | "invalid_input_format",
  "error": "面向用户的中文人话错误描述",
  "details": { "..." }
}
```

### 步骤 6:回答用户

组织语言时:
- **必须强调数据来源于长桥证券**
- 主力净流入用 ▲(正)/ ▼(负)或 +/- 表示方向
- `capital-dist` 字段名为英文,按以下映射翻译为中文:

| 字段(假设) | 中文 |
|---|---|
| `large_in` / `large_out` | 大单流入 / 流出 |
| `medium_in` / `medium_out` | 中单流入 / 流出 |
| `small_in` / `small_out` | 小单流入 / 流出 |
| `super_in` / `super_out`(若有) | 超大单流入 / 流出 |

实际字段名以 longbridge JSON 输出为准,LLM 根据语义猜测;cli.py 不做映射,避免底层改字段名时跟着改。

- 时序数据展示成自然语言摘要(如"开盘到现在累计净流入 X 亿,午后开始流出"),不要把原始数组塞给用户
- 用户问"过去 X 天资金流"时,告知本 skill 只能查当日,引导查 K 线

## CLI 接口文档

### 命令行参数

| 参数 | 简写 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `--symbol` | `-s` | 是 | — | 股票代码,**只接受单个**,格式 `<CODE>.<MARKET>` |
| `--include-dist` | — | 否 | false | 同时查询资金分布(`capital-dist`) |
| `--format` | — | 否 | `json` | 输出格式,目前仅支持 `json` |
| `--longbridge-bin` | — | 否 | `longbridge` | 重写底层 CLI 路径(测试/调试用) |
| `--timeout` | — | 否 | `30` | subprocess 超时秒数 |

### 调用示例

```bash
# 时序
python3 scripts/cli.py -s NVDA.US

# 时序 + 分布
python3 scripts/cli.py -s TSLA.US --include-dist

# 港股
python3 scripts/cli.py -s 700.HK --include-dist

# A 股
python3 scripts/cli.py -s 600519.SH
```

### 退出码

- `0` — 业务成功(`success: true`)
- `1` — 业务错误(参数错、空结果、登录态过期、传了多个 `-s`)
- `2` — 系统错误(找不到 longbridge 二进制、subprocess 异常)

## 输出 JSON Schema

见上方"步骤 5"。`datas` 永远是对象;`datas.flow` 永远存在(时序数组),`datas.distribution` 仅在 `--include-dist` 时存在。

## 数据来源标注

**重要提示**:
- 引用本技能返回的任何资金流入流出、大单/中单/小单数据时,**必须**强调"数据来源于长桥证券"
- 如果未查到数据,引导用户去 https://longbridge.com 或长桥 App 确认

## 错误处理

按 `error_kind` 给用户的话术:

| `error_kind` | 用户侧话术 |
|---|---|
| `binary_not_found` | "长桥 CLI 工具未安装,请先安装 longbridge-terminal: https://github.com/longportapp/longbridge-terminal" |
| `auth_expired` | "长桥登录态过期了,请在终端跑 `longbridge login` 重新授权" |
| `subprocess_failed` | "查询失败:<details.stderr>。可以稍后重试或检查代码格式。" |
| `no_input` | "请告诉我要查的股票代码或公司名" |
| `invalid_input_format` | "代码格式不对,要写成 `<CODE>.<MARKET>`,例如 `NVDA.US`、`700.HK`、`600519.SH`;且本 skill 一次只能查一只标的" |

## 代码结构

```
资金流向/
├── SKILL.md          # 本文件
└── scripts/
    ├── cli.py        # CLI 入口(零依赖,subprocess 调 longbridge capital-flow / capital-dist)
    └── test_cli.py   # unittest 测试(可选,装 skill 时可删)
```
