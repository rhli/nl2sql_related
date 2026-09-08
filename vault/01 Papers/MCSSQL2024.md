---
type: paper
title: "MCS-SQL: Leveraging Multiple Prompts and Multiple-Choice Selection for Text-to-SQL Generation"
authors:
  - "Dongjun Lee"
  - "Choongwon Park"
  - "Jaehyuk Kim"
  - "Heesoo Park"
year: 2024
venue: "COLING"
venue_class: other
era: llm
found_via: citation
themes: ["prompting"]
benchmarks: ["BIRD", "Spider"]
doi: ""
arxiv: "2405.07467"
cited_by: ["CHASESQL2025"]
status: reviewed
citekey: MCSSQL2024
---

## 问题

单一 prompt 风格覆盖不了不同难度的题。

## 方法

多种 prompt 出候选，再做 multiple-choice 选择。

## 对我们的关系

测试时扩展 / 多路径生成的早期形式，CHASE-SQL 多路径推理的近邻。
