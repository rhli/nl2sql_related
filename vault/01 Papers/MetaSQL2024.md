---
type: paper
title: "METASQL: A Generate-then-Rank Framework for Natural Language to SQL Translation"
authors:
  []
year: 2024
venue: "ICDE"
venue_class: DB
era: llm
found_via: venue
themes: ["prompting"]
benchmarks: ["Spider"]
doi: ""
arxiv: "2402.17144"
cited_by: []
status: reviewed
citekey: MetaSQL2024
---

## 问题

一次生成无法覆盖语义等价的多种 SQL 写法。

## 方法

generate-then-rank：先多样生成再排序。

## 对我们的关系

候选生成+排序，和 CHASE 选择器同一族，但还在 ICDE 2024。
