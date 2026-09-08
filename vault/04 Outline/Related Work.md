---
type: outline
---

# Related Work

按论文章节骨架写。方括号里是主题页，加粗是建议点名的代表工作。

## 0. 前 LLM 一代

跨域 Text-to-SQL 从 [[WikiSQL]] 的单表填槽走到 [[Spider]] 的多表复杂 SQL。编码器以 [[RATSQL2020|RAT-SQL]] 的 schema linking 和图结构为主，解码侧则以 [[SyntaxSQLNet2018|SyntaxSQLNet]]、[[IRNet2019|IRNet]] 的中间表示、以及 [[PICARD2021|PICARD]] 的约束解码收束。完整名单见 [[Pre-LLM Neural NL2SQL]] 与 [[Classics]]。

我们只把这一段当问题史：结构先验、schema 对齐、可执行性约束，后面 LLM 方法都在重做这三件事。

## 1. Prompting 与任务分解

[[DINSQL2023|DIN-SQL]] 把生成拆成 linking / 分类 / SQL / 自校正；[[DAILSQL2024|DAIL-SQL]] 系统化 example selection；[[C32023|C3]] 展示零样本 ChatGPT 流水线。更多见 [[Prompting and Decomposition]]。

对 BIRD top-1 的含义：单纯分解 prompt 已经不是差异化来源，差异在分解之后的检索、选候选和修复。

## 2. 多智能体与工作流

[[MACSQL2025|MAC-SQL]] 给出生成—选择—修复的角色原型；[[CHASESQL2025|CHASE-SQL]] 用多路径推理和偏好选择打上 BIRD 前列；[[DeepEyeSQL2026|DeepEye-SQL]] 把软件工程阶段门控引进来。见 [[Multi-agent and Workflow]]。

我们需要写清：自己的 agent 角色是否只是 MAC-SQL 换皮，还是在候选生成或选择上有新机制。

## 3. Schema linking 与检索

RAT-SQL 把 linking 做成显式模块。LLM 时代出现两条对立叙事：[[DeathOfSchemaLinking2024|Death of Schema Linking]] / [[LongContextNL2SQL2025|长上下文是否足够]]，以及 [[CHESS2024|CHESS]]、[[ESQL2024|E-SQL]]、[[LinkAlign2025|LinkAlign]]、[[DIVER2026|DIVER]] 证明大 schema 和 value grounding 仍然要检索。见 [[Schema Linking and Retrieval]]。

BIRD 的 evidence 和脏列名让我们更接近后一条：linking 没有死，它变成了检索和值接地。

## 4. 执行反馈与修复

从 PICARD 的解码约束，到 DIN-SQL 自校正、[[PETSQL2024|PET-SQL]] 的 cross-consistency、[[SafeQL2026|SafeQL]] 把 DBMS 变成主动搜索指导、[[AlphaSQL2025|Alpha-SQL]] 的 MCTS。见 [[Execution Feedback and Repair]]。

报 BIRD 分数时要交代：多少来自一次生成，多少来自修。

## 5. 微调与开源模型

[[CodeS2024|CodeS]]、[[SENSE2024|SENSE]]、[[OmniSQL2025|OmniSQL]] 走数据合成 + SFT；[[STaRSQL2025|STaR-SQL]]、[[SQLR12025|SQL-R1]]、[[ROUTE2025|ROUTE]] 走推理轨迹和 RL。见 [[Fine-tuning and Open Models]]。

若我们的系统是闭源 LLM agent，这一段用来说明开源模型已经能追到哪里，避免被审稿人认为忽略了可复现基线。

## 6. 基准与评测

[[BIRD2023|BIRD]] 是主场；[[Spider2018|Spider]] 是历史主榜；[[Spider22025|Spider 2.0]] 是企业工作流；[[NL2SQL3602024|NL2SQL360]] 提醒细粒度指标；[[AnnotationErrors2026|标注噪声]] 提醒榜本身不可全信。见 [[Benchmarks and Evaluation]]。当前榜单 top 30 与论文对应关系见 [[BIRD Leaderboard]]。

## 7. 系统与工业

成本、方言、金融/企业部署、交互澄清：[[FinSQL2024|FinSQL]]、[[OpenSearchSQL2025|OpenSearch-SQL]]、[[Sphinteract2025|Sphinteract]]。见 [[Systems and Industrial NL2SQL]]。

如果论文贡献偏榜上准确率，这一段写短，但不要零引用，否则 DB 审稿人会觉得这是一篇 NLP 投稿。
