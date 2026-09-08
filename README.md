# NL2SQL Related Work Vault

为 BIRD NL2SQL 榜 top-1 论文准备的 related-work 资料库。收录 2023 年起 SIGMOD / VLDB / ICDE / CIDR / TODS / VLDBJ / ACL / EMNLP / NAACL / NeurIPS / ICLR / ICML 的 NL2SQL 论文、它们引用的前 LLM 经典工作、以及 BIRD 榜单 top 30 系统，按 related work 章节组织。

## 用 Obsidian 打开

1. 安装 [Obsidian](https://obsidian.md/download)。
2. 克隆本仓库：

   ```bash
   git clone git@github.com:rhli/nl2sql_related.git
   ```

3. 打开 Obsidian → **Open folder as vault** → 选择仓库里的 **`vault/`** 子目录（不是仓库根目录）。
4. 首次打开时 Obsidian 会提示是否信任作者 / 启用社区插件，选择信任并启用。Dataview 插件已随仓库自带（`vault/.obsidian/plugins/dataview`），启用后 `Home.md` 底部的论文总表才会渲染。
5. 从 **`vault/00 Index/Home.md`** 开始：它链到全部论文、八个主题页、benchmark 页和 related work 大纲。

## 目录结构

```
vault/               Obsidian vault（用 Obsidian 打开这个目录）
  00 Index/          Home、按会议/年份/主题索引、经典工作、待精读队列
  01 Papers/         一篇论文一张笔记（YAML frontmatter + 问题/方法/对我们的关系）
  02 Themes/         八个主题图，对应 related work 的八个小节
  03 Benchmarks/     WikiSQL / Spider / BIRD / Spider 2.0 / BIRD 榜单 top 30
  04 Outline/        Related Work.md 章节骨架，可直接改写成初稿
scripts/build_vault.py   从 sources/ 重新生成整个 vault
sources/             检索底稿：handbook、Crossref 原始数据、收录表、query log
docs/                设计 spec 与实施计划
```

## 论文笔记约定

每篇笔记的 YAML 里几个关键字段：

- `era`: `llm`（2023+）/ `classic`（前 LLM 经典）
- `found_via`: `venue`（按会议检索）/ `citation`（related work 关键引用）/ `leaderboard`（BIRD 榜 top 30 中有公开论文的系统）
- `status`: `reviewed`（已写实质三段）/ `drafted`（只有标题级摘要，待精读，见 `00 Index/Reading Queue.md`）

## 重新生成 vault

vault 全部由脚本生成，不要手改 `01 Papers/` 里的笔记（重跑会被覆盖）。要改内容就改 `scripts/build_vault.py` 里的 curated 数据，然后：

```bash
python3 scripts/build_vault.py
```

无第三方依赖，Python 3.10+ 即可。
