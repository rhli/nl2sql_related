---
type: paper
title: "CSC-SQL: Corrective Self-Consistency in Text-to-SQL via Reinforcement Learning"
authors:
  - "Lei Sheng"
  - "Shuai-Shuai Xu"
year: 2025
venue: "arXiv"
venue_class: other
era: llm
found_via: leaderboard
themes: ["finetuning", "execution"]
benchmarks: ["BIRD", "Spider"]
doi: ""
arxiv: "2505.13271"
cited_by: []
status: reviewed
citekey: CSCSQL2025
---

## 问题

多数投票选候选时，错误候选之间也会互相「投」出一致错误。

## 方法

用 RL（GRPO）训出纠错式自一致性：先并行采样，再让模型修正后投票。

## 对我们的关系

self-consistency 的升级版，32B 开源模型打到 73+；候选选择段的开源对照。
