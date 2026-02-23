# Literature Review Plugin

一个用于深度文献综述的 Claude Code 插件，帮助你在多个学术数据库中进行文献调研并生成结构化综述。

## 功能特点

- **多数据库搜索**：支持 Semantic Scholar、OpenAlex、arXiv
- **智能聚合**：自动合并和去重搜索结果
- **主题分析**：识别核心论文和关键研究者
- **综述生成**：生成结构化的文献综述
- **可视化**：可生成知识图谱

## 安装方法

```bash
# 克隆仓库到你的插件目录
git clone https://github.com/xinyuanxing99/literature-review.git ~/.claude/plugins/literature-review
```

## 使用方法

1. 告诉我你想调研的主题，例如：
   - "帮我调研 AI 在医疗领域的应用"
   - "做一份关于量子计算的文献综述"

2. 指定时间范围（可选），例如：2020-2024

3. 指定关注点（可选），例如：算法进展、伦理问题

## Skill 列表

- **deep-literature-review**: 深度文献综述

## 项目结构

```
literature-review/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── deep-literature-review/
│       ├── SKILL.md
│       ├── scripts/           # 搜索和分析脚本
│       └── references/        # 参考文档
└── .gitignore
```

## 使用示例

```
# 搜索文献
python scripts/search_semantic_scholar.py "artificial intelligence" --year 2020-2024 --limit 50

# 聚合结果
python scripts/aggregate_results.py *.json --deduplicate --output merged.json

# 生成知识图谱
python scripts/generate_knowledge_graph.py merged.json --output graph.png
```

## 依赖

- Python 3.7+
- requests（用于 API 调用）

## 许可证

MIT License
