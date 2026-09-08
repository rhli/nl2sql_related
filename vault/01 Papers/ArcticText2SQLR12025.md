---
type: paper
title: "Arctic-Text2SQL-R1: Simple Rewards, Strong Reasoning in Text-to-SQL"
authors:
  - "Zhewei Yao"
  - "Guoheng Sun"
  - "Lukasz Borchmann"
  - "Gaurav Nuti"
  - "Zheyu Shen"
  - "Minghang Deng"
  - "Bohan Zhai"
  - "Hao Zhang"
  - "Ang Li"
  - "Yuxiong He"
year: 2025
venue: "arXiv"
venue_class: other
era: llm
found_via: leaderboard
themes: ["finetuning", "execution"]
benchmarks: ["BIRD", "Spider"]
doi: ""
arxiv: "2505.20315"
cited_by: []
status: reviewed
citekey: ArcticText2SQLR12025
---

## 问题

RL 训 Text-to-SQL 的奖励设计被普遍认为需要复杂塑形。

## 方法

反其道而行：只用简单执行奖励 + GRPO，就在 7B-32B 上训出强推理模型。

## 对我们的关系

单模型 track 前排，证明简单 RL 奖励就够；训练段必引的 Snowflake 工作。
