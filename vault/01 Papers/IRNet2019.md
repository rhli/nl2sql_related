---
type: paper
title: "Towards Complex Text-to-SQL in Cross-Domain Database with Intermediate Representation"
authors:
  - "Jiaqi Guo"
  - "Zecheng Zhan"
  - "Yan Gao"
  - "Yan Xiao"
  - "Jian-Guang Lou"
  - "Ting Liu"
  - "Dongmei Zhang"
year: 2019
venue: "ACL"
venue_class: NLP
era: classic
found_via: citation
themes: ["pre-llm"]
benchmarks: ["Spider"]
doi: ""
arxiv: "1905.08205"
cited_by: ["DINSQL2023", "RESDSQL2023"]
status: reviewed
citekey: IRNet2019
---

## 问题

直接生成 SQL 难以处理跨域 schema 对齐和复杂组合。

## 方法

先生成与 schema 解耦的 SemQL 中间表示，再确定性转 SQL。

## 对我们的关系

中间表示路线的代表。对照 LLM 时代把 IR 换成 CoT / 子问题分解。
