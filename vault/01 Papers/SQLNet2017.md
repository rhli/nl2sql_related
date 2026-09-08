---
type: paper
title: "SQLNet: Generating Structured Queries From Natural Language Without Reinforcement Learning"
authors:
  - "Xiaojun Xu"
  - "Chang Liu"
  - "Dawn Song"
year: 2017
venue: "arXiv"
venue_class: other
era: classic
found_via: citation
themes: ["pre-llm"]
benchmarks: ["WikiSQL"]
doi: ""
arxiv: "1711.04436"
cited_by: ["DINSQL2023", "CodeS2024"]
status: reviewed
citekey: SQLNet2017
---

## 问题

Seq2SQL 的 RL 训练不稳定，且 SQL 序列生成会受词序影响。

## 方法

用 sketch 填槽代替自左向右解码，避开强化学习。

## 对我们的关系

用来说明前 LLM 一代如何把 SQL 结构先验写进模型，对照现在把结构先验放到 prompt/约束解码。
