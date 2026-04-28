# 证券查找(skill #07)— 差异化设计

**Date:** 2026-04-28
**Status:** Draft
**Protocol:** 遵循 `2026-04-28-skill-platform-protocol.md`

## 业务范围

元数据查找:全市场证券列表 + 经纪商参与者字典。低频但偶有刚需。

| 子命令 | 何时调 |
|---|---|
| `security-list` | 用户问"X 市场全部股票"、"港股有多少只股票" |
| `participants` | 用户问"经纪商 ID xxx 是谁"、"完整经纪商列表" |

## front-matter

```yaml
---
name: 证券查找
description: 查询市场全部上市证券列表,以及港股市场参与者(经纪商 ID 与名字字典)。当用户询问某市场总共有多少只股票、列出全部 X 市场股票、按代码反查名字、经纪商 ID 翻译等场景必须使用此技能。返回原始字典,不做筛选——筛选请用 #04 资金流向或后续 selector skill。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
---
```

## scripts/cli.py 子命令风格

```
python3 cli.py securities  [--market HK|US|CN|SG]
python3 cli.py participants
```

| 参数 | 适用 | 默认 | 说明 |
|---|---|---|---|
| `--market` | securities | `HK` | 市场枚举 |

## 输出 JSON Schema

**`securities`**:

```json
{
  "success": true, ..., "subcommand": "securities",
  "market": "HK", "count": 2547,
  "datas": [ /* 原 security-list 数组,每条 {symbol, name_en, name_cn} */ ]
}
```

**`participants`**:

```json
{
  "success": true, ..., "subcommand": "participants",
  "datas": [ /* 原 participants 数组,每条 {broker_id, name_en, name_cn} */ ]
}
```

注:`security-list` 单市场返回的数据可能是上千条(港股 ~2.5k,A 股 ~5k+),JSON 体积大。SKILL.md 提示 LLM:**不要把整个数组贴给用户**,而是回答总数 + 让用户用具体代码/名字查询(此时引导到 #01 行情查询)。

## SKILL.md 提示词差异

### `## 何时使用本技能` 列举

- "港股一共有多少只股票" / "美股 listed 数量"
- "经纪商 ID 9000 是谁" / "0001 是哪家券商"
- "列出 A 股全部股票"(LLM 应反问范围,数据量大)
- "翻译一下经纪商列表"(→ participants)

### 步骤 5 回答规范

| 用户问的 | 回答策略 |
|---|---|
| "X 市场多少股票" | 用 count 直接回答,不展示 datas 全部 |
| "经纪商 ID xxx 是谁" | 在 datas 里 grep,只回该条 |
| "完整经纪商列表" | 列表 ≤ 100 条可全展示;否则回总数并建议按 ID 反查 |
| "列出全部股票" | 反问"想找哪只 / 哪个行业",引导到 #01 行情查询 |

## 验收清单

- [ ] securities:`cli.py securities --market HK` 返回 count > 1000
- [ ] participants:`cli.py participants` 返回非空数组
- [ ] 市场别名:`--market sh` 归一化为 CN
- [ ] 集成层:4 句话验证
  - "港股有多少只股票"
  - "经纪商 ID 9000 是谁"(从 datas 捞)
  - "美股一共多少只股票"
  - "列出经纪商完整列表"

## 已知 trade-off

- 数据量大(security-list 单市场几 MB JSON)。subprocess timeout 30s 应该够;若超时改 `--timeout 60`。
- LLM 把整个 datas 贴给用户会爆 context,SKILL.md 必须严格说**只展示用户关心的子集 + 总数**。
