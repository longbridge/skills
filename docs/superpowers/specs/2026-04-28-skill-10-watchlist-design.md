# 自选股(只读)(skill #10)— 差异化设计

**Date:** 2026-04-28
**Status:** Draft
**Protocol:** 遵循 `2026-04-28-skill-platform-protocol.md`
**Related:** 写入版见 #12 自选股管理(写)

## 业务范围

仅读,不写。用户的自选股分组 + 分组内的标的清单。

包装的子命令:`longbridge watchlist`(无 subcommand,直接 list)。

写入(create / update / delete)放 #12,显式分离让 LLM 路由更安全——LLM 看到"加到自选 / 删除"不会误用本 skill。

## front-matter

```yaml
---
name: 自选股
description: 查询用户在长桥的自选股分组,以及每个分组里的标的列表。当用户询问我的自选股 / 自选股里有哪些 / 我关注的股票 / 我的分组等场景必须使用此技能。本技能只读;增删改请使用「自选股管理」技能。需要 longbridge login。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: account_read
requires_login: true
default_install: true
---
```

## scripts/cli.py 接口

无子命令,只一个 list 入口:

```
python3 cli.py [--group <group_id>] [--group-name <name>]
```

| 参数 | 默认 | 说明 |
|---|---|---|
| `--group` | (空) | 按 group_id 过滤(精确匹配) |
| `--group-name` | (空) | 按分组名包含 / 等于过滤(模糊匹配,case-insensitive) |

不传任何过滤 → 返回全部分组与全部标的。

底层只调一次 `longbridge watchlist --format json`。过滤在 cli.py 内做(底层不支持 --group 参数)。

## 输出 JSON Schema

```json
{
  "success": true, "source": "longbridge", "skill": "自选股", "skill_version": "1.0.0",
  "group_count": 3, "total_symbol_count": 42,
  "datas": [
    {
      "group_id": "12345",
      "group_name": "科技股",
      "symbols": [
        {"symbol": "NVDA.US", "name": "NVIDIA Corp"},
        ...
      ]
    },
    ...
  ]
}
```

`--group` / `--group-name` 命中后 `datas` 只包含命中分组,`group_count` / `total_symbol_count` 反映过滤后的数量。

无命中:`success: true, datas: []`(走默认空结果分支,protocol)。

## SKILL.md 提示词差异

### `## 何时使用本技能` 列举

- "我的自选股有哪些"
- "我关注了多少只股票"
- "我的「科技股」分组里有什么"
- "自选股里港股涨幅"(双步:本 skill 拿 symbols → #01 行情查询拿涨幅)
- "我自选里美股最近一周谁涨得最多"(三步:本 skill → #01 → 在响应里排序)

### 与其它 skill 的协同

LLM 的常见组合任务:

| 用户问 | 流程 |
|---|---|
| "我自选股的港股涨幅" | 本 skill → 过滤 .HK → #01 行情查询(批量) |
| "我自选最近一周走势" | 本 skill → 全部 → #02 K 线查询(逐个) |
| "我自选的总市值" | 本 skill → 全部 → #01 行情 --include-static |

SKILL.md 提示词必须告诉 LLM:**取到 symbols 后,把要查涨幅 / K 线 / 静态信息的请求改路由到对应行情 / K 线 skill,而不是想办法在本 skill 里实现**。

### 隐私提示

自选股反映用户关注偏好,可能暴露交易策略。同 #08,SKILL.md 加隐私提示。

## 验收清单

- [ ] 全部:`cli.py` 返回 group_count > 0(假设用户至少有一个分组)
- [ ] group_id 过滤:`cli.py --group 12345` 只返该分组
- [ ] group_name 过滤:`cli.py --group-name 科技` 模糊匹配
- [ ] 空过滤:`--group nonexistent` → `success: true, datas: []`
- [ ] auth_expired:登出后 → `auth_expired`
- [ ] 集成层:5 句话验证
  - "我的自选股有哪些"
  - "我关注了多少只股票"
  - "我「科技股」分组里有什么"
  - "我自选里港股涨幅"(双步,验证 LLM 会 chain to 行情查询)
  - "我自选股美股最近一周走势"(三步,验证 LLM 会 chain to K 线查询)

## 已知 trade-off

- 写 / 改 / 删完全分离到 #12,即便部署在同一仓库,默认安装时会同时装 #10 和 #12;但 LLM 路由根据 description 区分。如果担心误路由,可以把 #12 设为 `default_install: false`(详见 #12 设计稿)。
