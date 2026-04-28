# 股票交易(skill #11)— 风险评估 + 设计

**Date:** 2026-04-28
**Status:** Draft — 风险评估稿,实施推迟到 P2,**default_install: false**
**Protocol:** 遵循 `2026-04-28-skill-platform-protocol.md`,但有大量加严
**审稿人:** 实施前必须经用户(zhanghong.yuan@longbridge-inc.com)亲自审一轮

## 一句话警告

**本 skill 直接调用 `longbridge buy / sell / cancel / replace`,真实账户、真实金钱。设计错误或 LLM 路由错误会导致**真金白银损失**。本设计稿的目标是把这个风险降到可接受。**

## 风险等级

- 量级:单次错误最坏可能下错一笔订单,金额由 LLM 推断的 `--qty` × `--price` 决定。已知历史上类似 LLM 工具误下订单事故,本 skill 必须假设 LLM 会犯错。
- 不可逆性:订单进入交易所后撤单成功率取决于市场状态;成交后**不可逆**(只能再下反向订单平仓,有滑点)。
- 监管:可能触及"未经授权交易"的合规边界,详细审稿前实施推迟。

## 业务范围

| 子命令 | 何时调 |
|---|---|
| `buy` | 用户明确说"买" + symbol + qty(+ 可选 price / order_type / tif) |
| `sell` | 用户明确说"卖" + symbol + qty(+ 可选 price / order_type / tif) |
| `cancel` | 用户明确说"撤单" + order_id |
| `replace` | 用户明确说"改单" + order_id + 新 qty(+ 可选 新 price) |

## front-matter

```yaml
---
name: 股票交易
description: 提交买入 / 卖出订单,撤销待处理订单,修改待处理订单的数量或价格。⚠️ 本技能会**实际下单到长桥账户**,真实账户、真实金钱。LLM 在所有调用前必须把订单详情向用户朗读并显式获得用户**第二次确认**(原话句中要包含"确认"或"yes")。当用户**清楚命令式**说"买 / 卖 / 撤单 / 改单"且给出 symbol、quantity 等具体参数时才使用本技能。模糊询问(如"我应该买什么")必须拒绝并引导。需要 longbridge login,且账户必须开通交易权限。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: mutating
requires_login: true
default_install: false
---
```

`default_install: false` 是关键:仓库 README 必须说明默认 cp -r 不会装这个 skill,用户**必须**单独 symlink:

```bash
ln -s "$PWD/股票交易" "$HOME/.claude/skills/longbridge-trading"
```

## 五道安全 gate

订单 / 撤单 / 改单的 cli.py 调用,必须依次通过这五道 gate,任何一道失败立即 abort 并返回 `error_kind: risk_block`。

### Gate 1 — 显式 confirm flag

cli.py 必须有 `--confirm` flag,**没传不下单**。即便 LLM 想下单,也得在 argparse 层就被拒。

```python
parser.add_argument(
    "--confirm",
    action="store_true",
    required=False,
    help="必须显式传此 flag 才会真正下单/撤单/改单;未传时 cli.py 仅打印 dry-run 计划",
)
```

不传 `--confirm` 时,cli.py 走 dry-run:打印将要执行的命令 + 估算金额(qty × price)+ 提示用户加 `--confirm` 复跑。返回 `success: true, dry_run: true`。

LLM 在调用本 skill 时**必须**采用两步:
1. 第一次不带 `--confirm`,拿到 dry-run 输出
2. 把 dry-run 内容**逐字读给用户**,等用户回复**包含"确认"或"yes"** 的回复
3. 第二次带 `--confirm` 真正执行

SKILL.md 必须用强调字号写明这两步流程,且明文要求"如果用户没明确说确认,**必须再问一遍**"。

### Gate 2 — 二进制路径锁死

`mutating` skill 的 `--longbridge-bin` 解析在 protocol 基础上加严:

```python
# protocol resolve_bin → 加严:
def resolve_trading_bin(arg):
    bin_path = shutil.which(arg) if "/" not in arg else None
    if bin_path is None or bin_path != shutil.which("longbridge"):
        return None  # 触发 risk_block: trading skill 不接受任意路径
    return bin_path
```

效果:**只能通过 PATH 上的 `longbridge`** 下单。`--longbridge-bin /tmp/fake-longbridge` 这类测试技巧在 trading skill 上**直接拒绝**,避免误把测试 fake binary 接到真账户。

### Gate 3 — 金额 / 数量软上限

cli.py 启动时读 `~/.longbridge/skill-trading.yml`(若不存在用内置默认):

```yaml
# ~/.longbridge/skill-trading.yml
caps:
  max_notional_usd: 10000      # 单次最大下单名义金额(USD 等值)
  max_qty: 1000                # 单次最大数量(股)
  forbidden_symbols: []        # 禁止交易的 symbol 列表
  allowed_markets: [HK, US]    # 只允许这些市场;CN/SG 默认禁
```

