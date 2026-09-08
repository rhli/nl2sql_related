---
type: paper
title: "Before Generation, Align it! A Novel and Effective Strategy for Mitigating Hallucinations in Text-to-SQL Generation"
authors:
  - "Ge Qu"
  - "Jinyang Li"
  - "Bowen Li"
  - "Bowen Qin"
  - "Nan Huo"
  - "Chenhao Ma"
  - "Reynold Cheng"
year: 2024
venue: "ACL Findings"
venue_class: NLP
era: llm
found_via: leaderboard
themes: ["prompting", "schema-linking"]
benchmarks: ["BIRD", "Spider"]
doi: ""
arxiv: "2405.15307"
cited_by: []
status: reviewed
citekey: TASQL2024
---

## 问题

LLM 生成 SQL 时幻觉出不存在的列/表，源于任务对齐不足。

## 方法

生成前先做任务对齐（TA）：把问题与 schema 元素显式对齐，再进入生成。

## 对我们的关系

BIRD 团队自己的幻觉缓解工作，mini-dev 的 column_meaning 也来自它；linking/对齐段可引。
