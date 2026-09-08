---
type: paper
title: "RESDSQL: Decoupling Schema Linking and Skeleton Parsing for Text-to-SQL"
authors:
  - "Haoyang Li"
  - "Jing Zhang"
  - "Cuiping Li"
  - "Hong Chen"
year: 2023
venue: "AAAI"
venue_class: other
era: llm
found_via: citation
themes: ["pre-llm", "schema-linking", "finetuning"]
benchmarks: ["Spider"]
doi: ""
arxiv: "2302.05965"
cited_by: ["CodeS2024", "OmniSQL2025", "DAILSQL2024"]
status: reviewed
citekey: RESDSQL2023
---

## 问题

linking 和 SQL 骨架生成缠在一起，难优化。

## 方法

先做 schema linking / 骨架排序，再填值，基于 T5。

## 对我们的关系

前 LLM 最强开源对照之一；CodeS / OmniSQL 常拿它当 PLM 基线。
