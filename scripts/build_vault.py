#!/usr/bin/env python3
"""Build the NL2SQL related-work Obsidian vault from handbook + Crossref + curated notes."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"
VAULT = ROOT / "vault"

VENUE_ALLOW = {
    "SIGMOD",
    "VLDB",
    "ICDE",
    "CIDR",
    "TODS",
    "VLDBJ",
    "ACL",
    "EMNLP",
    "NAACL",
    "NEURIPS",
    "ICLR",
    "ICML",
}
VENUE_CLASS = {
    "SIGMOD": "DB",
    "VLDB": "DB",
    "ICDE": "DB",
    "CIDR": "DB",
    "TODS": "DB",
    "VLDBJ": "DB",
    "ACL": "NLP",
    "EMNLP": "NLP",
    "NAACL": "NLP",
    "NEURIPS": "ML",
    "ICLR": "ML",
    "ICML": "ML",
}
VENUE_DISPLAY = {
    "NEURIPS": "NeurIPS",
    "SIGMOD": "SIGMOD",
    "VLDB": "VLDB",
    "ICDE": "ICDE",
    "CIDR": "CIDR",
    "TODS": "TODS",
    "VLDBJ": "VLDBJ",
    "ACL": "ACL",
    "EMNLP": "EMNLP",
    "NAACL": "NAACL",
    "ICLR": "ICLR",
    "ICML": "ICML",
}


def normalize_venue(venue: str) -> str:
    raw = venue.strip()
    lower = raw.lower()
    mapping = {
        "vldb": "VLDB",
        "sigmod": "SIGMOD",
        "icde": "ICDE",
        "cidr": "CIDR",
        "tods": "TODS",
        "vldbj": "VLDBJ",
        "acl": "ACL",
        "emnlp": "EMNLP",
        "naacl": "NAACL",
        "neurips": "NeurIPS",
        "iclr": "ICLR",
        "icml": "ICML",
    }
    if lower in mapping:
        return mapping[lower]
    for k, v in mapping.items():
        if lower.startswith(k + " "):
            return v + raw[len(k):]
    return raw

STRICT_CONTAINERS = [
    (re.compile(r"^Proceedings of the VLDB Endowment$", re.I), "VLDB", "DB"),
    (re.compile(r"^Proceedings of the ACM on Management of Data$", re.I), "SIGMOD", "DB"),
    (re.compile(r"Companion of the .*Management of Data", re.I), "SIGMOD Companion", "DB"),
    (re.compile(r"IEEE .*International Conference on Data Engineering(?!.*Workshop)", re.I), "ICDE", "DB"),
    (re.compile(r"Conference on Innovative Data Systems Research", re.I), "CIDR", "DB"),
    (re.compile(r"ACM Transactions on Database Systems", re.I), "TODS", "DB"),
    (re.compile(r"The VLDB Journal|VLDB Journal", re.I), "VLDBJ", "DB"),
]

TITLE_KW = re.compile(
    r"text[- ]?to[- ]?sql|nl2sql|text2sql|natural language to sql|nl[- ]?to[- ]?sql",
    re.I,
)

THEME_RULES = [
    ("multi-agent", re.compile(r"multi[- ]?agent|chase-sql|mac-sql|workflow|collaborat", re.I)),
    ("schema-linking", re.compile(r"schema link|schema retrieval|schema prun|value link|subsetting|linkalign|schemarag", re.I)),
    ("execution", re.compile(r"execution|self-correct|self-correc|repair|refin|debug|feedback|critic|verif|abstention", re.I)),
    ("finetuning", re.compile(r"fine-tun|finetun|open-source language model|synthesiz|sft|codes\b|omnisql|sense\b", re.I)),
    ("benchmark", re.compile(r"benchmark|survey|evaluat|spider|bird|dawn|state of the art|leaderboard|annotation error", re.I)),
    ("systems", re.compile(r"industrial|system|cost|latenc|financ|finsql|dialect|enterprise|production", re.I)),
    ("prompting", re.compile(r"prompt|few-shot|in-context|demonstrat|decompos|dail|din-sql|example", re.I)),
]


def slug_citekey(title: str, year: int) -> str:
    # Do not treat the generic phrase Text-to-SQL as a system name.
    sys = re.search(
        r"\b((?:DeepEye|CHESS|CHASE|ROUTE|YORO|SENSE|PICARD|BIRD|Spider|[A-Z][A-Za-z0-9+-]*(?:SQL|NL2SQL)))\b",
        title,
    )
    if sys and sys.group(1).lower() not in {"sql", "texttosql", "text-to-sql", "nl2sql"}:
        name = re.sub(r"[^A-Za-z0-9]", "", sys.group(1))
        if name.lower() not in {"sql", "texttosql", "nl2sql"}:
            return f"{name}{year}"
    tokens = [t for t in re.findall(r"[A-Za-z0-9]+", title) if t.lower() not in {"a", "an", "the", "for", "and", "of", "to", "with", "in"}]
    name = "".join(t.title() for t in tokens[:4]) or "Paper"
    return f"{name}{year}"


def clean_title(title: str) -> str:
    title = unescape(re.sub(r"<[^>]+>", " ", title))
    title = re.sub(r"\s+", " ", title).strip(" .")
    # Crossref wraps small-caps words as <scp>mbi</scp>; after tag stripping the
    # leading capital is detached ("A mbi SQL"). Reattach it.
    title = re.sub(r"\bA mbi\b", "Ambi", title)
    return title


def title_key(title: str) -> str:
    """Merge key tolerant to handbook typos and punctuation differences."""
    t = re.sub(r"[^a-z0-9]+", " ", title.lower())
    t = t.replace("subseing", "subsetting")  # known handbook typo
    return re.sub(r"\s+", " ", t).strip()


def themes_for(title: str, extra: list[str] | None = None) -> list[str]:
    found = []
    for theme, pat in THEME_RULES:
        if pat.search(title):
            found.append(theme)
    if extra:
        for t in extra:
            if t not in found:
                found.append(t)
    return found or ["prompting"]


def arxiv_of(url: str) -> str:
    m = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", url)
    return m.group(1) if m else ""


def doi_of(url: str) -> str:
    m = re.search(r"doi\.org/([^)\s]+)", url)
    if m:
        return m.group(1).rstrip(".")
    m = re.search(r"10\.\d{4,}/[^\s)>\]]+", url)
    return m.group(0).rstrip(".") if m else ""


def parse_handbook(path: Path) -> list[dict]:
    text = path.read_text()
    chunks = []
    for header, ender in [
        ("## 📚 Text-to-SQL Survey & Tutorial", "## 📰 Text-to-SQL Paper List"),
        ("## 📰 Text-to-SQL Paper List", "## 📊 Text-to-SQL Benchmark"),
    ]:
        a = text.find(header)
        b = text.find(ender)
        if a != -1 and b != -1:
            chunks.append(text[a:b])
    papers = []
    seen = set()
    item_re = re.compile(
        r"(?:^|\n)\d+\.\s+(.*?)(?=\n\d+\.\s+|\Z)",
        re.S,
    )
    badge_re = re.compile(r"badge/([^\"']+?)'(\d{4})")
    link_re = re.compile(r"\]\((https?://[^)]+)\)")
    for chunk in chunks:
        for m in item_re.finditer(chunk):
            block = m.group(1)
            badges = badge_re.findall(block)
            if not badges:
                continue
            venue_raw, year_s = badges[0]
            year = int(year_s)
            if year < 2023:
                continue
            venue_key = re.match(r"([A-Za-z]+)", venue_raw.replace(" ", ""))
            if not venue_key:
                continue
            venue_norm = venue_key.group(1).upper()
            if venue_norm == "NEURIPS":
                venue_norm = "NEURIPS"
            if venue_norm not in VENUE_ALLOW:
                continue
            title = clean_title(re.split(r"<img", block, maxsplit=1)[0])
            if not title or title_key(title) in seen:
                continue
            if not TITLE_KW.search(title) and "sql" not in title.lower() and "schema" not in title.lower():
                # keep surveys that say Natural Language Interfaces
                if "natural language" not in title.lower() and "survey" not in title.lower():
                    continue
            seen.add(title_key(title))
            links = link_re.findall(block)
            paper_url = next((u for u in links if "github.com" not in u), links[0] if links else "")
            display = VENUE_DISPLAY.get(venue_norm, venue_norm)
            if "Findings" in venue_raw or "findings" in venue_raw:
                display = f"{display} Findings"
            elif "workshop" in venue_raw.lower():
                display = f"{display} Workshop"
            elif "industry" in venue_raw.lower():
                display = f"{display} Industry"
            papers.append(
                {
                    "title": title,
                    "year": year,
                    "venue": display,
                    "venue_class": VENUE_CLASS[venue_norm],
                    "era": "llm",
                    "found_via": "venue",
                    "doi": doi_of(paper_url),
                    "arxiv": arxiv_of(paper_url),
                    "url": paper_url,
                    "why": "handbook venue badge in spec list",
                    "source": "handbook",
                    "authors": [],
                    "cited_by": [],
                    "status": "drafted",
                    "themes": themes_for(title),
                    "benchmarks": [],
                }
            )
    return papers


def parse_crossref(path: Path) -> list[dict]:
    items = json.loads(path.read_text())
    out = []
    seen = set()
    for it in items:
        title = clean_title((it.get("title") or [""])[0])
        if not TITLE_KW.search(title):
            continue
        container = (it.get("container-title") or [""])[0]
        matched = None
        for pat, venue, vclass in STRICT_CONTAINERS:
            if pat.search(container or ""):
                matched = (venue, vclass)
                break
        if not matched:
            continue
        year = None
        for k in ("issued", "published-print", "published-online"):
            parts = (it.get(k) or {}).get("date-parts")
            if parts:
                year = parts[0][0]
                break
        if not year or year < 2023:
            continue
        key = title_key(title)
        if key in seen:
            continue
        seen.add(key)
        authors = []
        for a in it.get("author") or []:
            given = a.get("given") or ""
            family = a.get("family") or ""
            name = f"{given} {family}".strip()
            if name:
                authors.append(name)
        doi = it.get("DOI") or ""
        out.append(
            {
                "title": title,
                "year": year,
                "venue": matched[0],
                "venue_class": matched[1],
                "era": "llm",
                "found_via": "venue",
                "doi": doi,
                "arxiv": "",
                "url": f"https://doi.org/{doi}" if doi else "",
                "why": "Crossref title+container whitelist",
                "source": "crossref",
                "authors": authors,
                "cited_by": [],
                "status": "drafted",
                "themes": themes_for(title),
                "benchmarks": [],
            }
        )
    return out


CLASSICS = [
    {
        "citekey": "Seq2SQL2017",
        "title": "Seq2SQL: Generating Structured Queries from Natural Language using Reinforcement Learning",
        "year": 2017,
        "venue": "arXiv / WikiSQL",
        "venue_class": "other",
        "authors": ["Victor Zhong", "Caiming Xiong", "Richard Socher"],
        "arxiv": "1709.00103",
        "why": "founding neural generation + WikiSQL benchmark",
        "themes": ["pre-llm", "benchmark"],
        "benchmarks": ["WikiSQL"],
        "problem": "把 NL 直接映射到 SQL，当时缺少大规模标注。",
        "method": "提出 WikiSQL，并用强化学习（Seq2SQL）按 SQL 子句生成查询。",
        "relation": "related work 里「第一代 neural NL2SQL」的起点；WikiSQL 单表设定用来对照 Spider/BIRD 的跨库难度。",
        "cited_by_hint": ["DINSQL2023", "DAILSQL2024", "BIRD2023"],
    },
    {
        "citekey": "SQLNet2017",
        "title": "SQLNet: Generating Structured Queries From Natural Language Without Reinforcement Learning",
        "year": 2017,
        "venue": "arXiv",
        "venue_class": "other",
        "authors": ["Xiaojun Xu", "Chang Liu", "Dawn Song"],
        "arxiv": "1711.04436",
        "why": "named founding sketch-based method",
        "themes": ["pre-llm"],
        "benchmarks": ["WikiSQL"],
        "problem": "Seq2SQL 的 RL 训练不稳定，且 SQL 序列生成会受词序影响。",
        "method": "用 sketch 填槽代替自左向右解码，避开强化学习。",
        "relation": "用来说明前 LLM 一代如何把 SQL 结构先验写进模型，对照现在把结构先验放到 prompt/约束解码。",
        "cited_by_hint": ["DINSQL2023", "CodeS2024"],
    },
    {
        "citekey": "Spider2018",
        "title": "Spider: A Large-Scale Human-Labeled Dataset for Complex and Cross-Domain Semantic Parsing and Text-to-SQL Task",
        "year": 2018,
        "venue": "EMNLP",
        "venue_class": "NLP",
        "authors": ["Tao Yu", "Rui Zhang", "Kai Yang", "Michihiro Yasunaga", "Dongxu Wang", "Zifan Li", "James Ma", "Irene Li", "Qingning Yao", "Shanelle Roman", "Zilin Zhang", "Dragomir Radev"],
        "arxiv": "1809.08887",
        "why": "canonical cross-domain benchmark",
        "themes": ["pre-llm", "benchmark"],
        "benchmarks": ["Spider"],
        "problem": "WikiSQL 只有单表、查询简单，无法衡量跨库泛化。",
        "method": "发布 200 库、多表复杂 SQL 的人工标注集，成为十年标准榜。",
        "relation": "必须引的问题设定。我们的主战场是 BIRD，但 Spider 仍是方法对照和历史主线。",
        "cited_by_hint": ["BIRD2023", "DINSQL2023", "DAILSQL2024", "Spider22025"],
    },
    {
        "citekey": "SParC2019",
        "title": "SParC: Cross-Domain Semantic Parsing in Context",
        "year": 2019,
        "venue": "ACL",
        "venue_class": "NLP",
        "authors": ["Tao Yu", "Rui Zhang", "Michihiro Yasunaga", "Yi Chern Tan", "Xi Victoria Lin", "Suyi Li", "Heyang Er", "Irene Li", "Bo Pang", "Tao Chen", "Emily Ji", "Shreya Dixit", "David Proctor", "Sungrok Shim", "Jonathan Kraft", "Vincent Zhang", "Caiming Xiong", "Richard Socher", "Dragomir Radev"],
        "arxiv": "1906.02285",
        "why": "context-dependent benchmark sourced from Spider",
        "themes": ["pre-llm", "benchmark"],
        "benchmarks": ["SParC"],
        "problem": "单轮 Spider 不能覆盖真实交互里的指代和省略。",
        "method": "在 Spider 库上标注多轮问题，要求模型跟踪对话上下文。",
        "relation": "若我们只做单轮 BIRD，这里一笔带过；若相关工作要谈交互式 NL2SQL，SParC/CoSQL 是源头。",
        "cited_by_hint": ["NL2SQL3602024"],
    },
    {
        "citekey": "CoSQL2019",
        "title": "CoSQL: A Conversational Text-to-SQL Challenge Towards Cross-Domain Natural Language Interfaces to Databases",
        "year": 2019,
        "venue": "EMNLP",
        "venue_class": "NLP",
        "authors": ["Tao Yu", "Rui Zhang", "Heyang Er", "Suyi Li", "Eric Xue", "Bo Pang", "Xi Victoria Lin", "Yi Chern Tan", "Tianze Shi", "Zihan Li", "Youxuan Jiang", "Michihiro Yasunaga", "Sungrok Shim", "Tao Chen", "Alexander Fabbri", "Zifan Li", "Luyao Chen", "Yuwen Zhang", "Shreya Dixit", "Vincent Zhang", "Caiming Xiong", "Richard Socher", "Walter Lasecki", "Dragomir Radev"],
        "arxiv": "1909.05378",
        "why": "conversational NL2SQL benchmark",
        "themes": ["pre-llm", "benchmark"],
        "benchmarks": ["CoSQL"],
        "problem": "真实数据库对话包含澄清、拒绝执行、改写请求，不只是连续提问。",
        "method": "引入 wizard-of-oz 式数据库对话，混合 SQL 与系统回复动作。",
        "relation": "BIRD-Interact 等新交互评测的前身；用来区分「多轮 Spider」和「真正的 DB 对话」。",
        "cited_by_hint": ["NL2SQL3602024"],
    },
    {
        "citekey": "IRNet2019",
        "title": "Towards Complex Text-to-SQL in Cross-Domain Database with Intermediate Representation",
        "year": 2019,
        "venue": "ACL",
        "venue_class": "NLP",
        "authors": ["Jiaqi Guo", "Zecheng Zhan", "Yan Gao", "Yan Xiao", "Jian-Guang Lou", "Ting Liu", "Dongmei Zhang"],
        "arxiv": "1905.08205",
        "why": "IRNet; named SemQL intermediate generation",
        "themes": ["pre-llm"],
        "benchmarks": ["Spider"],
        "problem": "直接生成 SQL 难以处理跨域 schema 对齐和复杂组合。",
        "method": "先生成与 schema 解耦的 SemQL 中间表示，再确定性转 SQL。",
        "relation": "中间表示路线的代表。对照 LLM 时代把 IR 换成 CoT / 子问题分解。",
        "cited_by_hint": ["DINSQL2023", "RESDSQL2023"],
    },
    {
        "citekey": "RATSQL2020",
        "title": "RAT-SQL: Relation-Aware Schema Encoding and Linking for Text-to-SQL Parsers",
        "year": 2020,
        "venue": "ACL",
        "venue_class": "NLP",
        "authors": ["Bailin Wang", "Richard Shin", "Xiaodong Liu", "Oleksandr Polozov", "Matthew Richardson"],
        "arxiv": "1911.04942",
        "why": "foundational schema linking encoder; cited as method heading",
        "themes": ["pre-llm", "schema-linking"],
        "benchmarks": ["Spider"],
        "problem": "问题词和 schema 元素的对齐是跨域 NL2SQL 的核心瓶颈。",
        "method": "用 relation-aware transformer 同时编码问题和 schema 图，显式做 schema linking。",
        "relation": "schema linking 必引。用来对照「独立 linking 模块」vs「LLM 隐式 linking / death of schema linking」。",
        "cited_by_hint": ["DINSQL2023", "CodeS2024", "LinkAlign2025"],
    },
    {
        "citekey": "BRIDGE2020",
        "title": "Bridging Textual and Tabular Data for Cross-Domain Text-to-SQL Semantic Parsing",
        "year": 2020,
        "venue": "Findings of EMNLP",
        "venue_class": "NLP",
        "authors": ["Xi Victoria Lin", "Richard Socher", "Caiming Xiong"],
        "arxiv": "2012.12627",
        "why": "BRIDGE; named BERT-era schema serialization baseline",
        "themes": ["pre-llm", "schema-linking"],
        "benchmarks": ["Spider"],
        "problem": "如何把表结构和单元格值一起喂给预训练语言模型。",
        "method": "序列化 schema 与被提及的单元格值，用 BERT 做跨模态编码。",
        "relation": "值接地（value grounding）的前 LLM 代表，对照 BIRD 上的 value retrieval / evidence。",
        "cited_by_hint": ["BIRD2023", "DINSQL2023"],
    },
    {
        "citekey": "PICARD2021",
        "title": "PICARD: Parsing Incrementally for Constrained Auto-Regressive Decoding from Language Models",
        "year": 2021,
        "venue": "EMNLP",
        "venue_class": "NLP",
        "authors": ["Torsten Scholak", "Nathan Schucher", "Dzmitry Bahdanau"],
        "arxiv": "2109.05093",
        "why": "constrained decoding baseline repeatedly named",
        "themes": ["pre-llm", "execution"],
        "benchmarks": ["Spider"],
        "problem": "T5 等 LM 会生成语法非法或引用不存在列的 SQL。",
        "method": "增量词法/语法检查，拒绝非法 token，把解码约束在可执行 SQL 空间。",
        "relation": "执行期约束的经典。对照 LLM 时代的 execution-guided repair / DBMS 反馈（SafeQL）。",
        "cited_by_hint": ["DINSQL2023", "DAILSQL2024", "CodeS2024"],
    },
    {
        "citekey": "SmBoP2021",
        "title": "SmBoP: Semi-autoregressive Bottom-up Semantic Parsing",
        "year": 2021,
        "venue": "NAACL",
        "venue_class": "NLP",
        "authors": ["Ohad Rubin", "Jonathan Berant"],
        "arxiv": "2010.12412",
        "why": "named bottom-up decoder baseline",
        "themes": ["pre-llm"],
        "benchmarks": ["Spider"],
        "problem": "自左向右生成难以先构造子树再组合复杂 SQL。",
        "method": "自底向上、半自回归地组合 SQL 子树。",
        "relation": "结构解码对照；我们若走 LLM prompting，不必当 baseline 重跑，但 related work 要承认这条线。",
        "cited_by_hint": ["DINSQL2023"],
    },
    {
        "citekey": "KaggleDBQA2021",
        "title": "KaggleDBQA: Realistic Evaluation of Text-to-SQL Parsers",
        "year": 2021,
        "venue": "ACL",
        "venue_class": "NLP",
        "authors": ["Chia-Hsuan Lee", "Oleksandr Polozov", "Matthew Richardson"],
        "why": "realistic small-domain benchmark",
        "themes": ["pre-llm", "benchmark"],
        "benchmarks": ["KaggleDBQA"],
        "problem": "Spider 的库经过规范化，列名对模型过于友好。",
        "method": "用真实 Kaggle 数据库和更自然的问题做小规模但更难的评测。",
        "relation": "BIRD 强调 dirty schema / 外部知识，这条线从 KaggleDBQA 就开始了。",
        "cited_by_hint": ["BIRD2023", "NL2SQL3602024"],
    },
    {
        "citekey": "RASAT2022",
        "title": "RASAT: Integrating Relational Structures into Pretrained Seq2Seq Model for Text-to-SQL",
        "year": 2022,
        "venue": "EMNLP",
        "venue_class": "NLP",
        "authors": ["Jiexing Qi", "Jingyao Tang", "Ziwei He", "Xiangpeng Wan", "Yu Cheng", "Chenghu Zhou", "Xinbing Wang", "Quanshi Zhang", "Zhouhan Lin"],
        "arxiv": "2205.06983",
        "why": "named relation-aware T5 baseline",
        "themes": ["pre-llm"],
        "benchmarks": ["Spider"],
        "problem": "纯 T5 看不到 schema 关系图。",
        "method": "把关系结构注入预训练 seq2seq 的 self-attention。",
        "relation": "PLM + 结构偏置的收官工作之一，用来结束「前 LLM 编码器」小节。",
        "cited_by_hint": ["CodeS2024", "DAILSQL2024"],
    },
    {
        "citekey": "S2SQL2022",
        "title": "S2SQL: Injecting Syntax to Question-Schema Interaction Graph Encoder for Text-to-SQL Parsers",
        "year": 2022,
        "venue": "Findings of ACL",
        "venue_class": "NLP",
        "authors": ["Binyuan Hui", "Ruiying Geng", "Lihan Wang", "Bowen Qin", "Bowen Li", "Jian Sun", "Yongbin Li"],
        "arxiv": "2203.06958",
        "why": "named syntax-augmented graph encoder",
        "themes": ["pre-llm", "schema-linking"],
        "benchmarks": ["Spider"],
        "problem": "问题句法结构没有被 schema 图编码器利用。",
        "method": "把句法注入 question-schema interaction graph。",
        "relation": "图编码器家族的代表，和 RAT-SQL / LGESQL 放在同一段。",
        "cited_by_hint": ["BIRD2023"],
    },
    {
        "citekey": "LGESQL2021",
        "title": "LGESQL: Line Graph Enhanced Text-to-SQL Model with Mixed Local and Non-Local Relations",
        "year": 2021,
        "venue": "ACL",
        "venue_class": "NLP",
        "authors": ["Ruisheng Cao", "Lu Chen", "Zhi Chen", "Yanbin Zhao", "Su Zhu", "Kai Yu"],
        "arxiv": "2106.01093",
        "why": "named line-graph schema encoder",
        "themes": ["pre-llm", "schema-linking"],
        "benchmarks": ["Spider"],
        "problem": "普通 schema 图难以表达边与边之间的高阶关系。",
        "method": "用 line graph 增强局部/非局部关系建模。",
        "relation": "RAT-SQL 之后最常被点名的图编码器之一。",
        "cited_by_hint": ["BIRD2023", "DINSQL2023"],
    },
    {
        "citekey": "TypeSQL2018",
        "title": "TypeSQL: Knowledge-based Type-Aware Neural Text-to-SQL Generation",
        "year": 2018,
        "venue": "NAACL",
        "venue_class": "NLP",
        "authors": ["Tao Yu", "Zifan Li", "Zilin Zhang", "Rui Zhang", "Dragomir Radev"],
        "arxiv": "1804.09769",
        "why": "founding type-aware slot filling on WikiSQL",
        "themes": ["pre-llm"],
        "benchmarks": ["WikiSQL"],
        "problem": "数字、人名等类型信息没有进入 SQL 填槽。",
        "method": "把类型/知识特征注入 SQLNet 风格的 sketch 模型。",
        "relation": "WikiSQL 时代的知识增强；BIRD 的 evidence / 外部知识可以追溯到这里。",
        "cited_by_hint": ["BIRD2023"],
    },
    {
        "citekey": "SyntaxSQLNet2018",
        "title": "SyntaxSQLNet: Syntax Tree Networks for Complex and Cross-Domain Text-to-SQL Task",
        "year": 2018,
        "venue": "EMNLP",
        "venue_class": "NLP",
        "authors": ["Tao Yu", "Michihiro Yasunaga", "Kai Yang", "Rui Zhang", "Dongxu Wang", "Zifan Li", "Dragomir Radev"],
        "arxiv": "1810.05237",
        "why": "first complex Spider-era syntax-tree decoder",
        "themes": ["pre-llm"],
        "benchmarks": ["Spider"],
        "problem": "WikiSQL 模块无法生成嵌套 SQL。",
        "method": "按 SQL 语法树模块化解码，是 Spider 早期强基线。",
        "relation": "复杂 SQL 结构解码的源头，用来开启 Spider 时代。",
        "cited_by_hint": ["Spider2018", "IRNet2019"],
    },
]

KEY_CITATIONS = [
    {
        "citekey": "C32023",
        "title": "C3: Zero-shot Text-to-SQL with ChatGPT",
        "year": 2023,
        "venue": "arXiv",
        "venue_class": "other",
        "authors": ["Xuemei Dong", "Chao Zhang", "Yuhang Ge", "Yuren Mao", "Yunjun Gao", "Lu Chen", "Jinshu Lin", "Dongfang Lou"],
        "arxiv": "2307.07306",
        "why": "named zero-shot ChatGPT pipeline; Spider test 82.3",
        "themes": ["prompting"],
        "benchmarks": ["Spider"],
        "problem": "ChatGPT 直接生成 SQL 容易忽略 schema 约束和清晰布局。",
        "method": "Clear prompting + Calibration with hints + Consistent self-consistency 的零样本流水线。",
        "relation": "早期 GPT-3.5 流水线代表，和 DIN-SQL / DAIL-SQL 一起构成 prompting 基线族。",
        "cited_by_hint": ["DAILSQL2024", "NL2SQL3602024"],
        "era": "llm",
    },
    {
        "citekey": "MACSQL2025",
        "title": "MAC-SQL: A Multi-Agent Collaborative Framework for Text-to-SQL",
        "year": 2025,
        "venue": "COLING",
        "venue_class": "other",
        "authors": ["Bing Wang", "Changyu Ren", "Jian Yang", "Xinnian Liang", "Jiaqi Bai", "Linzheng Chai", "Zhao Yan", "Qian-Wen Zhang", "Di Yin", "Xing Sun", "Zhoujun Li"],
        "arxiv": "2312.11242",
        "why": "named multi-agent baseline in almost every agent paper",
        "themes": ["multi-agent"],
        "benchmarks": ["BIRD", "Spider"],
        "problem": "单次生成无法覆盖分解、生成、精炼三种不同技能。",
        "method": "Selector / Decomposer / Refiner 多智能体协作。",
        "relation": "多智能体 NL2SQL 的标准对照。我们若用 agent workflow，必须和 MAC-SQL 的角色划分对齐或区分。",
        "cited_by_hint": ["CHASESQL2025", "DeepEyeSQL2026", "OpenSearchSQL2025"],
        "era": "llm",
    },
    {
        "citekey": "CHESS2024",
        "title": "CHESS: Contextual Harnessing for Efficient SQL Synthesis",
        "year": 2024,
        "venue": "arXiv",
        "venue_class": "other",
        "authors": ["Shayan Talaei", "Mohammadreza Pourreza", "Yu-Chen Chang", "Azalia Mirhoseini", "Amin Saberi"],
        "arxiv": "2405.16755",
        "why": "named retrieval+candidate ranking system; BIRD SOTA lineage",
        "themes": ["schema-linking", "execution"],
        "benchmarks": ["BIRD"],
        "problem": "大 schema 和证据文档不能整表塞进上下文。",
        "method": "实体/上下文检索、候选生成与修订，强调 efficient synthesis。",
        "relation": "BIRD 上检索增强流水线的关键对照，schema linking 并未消失，而是变成检索。",
        "cited_by_hint": ["CHASESQL2025", "LinkAlign2025"],
        "era": "llm",
    },
    {
        "citekey": "PETSQL2024",
        "title": "PET-SQL: A Prompt-Enhanced Two-Round Refinement of Text-to-SQL with Cross-consistency",
        "year": 2024,
        "venue": "arXiv",
        "venue_class": "other",
        "authors": ["Zhishuai Li", "Xiang Wang", "Jingjing Zhao", "Sun Yang", "Guoqing Du", "Xiaoru Hu", "Bin Zhang", "Yuxiao Ye", "Ziyue Li", "Rui Zhao", "Hangyu Mao"],
        "arxiv": "2403.09732",
        "why": "named two-round consistency refinement",
        "themes": ["prompting", "execution"],
        "benchmarks": ["BIRD", "Spider"],
        "problem": "单轮 prompt 的 schema 引用和最终 SQL 不一致。",
        "method": "两轮 prompt，用 cross-consistency 在多候选间投票。",
        "relation": "self-consistency / 多候选选择的对照，CHASE-SQL 的 pairwise selector 可以对着它写。",
        "cited_by_hint": ["CHASESQL2025", "OpenSearchSQL2025"],
        "era": "llm",
    },
    {
        "citekey": "ESQL2024",
        "title": "E-SQL: Direct Schema Linking via Question Enrichment in Text-to-SQL",
        "year": 2024,
        "venue": "arXiv",
        "venue_class": "other",
        "authors": ["Hasan Alp Caferoğlu", "Özgür Ulusoy"],
        "arxiv": "2409.16751",
        "why": "named question-enrichment linking",
        "themes": ["schema-linking"],
        "benchmarks": ["BIRD"],
        "problem": "把 linking 做成独立模块容易级联错误。",
        "method": "用相关 schema 信息改写问题，让生成阶段直接看见链接结果。",
        "relation": "「linking 作为问题改写」对照独立 retriever；和 Death of Schema Linking 讨论相关。",
        "cited_by_hint": ["LinkAlign2025"],
        "era": "llm",
    },
    {
        "citekey": "MCSSQL2024",
        "title": "MCS-SQL: Leveraging Multiple Prompts and Multiple-Choice Selection for Text-to-SQL Generation",
        "year": 2024,
        "venue": "COLING",
        "venue_class": "other",
        "authors": ["Dongjun Lee", "Choongwon Park", "Jaehyuk Kim", "Heesoo Park"],
        "arxiv": "2405.07467",
        "why": "named multiple-prompt selection baseline",
        "themes": ["prompting"],
        "benchmarks": ["BIRD", "Spider"],
        "problem": "单一 prompt 风格覆盖不了不同难度的题。",
        "method": "多种 prompt 出候选，再做 multiple-choice 选择。",
        "relation": "测试时扩展 / 多路径生成的早期形式，CHASE-SQL 多路径推理的近邻。",
        "cited_by_hint": ["CHASESQL2025"],
        "era": "llm",
    },
    {
        "citekey": "DeathOfSchemaLinking2024",
        "title": "The Death of Schema Linking? Text-to-SQL in the Age of Well-Reasoned Language Models",
        "year": 2024,
        "venue": "arXiv",
        "venue_class": "other",
        "authors": ["Karime Maamari", "Fadhil Abubaker", "Daniel Jaroslawicz", "Amine Mhedhbi"],
        "arxiv": "2408.07702",
        "why": "named position paper on schema linking",
        "themes": ["schema-linking"],
        "benchmarks": ["BIRD"],
        "problem": "独立 schema linking 模块在强推理模型上可能成为误差源。",
        "method": "论证对足够强的 LLM，完整 schema + 推理可能优于激进 pruning。",
        "relation": "schema linking 小节的对立面。我们要明确自己站在「仍需检索」还是「长上下文足够」。",
        "cited_by_hint": ["LinkAlign2025", "LongContextNL2SQL2025"],
        "era": "llm",
    },
    {
        "citekey": "RESDSQL2023",
        "title": "RESDSQL: Decoupling Schema Linking and Skeleton Parsing for Text-to-SQL",
        "year": 2023,
        "venue": "AAAI",
        "venue_class": "other",
        "authors": ["Haoyang Li", "Jing Zhang", "Cuiping Li", "Hong Chen"],
        "arxiv": "2302.05965",
        "why": "last strong PLM baseline before LLM era; named skeleton ranking",
        "themes": ["pre-llm", "schema-linking", "finetuning"],
        "benchmarks": ["Spider"],
        "problem": "linking 和 SQL 骨架生成缠在一起，难优化。",
        "method": "先做 schema linking / 骨架排序，再填值，基于 T5。",
        "relation": "前 LLM 最强开源对照之一；CodeS / OmniSQL 常拿它当 PLM 基线。",
        "cited_by_hint": ["CodeS2024", "OmniSQL2025", "DAILSQL2024"],
        "era": "llm",
    },
    {
        "citekey": "GraphixT52023",
        "title": "Graphix-T5: Mixing Pre-trained Transformers with Graph-Aware Layers for Text-to-SQL Parsing",
        "year": 2023,
        "venue": "AAAI",
        "venue_class": "other",
        "authors": ["Jinyang Li", "Binyuan Hui", "Reynold Cheng", "Bowen Qin", "Chenhao Ma", "Nan Huo", "Fei Huang", "Wenyu Du", "Luo Si", "Yongbin Li"],
        "arxiv": "2301.07507",
        "why": "named graph-aware T5 baseline",
        "themes": ["pre-llm", "schema-linking"],
        "benchmarks": ["Spider"],
        "problem": "T5 缺乏显式 schema 图偏置。",
        "method": "在 T5 中插入 graph-aware 层混合预训练表示与关系图。",
        "relation": "PLM+图 的 2023 代表，作为 LLM prompting 之前的最后一代结构模型。",
        "cited_by_hint": ["BIRD2023", "CodeS2024"],
        "era": "llm",
    },
]

CORE_NOTES = {
    "can llm already serve as a database interface": {
        "citekey": "BIRD2023",
        "authors": ["Jinyang Li", "Binyuan Hui", "Ge Qu", "Jiaxi Yang", "Binhua Li", "Bowen Li", "Bailin Wang", "Bowen Qin", "Rongyu Cao", "Ruiying Geng", "Nan Huo", "Xuanhe Zhou", "Chenhao Ma", "Guoliang Li", "Kevin C. C. Chang", "Fei Huang", "Reynold Cheng", "Yongbin Li"],
        "themes": ["benchmark"],
        "benchmarks": ["BIRD"],
        "problem": "Spider 上的高分无法迁移到更大、更脏、需要外部知识的真实数据库。",
        "method": "发布 BIRD：95 库、外键脏 schema、evidence，并引入执行准确率与 VES。",
        "relation": "我们的主评测场。related work 的问题设定段从这里起笔。",
    },
    "din-sql": {
        "citekey": "DINSQL2023",
        "authors": ["Mohammadreza Pourreza", "Davood Rafiei"],
        "themes": ["prompting", "execution"],
        "benchmarks": ["Spider", "BIRD"],
        "problem": "复杂 SQL 一次生成容易在 schema linking 和嵌套上同时出错。",
        "method": "把任务分解为 schema linking、分类、生成、自校正四个 prompt。",
        "relation": "LLM 分解式 prompting 的标准对照。我们的流水线若更重，要说明比 DIN-SQL 多在哪。",
    },
    "text-to-sql empowered by large language models": {
        "citekey": "DAILSQL2024",
        "authors": ["Dawei Gao", "Haibin Wang", "Yaliang Li", "Xiuyu Sun", "Yichen Qian", "Bolin Ding", "Jingren Zhou"],
        "themes": ["prompting", "benchmark"],
        "benchmarks": ["Spider", "BIRD"],
        "problem": "当时缺少对 prompt 工程选项的系统评测。",
        "method": "系统比较 example selection / 组织方式，提出 DAIL-SQL，并成为 Spider 测试集强基线。",
        "relation": "example selection 必引。也是「prompting 就能打榜」的证据。",
    },
    "the dawn of natural language to sql": {
        "citekey": "NL2SQL3602024",
        "authors": ["Boyan Li", "Yuyu Luo", "Chengliang Chai", "Guoliang Li", "Nan Tang"],
        "themes": ["benchmark", "systems"],
        "benchmarks": ["Spider", "BIRD"],
        "problem": "只看 EX 无法判断方法在难度、开销、鲁棒性上的差异。",
        "method": "NL2SQL360 测试床，多指标细粒度评估，并给出 SuperSQL 等观察。",
        "relation": "评测协议段必引。我们报 BIRD EX 时要用它来承认指标盲区。",
    },
    "codes: towards building open-source": {
        "citekey": "CodeS2024",
        "authors": ["Haoyang Li", "Jing Zhang", "Hanbing Liu", "Ju Fan", "Xiaokang Zhang", "Jun Zhu", "Renjie Wei", "Hongyan Pan", "Cuiping Li", "Hong Chen"],
        "themes": ["finetuning"],
        "benchmarks": ["Spider", "BIRD"],
        "problem": "闭源 LLM prompting 贵、不可定制，开源模型缺 SQL 数据。",
        "method": "增量预训练 + 双向数据增强，发布 CodeS 系列开源 Text-to-SQL 模型。",
        "relation": "开源 SFT 主对照。我们若走闭源 agent，要解释为何不走 CodeS 路线；若走开源，它是底座。",
    },
    "chase-sql": {
        "citekey": "CHASESQL2025",
        "authors": ["Mohammadreza Pourreza", "Hailong Li", "Ruoxi Sun", "Yeounoh Chung", "Shayan Talaei", "Gaurav Tarlok Kakkar", "Yu Gan", "Amin Saberi", "Fatma Ozcan", "Sercan O. Arik"],
        "themes": ["multi-agent", "prompting"],
        "benchmarks": ["BIRD"],
        "problem": "单一推理路径覆盖不了复杂题，多数投票也选不好候选。",
        "method": "多路径生成（分治、执行计划 CoT、实例感知示例）+ 成对偏好选择 agent。",
        "relation": "BIRD 上测试时扩展 / 多候选选择的关键 SOTA。我们的选 SQL 策略必须对着它写。",
    },
    "spider 2.0": {
        "citekey": "Spider22025",
        "authors": ["Fangyu Lei", "Jixuan Chen", "Yuxiao Ye", "Ruisheng Cao", "Dongchan Shin", "Hongjin Su", "Zhaoqing Suo", "Hongcheng Gao", "Wenjing Hu", "Pengcheng Yin", "Victor Zhong", "Caiming Xiong", "Ruoxi Sun", "Qian Liu", "Sida Wang", "Tao Yu"],
        "themes": ["benchmark", "systems"],
        "benchmarks": ["Spider2"],
        "problem": "学术 Spider/BIRD 仍远小于真实企业仓库上的多方言、长上下文工作流。",
        "method": "企业级 workflow 评测，Snow/Lite 子集，强调 agent 与多步操作。",
        "relation": "若我们声称生产可用，必须讨论 Spider 2.0；只打 BIRD 则要承认评测差距。",
    },
    "omnisql": {
        "citekey": "OmniSQL2025",
        "authors": ["Haoyang Li", "Shang Wu", "Xiaokang Zhang", "Xinmei Huang", "Jing Zhang", "Fuxin Jiang", "Shuai Wang", "Tieying Zhang", "Jianjun Chen", "Rui Shi", "Hong Chen", "Cuiping Li"],
        "themes": ["finetuning"],
        "benchmarks": ["BIRD", "Spider"],
        "problem": "公开训练数据覆盖不够，SFT 模型泛化差。",
        "method": "自动合成 SynSQL-2.5M（库+问题+SQL+CoT），再训 OmniSQL 7B/14B/32B。",
        "relation": "数据合成路线的代表。和 CodeS 一起构成开源模型段。",
    },
    "opensearch-sql": {
        "citekey": "OpenSearchSQL2025",
        "authors": ["Xiangjin Xie", "Guangwei Xu", "Lingyan Zhao", "Ruijie Guo"],
        "themes": ["prompting", "execution"],
        "benchmarks": ["BIRD"],
        "problem": "few-shot 与多候选对齐在 BIRD 上仍不稳定。",
        "method": "动态 few-shot + consistency alignment 的完整流水线。",
        "relation": "工业检索系统背景的 BIRD 流水线，系统和 prompting 两段都可以引。",
    },
    "deepeye-sql": {
        "citekey": "DeepEyeSQL2026",
        "themes": ["multi-agent", "systems"],
        "benchmarks": ["BIRD"],
        "problem": "现有 agent 流水线缺少软件工程式的阶段门控和质量保证。",
        "method": "把 SDLC 思想搬到 Text-to-SQL：分阶段开发、验证、修复。",
        "relation": "2026 SIGMOD 的系统/agent 对照。强调工程化 workflow，而不是单点 prompting。",
    },
    "diver: a robust text-to-sql": {
        "citekey": "DIVER2026",
        "themes": ["schema-linking", "systems"],
        "benchmarks": ["BIRD"],
        "problem": "BIRD 上 value linking 与 evidence 推理仍然脆弱。",
        "method": "动态交互式 value linking + evidence reasoning，带工具箱和结构化工作区。",
        "relation": "值接地 / evidence 段的 2026 对照。BIRD 外部知识题要引。",
    },
    "alpha-sql": {
        "citekey": "AlphaSQL2025",
        "authors": ["Boyan Li", "Jiayi Zhang", "Ju Fan", "Yanwei Xu", "Chong Chen", "Nan Tang", "Yuyu Luo"],
        "themes": ["execution", "multi-agent"],
        "benchmarks": ["BIRD"],
        "problem": "零样本模型不会搜索中间 SQL 假设。",
        "method": "用 MCTS 在执行反馈上搜索 SQL，无需任务微调。",
        "relation": "测试时搜索对照。和自校正循环、SafeQL 的 DBMS 引导搜索放在一段。",
    },
    "linkalign": {
        "citekey": "LinkAlign2025",
        "themes": ["schema-linking"],
        "benchmarks": ["Spider2", "BIRD", "Spider"],
        "problem": "真实多库、超大 schema 下 database retrieval 和 item grounding 都失败。",
        "method": "多轮语义检索 + 无关库隔离 + schema extraction，Agent/Pipeline 双模式。",
        "relation": "大规模 schema linking 的新 SOTA 叙事，尤其 Spider 2.0-Lite。",
    },
    "star-sql": {
        "citekey": "STaRSQL2025",
        "authors": ["Mingqian He", "Yongliang Shen", "Wenqi Zhang", "Qiuying Peng", "Jun Wang", "Weiming Lu"],
        "themes": ["finetuning", "execution"],
        "benchmarks": ["BIRD", "Spider"],
        "problem": "SQL 生成很少被当成可自我训练的推理过程。",
        "method": "Self-Taught Reasoner：用结果监督奖励模型迭代改进推理轨迹。",
        "relation": "推理/RL 微调段。和 SQL-R1、Reward-SQL 构成 2025 训练路线。",
    },
    "sciencebenchmark": {
        "citekey": "ScienceBenchmark2024",
        "themes": ["benchmark"],
        "benchmarks": ["ScienceBenchmark"],
        "problem": "通用 Spider 不能代表科研库的领域术语和复杂 schema。",
        "method": "三个真实科学数据库上的 NL2SQL 基准。",
        "relation": "领域基准对照，说明 BIRD 也不是唯一真实设定。",
    },
    "finsql": {
        "citekey": "FinSQL2024",
        "themes": ["systems", "finetuning"],
        "benchmarks": ["BULL"],
        "problem": "金融库需要模型无关、可私有部署的 NL2SQL。",
        "method": "模型无关 LLM 框架 + 金融场景数据 BULL。",
        "relation": "工业/垂直场景段。对照通用 BIRD 榜。",
    },
    "purple": {
        "citekey": "PURPLE2024",
        "themes": ["prompting", "schema-linking"],
        "benchmarks": ["Spider"],
        "problem": "LLM 写 SQL 时对中间结构的利用不够。",
        "method": "解析、检索、提示、修复的组合，让 LLM 更像 SQL writer。",
        "relation": "ICDE 2024 的模块化流水线，DB 会议里的 prompting 代表。",
    },
    "metasql": {
        "citekey": "MetaSQL2024",
        "themes": ["prompting"],
        "benchmarks": ["Spider"],
        "problem": "一次生成无法覆盖语义等价的多种 SQL 写法。",
        "method": "generate-then-rank：先多样生成再排序。",
        "relation": "候选生成+排序，和 CHASE 选择器同一族，但还在 ICDE 2024。",
    },
    "synthesizing text-to-sql data from weak and strong": {
        "citekey": "SENSE2024",
        "themes": ["finetuning"],
        "benchmarks": ["Spider", "BIRD"],
        "problem": "强模型数据贵，弱模型数据噪。",
        "method": "用强弱 LLM 合成互补数据，训 SENSE。",
        "relation": "ACL 2024 数据合成，和 OmniSQL 前后相接。",
    },
    "act-sql": {
        "citekey": "ACTSQL2023",
        "themes": ["prompting"],
        "benchmarks": ["Spider"],
        "problem": "手工 CoT 示范贵。",
        "method": "自动生成 chain-of-thought 示范再做 ICL。",
        "relation": "自动 CoT 对照 DIN-SQL 手工分解。",
    },
    "selective demonstrations for cross-domain": {
        "citekey": "ODIS2023",
        "themes": ["prompting"],
        "benchmarks": ["Spider"],
        "problem": "跨域 few-shot 选例不当会伤害泛化。",
        "method": "ODIS：为跨域 Text-to-SQL 选择示范。",
        "relation": "example selection 和 DAIL-SQL 同一段。",
    },
    "route: robust multitask": {
        "citekey": "ROUTE2025",
        "themes": ["finetuning", "multi-agent"],
        "benchmarks": ["BIRD"],
        "problem": "单任务 SFT 不够鲁棒。",
        "method": "多任务调优 + 协作，增强 Text-to-SQL。",
        "relation": "ICLR 2025 开源协作/多任务对照。",
    },
    "sql-r1": {
        "citekey": "SQLR12025",
        "authors": ["Peixian Ma", "Xialie Zhuang", "Chengjin Xu", "Xuhui Jiang", "Ran Chen", "Jian Guo"],
        "themes": ["finetuning", "execution"],
        "benchmarks": ["BIRD"],
        "problem": "监督微调学不到可验证的 SQL 推理。",
        "method": "用强化学习训 NL2SQL 推理模型。",
        "relation": "NeurIPS 2025 RL 路线，和 STaR-SQL 一起写训练段。",
    },
    "you only read once": {
        "citekey": "YORO2025",
        "themes": ["schema-linking", "finetuning"],
        "benchmarks": ["BIRD"],
        "problem": "每次推理都把整个库读进上下文又慢又容易丢值。",
        "method": "把数据库知识内化进模型，降低反复读 schema 的需求。",
        "relation": "schema 内化 vs 检索的对照，适合系统和 linking 两段。",
    },
    "natural language to sql: state of the art": {
        "citekey": "NL2SQLSOTA2025",
        "themes": ["benchmark", "systems"],
        "benchmarks": ["BIRD", "Spider"],
        "problem": "LLM 时代 NL2SQL 的开放问题需要从系统视角重述。",
        "method": "VLDB 2025 教程/综述：现状、模块划分、开放问题。",
        "relation": "DB 视角综述，related work 框架可以直接借模块划分。",
    },
    "natural language interfaces for databases with deep learning": {
        "citekey": "NLIDBTutorial2023",
        "authors": ["George Katsogiannis-Meimarakis", "Mike Xydas", "Georgia Koutrika"],
        "themes": ["systems"],
        "benchmarks": [],
        "problem": "深度学习 NLIDB 的模块和流程缺乏面向 DB 社区的系统梳理。",
        "method": "VLDB 2023 教程：从语义解析到 LLM 的 NLIDB 全景。",
        "relation": "DB 视角的教程，related work 开头可用来一句话收束 NLIDB 历史。",
    },
    "generating succinct descriptions of database schemata": {
        "citekey": "SchemaDescriptions2024",
        "themes": ["schema-linking", "systems"],
        "benchmarks": [],
        "problem": "把整库 schema 塞进 prompt 太贵，列描述冗余。",
        "method": "自动生成简洁的 schema 描述，降低 prompting 成本。",
        "relation": "schema 压缩 / 成本控制段可引，和 linking 的「少即是多」同族。",
    },
    "sql-exchange": {
        "citekey": "SQLExchange2026",
        "themes": ["systems"],
        "benchmarks": [],
        "problem": "NL2SQL 的训练/评测数据难以跨域迁移。",
        "method": "把 SQL 查询在域之间转换，扩充跨域数据。",
        "relation": "数据增广对照；与 NL2SQL 主线相邻，写数据合成段时可一句带过。",
    },
    "hexgen-flow": {
        "citekey": "HexGenFlow2026",
        "themes": ["systems"],
        "benchmarks": [],
        "problem": "agentic Text-to-SQL 的多轮 LLM 请求调度开销大。",
        "method": "优化 LLM 推理请求调度，降低 agent 流水线的延迟和成本。",
        "relation": "系统段：证明 agentic NL2SQL 的成本问题已经被 DB 社区认真对待。",
    },
    "a survey on deep learning approaches for text-to-sql": {
        "citekey": "KatsogiannisSurvey2023",
        "themes": ["benchmark"],
        "benchmarks": ["Spider"],
        "problem": "深度学习 NL2SQL 方法缺乏统一梳理。",
        "method": "VLDBJ 综述覆盖编码、解码、数据集。",
        "relation": "用来迅速收束前 LLM 文献，避免 related work 写成编年史。",
    },
    "safeql": {
        "citekey": "SafeQL2026",
        "themes": ["execution"],
        "benchmarks": ["BIRD", "Spider"],
        "problem": "失败后整句重生成，DBMS 只当报错器。",
        "method": "把 DBMS 反馈变成对错误子句的引导搜索，在安全查询空间里修。",
        "relation": "执行反馈段 2026 代表。我们的 repair 循环要说明是否也把 DBMS 当主动指导。",
    },
    "is long context all you need": {
        "citekey": "LongContextNL2SQL2025",
        "themes": ["schema-linking", "systems"],
        "benchmarks": ["BIRD"],
        "problem": "schema pruning 可能丢掉必要列，长上下文模型或许能吃全库。",
        "method": "用 Gemini 等长上下文直接喂更多 schema，检验是否还要 linking。",
        "relation": "和 Death of Schema Linking 同一争论。用实验而不是口号来站队。",
    },
    "sphinteract": {
        "citekey": "Sphinteract2025",
        "themes": ["systems"],
        "benchmarks": ["Spider"],
        "problem": "NL 歧义不能只靠模型猜。",
        "method": "通过用户交互消除 NL2SQL 歧义。",
        "relation": "交互式澄清。若我们做单轮 BIRD，要承认这是另一条产品线。",
    },
    "taco: a benchmark": {
        "citekey": "TACO2026",
        "themes": ["benchmark"],
        "benchmarks": ["TACO"],
        "problem": "现有榜很少同时覆盖歧义和跨库检索。",
        "method": "开放域、歧义、跨库 Text-to-SQL 基准。",
        "relation": "2026 新评测，用来说明 BIRD 仍假设库已知。",
    },
    "pervasive annotation errors": {
        "citekey": "AnnotationErrors2026",
        "themes": ["benchmark"],
        "benchmarks": ["BIRD", "Spider"],
        "problem": "标注错误会让 leaderboard 失真。",
        "method": "量化 Text-to-SQL 基准中的 pervasive annotation errors。",
        "relation": "评测可信度。报 top-1 时必须面对「榜本身有噪声」。",
    },
}


LEADERBOARD_PAPERS = [
    {
        "citekey": "XiYanSQL2025",
        "title": "XiYan-SQL: A Novel Multi-Generator Framework For Text-to-SQL",
        "year": 2025,
        "venue": "arXiv",
        "venue_class": "other",
        "authors": ["Yifu Liu", "Yin Zhu", "Yingqi Gao", "Zhiling Luo", "Xiaoxia Li", "Xiaorong Shi", "Yuntao Hong", "Jinyang Gao", "Yu Li", "Bolin Ding", "Jingren Zhou"],
        "arxiv": "2507.04701",
        "why": "BIRD top-30 常驻工业系统（Alibaba Cloud，test 75.63）",
        "themes": ["prompting", "execution"],
        "benchmarks": ["BIRD", "Spider"],
        "problem": "单一生成器（无论 ICL 还是 SFT）覆盖不了不同风格和难度的题。",
        "method": "多生成器集成：ICL generator + SFT generator 各出候选，再由选择/精炼模块定稿。",
        "relation": "多生成器 + 候选选择路线的工业代表，2024 年底起长期挂在 BIRD 前列；写候选选择段绕不开。",
        "cited_by_hint": [],
        "era": "llm",
    },
    {
        "citekey": "AgentarScaleSQL2025",
        "title": "Agentar-Scale-SQL: Advancing Text-to-SQL through Orchestrated Test-Time Scaling",
        "year": 2025,
        "venue": "arXiv",
        "venue_class": "other",
        "authors": ["Pengfei Wang", "Baolin Sun", "Xuemei Dong", "Yaxun Dai", "Hongwei Yuan", "Mengdie Chu", "Yingqi Gao", "Xiang Qi", "Peng Zhang", "Ying Yan"],
        "arxiv": "2509.24403",
        "why": "BIRD test 81.67（Ant Group），orchestrated test-time scaling",
        "themes": ["multi-agent", "execution"],
        "benchmarks": ["BIRD"],
        "problem": "测试时扩展各组件（分解、候选、校验）孤立使用收益有限。",
        "method": "把任务分解、多候选生成、执行反馈校验编排成统一的 test-time scaling 流水线。",
        "relation": "蚂蚁集团上榜系统（test 81.67），「编排式 TTS」和我们系统的流水线设计直接对照。",
        "cited_by_hint": [],
        "era": "llm",
    },
    {
        "citekey": "ReasoningSQL2025",
        "title": "Reasoning-SQL: Reinforcement Learning with SQL Tailored Partial Rewards for Reasoning-Enhanced Text-to-SQL",
        "year": 2025,
        "venue": "arXiv",
        "venue_class": "other",
        "authors": ["Mohammadreza Pourreza", "Shayan Talaei", "Ruoxi Sun", "Xingchen Wan", "Hailong Li", "Azalia Mirhoseini", "Amin Saberi", "Sercan O. Arik"],
        "arxiv": "2503.23157",
        "why": "BIRD 榜 Reasoning-SQL 14B（Google Cloud / Stanford，test 72.78）",
        "themes": ["finetuning", "execution"],
        "benchmarks": ["BIRD"],
        "problem": "RL 只用最终执行结果做奖励太稀疏，中间步骤学不到信号。",
        "method": "设计 SQL 专用的部分奖励（partial rewards），按子句正确性给中间反馈。",
        "relation": "CHASE-SQL 同组的 RL 训练线，和 SQL-R1 / Arctic-Text2SQL-R1 一起构成 2025 RL 段。",
        "cited_by_hint": [],
        "era": "llm",
    },
    {
        "citekey": "CSCSQL2025",
        "title": "CSC-SQL: Corrective Self-Consistency in Text-to-SQL via Reinforcement Learning",
        "year": 2025,
        "venue": "arXiv",
        "venue_class": "other",
        "authors": ["Lei Sheng", "Shuai-Shuai Xu"],
        "arxiv": "2505.13271",
        "why": "BIRD 榜 CSC-SQL 32B/7B（test 73.67 / 71.72）",
        "themes": ["finetuning", "execution"],
        "benchmarks": ["BIRD", "Spider"],
        "problem": "多数投票选候选时，错误候选之间也会互相「投」出一致错误。",
        "method": "用 RL（GRPO）训出纠错式自一致性：先并行采样，再让模型修正后投票。",
        "relation": "self-consistency 的升级版，32B 开源模型打到 73+；候选选择段的开源对照。",
        "cited_by_hint": [],
        "era": "llm",
    },
    {
        "citekey": "ArcticText2SQLR12025",
        "title": "Arctic-Text2SQL-R1: Simple Rewards, Strong Reasoning in Text-to-SQL",
        "year": 2025,
        "venue": "arXiv",
        "venue_class": "other",
        "authors": ["Zhewei Yao", "Guoheng Sun", "Lukasz Borchmann", "Gaurav Nuti", "Zheyu Shen", "Minghang Deng", "Bohan Zhai", "Hao Zhang", "Ang Li", "Yuxiong He"],
        "arxiv": "2505.20315",
        "why": "Snowflake 单模型 track 强基线（32B test 73.84）",
        "themes": ["finetuning", "execution"],
        "benchmarks": ["BIRD", "Spider"],
        "problem": "RL 训 Text-to-SQL 的奖励设计被普遍认为需要复杂塑形。",
        "method": "反其道而行：只用简单执行奖励 + GRPO，就在 7B-32B 上训出强推理模型。",
        "relation": "单模型 track 前排，证明简单 RL 奖励就够；训练段必引的 Snowflake 工作。",
        "cited_by_hint": [],
        "era": "llm",
    },
    {
        "citekey": "TASQL2024",
        "title": "Before Generation, Align it! A Novel and Effective Strategy for Mitigating Hallucinations in Text-to-SQL Generation",
        "year": 2024,
        "venue": "ACL Findings",
        "venue_class": "NLP",
        "authors": ["Ge Qu", "Jinyang Li", "Bowen Li", "Bowen Qin", "Nan Huo", "Chenhao Ma", "Reynold Cheng"],
        "arxiv": "2405.15307",
        "why": "TA-SQL；ACL 2024 Findings，BIRD 榜 TA-SQL + GPT-4",
        "themes": ["prompting", "schema-linking"],
        "benchmarks": ["BIRD", "Spider"],
        "problem": "LLM 生成 SQL 时幻觉出不存在的列/表，源于任务对齐不足。",
        "method": "生成前先做任务对齐（TA）：把问题与 schema 元素显式对齐，再进入生成。",
        "relation": "BIRD 团队自己的幻觉缓解工作，mini-dev 的 column_meaning 也来自它；linking/对齐段可引。",
        "cited_by_hint": [],
        "era": "llm",
    },
    {
        "citekey": "AskData2025",
        "title": "Automatic Metadata Extraction for Text-to-SQL",
        "year": 2025,
        "venue": "arXiv",
        "venue_class": "other",
        "authors": ["Vladislav Shkapenyuk", "Divesh Srivastava", "Theodore Johnson", "Parisa Ghane"],
        "arxiv": "2505.19988",
        "why": "AT&T AskData + GPT-4o（BIRD test 81.95）挂名的公开论文",
        "themes": ["schema-linking", "systems"],
        "benchmarks": ["BIRD"],
        "problem": "工业库缺注释，LLM 看不到列语义，AskData 这类系统先要补元数据。",
        "method": "自动从库内容和查询日志抽取 text-to-SQL 所需的元数据/描述。",
        "relation": "榜上第 3 的工业系统公开出来的核心组件；说明元数据准备本身就是贡献点。",
        "cited_by_hint": [],
        "era": "llm",
    },
]

BIRD_TOP30 = [
    (1, "Aug 22, 2026", "SiriusAI-SQL", "Tencent Data Computing Platform", "UNK", "77.77", "82.28", None, "无公开论文"),
    (2, "Sep 02, 2026", "DataGallery-Text2SQL", "Huawei 2012 Labs [Yufei Cheng et al.]", "UNK", "77.71", "82.22", None, "本论文系统"),
    (3, "Dec 16, 2025", "AskData + GPT-4o", "AT&T CDO - DSAIR", "UNK", "77.64", "81.95", "AskData2025", ""),
    (4, "Sep 25, 2025", "Agentar-Scale-SQL", "Ant Group", "UNK", "74.90", "81.67", "AgentarScaleSQL2025", ""),
    (5, "Jun 19, 2026", "Sber Text2SQL", "SberData Research", "UNK", "75.74", "81.33", None, "无公开论文"),
    (6, "May 27, 2026", "Xiaomi Text2SQL", "Xiaomi ITP & Data", "UNK", "73.66", "80.83", None, "无公开论文"),
    (7, "Aug 19, 2026", "RAS", "Adya AI", "UNK", "72.49", "79.82", None, "无公开论文"),
    (8, "Jul 14, 2026", "DeepEye", "HKUST(GZ) [Boyan Li et al. '26]", "UNK", "74.49", "79.09", "DeepEyeSQL2026", "DeepEye 新版条目"),
    (9, "Jul 04, 2026", "MarkovSQL", "Anonymous", "UNK", "75.10", "78.70", None, "匿名"),
    (10, "Jul 10, 2026", "DeepEye-SQL (27B)", "HKUST(GZ)", "27B", "74.49", "78.42", "DeepEyeSQL2026", ""),
    (11, "Jul 11, 2026", "Spektr-SQL", "Amazon Ads - SpektrBot", "UNK", "73.09", "78.31", None, "无公开论文"),
    (12, "Jun 09, 2026", "DataGallery-Text2SQL", "Huawei 2012 Labs", "UNK", "74.64", "77.53", None, "本论文系统（早期提交）"),
    (13, "Jul 14, 2025", "LongData-SQL", "LongShine AI Research", "UNK", "74.32", "77.53", None, "无公开论文"),
    (14, "Aug 03, 2026", "AxisSQL", "UST", "31B", "", "76.86", None, "无公开论文"),
    (15, "Jul 07, 2026", "GT-ChatBI-SQL", "MR Tech", "UNK", "75.95", "76.80", None, "无公开论文"),
    (16, "Jan 02, 2026", "Zhiwen-Lingsi-Agent", "China Telecom, TeleAI", "UNK", "73.53", "76.63", None, "无公开论文"),
    (17, "Jan 26, 2026", "DeepEye-SQL", "HKUST(GZ)", "UNK", "73.53", "76.58", "DeepEyeSQL2026", ""),
    (18, "Dec 4, 2025", "Q-SQL", "AWS-Quick Science", "30B-3B-MoE", "72.99", "76.47", None, "无公开论文"),
    (19, "Feb 6, 2026", "MIC2-SQL", "Anonymous", "UNK", "74.45", "76.41", None, "匿名"),
    (20, "Jul 14, 2026", "DataSpace-Text2SQL", "Institute of Dataspace, Hefei", "UNK", "", "76.36", None, "无公开论文"),
    (21, "Apr 16, 2025", "CHASE-SQL + Gemini", "Google Cloud", "UNK", "74.90", "76.02", "CHASESQL2025", ""),
    (22, "Apr 3, 2026", "xiaoyi-text-to-sql", "wenyuai", "UNK", "72.75", "75.96", None, "无公开论文"),
    (23, "Feb 21, 2026", "RED-SQL", "South China Normal University", "30B", "74.19", "75.91", None, "无公开论文"),
    (24, "Sep 22, 2025", "JoyDataAgent-SQL", "JD:CHO-JDT-JDL", "UNK", "74.25", "75.85", None, "无公开论文"),
    (25, "Oct 23, 2025", "Sinovatio-SQL", "Sinovatio AI Lab", "UNK", "73.72", "75.80", None, "无公开论文"),
    (26, "May 30, 2025", "TCDataAgent-SQL", "Tencent Cloud", "UNK", "74.12", "75.74", None, "无公开论文"),
    (27, "Feb 27, 2025", "Contextual-SQL", "Contextual AI", "UNK", "73.50", "75.63", None, "无公开论文"),
    (28, "Dec 17, 2024", "XiYan-SQL", "Alibaba Cloud", "UNK", "73.34", "75.63", "XiYanSQL2025", ""),
    (29, "Sep 1, 2025", "DB-SQL", "Anonymous", "UNK", "73.66", "75.35", None, "匿名"),
    (30, "May 30, 2025", "CYAN-SQL", "Tencent Cloud / Fudan University", "UNK", "73.47", "75.35", "CYANSQL2026", "对应 ICDE 2026 CYANSQL 论文"),
]


def write_leaderboard(rows) -> str:
    lines = [
        "---",
        "type: benchmark",
        "benchmark: BIRD",
        "---",
        "",
        "# BIRD Leaderboard Top 30 (EX, test)",
        "",
        "2026-09-08 抓取自 bird-bench.github.io 总榜（Execution Accuracy, test set）。",
        "有论文的条目链到 `01 Papers/` 笔记；无论文的工业/匿名系统只留表，不建笔记（spec 约定）。",
        "",
        "| # | 日期 | 系统 | 团队 | Size | Dev | Test | 笔记 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for rank, date, system, org, size, dev, test, ck, note in rows:
        link = f"[[{ck}]]" if ck else (note or "—")
        if ck and note:
            link = f"[[{ck}]]（{note}）"
        lines.append(f"| {rank} | {date} | {system} | {org} | {size} | {dev} | {test} | {link} |")
    lines += [
        "",
        "## 观察",
        "",
        "- Top 30 全部使用 oracle knowledge（evidence 列全勾），说明 evidence 利用已是上榜门槛。",
        "- 前排（82+）与第 20 名差距约 6 个点，头部系统差距在 1 个点以内，评测噪声不可忽略（见 [[AnnotationErrors2026]]）。",
        "- 有公开论文的系统集中在 2024 底–2025（XiYan-SQL、CHASE-SQL、DeepEye-SQL），2026 前排多为无论文的工业提交。",
        "- 单模型 track 另有 Arctic-Text2SQL-R1（[[ArcticText2SQLR12025]]）等 RL 训练模型，与流水线路线对照。",
        "",
    ]
    return "\n".join(lines)


def merge_papers(handbook, crossref) -> list[dict]:
    by_title = {}
    for p in handbook + crossref:
        key = title_key(p["title"])
        if key not in by_title:
            by_title[key] = p
        else:
            cur = by_title[key]
            # prefer the cleaner (usually Crossref) title when the merge key
            # only matched because of a handbook typo
            if "subseing" in cur["title"].lower() and "subseing" not in p["title"].lower():
                cur["title"] = p["title"]
            if not cur.get("authors") and p.get("authors"):
                cur["authors"] = p["authors"]
            if not cur.get("doi") and p.get("doi"):
                cur["doi"] = p["doi"]
            if not cur.get("arxiv") and p.get("arxiv"):
                cur["arxiv"] = p["arxiv"]
    return list(by_title.values())


def apply_core(papers: list[dict]) -> None:
    for p in papers:
        t = p["title"].lower()
        for needle, note in CORE_NOTES.items():
            if needle in t:
                p["citekey"] = note.get("citekey", p.get("citekey"))
                if note.get("authors"):
                    p["authors"] = note["authors"]
                p["themes"] = note.get("themes", p["themes"])
                p["benchmarks"] = note.get("benchmarks", [])
                p["problem"] = note["problem"]
                p["method"] = note["method"]
                p["relation"] = note["relation"]
                p["status"] = "reviewed"
                break


# Entries that pass the venue filter but are out of the spec scope
# (PL/SQL dialect generation, SQL-to-SQL translation, generic tutorials, ...).
DROP_TITLES = [
    re.compile(r"procedural extensions of sql", re.I),  # PLForge: PL/SQL generation, not NL2SQL
]


def drop_out_of_scope(papers: list[dict]) -> list[dict]:
    kept = []
    for p in papers:
        if p["source"] == "curated":
            kept.append(p)
            continue
        if any(pat.search(p["title"]) for pat in DROP_TITLES):
            continue
        kept.append(p)
    return kept


def ensure_citekeys(papers: list[dict]) -> None:
    used = set()
    for p in papers:
        ck = p.get("citekey") or slug_citekey(p["title"], p["year"])
        ck = re.sub(r"[^A-Za-z0-9]", "", ck) or "Paper"
        base = ck
        i = 2
        while ck.lower() in used:
            ck = f"{base}v{i}"
            i += 1
        p["citekey"] = ck
        used.add(ck.lower())


SEED_EXTRA = [
    {
        "citekey": "BIRD2023",
        "title": "Can LLM Already Serve as A Database Interface? A BIg Bench for Large-Scale Database Grounded Text-to-SQLs",
        "year": 2023,
        "venue": "NeurIPS",
        "venue_class": "ML",
        "era": "llm",
        "authors": ["Jinyang Li", "Binyuan Hui", "Ge Qu", "Jiaxi Yang", "Binhua Li", "Bowen Li", "Bailin Wang", "Bowen Qin", "Rongyu Cao", "Ruiying Geng", "Nan Huo", "Xuanhe Zhou", "Chenhao Ma", "Guoliang Li", "Kevin C. C. Chang", "Fei Huang", "Reynold Cheng", "Yongbin Li"],
        "arxiv": "2305.03111",
        "why": "BIRD benchmark; NeurIPS 2023 Datasets and Benchmarks",
        "themes": ["benchmark"],
        "benchmarks": ["BIRD"],
        "problem": "Spider 上的高分无法迁移到更大、更脏、需要外部知识的真实数据库。",
        "method": "发布 BIRD：95 库、外键脏 schema、evidence，并引入执行准确率与 VES。",
        "relation": "我们的主评测场。related work 的问题设定段从这里起笔。",
        "found_via": "venue",
    },
    {
        "citekey": "LinkAlign2025",
        "title": "LinkAlign: Scalable Schema Linking for Real-World Large-Scale Multi-Database Text-to-SQL",
        "year": 2025,
        "venue": "EMNLP",
        "venue_class": "NLP",
        "era": "llm",
        "authors": ["Yihan Wang", "Peiyu Liu", "Xin Yang"],
        "arxiv": "2503.18596",
        "why": "EMNLP 2025 schema linking; Spider 2.0-Lite SOTA lineage",
        "themes": ["schema-linking"],
        "benchmarks": ["Spider2", "BIRD", "Spider"],
        "problem": "真实多库、超大 schema 下 database retrieval 和 item grounding 都失败。",
        "method": "多轮语义检索 + 无关库隔离 + schema extraction，Agent/Pipeline 双模式。",
        "relation": "大规模 schema linking 的新 SOTA 叙事，尤其 Spider 2.0-Lite。",
        "found_via": "venue",
    },
]


def add_curated(papers: list[dict], rows: list[dict], era_default: str, found_via: str) -> None:
    existing = {title_key(p["title"]): p for p in papers}
    for row in rows:
        if title_key(row["title"]) in existing:
            p = existing[title_key(row["title"])]
            p["problem"] = row.get("problem", p.get("problem"))
            p["method"] = row.get("method", p.get("method"))
            p["relation"] = row.get("relation", p.get("relation"))
            if row.get("citekey"):
                p["citekey"] = row["citekey"]
            if row.get("authors") and not p.get("authors"):
                p["authors"] = row["authors"]
            if row.get("arxiv") and not p.get("arxiv"):
                p["arxiv"] = row["arxiv"]
            p["themes"] = row.get("themes", p["themes"])
            p["benchmarks"] = row.get("benchmarks", p.get("benchmarks", []))
            p["cited_by"] = row.get("cited_by_hint", p.get("cited_by", []))
            p["status"] = "reviewed"
            continue
        p = {
            "citekey": row.get("citekey"),
            "title": row["title"],
            "year": row["year"],
            "venue": row["venue"],
            "venue_class": row["venue_class"],
            "era": row.get("era", era_default),
            "found_via": found_via,
            "doi": row.get("doi", ""),
            "arxiv": row.get("arxiv", ""),
            "url": f"https://arxiv.org/abs/{row['arxiv']}" if row.get("arxiv") else "",
            "why": row["why"],
            "source": "curated",
            "authors": row.get("authors", []),
            "cited_by": row.get("cited_by_hint", []),
            "status": "reviewed",
            "themes": row.get("themes", ["pre-llm"]),
            "benchmarks": row.get("benchmarks", []),
            "problem": row["problem"],
            "method": row["method"],
            "relation": row["relation"],
        }
        papers.append(p)


def default_notes(p: dict) -> None:
    if p.get("problem"):
        return
    title = p["title"]
    p["problem"] = f"围绕 Text-to-SQL / NL2SQL 的具体问题，见论文题目：{title}。"
    p["method"] = "方法细节待精读；当前按标题与会议归入对应 theme。"
    p["relation"] = "入口论文，写作 related work 前需精读后改这一段。"
    p["status"] = "drafted"


def yaml_list(vals) -> str:
    if not vals:
        return "[]"
    return "[" + ", ".join(json.dumps(v, ensure_ascii=False) for v in vals) + "]"


def dump_paper(p: dict) -> str:
    citekey = re.sub(r"[^A-Za-z0-9_+\-]", "", p["citekey"]) or "Paper"
    p["citekey"] = citekey
    authors = p.get("authors") or []
    if authors:
        authors_yaml = "\n".join(f'  - "{a}"' for a in authors)
    else:
        authors_yaml = "  []"
    cited = p.get("cited_by") or []
    return f"""---
