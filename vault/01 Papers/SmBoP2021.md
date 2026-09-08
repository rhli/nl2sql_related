---
type: paper
title: "SmBoP: Semi-autoregressive Bottom-up Semantic Parsing"
authors:
  - "Ohad Rubin"
  - "Jonathan Berant"
year: 2021
venue: "NAACL"
venue_class: NLP
era: classic
found_via: citation
themes: ["pre-llm"]
benchmarks: ["Spider"]
doi: ""
arxiv: "2010.12412"
cited_by: ["DINSQL2023"]
status: reviewed
citekey: SmBoP2021
---

## 问题

自左向右生成难以先构造子树再组合复杂 SQL。

## 方法

自底向上、半自回归地组合 SQL 子树。

## 对我们的关系

结构解码对照；我们若走 LLM prompting，不必当 baseline 重跑，但 related work 要承认这条线。
