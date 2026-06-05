# Market Data: Quotes, K-Lines, and Order Book

覆盖原技能：`longbridge-quote`, `longbridge-kline`, `longbridge-depth`

---

## longbridge-quote — 实时报价与静态信息

**触发场景**：用户询问当前价格、涨跌幅、成交量、市值、PE/PB、换手率、行业分类。

**数据类型**：
- 实时报价（最新价/开高低收/前收/成交量/成交额/交易状态）
- 静态参考数据（公司名/行业/手数/总股本/流通股本/EPS/BPS/股息率/货币）
- 估值指数（PE TTM/PB/换手率/总市值/5日10日涨跌幅等）

**工作流**：
1. 提取标的；统一格式为 `<CODE>.<MARKET>`（如 `NVDA.US`、`700.HK`、`600519.SH`）
2. `longbridge --help` → `longbridge <quote-subcommand> --help`
3. 按需调用报价/静态/估值指数子命令（可并行）
4. 合并输出；来源标注 **Longbridge Securities**

**符号格式参考**：
| 市场 | 后缀 | 示例 |
|---|---|---|
| 美股 | `.US` | `NVDA.US`, `AAPL.US` |
| 港股 | `.HK` | `700.HK`, `9988.HK` |
| 沪市 | `.SH` | `600519.SH` |
| 深市 | `.SZ` | `300750.SZ` |
| 新加坡 | `.SG` | `D05.SG` |

市场不明时**询问用户**，不要猜测。

---

## longbridge-kline — K线与分时数据

**触发场景**：K线图/蜡烛图、历史 OHLCV、分时走势。

**数据类型**：
- K线：日/周/月/年/60分/30分/15分/5分/1分
- 分时：当日逐分钟价格与成交量

**工作流**：
1. 确认周期（日/周/月/分钟级）和时间范围
2. `longbridge <kline-subcommand> --help` 确认周期参数
3. 获取数据；对于技术分析，将数据传给 `longbridge-quant` 技能

---

## longbridge-depth — 盘口与逐笔成交

**触发场景**：盘口五档/十档、港股经纪商队列、逐笔成交。

**数据类型**：
- 买卖五档/十档委托
- 港股逐经纪商委托队列
- 逐笔成交（时间/价格/方向/量）

**工作流**：
1. `longbridge <depth-subcommand> --help` 确认支持的档位深度
2. 港股经纪队列需单独子命令（`--help` 确认）
3. 深度数据为快照，实时性要求高时提示用户刷新