type: paper
title: {json.dumps(p["title"], ensure_ascii=False)}
authors:
{authors_yaml}
year: {p["year"]}
venue: {json.dumps(p["venue"], ensure_ascii=False)}
venue_class: {p["venue_class"]}
era: {p["era"]}
found_via: {p["found_via"]}
themes: {yaml_list(p.get("themes") or [])}
benchmarks: {yaml_list(p.get("benchmarks") or [])}
doi: {json.dumps(p.get("doi") or "")}
arxiv: {json.dumps(p.get("arxiv") or "")}
cited_by: {yaml_list(cited)}
status: {p.get("status", "drafted")}
citekey: {p["citekey"]}
---

## 问题

{p["problem"]}

## 方法

{p["method"]}

## 对我们的关系

{p["relation"]}
"""


THEME_PAGES = [
    (
        "Prompting and Decomposition",
        "prompting",
        "LLM 时代第一波主力：把 Text-to-SQL 拆成 schema linking、分类、生成、自校正等子任务，或用示范选择改善 in-context learning。DIN-SQL、DAIL-SQL、C3、ACT-SQL、ODIS、MCS-SQL 是这条线的骨架。",
    ),
    (
        "Multi-agent and Workflow",
        "multi-agent",
        "把分解从 prompt 升级成角色：生成、选择、修复、检索各由一个 agent 负责。MAC-SQL 定了 Selector/Decomposer/Refiner 原型，CHASE-SQL 把多路径推理和偏好选择做成测试时扩展，DeepEye-SQL 进一步工程化。",
    ),
    (
        "Schema Linking and Retrieval",
        "schema-linking",
        "从 RAT-SQL 的显式 linking，到 LLM 时代的检索、问题改写、长上下文「还要不要 linking」之争。BIRD / Spider 2.0 的大 schema 让这个问题重新成为系统瓶颈。",
    ),
    (
        "Execution Feedback and Repair",
        "execution",
        "PICARD 把约束放进解码；DIN-SQL / PET-SQL / SafeQL / Alpha-SQL 把执行结果或 DBMS 报错变成修正信号。BIRD 上很多分数来自修，而不是一次生成。",
    ),
    (
        "Fine-tuning and Open Models",
        "finetuning",
        "CodeS、SENSE、OmniSQL 用合成数据训开源模型；STaR-SQL、SQL-R1、ROUTE 把推理轨迹和 RL 引进来。这条线和闭源 agent 流水线是 related work 里最需要站队的分叉。",
    ),
    (
        "Benchmarks and Evaluation",
        "benchmark",
        "Spider 定义跨域，BIRD 定义脏库+知识，Spider 2.0 定义企业工作流。NL2SQL360 和标注噪声论文提醒：EX 不是全部，榜也不是干净的。",
    ),
    (
        "Systems and Industrial NL2SQL",
        "systems",
        "DB 会议特有的一段：成本、延迟、方言、金融/企业部署、交互澄清、长上下文能否省掉检索。FinSQL、OpenSearch-SQL、Sphinteract、长上下文实验属于这里。",
    ),
    (
        "Pre-LLM Neural NL2SQL",
        "pre-llm",
        "WikiSQL → Spider → RAT-SQL / PICARD / 图编码器。LLM 论文 related work 通常压缩成半页，但这些是 schema linking、约束解码、复杂 SQL 结构的源头。",
    ),
]


def write_theme(name: str, theme: str, blurb: str, papers: list[dict]) -> str:
    rows = [p for p in papers if theme in (p.get("themes") or [])]
    rows.sort(key=lambda x: (-x["year"], x["title"]))
    links = "\n".join(f"- [[{p['citekey']}|{p['title']}]] ({p['year']}, {p['venue']})" for p in rows)
    return f"""---
