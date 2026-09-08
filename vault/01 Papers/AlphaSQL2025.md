---
type: paper
title: "Alpha-SQL: Zero-Shot Text-to-SQL using Monte Carlo Tree Search"
authors:
  - "Boyan Li"
  - "Jiayi Zhang"
  - "Ju Fan"
  - "Yanwei Xu"
  - "Chong Chen"
  - "Nan Tang"
  - "Yuyu Luo"
year: 2025
venue: "ICML"
venue_class: ML
era: llm
found_via: venue
themes: ["execution", "multi-agent"]
benchmarks: ["BIRD"]
doi: ""
arxiv: "2502.17248"
cited_by: []
status: reviewed
citekey: AlphaSQL2025
---

## 问题

零样本模型不会搜索中间 SQL 假设。

## 方法

用 MCTS 在执行反馈上搜索 SQL，无需任务微调。

## 对我们的关系

测试时搜索对照。和自校正循环、SafeQL 的 DBMS 引导搜索放在一段。
