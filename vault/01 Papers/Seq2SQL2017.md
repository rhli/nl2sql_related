---
type: paper
title: "Seq2SQL: Generating Structured Queries from Natural Language using Reinforcement Learning"
authors:
  - "Victor Zhong"
  - "Caiming Xiong"
  - "Richard Socher"
year: 2017
venue: "arXiv / WikiSQL"
venue_class: other
era: classic
found_via: citation
themes: ["pre-llm", "benchmark"]
benchmarks: ["WikiSQL"]
doi: ""
arxiv: "1709.00103"
cited_by: ["DINSQL2023", "DAILSQL2024", "BIRD2023"]
status: reviewed
citekey: Seq2SQL2017
---

## 问题

把 NL 直接映射到 SQL，当时缺少大规模标注。

## 方法

提出 WikiSQL，并用强化学习（Seq2SQL）按 SQL 子句生成查询。

## 对我们的关系

related work 里「第一代 neural NL2SQL」的起点；WikiSQL 单表设定用来对照 Spider/BIRD 的跨库难度。