type: theme
theme: {theme}
---

# {name}

{blurb}

## 论文

{links or "（暂无）"}
"""


def write_benchmark(name: str, key: str, blurb: str, papers: list[dict]) -> str:
    rows = [p for p in papers if key in (p.get("benchmarks") or []) or key.lower() in p["title"].lower()]
    rows.sort(key=lambda x: (-x["year"], x["title"]))
    links = "\n".join(f"- [[{p['citekey']}|{p['title']}]] ({p['year']})" for p in rows)
    return f"""---
type: benchmark
benchmark: {key}
---

# {name}

{blurb}

## 相关论文

{links or "（暂无）"}
"""


def index_by(papers, keyfn, title: str) -> str:
    groups = defaultdict(list)
    for p in papers:
        groups[keyfn(p)].append(p)
    parts = [f"# {title}", ""]
    for g in sorted(groups, key=lambda x: str(x), reverse=isinstance(next(iter(groups), None), int)):
        parts.append(f"## {g}")
        parts.append("")
        for p in sorted(groups[g], key=lambda x: x["title"]):
            parts.append(f"- [[{p['citekey']}|{p['title']}]] ({p['year']}, {p['venue']})")
        parts.append("")
    return "\n".join(parts)


def main() -> None:
    handbook = parse_handbook(SOURCES / "handbook.md")
    crossref = parse_crossref(SOURCES / "crossref_raw" / "all_items.json")
    papers = drop_out_of_scope(merge_papers(handbook, crossref))
    add_curated(papers, SEED_EXTRA, "llm", "venue")
    apply_core(papers)
    add_curated(papers, CLASSICS, "classic", "citation")
    add_curated(papers, KEY_CITATIONS, "llm", "citation")
    add_curated(papers, LEADERBOARD_PAPERS, "llm", "leaderboard")
    for p in papers:
        p["venue"] = normalize_venue(p["venue"])
    # mark era for classics overlay
    classic_titles = {title_key(c["title"]) for c in CLASSICS}
    for p in papers:
        if title_key(p["title"]) in classic_titles:
            p["era"] = "classic"
            p["found_via"] = "citation"
            if "pre-llm" not in p["themes"]:
                p["themes"] = ["pre-llm"] + list(p["themes"])
        default_notes(p)
    ensure_citekeys(papers)
    papers.sort(key=lambda x: (x["era"] != "classic", -x["year"], x["title"]))

    paper_dir = VAULT / "01 Papers"
    paper_dir.mkdir(parents=True, exist_ok=True)
    for old in paper_dir.glob("*.md"):
        old.unlink()
    for p in papers:
        (paper_dir / f"{p['citekey']}.md").write_text(dump_paper(p), encoding="utf-8")

    theme_dir = VAULT / "02 Themes"
    theme_dir.mkdir(parents=True, exist_ok=True)
    for name, theme, blurb in THEME_PAGES:
        (theme_dir / f"{name}.md").write_text(write_theme(name, theme, blurb, papers), encoding="utf-8")

    bench_dir = VAULT / "03 Benchmarks"
    bench_dir.mkdir(parents=True, exist_ok=True)
    benches = [
        ("WikiSQL", "WikiSQL", "2017 单表填槽基准，Seq2SQL 同期发布。LLM 论文里通常只作为历史起点。"),
        ("Spider", "Spider", "2018 跨域复杂 SQL 标准榜。几乎所有方法仍会报 Spider；它定义了「跨库泛化」这个问题。"),
        ("BIRD", "BIRD", "2023 大规模脏 schema + 外部知识。我们的主榜。VES 和 evidence 是它相对 Spider 的真正增量。"),
        ("Spider 2.0", "Spider2", "2025 企业工作流评测。如果 related work 只写 BIRD，审稿人可能会问生产差距。"),
    ]
    for name, key, blurb in benches:
        (bench_dir / f"{name}.md").write_text(write_benchmark(name, key, blurb, papers), encoding="utf-8")
    (bench_dir / "BIRD Leaderboard.md").write_text(write_leaderboard(BIRD_TOP30), encoding="utf-8")

    idx = VAULT / "00 Index"
    idx.mkdir(parents=True, exist_ok=True)
    venue_hits = [p for p in papers if p["found_via"] == "venue"]
    classics = [p for p in papers if p["era"] == "classic"]
    extra_cites = [p for p in papers if p["found_via"] == "citation" and p["era"] != "classic"]
    lb_papers = [p for p in papers if p["found_via"] == "leaderboard"]
    drafted = [p for p in papers if p.get("status") == "drafted"]

    (idx / "Home.md").write_text(
        f"""---
