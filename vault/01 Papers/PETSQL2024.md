---
type: paper
title: "PET-SQL: A Prompt-Enhanced Two-Round Refinement of Text-to-SQL with Cross-consistency"
authors:
  - "Zhishuai Li"
  - "Xiang Wang"
  - "Jingjing Zhao"
  - "Sun Yang"
  - "Guoqing Du"
  - "Xiaoru Hu"
  - "Bin Zhang"
  - "Yuxiao Ye"
  - "Ziyue Li"
  - "Rui Zhao"
  - "Hangyu Mao"
year: 2024
venue: "arXiv"
venue_class: other
era: llm
found_via: citation
themes: ["prompting", "execution"]
benchmarks: ["BIRD", "Spider"]
doi: ""
arxiv: "2403.09732"
cited_by: ["CHASESQL2025", "OpenSearchSQL2025"]
status: reviewed
citekey: PETSQL2024
---

## 问题

单轮 prompt 的 schema 引用和最终 SQL 不一致。

## 方法

两轮 prompt，用 cross-consistency 在多候选间投票。

## 对我们的关系

self-consistency / 多候选选择的对照，CHASE-SQL 的 pairwise selector 可以对着它写。
