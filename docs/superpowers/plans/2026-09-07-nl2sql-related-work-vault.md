# NL2SQL Related Work Vault Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Do not commit until the user asks.

**Goal:** 建一个可被 Obsidian 打开的 related-work vault：2023+ 顶会入口论文 + 它们引用的关键经典工作，并给出可改写成论文章节的大纲。

**Architecture:** DBLP / ACL Anthology 检索得到入口列表，按 spec 过滤后写 `sources/`；再从 related work 与 baseline 抽经典工作；最后生成 `vault/` 下的论文笔记、主题图、benchmark 页和 related-work 骨架。不入库 PDF，不绑 Zotero。

**Tech Stack:** Obsidian markdown + YAML frontmatter + Dataview；检索用 DBLP API 与公开 anthology / DOI 页面。

## Global Constraints

- 入口会议：SIGMOD、VLDB、ICDE、CIDR、TODS、VLDBJ、ACL、EMNLP、NAACL、NeurIPS、ICLR、ICML；年份 2023–2026。
- 经典工作：benchmark 源头、≥2 篇入口点名的方法、被写成 founding 的 NL2SQL 工作；不收通用 LLM 与路过引用。
- 一篇论文一张笔记；正文只写问题 / 方法 / 对我们的关系三段。
- 不 commit；初版完成后再由用户一并提交。
- Findings / Companion / Workshop 只收标题或摘要明确做 NL2SQL 的条目。

## File map

- `sources/entry-papers.md` — 入口论文清单（venue、year、doi/arxiv、收录理由）
- `sources/classics.md` — 经典工作清单（被哪些入口论文点名）
- `sources/query-log.md` — 检索词与命中数
- `vault/.obsidian/` — 最小 Dataview 配置
- `vault/_templates/paper.md` — 论文笔记模板
- `vault/01 Papers/<citekey>.md` — 论文笔记
- `vault/02 Themes/*.md` — 八个主题图
- `vault/03 Benchmarks/*.md` — benchmark 页
- `vault/04 Outline/Related Work.md` — 章节骨架
- `vault/00 Index/*.md` — Home / By Venue / By Year / By Theme / Classics / Reading Queue

---

### Task 1: Scaffold vault and templates

**Files:**
- Create: `vault/.obsidian/app.json`
- Create: `vault/.obsidian/core-plugins.json`
- Create: `vault/.obsidian/community-plugins.json`
- Create: `vault/.obsidian/plugins/dataview/manifest.json` (copy from `semantic_survey` if present, else enable plugin id only)
- Create: `vault/_templates/paper.md`
- Create: `sources/query-log.md`

**Interfaces:**
- Consumes: spec at `docs/superpowers/specs/2026-09-07-nl2sql-related-work-vault-design.md`
- Produces: YAML keys `type, title, authors, year, venue, venue_class, era, found_via, themes, benchmarks, doi, arxiv, status, cited_by`

- [ ] **Step 1: Write paper template with exact YAML keys**

```yaml
---
type: paper
title: ""
authors: []
year: 2023
venue: ""
venue_class: DB
era: llm
found_via: venue
themes: []
benchmarks: []
doi: ""
arxiv: ""
cited_by: []
status: drafted
---

## 问题

## 方法

## 对我们的关系
```

- [ ] **Step 2: Enable Dataview in `.obsidian/community-plugins.json` as `["dataview"]`**

- [ ] **Step 3: Verify** `test -f vault/_templates/paper.md && python3 -c "import pathlib; t=pathlib.Path('vault/_templates/paper.md').read_text(); assert 'cited_by:' in t"`

---

### Task 2: Search entry papers

**Files:**
- Create: `sources/query-log.md`
- Create: `sources/entry-papers.md`

**Interfaces:**
- Consumes: DBLP search API `https://dblp.org/search/publ/api?q=<query>&h=1000&format=json`
- Produces: markdown table of included papers with columns `citekey | title | year | venue | venue_class | doi | why`

Queries (each logged with hit count):

- `text-to-sql year:2023:`
- `nl2sql year:2023:`
- `text2sql year:2023:`
- `"natural language to sql" year:2023:`
- `schema linking sql year:2023:`

Include if venue matches spec list (PVLDB counts as VLDB; ACL Findings / SIGMOD Companion / NeurIPS Datasets track allowed when title/abstract is NL2SQL).

Exclude generic code-gen, KBQA-only, semantic-layer-without-SQL.

- [ ] **Step 1: Run the five DBLP queries and write raw hit counts to `sources/query-log.md`**
- [ ] **Step 2: Dedup by DOI / title, filter by venue + inclusion rule**
- [ ] **Step 3: Write `sources/entry-papers.md` as a table; uncertain items go to a `Candidates` subsection, not silently dropped**
- [ ] **Step 4: Verify** every row has year ≥ 2023 and a venue from the spec list