type: meta
---

# NL2SQL Related Work Vault

为 BIRD top-1 论文准备的 related-work 库。Obsidian 打开本 `vault/` 目录。

## 规模

- 论文笔记：{len(papers)}
- 按会议检索（2023+ 目标会议）：{len(venue_hits)}
- 经典工作（前 LLM / 源头，从 related work 抽出）：{len(classics)}
- 关键引用（不在目标会议、但被反复点名）：{len(extra_cites)}
- BIRD 榜单系统（top 30 中有公开论文的）：{len(lb_papers)}
- 待精读：{len(drafted)}

## 入口

- 章节骨架：[[Related Work]]
- 主题：[[Prompting and Decomposition]] · [[Multi-agent and Workflow]] · [[Schema Linking and Retrieval]] · [[Execution Feedback and Repair]] · [[Fine-tuning and Open Models]] · [[Benchmarks and Evaluation]] · [[Systems and Industrial NL2SQL]] · [[Pre-LLM Neural NL2SQL]]
- 基准：[[WikiSQL]] · [[Spider]] · [[BIRD]] · [[Spider 2.0]] · [[BIRD Leaderboard]]
- 索引：[[By Venue]] · [[By Year]] · [[By Theme]] · [[Classics]] · [[Reading Queue]]

## 怎么用

