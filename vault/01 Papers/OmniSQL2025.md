---
type: paper
title: "OmniSQL: Synthesizing High-quality Text-to-SQL Data at Scale"
authors:
  - "Haoyang Li"
  - "Shang Wu"
  - "Xiaokang Zhang"
  - "Xinmei Huang"
  - "Jing Zhang"
  - "Fuxin Jiang"
  - "Shuai Wang"
  - "Tieying Zhang"
  - "Jianjun Chen"
  - "Rui Shi"
  - "Hong Chen"
  - "Cuiping Li"
year: 2025
venue: "VLDB"
venue_class: DB
era: llm
found_via: venue
themes: ["finetuning"]
benchmarks: ["BIRD", "Spider"]
doi: "10.14778/3749646.3749723"
arxiv: "2503.02240"
cited_by: []
status: reviewed
citekey: OmniSQL2025
---

## 问题

公开训练数据覆盖不够，SFT 模型泛化差。

## 方法

自动合成 SynSQL-2.5M（库+问题+SQL+CoT），再训 OmniSQL 7B/14B/32B。

## 对我们的关系

数据合成路线的代表。和 CodeS 一起构成开源模型段。
