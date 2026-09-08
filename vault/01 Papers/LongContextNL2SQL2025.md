---
type: paper
title: "Is Long Context All You Need? Leveraging LLM's Extended Context for NL2SQL"
authors:
  - "Yeounoh Chung"
  - "Gaurav T. Kakkar"
  - "Yu Gan"
  - "Brenton Milne"
  - "Fatma Özcan"
year: 2025
venue: "VLDB"
venue_class: DB
era: llm
found_via: venue
themes: ["schema-linking", "systems"]
benchmarks: ["BIRD"]
doi: "10.14778/3742728.3742761"
arxiv: "2501.12372"
cited_by: []
status: reviewed
citekey: LongContextNL2SQL2025
---

## 问题

schema pruning 可能丢掉必要列，长上下文模型或许能吃全库。

## 方法

用 Gemini 等长上下文直接喂更多 schema，检验是否还要 linking。

## 对我们的关系

和 Death of Schema Linking 同一争论。用实验而不是口号来站队。