写 related work 时先打开 [[Related Work]]，按八段往下填。每段已链到主题页和代表论文。`status: drafted` 的笔记只有标题级摘要，精读后改「对我们的关系」。

`found_via`：`venue` = 按会议检索收录；`citation` = 从 related work / baseline 里抽出的关键引用；`leaderboard` = BIRD 榜 top 30 里有公开论文的系统。

```dataview
TABLE year, venue, era, found_via, status
FROM "01 Papers"
SORT year DESC
```
""",
        encoding="utf-8",
    )
    (idx / "By Venue.md").write_text(index_by(papers, lambda p: p["venue"], "By Venue"), encoding="utf-8")
    (idx / "By Year.md").write_text(index_by(papers, lambda p: p["year"], "By Year"), encoding="utf-8")
    (idx / "By Theme.md").write_text(
        index_by(papers, lambda p: ", ".join(p.get("themes") or ["untagged"]), "By Theme"),
        encoding="utf-8",
    )

    classic_lines = ["# Classics", "", "入口论文 related work / baseline 里反复出现的源头工作。", ""]
    for p in sorted(classics, key=lambda x: x["year"]):
        cited = ", ".join(f"[[{c}]]" for c in (p.get("cited_by") or [])[:8]) or "（见正文）"
        classic_lines.append(f"- [[{p['citekey']}|{p['title']}]] ({p['year']}, {p['venue']}) — {p['why']}")
        classic_lines.append(f"  - cited by: {cited}")
    (idx / "Classics.md").write_text("\n".join(classic_lines) + "\n", encoding="utf-8")

    rq = ["# Reading Queue", "", "缺作者、只有标题级摘要、或 venue 需要复核的条目。", ""]
    for p in drafted:
        rq.append(f"- [[{p['citekey']}|{p['title']}]] ({p['year']}, {p['venue']}) `{p['why']}`")
    if extra_cites:
        rq += ["", "## 关键引用（不在目标会议，但 related work 里反复出现）", ""]
        for p in extra_cites:
            rq.append(f"- [[{p['citekey']}|{p['title']}]] ({p['year']}, {p['venue']})")
    (idx / "Reading Queue.md").write_text("\n".join(rq) + "\n", encoding="utf-8")

    outline = VAULT / "04 Outline"
    outline.mkdir(parents=True, exist_ok=True)
    (outline / "Related Work.md").write_text(
        """---
