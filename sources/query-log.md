# Query log

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