cli.py 在带 `--confirm` 真下单前:
- 估算 `qty * price`(单价非 LO 时按当前市价,需要再调 quote 拿,subprocess 增 1 次)
- 换算到 USD(汇率取 longbridge balance 的多币种现金可估算,或硬编码 0.13 港币、0.14 元)
- 超过 `max_notional_usd` → `risk_block`,error 写明上限值与本次估算
- 数量超 `max_qty` → `risk_block`
- symbol 在 `forbidden_symbols` 或 market 不在 `allowed_markets` → `risk_block`

软上限是为了限制**单次错误的爆炸半径**,不是 absolute 安全;真要交易大额,用户在 `~/.longbridge/skill-trading.yml` 里改后跑。

### Gate 4 — 底层 confirm prompt 不绕过

`longbridge buy` 等子命令底层就有 confirm prompt(默认 stdin 回 y)。cli.py **不传 `--yes` 一类绕过 flag**(longbridge 目前没有,即使有也不传)。subprocess 调用必须给 stdin 一个真实的"y\n",或干脆走交互 PTY——

但 subprocess 是脚本调用,LLM 自动 pipe 不下来 PTY。可行方案二选一:

**方案 A:** longbridge CLI 加一个 `--confirm` flag 在 cli.py 上传(底层支持显式 confirm 跳过交互)。本 cli.py 在带 `--confirm` 时给底层加 `--confirm`(若底层支持)或 echo "y" 给 stdin。

**方案 B:** cli.py 走 `expect` 模式,捕获底层 prompt 输出 + 写回 y。

**推荐方案 A**:实施前先让 longbridge-terminal 加底层 `--confirm` flag(改动小,可控);或者放弃 cancel/replace 的撤单改单 confirm bypass,只支持简单 buy/sell。该问题的最终决策放在 plan 阶段、与 longbridge-terminal 维护者对齐后再定。

**这是这份设计的最大开放问题。** 实施前必须解决。

### Gate 5 — Audit log

每次带 `--confirm` 的真实调用,cli.py 在 subprocess 之前与之后**都**写一条记录到 `~/.longbridge/skill-trading-audit.log`(append-only,JSON Lines):

```json
{"ts": "2026-04-28T11:23:45Z", "phase": "pre", "subcommand": "buy", "symbol": "NVDA.US", "qty": 100, "price": "180.50", "order_type": "LO", "estimated_notional_usd": 18050.0}
{"ts": "2026-04-28T11:23:48Z", "phase": "post", "result": "success", "order_id": "20260428-...", "subprocess_returncode": 0}
```

权限 `chmod 600`。任何调用流程异常(subprocess 抛错、LLM 中断)都不删 pre 行——以便事后审计"我下了什么单"。

## scripts/cli.py 子命令风格

```
python3 cli.py buy     <symbol> <qty> [--price <decimal>] [--order-type LO|MO|...] [--tif Day|GTC|GTD] [--confirm]
python3 cli.py sell    <symbol> <qty> [--price <decimal>] [--order-type LO|MO|...] [--tif Day|GTC|GTD] [--confirm]
python3 cli.py cancel  <order_id> [--confirm]
python3 cli.py replace <order_id> --qty <new_qty> [--price <decimal>] [--confirm]
```

参数含义与底层 longbridge 一致(本 cli.py 不二次映射);`--confirm` 是本 cli.py 私有的,见 Gate 1。

## 输出 JSON Schema

**Dry-run**(无 `--confirm`):

```json
{
  "success": true, "source": "longbridge", "skill": "股票交易", "skill_version": "1.0.0",
  "dry_run": true,
  "subcommand": "buy",
  "plan": {
    "symbol": "NVDA.US", "side": "buy", "qty": 100, "price": "180.50",
    "order_type": "LO", "tif": "Day",
    "estimated_notional_usd": 18050.0,
    "caps_passed": true,
    "caps": { "max_notional_usd": 10000, "max_qty": 1000 }
  },
  "next_step": "若用户明确确认,以完全相同的参数加 --confirm 重跑 cli.py"
}
```

**真实下单成功**(带 `--confirm` 通过所有 gate):

```json
{
  "success": true, ..., "dry_run": false,
  "subcommand": "buy",
  "datas": { "order_id": "20260428-...", /* 原 longbridge buy 返回 */ }
}
```

**`risk_block`**:

```json
{
  "success": false, ..., "error_kind": "risk_block",
  "error": "本次下单估算 18050 USD 超过单次上限 10000 USD。请检查参数,或在 ~/.longbridge/skill-trading.yml 里调整 max_notional_usd 后重试。",
  "details": { "subcommand": "buy", "estimated_notional_usd": 18050.0, "cap": 10000, "gate": "amount_cap" }
}
```