type: outline
---

# Related Work

按论文章节骨架写。方括号里是主题页，加粗是建议点名的代表工作。

## 0. 前 LLM 一代

跨域 Text-to-SQL 从 [[WikiSQL]] 的单表填槽走到 [[Spider]] 的多表复杂 SQL。编码器以 [[RATSQL2020|RAT-SQL]] 的 schema linking 和图结构为主，解码侧则以 [[SyntaxSQLNet2018|SyntaxSQLNet]]、[[IRNet2019|IRNet]] 的中间表示、以及 [[PICARD2021|PICARD]] 的约束解码收束。完整名单见 [[Pre-LLM Neural NL2SQL]] 与 [[Classics]]。

我们只把这一段当问题史：结构先验、schema 对齐、可执行性约束，后面 LLM 方法都在重做这三件事。

## 1. Prompting 与任务分解

[[DINSQL2023|DIN-SQL]] 把生成拆成 linking / 分类 / SQL / 自校正；[[DAILSQL2024|DAIL-SQL]] 系统化 example selection；[[C32023|C3]] 展示零样本 ChatGPT 流水线。更多见 [[Prompting and Decomposition]]。

对 BIRD top-1 的含义：单纯分解 prompt 已经不是差异化来源，差异在分解之后的检索、选候选和修复。

