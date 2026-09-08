---
type: benchmark
benchmark: BIRD
---

# BIRD Leaderboard Top 30 (EX, test)

2026-09-08 抓取自 bird-bench.github.io 总榜（Execution Accuracy, test set）。
有论文的条目链到 `01 Papers/` 笔记；无论文的工业/匿名系统只留表，不建笔记（spec 约定）。

| # | 日期 | 系统 | 团队 | Size | Dev | Test | 笔记 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Aug 22, 2026 | SiriusAI-SQL | Tencent Data Computing Platform | UNK | 77.77 | 82.28 | 无公开论文 |
| 2 | Sep 02, 2026 | DataGallery-Text2SQL | Huawei 2012 Labs [Yufei Cheng et al.] | UNK | 77.71 | 82.22 | 本论文系统 |
| 3 | Dec 16, 2025 | AskData + GPT-4o | AT&T CDO - DSAIR | UNK | 77.64 | 81.95 | [[AskData2025]] |
| 4 | Sep 25, 2025 | Agentar-Scale-SQL | Ant Group | UNK | 74.90 | 81.67 | [[AgentarScaleSQL2025]] |
| 5 | Jun 19, 2026 | Sber Text2SQL | SberData Research | UNK | 75.74 | 81.33 | 无公开论文 |
| 6 | May 27, 2026 | Xiaomi Text2SQL | Xiaomi ITP & Data | UNK | 73.66 | 80.83 | 无公开论文 |
| 7 | Aug 19, 2026 | RAS | Adya AI | UNK | 72.49 | 79.82 | 无公开论文 |
| 8 | Jul 14, 2026 | DeepEye | HKUST(GZ) [Boyan Li et al. '26] | UNK | 74.49 | 79.09 | [[DeepEyeSQL2026]]（DeepEye 新版条目） |
| 9 | Jul 04, 2026 | MarkovSQL | Anonymous | UNK | 75.10 | 78.70 | 匿名 |
| 10 | Jul 10, 2026 | DeepEye-SQL (27B) | HKUST(GZ) | 27B | 74.49 | 78.42 | [[DeepEyeSQL2026]] |
| 11 | Jul 11, 2026 | Spektr-SQL | Amazon Ads - SpektrBot | UNK | 73.09 | 78.31 | 无公开论文 |
| 12 | Jun 09, 2026 | DataGallery-Text2SQL | Huawei 2012 Labs | UNK | 74.64 | 77.53 | 本论文系统（早期提交） |
| 13 | Jul 14, 2025 | LongData-SQL | LongShine AI Research | UNK | 74.32 | 77.53 | 无公开论文 |
| 14 | Aug 03, 2026 | AxisSQL | UST | 31B |  | 76.86 | 无公开论文 |
| 15 | Jul 07, 2026 | GT-ChatBI-SQL | MR Tech | UNK | 75.95 | 76.80 | 无公开论文 |
| 16 | Jan 02, 2026 | Zhiwen-Lingsi-Agent | China Telecom, TeleAI | UNK | 73.53 | 76.63 | 无公开论文 |
| 17 | Jan 26, 2026 | DeepEye-SQL | HKUST(GZ) | UNK | 73.53 | 76.58 | [[DeepEyeSQL2026]] |
| 18 | Dec 4, 2025 | Q-SQL | AWS-Quick Science | 30B-3B-MoE | 72.99 | 76.47 | 无公开论文 |
| 19 | Feb 6, 2026 | MIC2-SQL | Anonymous | UNK | 74.45 | 76.41 | 匿名 |
| 20 | Jul 14, 2026 | DataSpace-Text2SQL | Institute of Dataspace, Hefei | UNK |  | 76.36 | 无公开论文 |
| 21 | Apr 16, 2025 | CHASE-SQL + Gemini | Google Cloud | UNK | 74.90 | 76.02 | [[CHASESQL2025]] |
| 22 | Apr 3, 2026 | xiaoyi-text-to-sql | wenyuai | UNK | 72.75 | 75.96 | 无公开论文 |
| 23 | Feb 21, 2026 | RED-SQL | South China Normal University | 30B | 74.19 | 75.91 | 无公开论文 |
| 24 | Sep 22, 2025 | JoyDataAgent-SQL | JD:CHO-JDT-JDL | UNK | 74.25 | 75.85 | 无公开论文 |
| 25 | Oct 23, 2025 | Sinovatio-SQL | Sinovatio AI Lab | UNK | 73.72 | 75.80 | 无公开论文 |
| 26 | May 30, 2025 | TCDataAgent-SQL | Tencent Cloud | UNK | 74.12 | 75.74 | 无公开论文 |
| 27 | Feb 27, 2025 | Contextual-SQL | Contextual AI | UNK | 73.50 | 75.63 | 无公开论文 |
| 28 | Dec 17, 2024 | XiYan-SQL | Alibaba Cloud | UNK | 73.34 | 75.63 | [[XiYanSQL2025]] |
| 29 | Sep 1, 2025 | DB-SQL | Anonymous | UNK | 73.66 | 75.35 | 匿名 |
| 30 | May 30, 2025 | CYAN-SQL | Tencent Cloud / Fudan University | UNK | 73.47 | 75.35 | [[CYANSQL2026]]（对应 ICDE 2026 CYANSQL 论文） |

## 观察

- Top 30 全部使用 oracle knowledge（evidence 列全勾），说明 evidence 利用已是上榜门槛。
- 前排（82+）与第 20 名差距约 6 个点，头部系统差距在 1 个点以内，评测噪声不可忽略（见 [[AnnotationErrors2026]]）。
- 有公开论文的系统集中在 2024 底–2025（XiYan-SQL、CHASE-SQL、DeepEye-SQL），2026 前排多为无论文的工业提交。
- 单模型 track 另有 Arctic-Text2SQL-R1（[[ArcticText2SQLR12025]]）等 RL 训练模型，与流水线路线对照。
