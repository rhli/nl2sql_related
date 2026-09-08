---
type: paper
title: "RAT-SQL: Relation-Aware Schema Encoding and Linking for Text-to-SQL Parsers"
authors:
  - "Bailin Wang"
  - "Richard Shin"
  - "Xiaodong Liu"
  - "Oleksandr Polozov"
  - "Matthew Richardson"
year: 2020
venue: "ACL"
venue_class: NLP
era: classic
found_via: citation
themes: ["pre-llm", "schema-linking"]
benchmarks: ["Spider"]
doi: ""
arxiv: "1911.04942"
cited_by: ["DINSQL2023", "CodeS2024", "LinkAlign2025"]
status: reviewed
citekey: RATSQL2020
---

## 问题

问题词和 schema 元素的对齐是跨域 NL2SQL 的核心瓶颈。

## 方法

用 relation-aware transformer 同时编码问题和 schema 图，显式做 schema linking。

## 对我们的关系

schema linking 必引。用来对照「独立 linking 模块」vs「LLM 隐式 linking / death of schema linking」。