## 2. 多智能体与工作流

[[MACSQL2025|MAC-SQL]] 给出生成—选择—修复的角色原型；[[CHASESQL2025|CHASE-SQL]] 用多路径推理和偏好选择打上 BIRD 前列；[[DeepEyeSQL2026|DeepEye-SQL]] 把软件工程阶段门控引进来。见 [[Multi-agent and Workflow]]。

我们需要写清：自己的 agent 角色是否只是 MAC-SQL 换皮，还是在候选生成或选择上有新机制。

## 3. Schema linking 与检索

RAT-SQL 把 linking 做成显式模块。LLM 时代出现两条对立叙事：[[DeathOfSchemaLinking2024|Death of Schema Linking]] / [[LongContextNL2SQL2025|长上下文是否足够]]，以及 [[CHESS2024|CHESS]]、[[ESQL2024|E-SQL]]、[[LinkAlign2025|LinkAlign]]、[[DIVER2026|DIVER]] 证明大 schema 和 value grounding 仍然要检索。见 [[Schema Linking and Retrieval]]。

BIRD 的 evidence 和脏列名让我们更接近后一条：linking 没有死，它变成了检索和值接地。

## 4. 执行反馈与修复

从 PICARD 的解码约束，到 DIN-SQL 自校正、[[PETSQL2024|PET-SQL]] 的 cross-consistency、[[SafeQL2026|SafeQL]] 把 DBMS 变成主动搜索指导、[[AlphaSQL2025|Alpha-SQL]] 的 MCTS。见 [[Execution Feedback and Repair]]。

