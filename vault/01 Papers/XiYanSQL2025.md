---
type: paper
title: "XiYan-SQL: A Novel Multi-Generator Framework For Text-to-SQL"
authors:
  - "Yifu Liu"
  - "Yin Zhu"
  - "Yingqi Gao"
  - "Zhiling Luo"
  - "Xiaoxia Li"
  - "Xiaorong Shi"
  - "Yuntao Hong"
  - "Jinyang Gao"
  - "Yu Li"
  - "Bolin Ding"
  - "Jingren Zhou"
year: 2025
venue: "arXiv"
venue_class: other
era: llm
found_via: leaderboard
themes: ["prompting", "execution"]
benchmarks: ["BIRD", "Spider"]
doi: ""
arxiv: "2507.04701"
cited_by: []
status: reviewed
citekey: XiYanSQL2025
---

## 问题

单一生成器（无论 ICL 还是 SFT）覆盖不了不同风格和难度的题。

## 方法

多生成器集成：ICL generator + SFT generator 各出候选，再由选择/精炼模块定稿。

## 对我们的关系

多生成器 + 候选选择路线的工业代表，2024 年底起长期挂在 BIRD 前列；写候选选择段绕不开。
