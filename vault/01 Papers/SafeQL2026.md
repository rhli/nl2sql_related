---
type: paper
title: "SafeQL: Search-based Refinement for Safe and Efficient LLM-based Text-to-SQL"
authors:
  - "Geonho Lee"
  - "Min-Soo Kim"
year: 2026
venue: "VLDB"
venue_class: DB
era: llm
found_via: venue
themes: ["execution"]
benchmarks: ["BIRD", "Spider"]
doi: "10.14778/3819518.3819545"
arxiv: ""
cited_by: []
status: reviewed
citekey: SafeQL2026
---

## 问题

失败后整句重生成，DBMS 只当报错器。

## 方法

把 DBMS 反馈变成对错误子句的引导搜索，在安全查询空间里修。

## 对我们的关系

执行反馈段 2026 代表。我们的 repair 循环要说明是否也把 DBMS 当主动指导。
