# Classics

入口论文 related work / baseline 里反复出现的源头工作。

- [[SQLNet2017|SQLNet: Generating Structured Queries From Natural Language Without Reinforcement Learning]] (2017, arXiv) — named founding sketch-based method
  - cited by: [[DINSQL2023]], [[CodeS2024]]
- [[Seq2SQL2017|Seq2SQL: Generating Structured Queries from Natural Language using Reinforcement Learning]] (2017, arXiv / WikiSQL) — founding neural generation + WikiSQL benchmark
  - cited by: [[DINSQL2023]], [[DAILSQL2024]], [[BIRD2023]]
- [[Spider2018|Spider: A Large-Scale Human-Labeled Dataset for Complex and Cross-Domain Semantic Parsing and Text-to-SQL Task]] (2018, EMNLP) — canonical cross-domain benchmark
  - cited by: [[BIRD2023]], [[DINSQL2023]], [[DAILSQL2024]], [[Spider22025]]
- [[SyntaxSQLNet2018|SyntaxSQLNet: Syntax Tree Networks for Complex and Cross-Domain Text-to-SQL Task]] (2018, EMNLP) — first complex Spider-era syntax-tree decoder
  - cited by: [[Spider2018]], [[IRNet2019]]
- [[TypeSQL2018|TypeSQL: Knowledge-based Type-Aware Neural Text-to-SQL Generation]] (2018, NAACL) — founding type-aware slot filling on WikiSQL
  - cited by: [[BIRD2023]]
- [[CoSQL2019|CoSQL: A Conversational Text-to-SQL Challenge Towards Cross-Domain Natural Language Interfaces to Databases]] (2019, EMNLP) — conversational NL2SQL benchmark
  - cited by: [[NL2SQL3602024]]
- [[SParC2019|SParC: Cross-Domain Semantic Parsing in Context]] (2019, ACL) — context-dependent benchmark sourced from Spider
  - cited by: [[NL2SQL3602024]]
- [[IRNet2019|Towards Complex Text-to-SQL in Cross-Domain Database with Intermediate Representation]] (2019, ACL) — IRNet; named SemQL intermediate generation
  - cited by: [[DINSQL2023]], [[RESDSQL2023]]
- [[BRIDGE2020|Bridging Textual and Tabular Data for Cross-Domain Text-to-SQL Semantic Parsing]] (2020, Findings of EMNLP) — BRIDGE; named BERT-era schema serialization baseline
  - cited by: [[BIRD2023]], [[DINSQL2023]]
- [[RATSQL2020|RAT-SQL: Relation-Aware Schema Encoding and Linking for Text-to-SQL Parsers]] (2020, ACL) — foundational schema linking encoder; cited as method heading
  - cited by: [[DINSQL2023]], [[CodeS2024]], [[LinkAlign2025]]
- [[KaggleDBQA2021|KaggleDBQA: Realistic Evaluation of Text-to-SQL Parsers]] (2021, ACL) — realistic small-domain benchmark
  - cited by: [[BIRD2023]], [[NL2SQL3602024]]
- [[LGESQL2021|LGESQL: Line Graph Enhanced Text-to-SQL Model with Mixed Local and Non-Local Relations]] (2021, ACL) — named line-graph schema encoder
  - cited by: [[BIRD2023]], [[DINSQL2023]]
- [[PICARD2021|PICARD: Parsing Incrementally for Constrained Auto-Regressive Decoding from Language Models]] (2021, EMNLP) — constrained decoding baseline repeatedly named
  - cited by: [[DINSQL2023]], [[DAILSQL2024]], [[CodeS2024]]
- [[SmBoP2021|SmBoP: Semi-autoregressive Bottom-up Semantic Parsing]] (2021, NAACL) — named bottom-up decoder baseline
  - cited by: [[DINSQL2023]]
- [[RASAT2022|RASAT: Integrating Relational Structures into Pretrained Seq2Seq Model for Text-to-SQL]] (2022, EMNLP) — named relation-aware T5 baseline
  - cited by: [[CodeS2024]], [[DAILSQL2024]]
- [[S2SQL2022|S2SQL: Injecting Syntax to Question-Schema Interaction Graph Encoder for Text-to-SQL Parsers]] (2022, Findings of ACL) — named syntax-augmented graph encoder
  - cited by: [[BIRD2023]]