`gate` 字段说明触发的是 Gate 1/2/3:
- `gate: "no_confirm"` — 没传 --confirm(其实已经在 Gate 1 走 dry-run,不会到这里;留作 belt-and-suspenders)
- `gate: "binary_locked"` — Gate 2 拒绝
- `gate: "amount_cap"` / `qty_cap` / `forbidden_symbol` / `forbidden_market` — Gate 3
- `gate: "audit_log_write_failed"` — Gate 5(写 log 失败,不下单)

## SKILL.md 强制章节

除 protocol 9 个章节外,本 skill 必须额外加:

10. `## ⚠️ 高风险提示` — 一段不少于 200 字的警告,首段大字
11. `## 二步确认流程` — 用图示说明 dry-run → 用户确认 → 真实下单
12. `## 软上限配置` — `~/.longbridge/skill-trading.yml` 范例 + 调整指南
13. `## 审计日志` — 说明 audit log 路径与含义,引导用户定期 review

## 验收清单(实施时,必须全过才能发布)

- [ ] dry-run:不带 `--confirm` 跑 buy 100 NVDA.US,返回 dry_run 计划
- [ ] confirm 流程:带 `--confirm` 在测试账户(若长桥提供 sandbox)走完整流程,确认 order_id 返回
- [ ] Gate 1:argparse 无 `--confirm` 时**绝不**调到 longbridge subprocess(grep cli.py 源码不能有任何路径绕过)
- [ ] Gate 2:`--longbridge-bin /tmp/anything` 直接 risk_block,即使带 --confirm
- [ ] Gate 3 amount cap:notional 超 max_notional_usd 触发 risk_block
- [ ] Gate 3 qty cap:qty 超 max_qty 触发
- [ ] Gate 3 forbidden:CN 市场默认拒绝
- [ ] Gate 3 配置文件:不存在时用默认值;格式错时拒绝启动并打印路径
- [ ] Gate 4(待最终方案确定后):底层 confirm prompt 行为符合预期,无意外绕过
- [ ] Gate 5 audit log:pre/post 两行都写入,文件权限 0600
- [ ] auth_expired:登出后 → 走通常 auth_expired,不触及任何 gate
- [ ] cancel:带 `--confirm` 撤一个真实 pending order,成功
- [ ] replace:带 `--confirm` 改一个真实 pending order,成功
- [ ] 集成层(在测试账户上):
  - "买 100 股 NVDA 限价 180" → LLM 走 dry-run → 朗读详情 → 用户回"确认" → LLM 复跑 --confirm → 成功
  - "买"(没给参数) → LLM 必须反问,不调 cli.py
  - "我应该买什么"(咨询性) → LLM 必须明确"本 skill 不做投资建议"

## 部署 gate(default_install: false 的具体落实)

仓库 `README.md` 关于本 skill 必须有一段:

```markdown
## ⚠️ 股票交易 skill(默认不安装)

`股票交易/` 目录会**实际下单到你的长桥账户**。批量 cp 默认不会装它。安装步骤:

1. 仔细阅读 `股票交易/SKILL.md` 的"高风险提示"章节
2. 配置 `~/.longbridge/skill-trading.yml`(参考 `股票交易/skill-trading.example.yml`)
3. 用以下命令显式安装(不能用 cp -r,要用 symlink 以便仓库内更新立即生效):

   ln -s "$PWD/股票交易" "$HOME/.claude/skills/longbridge-trading"

4. 在第一次让 LLM 下单前,**先用极小金额(< 1 USD 等值)试一笔**,验证 audit log 与 dry-run 流程。

不打算交易的用户:**不要**装这个 skill。
```

## 实施先决条件

实施 plan 启动前,以下问题必须有明确答案:

1. **底层 confirm 解决方案(Gate 4)**:longbridge-terminal 加 `--confirm` flag,还是 cli.py 走 expect 模式,还是放弃自动化、要求用户每次手动 yes?(三选一)
2. **测试账户**:长桥是否提供 sandbox / paper trading 模式?如果没有,验收第 4 步"测试账户上集成"怎么做?(可能需要在 longbridge-terminal 加 --paper-mode flag 或者引入仿真桩)
3. **汇率换算**:Gate 3 估算 USD 名义金额需要汇率,是硬编码、还是从 longbridge balance 多币种动态推、还是接 fx 接口?(影响 cli.py 复杂度)
4. **Cap 默认值**:`max_notional_usd: 10000` `max_qty: 1000` 用户接受吗?太严会让无辜调用都被拒,太宽 gate 形同虚设。

这些问题不解决,plan 阶段写不下去——所以本设计稿处于"已 design,等用户回答上面 4 题"状态。
