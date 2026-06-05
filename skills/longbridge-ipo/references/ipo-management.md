# IPO: Management and Lifecycle

覆盖原技能：`longbridge-ipo`

---

## longbridge-ipo — IPO 全生命周期管理

**触发场景**：查看 IPO 日历、认购期、个人申购记录、中签结果。

**Longbridge IPO 流程**：
```
公告期 → 招股期（认购期）→ 暗盘交易（港股）→ 上市首日
```

**操作类型**：

1. **IPO 日历（无需登录）**
   - 港股 IPO 日历：列出近期/即将上市的港股新股
   - 美股 IPO 日历：列出近期/即将上市的美股新股
   - 显示：发行名称/发行价格区间/认购截止日/预计上市日

2. **认购期查询（无需登录）**
   - 港股当前在认购阶段的新股
   - 美股当前在认购阶段的新股
   - 显示：发行价/认购截止时间/预计发行规模

3. **个人申购记录（需 trade 权限）**
   - 查看本人的历史申购记录
   - 显示：申购数量/申购金额/状态（待分配/已中签/未中签）

4. **中签结果（需 trade 权限）**
   - 查看已中签的 IPO 股份
   - 显示：分配股份数/分配价格/预计划转时间

**工作流**：
```bash
# 日历查询（无需登录）
longbridge <ipo-subcommand> calendar --format json
longbridge <ipo-subcommand> us-subscriptions --format json

# 个人申购记录（需登录）
longbridge auth login
longbridge <ipo-subcommand> subscriptions --format json
```

**输出格式**：
```
近期港股 IPO — 来源：Longbridge Securities

| 公司 | 代码 | 发行价区间 | 认购截止 | 预计上市 |
|---|---|---|---|---|
| XX集团 | XXXX.HK | HK$X - HK$Y | 2026-06-10 | 2026-06-15 |
```
