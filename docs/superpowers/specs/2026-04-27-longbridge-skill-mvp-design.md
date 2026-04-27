# Longbridge Skill MVP — 设计稿

**Date:** 2026-04-27
**Status:** Draft (awaiting user review)

## 背景

我们已经在 `/Users/hogan/work/longbridge/longbridge-terminal/` 维护一个名为 `longbridge` 的 Rust CLI(v0.17.4),包装了长桥 OpenAPI 30+ 个端点(行情、K 线、期权、窝轮、持仓、下单、资讯、基本面 等),所有命令都已支持 `--format json`。

参考 https://www.iwencai.com/skillhub 上"事件数据查询"那个 skill 的形态,我们希望把 longbridge CLI 的能力包装成 Anthropic Agent Skills 风格的可复用 skill 包,落到 `/Users/hogan/work/longbridge/longbridge-skills/`,后续可以 `cp -r` 到 `~/.claude/skills/` 在 Claude Code 里直接被自动调用。

## 目标 / 非目标

### MVP 目标

- 跑通"一个 SKILL.md + 一个 scripts/cli.py 包装一条 CLI 能力"的范式
- 第一个 skill 选 `行情查询`(`longbridge quote` + 可选 `longbridge static`)
- 验证:`cp -r 行情查询/ ~/.claude/skills/`,在新 Claude Code 会话里问"NVDA 现在多少",模型能识别并调用,返回正确数据
- 提示词工艺达到 LLM 能稳定路由 + 正确改写参数的程度

### 非目标(MVP 不做)

- 多个 skill(只做 1 个)
- 安装器 CLI(类似 `iwencai-skillhub-cli`)
- 远程分发(zip 上 CDN、版本管理、自动更新)
- 鉴权管理(假设用户已经 `longbridge login` 过)
- 跨平台 skill 主机适配(只验 Claude Code,后续再看 OpenClaw 等)

## 架构

### Skill 锚定:Anthropic Agent Skills 标准格式

```
longbridge-skills/
└── 行情查询/
    ├── SKILL.md
    └── scripts/
        └── cli.py
```

不像 iwencai 那样多嵌一层(他们 zip 内部还有 `hithink-event-query/` 一层是打包副作用),我们直接平铺。

### 调用关系

```
LLM (Claude Code)
  ↓ 读 SKILL.md,识别意图
  ↓ 决定调用 scripts/cli.py
  ↓
python3 scripts/cli.py -s NVDA.US -s 700.HK [--include-static]
  ↓ subprocess
longbridge quote NVDA.US 700.HK --format json
[longbridge static NVDA.US 700.HK --format json]   # 仅 --include-static
  ↓ stdout JSON
cli.py 合并/规整 → stdout JSON
  ↓
LLM 解析 → 自然语言回答用户
```

关键:`scripts/cli.py` 是**薄壳**,不直接打 HTTP、不管 token、不重试——这些 `longbridge` CLI 已经处理。

## SKILL.md 内容规约

### 文件头(YAML front-matter)

```yaml
---
name: 行情查询
description: 查询股票实时行情和静态参考信息(报价、涨跌、成交量、行业、市值等)。当用户询问股票当前价格、涨跌幅、成交、所属行业、市值、上市状态等场景必须使用此技能。支持港股(.HK)、美股(.US)、A股(.SH/.SZ)、新加坡(.SG)。
---
```

`description` 写法参考 iwencai 的"事件数据查询" SKILL.md:第一句概括能力,第二句明确触发条件("当...场景必须使用此技能"),第三句说明限制/支持范围。这是 Claude Code skill 路由器决定要不要加载本 skill 的关键字段,要写到模型一看就知道何时该用。

### 必备章节(参照 iwencai 的"事件数据查询")

1. **技能概述** —— 一段话,讲能查什么,不能查什么。
2. **何时使用本技能** —— 列举 5–8 个典型用户问句样本,让 LLM 模式匹配。
3. **核心处理流程** —— 编号步骤:
   - 步骤 1:接收用户 Query,识别股票代码或公司名
   - 步骤 2:把名字补全为 `<CODE>.<MARKET>` 格式(规则:
     - 全大写字母 + 美国常见 ticker → 加 `.US`
     - 4–6 位数字 → 港股加 `.HK`、A 股区分 `.SH`/`.SZ`(60xxxx → SH,000xxx/300xxx → SZ)
     - 无法判断时反问用户
     )
   - 步骤 3:调用 `python3 scripts/cli.py -s <SYMBOL>...`,需要静态信息时加 `--include-static`
   - 步骤 4:解析返回的 JSON,提取相关字段
   - 步骤 5:组织语言回答,**必须强调数据来源于长桥证券**
4. **CLI 接口文档** —— 参数表 + 示例 + 返回 JSON 示例(下节有详细规约)。
5. **数据来源标注** —— 引用必须强调"数据来源于长桥证券",空数据时引导用户去 https://longbridge.com
6. **错误处理** —— 三种典型错误及给用户的话术:
   - `longbridge` 未安装/不在 PATH → 引导安装
   - Token 过期/未登录 → 引导执行 `longbridge login`
   - 符号格式错误 / 空结果 → 引导确认代码或市场后缀
