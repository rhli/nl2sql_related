---
type: paper
title: "Pervasive Annotation Errors Break Text-to-SQL Benchmarks and Leaderboards"
authors:
  - "Tengjun Jin"
  - "Yoojin Choi"
  - "Yuxuan Zhu"
  - "Daniel Kang"
year: 2026
venue: "VLDB"
venue_class: DB
era: llm
found_via: venue
themes: ["benchmark"]
benchmarks: ["BIRD", "Spider"]
doi: "10.14778/3796195.3796206"
arxiv: "2601.08778"
cited_by: []
status: reviewed
citekey: AnnotationErrors2026
---

## 问题

标注错误会让 leaderboard 失真。

## 方法

量化 Text-to-SQL 基准中的 pervasive annotation errors。

## 对我们的关系

评测可信度。报 top-1 时必须面对「榜本身有噪声」。
