---
type: paper
title: "DIN-SQL: Decomposed In-Context Learning of Text-to-SQL with Self-Correction"
authors:
  - "Mohammadreza Pourreza"
  - "Davood Rafiei"
year: 2023
venue: "NeurIPS"
venue_class: ML
era: llm
found_via: venue
themes: ["prompting", "execution"]
benchmarks: ["Spider", "BIRD"]
doi: ""
arxiv: "2304.11015"
cited_by: []
status: reviewed
citekey: DINSQL2023
---

## 问题

复杂 SQL 一次生成容易在 schema linking 和嵌套上同时出错。

## 方法

把任务分解为 schema linking、分类、生成、自校正四个 prompt。

## 对我们的关系

LLM 分解式 prompting 的标准对照。我们的流水线若更重，要说明比 DIN-SQL 多在哪。
