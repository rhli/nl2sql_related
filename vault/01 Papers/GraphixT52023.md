---
type: paper
title: "Graphix-T5: Mixing Pre-trained Transformers with Graph-Aware Layers for Text-to-SQL Parsing"
authors:
  - "Jinyang Li"
  - "Binyuan Hui"
  - "Reynold Cheng"
  - "Bowen Qin"
  - "Chenhao Ma"
  - "Nan Huo"
  - "Fei Huang"
  - "Wenyu Du"
  - "Luo Si"
  - "Yongbin Li"
year: 2023
venue: "AAAI"
venue_class: other
era: llm
found_via: citation
themes: ["pre-llm", "schema-linking"]
benchmarks: ["Spider"]
doi: ""
arxiv: "2301.07507"
cited_by: ["BIRD2023", "CodeS2024"]
status: reviewed
citekey: GraphixT52023
---

## 问题

T5 缺乏显式 schema 图偏置。

## 方法

在 T5 中插入 graph-aware 层混合预训练表示与关系图。

## 对我们的关系

PLM+图 的 2023 代表，作为 LLM prompting 之前的最后一代结构模型。
