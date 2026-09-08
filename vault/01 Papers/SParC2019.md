---
type: paper
title: "SParC: Cross-Domain Semantic Parsing in Context"
authors:
  - "Tao Yu"
  - "Rui Zhang"
  - "Michihiro Yasunaga"
  - "Yi Chern Tan"
  - "Xi Victoria Lin"
  - "Suyi Li"
  - "Heyang Er"
  - "Irene Li"
  - "Bo Pang"
  - "Tao Chen"
  - "Emily Ji"
  - "Shreya Dixit"
  - "David Proctor"
  - "Sungrok Shim"
  - "Jonathan Kraft"
  - "Vincent Zhang"
  - "Caiming Xiong"
  - "Richard Socher"
  - "Dragomir Radev"
year: 2019
venue: "ACL"
venue_class: NLP
era: classic
found_via: citation
themes: ["pre-llm", "benchmark"]
benchmarks: ["SParC"]
doi: ""
arxiv: "1906.02285"
cited_by: ["NL2SQL3602024"]
status: reviewed
citekey: SParC2019
---

## 问题

单轮 Spider 不能覆盖真实交互里的指代和省略。

## 方法

在 Spider 库上标注多轮问题，要求模型跟踪对话上下文。

## 对我们的关系

若我们只做单轮 BIRD，这里一笔带过；若相关工作要谈交互式 NL2SQL，SParC/CoSQL 是源头。
