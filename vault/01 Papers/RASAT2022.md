---
type: paper
title: "RASAT: Integrating Relational Structures into Pretrained Seq2Seq Model for Text-to-SQL"
authors:
  - "Jiexing Qi"
  - "Jingyao Tang"
  - "Ziwei He"
  - "Xiangpeng Wan"
  - "Yu Cheng"
  - "Chenghu Zhou"
  - "Xinbing Wang"
  - "Quanshi Zhang"
  - "Zhouhan Lin"
year: 2022
venue: "EMNLP"
venue_class: NLP
era: classic
found_via: citation
themes: ["pre-llm"]
benchmarks: ["Spider"]
doi: ""
arxiv: "2205.06983"
cited_by: ["CodeS2024", "DAILSQL2024"]
status: reviewed
citekey: RASAT2022
---

## 问题

纯 T5 看不到 schema 关系图。

## 方法

把关系结构注入预训练 seq2seq 的 self-attention。

## 对我们的关系

PLM + 结构偏置的收官工作之一，用来结束「前 LLM 编码器」小节。