7. **代码结构** —— 平铺目录树(只有 SKILL.md 和 scripts/cli.py,**不要写自己没有的文件**,避免 iwencai 那种"声称有 references/ 实际没有"的不一致)。

## scripts/cli.py 接口规约

### 强制约束

- **零依赖**(只用 Python 3.8+ 标准库)
- 单文件(整个 skill 只这一个 .py)
- stdout 仅输出 JSON,日志/错误信息走 stderr
- exit code:0 = 成功;1 = 业务错误(空结果、参数错);2 = 系统错误(找不到 longbridge、subprocess 失败)

### CLI 参数

| 参数 | 简写 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|---|
| `--symbol` | `-s` | str(可重复) | 是 | — | 股票代码,格式 `<CODE>.<MARKET>`,可重复多个 |
| `--include-static` | — | flag | 否 | false | 同时取静态参考(行业、市值、状态等) |
| `--format` | — | enum | 否 | `json` | 仅 `json`(预留,目前固定) |
| `--longbridge-bin` | — | str | 否 | `longbridge` | 重写底层 CLI 路径(便于测试) |

### 子进程调用规范

```python
# quote 部分(总是调用)
["longbridge", "quote", *symbols, "--format", "json"]

# static 部分(--include-static 时追加调用)
["longbridge", "static", *symbols, "--format", "json"]
```

- subprocess 超时 30s
- 把底层非零 exit + stderr 完整捕获,转成结构化错误向上抛
- 不解析 longbridge 的 stdout 结构,**原样合并**(下面 schema 说怎么合)

### 输出 JSON Schema

#### 默认(只调 quote)

```json
{
  "success": true,
  "count": 2,
  "symbols": ["NVDA.US", "700.HK"],
  "datas": [ /* longbridge quote --format json 原样数组 */ ]
}
```

#### `--include-static` 时

```json
{
  "success": true,
  "count": 2,
  "symbols": ["NVDA.US", "700.HK"],
  "datas": [
    {
      "symbol": "NVDA.US",
      "quote": { /* 原 quote 对象 */ },
      "static": { /* 原 static 对象,合并依据 symbol 字段 */ }
    }
  ]
}
```

如果某个 symbol 在 quote / static 中查不到,对应字段填 `null`,不让整个调用失败。

#### 错误时

```json
{
  "success": false,
  "error_kind": "auth_expired" | "binary_not_found" | "subprocess_failed" | "no_symbols" | "invalid_symbol_format",
  "error": "面向 LLM 的中文人话错误描述,告诉它怎么对用户说",
  "details": { /* 可选:底层 stderr 摘要、命令行等 */ }
}
```

`error_kind` 是给 LLM 路由错误处理用的稳定枚举;`error` 是 SKILL.md 里的"错误处理"章节会引用的话术。

### 错误检测点

- `shutil.which(args.longbridge_bin)` 返回 None → `binary_not_found`
- subprocess 退出非 0 且 stderr 含 "login" / "token" / "unauthorized" → `auth_expired`
- subprocess 退出非 0 其它 → `subprocess_failed`
- `--symbol` 列表为空 → `no_symbols`
- 任一 symbol 不匹配 `^[A-Z0-9]+\.(US|HK|SH|SZ|SG)$` → `invalid_symbol_format`(LLM 应在 SKILL.md 步骤 2 就规避到)

## 验收标准

1. **单元层**:`python3 scripts/cli.py -s NVDA.US -s 700.HK` 返回 `success: true`,`count: 2`,`datas` 含两条快照价
2. **静态层**:加 `--include-static` 后,每条 data 含非空 `quote` 和 `static`
3. **错误层**:
   - 没装 longbridge 时返回 `binary_not_found`
   - token 过期时返回 `auth_expired`
   - 传非法符号(如 "NVDA")返回 `invalid_symbol_format`
4. **集成层**:`cp -r 行情查询/ ~/.claude/skills/`,新开 Claude Code 会话问下面 4 句,模型每句都正确路由到本 skill 并给出含价格的回答:
   - "NVDA 现在多少钱"
   - "AAPL 和 NVDA 哪个涨得多"
   - "看一下 700.HK 的市值"(应触发 `--include-static`)
   - "茅台股价多少"(应触发 LLM 把"茅台"映射到 `600519.SH`)

## 风险 / 已知 Trade-off

- **`茅台 → 600519.SH` 这种映射**靠 LLM 自有知识,不在 skill 内做映射表。第一版接受这个不确定性,如果验收 4.4 失败,后续再考虑加 `references/symbol-aliases.md`。
- **多市场后缀的歧义**(如纯字母 ticker 在 US 和 SG 都有可能)留给 LLM 反问用户,不在 cli.py 处理。
- **下游 longbridge CLI 的输出 schema 漂移**:我们不解析具体字段,所以 longbridge 改字段名也不会让 cli.py 崩,但 LLM 那侧可能错读——SKILL.md 不固化字段名,只描述大意,降低耦合。

## 后续(MVP 验收通过后,下一阶段)

按这个范式批量做:`K线查询`、`盘口深度`、`自选股`、`持仓查询`、`资金流`、`期权链`、`资讯查询`...
评估时机做 `longbridge-skillhub-cli` 安装器(参考 `iwencai-skillhub-cli` 的实现,zip + 远程下载)。