---

### Task 3: Collect classic works from entry papers

**Files:**
- Create: `sources/classics.md`

**Interfaces:**
- Consumes: `sources/entry-papers.md` plus related-work / baseline sections of those papers
- Produces: table `citekey | title | year | venue | why | cited_by`

Rules copied from spec:

1. Benchmark 源头
2. ≥2 篇入口论文点名的 NL2SQL 方法
3. 被写成 founding / seminal 的 NL2SQL 工作

Do not include BERT/T5/GPT/Codex unless the paper itself is NL2SQL.

- [ ] **Step 1: For each entry paper, extract named baselines and founding citations**
- [ ] **Step 2: Keep items that meet a classic rule; record `cited_by` as citekeys of entry papers**
- [ ] **Step 3: Write `sources/classics.md`**
- [ ] **Step 4: Verify** every classic row has a non-empty `cited_by` list

---

### Task 4: Write paper notes

**Files:**
- Create: `vault/01 Papers/<citekey>.md` for every entry and classic paper

**Interfaces:**
- Consumes: `sources/entry-papers.md`, `sources/classics.md`, template YAML keys
- Produces: one note per paper; `era: llm` for entry, `era: classic` for classics; `found_via: venue` vs `citation`

Citekey format: `FirstAuthorYearShortTitle` (BibTeX-style, no spaces). Filename is the citekey.

Theme tags must be a subset of:

- `prompting`
- `multi-agent`
- `schema-linking`
- `execution`
- `finetuning`
- `benchmark`
- `systems`
- `pre-llm`

- [ ] **Step 1: Generate notes for all entry papers**
- [ ] **Step 2: Generate notes for all classics, filling `cited_by`**
- [ ] **Step 3: Verify** `rg -l '^type: paper' vault/01\ Papers | wc -l` equals row count of entry + classics; every file has the three body headings

---

### Task 5: Themes, benchmarks, indexes, outline

**Files:**
- Create: `vault/02 Themes/Prompting and Decomposition.md`
- Create: `vault/02 Themes/Multi-agent and Workflow.md`
- Create: `vault/02 Themes/Schema Linking and Retrieval.md`
- Create: `vault/02 Themes/Execution Feedback and Repair.md`
- Create: `vault/02 Themes/Fine-tuning and Open Models.md`
- Create: `vault/02 Themes/Benchmarks and Evaluation.md`
- Create: `vault/02 Themes/Systems and Industrial NL2SQL.md`
- Create: `vault/02 Themes/Pre-LLM Neural NL2SQL.md`
- Create: `vault/03 Benchmarks/WikiSQL.md`
- Create: `vault/03 Benchmarks/Spider.md`
- Create: `vault/03 Benchmarks/BIRD.md`
- Create: `vault/03 Benchmarks/Spider 2.0.md`
- Create: `vault/04 Outline/Related Work.md`
- Create: `vault/00 Index/Home.md`
- Create: `vault/00 Index/By Venue.md`
- Create: `vault/00 Index/By Year.md`
- Create: `vault/00 Index/By Theme.md`
- Create: `vault/00 Index/Classics.md`
- Create: `vault/00 Index/Reading Queue.md`

**Interfaces:**
- Consumes: paper YAML `themes`, `benchmarks`, `era`, `venue`, `year`
- Produces: wiki-links from themes/indexes/outline to `01 Papers/<citekey>`

Each theme page: 5–12 行综述 + Dataview 或静态列表，链到该 theme 下的论文。

`04 Outline/Related Work.md` 八段（七个 LLM 主题 + 前 LLM），每段可直接改写成 related work 初稿。

`Home.md` 链到全部 Index / Themes / Benchmarks / Outline。

- [ ] **Step 1: Write eight theme pages and four benchmark pages**
- [ ] **Step 2: Write indexes from the paper YAML (do not hand-type a stale subset)**
- [ ] **Step 3: Write related-work outline with wiki-links**
- [ ] **Step 4: Verify** every `vault/01 Papers/*.md` is linked from at least one of Home/By Venue/By Theme/Classics; `Home.md` exists; no PDF files under `vault/`

---

## Self-review vs spec

- 检索范围、排除规则 → Task 2
- 经典工作三类规则与 `cited_by` → Task 3–4
- vault 目录、YAML、三段正文 → Task 1, 4
- 八主题、benchmark、outline、indexes → Task 5
- 不做 Zotero / MinerU / 无论文系统 → 全任务均不创建
- 不 commit → 全局约束
