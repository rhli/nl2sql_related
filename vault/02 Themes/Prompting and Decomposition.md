---
type: theme
theme: prompting
---

# Prompting and Decomposition

LLM 时代第一波主力：把 Text-to-SQL 拆成 schema linking、分类、生成、自校正等子任务，或用示范选择改善 in-context learning。DIN-SQL、DAIL-SQL、C3、ACT-SQL、ODIS、MCS-SQL 是这条线的骨架。

## 论文

- [[AmbiSqlInteractiveAmbiguity2026|Ambi SQL: Interactive Ambiguity Detection and Resolution for Text-to-SQL]] (2026, SIGMOD Companion)
- [[BridgingNl2SqlCanSignal2026|Bridging NL2SQL for CAN Signal Analytics at NIO: From Externalized Schemas to CTE Pipelines]] (2026, VLDB)
- [[CYANSQL2026|CYANSQL: Unlock the Power of NL2SQL via Clustering-based Test-Time Scaling]] (2026, ICDE)
- [[LEAFSQL2026|LEAF-SQL: Level-wise Exploration with Adaptive Fine-graining for Text-to-SQL Skeleton Prediction]] (2026, ICDE)
- [[ReliableAnswersRecurringQuestions2026|Reliable Answers for Recurring Questions: Boosting Text-to-SQL Accuracy with Template-Constrained Decoding]] (2026, SIGMOD)
- [[Text2SQL2026v2|Text2SQL-Flow: A Robust SQL-Aware Data Augmentation Framework for Text-to-SQL]] (2026, ICDE)
- [[AIDSQL2025|AID-SQL: Adaptive In-Context Learning of Text-to-SQL with Difficulty-Aware Instruction and Retrieval-Augmented Generation]] (2025, ICDE)
- [[AreYourLlmBased2025|Are Your LLM-based Text-to-SQL Models Secure? Exploring SQL Injection via Backdoor Attacks]] (2025, SIGMOD)
- [[CHASESQL2025|CHASE-SQL: Multi-Path Reasoning and Preference Optimized Candidate Selection in Text-to-SQL]] (2025, ICLR)
- [[ClearParserIndependentDisambiguation2025|CLEAR: A Parser-Independent Disambiguation Framework for NL2SQL]] (2025, ICDE)
- [[DCGSQL2025|DCG-SQL: Enhancing In-Context Learning for Text-to-SQL with Deep Contextual Schema Link Graph]] (2025, ACL)
- [[EvoschemaTowardsTextSql2025|EVOSCHEMA: TOWARDS TEXT-TO-SQL ROBUSTNESS AGAINST SCHEMA EVOLUTION]] (2025, VLDB)
- [[GroundingNaturalLanguageSql2025|Grounding Natural Language to SQL Translation with Data-Based Self-Explanations]] (2025, ICDE)
- [[KnowledgeBaseConstructionKnowledge2025|Knowledge Base Construction for Knowledge-Augmented Text-to-SQL]] (2025, ACL Findings)
- [[OpenSearchSQL2025|OpenSearch-SQL: Enhancing Text-to-SQL with Dynamic Few-shot and Consistency Alignment]] (2025, SIGMOD)
- [[PARSQL2025|PARSQL: Enhancing Text-to-SQL through SQL Parsing and Reasoning]] (2025, ACL Findings)
- [[RtsReliableTextSql2025|RTS+: Reliable Text to SQL]] (2025, SIGMOD Companion)
- [[ShareSlmBasedHierarchical2025|SHARE: An SLM-based Hierarchical Action CorREction Assistant for Text-to-SQL]] (2025, ACL)
- [[SnailsSchemaNamingAssessments2025|SNAILS: Schema Naming Assessments for Improved LLM-Based SQL Inference]] (2025, SIGMOD)
- [[SqlongEnhancedNl2SqlLonger2025|SQLong: Enhanced NL2SQL for Longer Contexts with LLMs]] (2025, ACL Workshop)
- [[StructureGuidedLargeLanguage2025|Structure-Guided Large Language Models for Text-to-SQL Generation]] (2025, ICML)
- [[PowerConstraintsNaturalLanguage2025|The Power of Constraints in Natural Language to SQL Translation]] (2025, VLDB)
- [[UCSSQL2025|UCS-SQL: Uniting Content and Structure for Enhanced Semantic Bridging In Text-to-SQL]] (2025, ACL Findings)
- [[UncoveringImpactChainThought2025|Uncovering the Impact of Chain-of-Thought Reasoning for Direct Preference Optimization: Lessons from Text-to-SQL]] (2025, ACL)
- [[XiYanSQL2025|XiYan-SQL: A Novel Multi-Generator Framework For Text-to-SQL]] (2025, arXiv)
- [[TASQL2024|Before Generation, Align it! A Novel and Effective Strategy for Mitigating Hallucinations in Text-to-SQL Generation]] (2024, ACL Findings)
- [[CombiningSmallLanguageModels2024|Combining Small Language Models and Large Language Models for Zero-Shot NL2SQL]] (2024, VLDB)
- [[DataCentricTextSql2024|Data-Centric Text-to-SQL with Large Language Models]] (2024, NeurIPS Workshop)
- [[InterleavingPreTrainedLanguage2024|Interleaving Pre-Trained Language Models and Large Language Models for Zero-Shot NL2SQL Generation]] (2024, VLDB)
- [[MCSSQL2024|MCS-SQL: Leveraging Multiple Prompts and Multiple-Choice Selection for Text-to-SQL Generation]] (2024, COLING)
- [[MetaSQL2024|METASQL: A Generate-then-Rank Framework for Natural Language to SQL Translation]] (2024, ICDE)
- [[PETSQL2024|PET-SQL: A Prompt-Enhanced Two-Round Refinement of Text-to-SQL with Cross-consistency]] (2024, arXiv)
- [[PTDSQL2024|PTD-SQL: Partitioning and Targeted Drilling with LLMs in Text-to-SQL]] (2024, EMNLP)
- [[PURPLE2024|PURPLE: Making a Large Language Model a Better SQL Writer]] (2024, ICDE)
- [[DAILSQL2024|Text-to-SQL Empowered by Large Language Models: A Benchmark Evaluation]] (2024, VLDB)
- [[ACTSQL2023|ACT-SQL: In-Context Learning for Text-to-SQL with Automatically-Generated Chain-of-Thought]] (2023, EMNLP)
- [[C32023|C3: Zero-shot Text-to-SQL with ChatGPT]] (2023, arXiv)
- [[CatSQL2023|CatSQL: Towards Real World Natural Language to SQL Applications]] (2023, VLDB)
- [[DINSQL2023|DIN-SQL: Decomposed In-Context Learning of Text-to-SQL with Self-Correction]] (2023, NeurIPS)
- [[DataAmbiguityStrikesBack2023|Data Ambiguity Strikes Back: How Documentation Improves GPT's Text-to-SQL]] (2023, NeurIPS Workshop)
- [[FewShotTextSql2023|Few-shot Text-to-SQL Translation using Structure and Content Prompt Learning]] (2023, VLDB)
- [[G3RGraph2023|G 3 R: A Graph-Guided Generate-and-Rerank Framework for Complex and Cross-domain Text-to-SQL Generation]] (2023, ACL Findings)
- [[ImprovingGeneralizationLanguageModel2023|Improving Generalization in Language Model-based Text-to-SQL Semantic Parsing: Two Simple Semantic Boundary-based Techniques]] (2023, ACL)
- [[KnowWhatIDon2023|Know What I don’t Know: Handling Ambiguous and Unknown Questions for Text-to-SQL]] (2023, ACL Findings)
- [[ODIS2023|Selective Demonstrations for Cross-domain Text-to-SQL]] (2023, EMNLP)
