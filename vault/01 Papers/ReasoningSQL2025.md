---
type: paper
title: "Reasoning-SQL: Reinforcement Learning with SQL Tailored Partial Rewards for Reasoning-Enhanced Text-to-SQL"
authors:
  - "Mohammadreza Pourreza"
  - "Shayan Talaei"
  - "Ruoxi Sun"
  - "Xingchen Wan"
  - "Hailong Li"
  - "Azalia Mirhoseini"
  - "Amin Saberi"
  - "Sercan O. Arik"
year: 2025
venue: "arXiv"
venue_class: other
era: llm
found_via: leaderboard
themes: ["finetuning", "execution"]
benchmarks: ["BIRD"]
doi: ""
arxiv: "2503.23157"
cited_by: []
status: reviewed
citekey: ReasoningSQL2025
---

## 问题

RL 只用最终执行结果做奖励太稀疏，中间步骤学不到信号。

## 方法

设计 SQL 专用的部分奖励（partial rewards），按子句正确性给中间反馈。

## 对我们的关系

CHASE-SQL 同组的 RL 训练线，和 SQL-R1 / Arctic-Text2SQL-R1 一起构成 2025 RL 段。
