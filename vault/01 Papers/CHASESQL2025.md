---
type: paper
title: "CHASE-SQL: Multi-Path Reasoning and Preference Optimized Candidate Selection in Text-to-SQL"
authors:
  - "Mohammadreza Pourreza"
  - "Hailong Li"
  - "Ruoxi Sun"
  - "Yeounoh Chung"
  - "Shayan Talaei"
  - "Gaurav Tarlok Kakkar"
  - "Yu Gan"
  - "Amin Saberi"
  - "Fatma Ozcan"
  - "Sercan O. Arik"
year: 2025
venue: "ICLR"
venue_class: ML
era: llm
found_via: venue
themes: ["multi-agent", "prompting"]
benchmarks: ["BIRD"]
doi: ""
arxiv: "2410.01943"
cited_by: []
status: reviewed
citekey: CHASESQL2025
---

## 问题

单一推理路径覆盖不了复杂题，多数投票也选不好候选。

## 方法

多路径生成（分治、执行计划 CoT、实例感知示例）+ 成对偏好选择 agent。

## 对我们的关系

BIRD 上测试时扩展 / 多候选选择的关键 SOTA。我们的选 SQL 策略必须对着它写。
