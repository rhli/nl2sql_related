---
type: meta
---

# NL2SQL Related Work Vault

为 BIRD top-1 论文准备的 related-work 库。Obsidian 打开本 `vault/` 目录。

## 规模

- 论文笔记：126
- 按会议检索（2023+ 目标会议）：94
- 经典工作（前 LLM / 源头，从 related work 抽出）：16
- 关键引用（不在目标会议、但被反复点名）：9
- BIRD 榜单系统（top 30 中有公开论文的）：7
- 待精读：59

## 入口

- 章节骨架：[[Related Work]]
- 主题：[[Prompting and Decomposition]] · [[Multi-agent and Workflow]] · [[Schema Linking and Retrieval]] · [[Execution Feedback and Repair]] · [[Fine-tuning and Open Models]] · [[Benchmarks and Evaluation]] · [[Systems and Industrial NL2SQL]] · [[Pre-LLM Neural NL2SQL]]
- 基准：[[WikiSQL]] · [[Spider]] · [[BIRD]] · [[Spider 2.0]] · [[BIRD Leaderboard]]
- 索引：[[By Venue]] · [[By Year]] · [[By Theme]] · [[Classics]] · [[Reading Queue]]

## 怎么用

写 related work 时先打开 [[Related Work]]，按八段往下填。每段已链到主题页和代表论文。`status: drafted` 的笔记只有标题级摘要，精读后改「对我们的关系」。

`found_via`：`venue` = 按会议检索收录；`citation` = 从 related work / baseline 里抽出的关键引用；`leaderboard` = BIRD 榜 top 30 里有公开论文的系统。

```dataview
TABLE year, venue, era, found_via, status
FROM "01 Papers"
SORT year DESC
```
