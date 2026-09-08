---
type: paper
title: "PICARD: Parsing Incrementally for Constrained Auto-Regressive Decoding from Language Models"
authors:
  - "Torsten Scholak"
  - "Nathan Schucher"
  - "Dzmitry Bahdanau"
year: 2021
venue: "EMNLP"
venue_class: NLP
era: classic
found_via: citation
themes: ["pre-llm", "execution"]
benchmarks: ["Spider"]
doi: ""
arxiv: "2109.05093"
cited_by: ["DINSQL2023", "DAILSQL2024", "CodeS2024"]
status: reviewed
citekey: PICARD2021
---

## 问题

T5 等 LM 会生成语法非法或引用不存在列的 SQL。

## 方法

增量词法/语法检查，拒绝非法 token，把解码约束在可执行 SQL 空间。

## 对我们的关系

执行期约束的经典。对照 LLM 时代的 execution-guided repair / DBMS 反馈（SafeQL）。
