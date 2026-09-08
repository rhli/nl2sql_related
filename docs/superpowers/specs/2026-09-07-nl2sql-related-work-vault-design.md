# NL2SQL Related Work Vault 设计

## 目标

为 BIRD NL2SQL 榜 top-1 论文建一个 Obsidian vault：先检索 2023 年起的顶会入口论文，再收集它们引用的关键经典工作，按 related work 章节组织，写论文时从主题图落到具体引用。

## 检索范围

### 入口会议（2023–2026）

- DB：SIGMOD、VLDB、ICDE、CIDR、TODS、VLDBJ
- NL2SQL 主战场：ACL、EMNLP、NAACL、NeurIPS、ICLR、ICML

Findings / Industry / Companion / Workshop 只收标题或摘要明确做 NL2SQL 的条目，不整本会议入库。

### 检索词

主词：`text-to-sql`、`nl2sql`、`text2sql`、`natural language to sql`  
辅词：`schema linking`、`semantic parsing` + `sql`

### 入口收录

标题或摘要满足任一即可：

- 核心任务是 NL2SQL / Text-to-SQL
- 提出 NL2SQL 系统、工作流、模型或训练方法
- 提出或修订 NL2SQL benchmark / 评测协议
- 工业 NL2SQL 系统论文，且有 SQL 生成实验

### 排除

- 通用 LLM / 代码生成，但不产 SQL
- KBQA、TableQA、SPARQL，没有 SQL 实验
- BI 语义层 / 指标层，没有 text-to-SQL 实验
- 只把 SQL 当下游例子的 prompting 综述

## 经典工作（一等公民）

入口论文收完后，从它们的 related work、method、experimental baseline 里抽**关键经典工作**，写入同一套 `01 Papers/`，用 `era: classic` 标记。不把整篇参考文献搬进来。

### 什么算经典

满足任一即收，年份可以早于 2023：

1. **Benchmark 源头**：入口论文实际评测或作为问题设定引用的数据集论文（WikiSQL、Spider、SParC、CoSQL、KaggleDBQA 等）。
2. **反复出现的方法对照**：至少 2 篇入口论文在 related work 小标题或实验 baseline 里点名的 NL2SQL 方法（RAT-SQL、PICARD、RESDSQL、Graphix-T5 等）。
3. **点名的奠基工作**：至少 1 篇入口论文把它写成 founding / seminal / first neural generation 的 NL2SQL 工作（Seq2SQL、SQLNet、WikiSQL 等）。

### 经典工作不收

- BERT / T5 / GPT / Codex / PaLM 等通用模型，除非该文本身是 NL2SQL 方法
- 只在长引用列表里出现、从未当 baseline 或小节标题的论文
- GeoQuery / ATIS 等非 SQL 语义解析，除非入口论文把它当作 NL2SQL 问题设定的专节来写

经典笔记和 2023+ 笔记用同一模板；`00 Index/Classics.md` 单独做一张表，方便 related work 开头写「前 LLM 一代」。

## Vault 结构

```
vault/
  .obsidian/           Dataview；复用 semantic_survey 的核心插件配置
  00 Index/
    Home.md
    By Venue.md
    By Year.md
    By Theme.md
    Classics.md
    Reading Queue.md
  01 Papers/           一篇论文一张笔记，文件名用 citekey
  02 Themes/           七个方法族 + 一张前 LLM 地图
  03 Benchmarks/       Spider / BIRD / Spider 2.0 等
  04 Outline/          related work 章节骨架
  _templates/paper.md
```

仓库根目录只放 `vault/`、`docs/`、检索底稿（`sources/` 下的 query log 与 paper list）。vault 必须能被 Obsidian 直接打开。

## 论文笔记

每篇固定 YAML：

```yaml
type: paper
title: ""
authors: []
year: 2023
venue: SIGMOD
venue_class: DB | NLP | ML | other
era: llm | classic
found_via: venue | citation | leaderboard
themes: []
benchmarks: []
doi: ""
arxiv: ""
status: drafted
```

正文只写三段，每段不超过 8 行：

1. **问题**：这篇要解决什么
2. **方法**：核心机制，一句话能讲清
3. **对我们的关系**：baseline / 对照 / 可引用主张 / 不必展开

禁止写成读书笔记。PDF 不入库。

## 主题切分

`02 Themes/` 按 related work 章节切，一篇论文可挂多个 theme：

| 文件 | 覆盖 |
|---|---|
| Prompting and Decomposition | DIN-SQL、DAIL-SQL、example selection |
| Multi-agent and Workflow | MAC-SQL、CHASE-SQL、多智能体纠错 |
| Schema Linking and Retrieval | linking、value retrieval、schema pruning |
| Execution Feedback and Repair | self-debug、execution-guided、CRITIC |
| Fine-tuning and Open Models | CodeS、DTS-SQL 等 SFT / 开源模型 |
| Benchmarks and Evaluation | 数据集与评测协议（与 `03 Benchmarks/` 互链） |
| Systems and Industrial NL2SQL | 端到端系统、延迟、成本、生产部署 |
| Pre-LLM Neural NL2SQL | 经典工作总图，指向 `era: classic` 笔记 |

`04 Outline/Related Work.md` 按上述顺序写成可直接改的章节骨架，每段 wiki-link 到主题页和论文笔记。

## 检索流程

1. 按会议 + 年份扫 DBLP / ACL Anthology / 会议程序，得到入口候选。
2. 按收录规则过滤，写入 `sources/entry-papers.md`。
3. 读入口论文的 related work、experiments、bibliography，按经典工作规则抽出关键引用，写入 `sources/classics.md`。
4. 为每篇生成 `01 Papers/` 笔记和 YAML。
5. 生成 Index、Themes、Benchmarks、Outline。
6. 缺摘要或 venue 对不上的条目进 `Reading Queue`，不丢弃、不编造。

## 验收标准

- Obsidian 打开 `vault/` 后，从 `Home.md` 能到达全部论文、主题、benchmark、大纲。
- 每篇入口论文都能指出至少一条「对我们的关系」。
- 经典工作有独立索引，且每篇能回溯到「被哪些入口论文当作关键引用」。
- Outline 七段 + 前 LLM 一段都能直接改写成 related work 初稿。
- 没有 PDF、没有整本会议目录、没有通用 LLM 论文冒充 NL2SQL。

## 不做

- Zotero / ZotLit 同步（本库不绑现有 `paper_reorg`）
- MinerU 全文抽取
- 自动生成最终 related work 英文成稿（只提供中文骨架和引用链接）
- 把 BIRD 榜上无论文的系统写成论文笔记
