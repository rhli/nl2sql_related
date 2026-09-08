---
type: paper
title: "KaggleDBQA: Realistic Evaluation of Text-to-SQL Parsers"
authors:
  - "Chia-Hsuan Lee"
  - "Oleksandr Polozov"
  - "Matthew Richardson"
year: 2021
venue: "ACL"
venue_class: NLP
era: classic
found_via: citation
themes: ["pre-llm", "benchmark"]
benchmarks: ["KaggleDBQA"]
doi: ""
arxiv: ""
cited_by: ["BIRD2023", "NL2SQL3602024"]
status: reviewed
citekey: KaggleDBQA2021
---

## 问题

Spider 的库经过规范化，列名对模型过于友好。

## 方法

用真实 Kaggle 数据库和更自然的问题做小规模但更难的评测。

## 对我们的关系

BIRD 强调 dirty schema / 外部知识，这条线从 KaggleDBQA 就开始了。
