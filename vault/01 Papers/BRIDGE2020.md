---
type: paper
title: "Bridging Textual and Tabular Data for Cross-Domain Text-to-SQL Semantic Parsing"
authors:
  - "Xi Victoria Lin"
  - "Richard Socher"
  - "Caiming Xiong"
year: 2020
venue: "Findings of EMNLP"
venue_class: NLP
era: classic
found_via: citation
themes: ["pre-llm", "schema-linking"]
benchmarks: ["Spider"]
doi: ""
arxiv: "2012.12627"
cited_by: ["BIRD2023", "DINSQL2023"]
status: reviewed
citekey: BRIDGE2020
---

## 问题

如何把表结构和单元格值一起喂给预训练语言模型。

## 方法

序列化 schema 与被提及的单元格值，用 BERT 做跨模态编码。

## 对我们的关系

值接地（value grounding）的前 LLM 代表，对照 BIRD 上的 value retrieval / evidence。
