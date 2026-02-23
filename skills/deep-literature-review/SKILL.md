---
name: Deep Literature Review
description: This skill should be used when the user asks to "do a literature review", "research a topic", "write a literature survey", "review academic papers", "survey literature on", "find research on", "explore academic sources", "conduct a comprehensive literature search", or needs to understand a topic deeply through academic sources.
version: 0.1.0
---

# Deep Literature Review Skill

Conduct comprehensive, in-depth literature reviews across multiple academic databases. Generate structured but accessible reviews suitable for knowledge exploration rather than academic publication.

## When to Use This Skill

Use this skill when:
- User wants to explore a topic deeply through academic sources
- User asks to "research X", "do a literature review on X", "survey literature about X"
- User wants to understand the main concepts, debates, and frontier of a topic
- User needs to find key papers and influential research on a subject
- User wants a comprehensive overview of a field or subfield

Do NOT use this skill when:
- User needs a quick, superficial overview (provide a brief summary instead)
- User is writing for academic publication (use psych-review or domain-specific skills)
- User needs specific clinical or medical guidelines (use specialized medical resources)

## Overview

This skill provides a complete workflow for:

1. **Multi-database Search** - Search across Semantic Scholar, OpenAlex, arXiv, and other academic sources
2. **Intelligent Analysis** - Group results by themes, identify core papers and key authors
3. **Structured Review Generation** - Create comprehensive but accessible reviews
4. **Knowledge Visualization** - Optionally generate knowledge graphs (when requested)

## Workflow

### Step 1: Define Research Scope

Work with user to clarify:
- Research topic or question
- Time range (e.g., last 5 years, 2018-2023)
- Key aspects or subtopics to explore
- Preferred depth level

Create a research framework document in the project directory.

### Step 2: Execute Multi-Database Search

Use the search scripts to query multiple databases:

```bash
# Search Semantic Scholar (recommended for breadth)
python scripts/search_semantic_scholar.py "your topic" \
  --year 2020-2024 \
  --limit 50 \
  --output data/project-name/ss_results.json

# Search OpenAlex (good for citations and open access)
python scripts/search_openalex.py "your topic" \
  --from-year 2020 \
  --limit 50 \
  --output data/project-name/oa_results.json

# Search arXiv (for CS, physics, math)
python scripts/search_arxiv.py "your topic" \
  --year 2020-2024 \
  --limit 30 \
  --output data/project-name/arxiv_results.json
```

### Step 3: Aggregate and Deduplicate

Combine results from multiple sources:

```bash
python scripts/aggregate_results.py \
  data/project-name/ss_results.json \
  data/project-name/oa_results.json \
  data/project-name/arxiv_results.json \
  --deduplicate \
  --output data/project-name/merged_results.json
```

### Step 4: Analyze and Organize

Review merged results to:
- Identify major themes and subtopics
- Note key authors and influential papers
- Identify debates, disagreements, or gaps in the field
- Group papers by theme

Document this analysis in `data/project-name/theme_analysis.md`.

### Step 5: Generate Review

Create a structured review document following this structure:

```markdown
# [Topic Name] - Literature Review

## Executive Summary
[2-3 paragraphs capturing main findings]

## Introduction
[Why this topic matters, what this review covers]

## Main Themes

### Theme 1: [Name]
- Overview of the theme
- Key papers and findings
- Current state of research

### Theme 2: [Name]
[Same structure]

## Key Researchers and Influential Papers
[List of most cited/influential works]

## Debates and Gaps
[Where researchers disagree, what's unknown]

## Recent Trends
[What's emerging, future directions]

## Conclusion
[Main takeaways]

## References
[Formatted citations]
```

### Step 6: Optional Knowledge Graph

If user requests visualization:

```bash
python scripts/generate_knowledge_graph.py \
  data/project-name/merged_results.json \
  --output data/project-name/knowledge-graph.png
```

## Project Organization

Maintain organized project structure:

```
literature-review-projects/
├── project-name/
│   ├── research_framework.md
│   ├── ss_results.json
│   ├── oa_results.json
│   ├── arxiv_results.json
│   ├── merged_results.json
│   ├── theme_analysis.md
│   ├── review.md
│   └── knowledge-graph.png (if generated)
├── another-project/
│   └── ...
└── templates/
    └── research_framework_template.md
```

## Scripts Reference

### search_semantic_scholar.py
Search Semantic Scholar API for academic papers.
- Args: query, --year, --field, --limit, --output
- Returns: JSON with paper titles, abstracts, citations, authors

### search_openalex.py
Search OpenAlex for academic literature.
- Args: query, --from-year, --to-year, --limit, --peer-reviewed, --output
- Returns: JSON with papers, citations, concepts

### search_arxiv.py
Search arXiv preprint repository.
- Args: query, --year, --categories, --limit, --output
- Returns: JSON with preprints

### aggregate_results.py
Merge and deduplicate results from multiple sources.
- Args: input files, --deduplicate, --output
- Returns: Cleaned, merged JSON

### generate_knowledge_graph.py
Generate visual knowledge graph from papers.
- Args: results.json, --output, --max-papers
- Returns: PNG image

## Database Selection Guide

| Database | Best For | Limitations |
|----------|----------|-------------|
| Semantic Scholar | Broad coverage, citations | Limited older papers |
| OpenAlex | Citations, open access | Complex API |
| arXiv | CS, physics, math preprints | Mostly preprints |
| CrossRef | DOIs, metadata | Search not primary |

## Quality Indicators

When evaluating papers, consider:
- Citation count (not always reliable but indicative)
- Journal/conference prestige
- Author reputation and h-index
- Recency (for frontier research)
- Reproducibility indicators

## Tips for Effective Reviews

1. **Start broad, then narrow** - First get wide coverage, then focus on key papers
2. **Use citation networks** - Follow "cited by" and "references" to find related work
3. **Note the narrative** - Don't just list papers; explain how the field evolved
4. **Be critical but fair** - Acknowledge limitations without dismissiveness
5. **Identify patterns** - Look for consensus, debates, and gaps

## Additional Resources

### Reference Files
- **`references/database_guide.md`** - Detailed database selection guide
- **`references/review_template.md`** - Review template with examples

### Scripts
- **`scripts/search_semantic_scholar.py`** - Semantic Scholar search
- **`scripts/search_openalex.py`** - OpenAlex search
- **`scripts/search_arxiv.py`** - arXiv search
- **`scripts/aggregate_results.py`** - Result aggregation
- **`scripts/generate_knowledge_graph.py`** - Visualization
