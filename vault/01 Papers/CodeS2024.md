---
type: paper
title: "CodeS: Towards Building Open-source Language Models for Text-to-SQL"
authors:
  - "Haoyang Li"
  - "Jing Zhang"
  - "Hanbing Liu"
  - "Ju Fan"
  - "Xiaokang Zhang"
  - "Jun Zhu"
  - "Renjie Wei"
  - "Hongyan Pan"
  - "Cuiping Li"
  - "Hong Chen"
year: 2024
venue: "SIGMOD"
venue_class: DB
era: llm
found_via: venue
themes: ["finetuning"]
benchmarks: ["Spider", "BIRD"]
doi: "10.1145/3654930"
arxiv: "2402.16347"
cited_by: []
status: reviewed
citekey: CodeS2024
---

## 问题

闭源 LLM prompting 贵、不可定制，开源模型缺 SQL 数据。

## 方法

增量预训练 + 双向数据增强，发布 CodeS 系列开源 Text-to-SQL 模型。

## 对我们的关系

开源 SFT 主对照。我们若走闭源 agent，要解释为何不走 CodeS 路线；若走开源，它是底座。
