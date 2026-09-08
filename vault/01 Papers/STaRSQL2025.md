---
type: paper
title: "STaR-SQL: Self-Taught Reasoner for Text-to-SQL"
authors:
  - "Mingqian He"
  - "Yongliang Shen"
  - "Wenqi Zhang"
  - "Qiuying Peng"
  - "Jun Wang"
  - "Weiming Lu"
year: 2025
venue: "ACL"
venue_class: NLP
era: llm
found_via: venue
themes: ["finetuning", "execution"]
benchmarks: ["BIRD", "Spider"]
doi: ""
arxiv: "2502.13550"
cited_by: []
status: reviewed
citekey: STaRSQL2025
---

## 问题

SQL 生成很少被当成可自我训练的推理过程。

## 方法

Self-Taught Reasoner：用结果监督奖励模型迭代改进推理轨迹。

## 对我们的关系

推理/RL 微调段。和 SQL-R1、Reward-SQL 构成 2025 训练路线。