报 BIRD 分数时要交代：多少来自一次生成，多少来自修。

## 5. 微调与开源模型

[[CodeS2024|CodeS]]、[[SENSE2024|SENSE]]、[[OmniSQL2025|OmniSQL]] 走数据合成 + SFT；[[STaRSQL2025|STaR-SQL]]、[[SQLR12025|SQL-R1]]、[[ROUTE2025|ROUTE]] 走推理轨迹和 RL。见 [[Fine-tuning and Open Models]]。

若我们的系统是闭源 LLM agent，这一段用来说明开源模型已经能追到哪里，避免被审稿人认为忽略了可复现基线。

## 6. 基准与评测

[[BIRD2023|BIRD]] 是主场；[[Spider2018|Spider]] 是历史主榜；[[Spider22025|Spider 2.0]] 是企业工作流；[[NL2SQL3602024|NL2SQL360]] 提醒细粒度指标；[[AnnotationErrors2026|标注噪声]] 提醒榜本身不可全信。见 [[Benchmarks and Evaluation]]。当前榜单 top 30 与论文对应关系见 [[BIRD Leaderboard]]。

## 7. 系统与工业

成本、方言、金融/企业部署、交互澄清：[[FinSQL2024|FinSQL]]、[[OpenSearchSQL2025|OpenSearch-SQL]]、[[Sphinteract2025|Sphinteract]]。见 [[Systems and Industrial NL2SQL]]。

如果论文贡献偏榜上准确率，这一段写短，但不要零引用，否则 DB 审稿人会觉得这是一篇 NLP 投稿。
""",
        encoding="utf-8",
    )

    # sources tables
    def table(rows: list[dict], cols: list[str]) -> str:
        header = "| " + " | ".join(cols) + " |"
        sep = "| " + " | ".join("---" for _ in cols) + " |"
        body = []
        for r in rows:
            body.append("| " + " | ".join(str(r.get(c, "")).replace("|", "\\|")[:80] for c in cols) + " |")
        return "\n".join([header, sep, *body])

    (SOURCES / "entry-papers.md").write_text(
        "# Entry papers\n\n"
        + table(
            [p for p in papers if p["found_via"] == "venue"],
            ["citekey", "title", "year", "venue", "why"],
        )
        + "\n",
        encoding="utf-8",
    )
    (SOURCES / "classics.md").write_text(
        "# Classic works\n\n"
        + table(classics, ["citekey", "title", "year", "venue", "why"])
        + "\n",
        encoding="utf-8",
    )
    (SOURCES / "query-log.md").write_text(
        """# Query log

## DBLP

DBLP API 被 Anubis bot wall 挡住（返回 HTML challenge），未采用。

## Crossref

按 venue container-title 粗查 `text-to-sql` / `nl2sql`，年份 2023–2026。原始命中见 `sources/crossref_raw/log.txt`。入库过滤：标题含 NL2SQL 关键词，且 container 仅限 PVLDB、PACMMOD、ICDE 主会、CIDR、TODS、VLDBJ、SIGMOD Companion。NLP/ML 会场不以 Crossref 为准。

## Handbook

主入口：HKUSTDial/NL2SQL_Handbook 会标。只收 SIGMOD / VLDB / ICDE / CIDR / TODS / VLDBJ / ACL / EMNLP / NAACL / NeurIPS / ICLR / ICML（含 Findings / Workshop / Industry / Companion）。

Crossref 只用来补 DB 会场（PVLDB / PACMMOD / ICDE / CIDR / TODS / VLDBJ / SIGMOD Companion），避免 container 误伤把非目标会议标成 ACL。BIRD（NeurIPS 2023）与 LinkAlign（EMNLP 2025）在 handbook 列表里缺失，已手工补为入口论文。

## 关键引用

经典工作按 spec 三类规则手工收录。不在目标会议、但被反复点名的方法（C3、MAC-SQL、CHESS、PET-SQL、E-SQL、MCS-SQL、Death of Schema Linking、RESDSQL、Graphix-T5）记为 `found_via: citation`。

## BIRD 榜单

2026-09-08 抓 bird-bench.github.io 总榜 top 30（EX, test），存于 `vault/03 Benchmarks/BIRD Leaderboard.md`。有公开论文的系统建笔记（`found_via: leaderboard`）：XiYan-SQL、Agentar-Scale-SQL、Reasoning-SQL、CSC-SQL、Arctic-Text2SQL-R1、TA-SQL、AskData（元数据抽取）。无论文的工业/匿名系统只留表。TA-SQL 同时补上 ACL 2024 Findings 的会场缺口。
""",
        encoding="utf-8",
    )
    catalog = [{k: p[k] for k in p if k not in {"problem", "method", "relation"}} | {"has_notes": bool(p.get("problem"))} for p in papers]
    (SOURCES / "catalog.json").write_text(json.dumps(papers, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"papers={len(papers)} venue={len(venue_hits)} classic={len(classics)} citation={len(extra_cites)} drafted={len(drafted)}")


if __name__ == "__main__":
    main()
