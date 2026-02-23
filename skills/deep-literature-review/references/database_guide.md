# Academic Database Selection Guide

## Overview

Different academic databases have different strengths and coverage. This guide helps you choose the right database(s) for your literature review.

## Major Databases

### Semantic Scholar
**Best for:** Broad coverage, citation analysis, quick start

- **Coverage:** Computer science, biology, physics, psychology, economics
- **Strengths:**
  - Large paper database (>200 million papers)
  - Good citation coverage
  - Clean API
  - Paper summaries and key figures
- **Limitations:**
  - Less coverage of humanities
  - Some older papers missing

**Use when:** You need a quick, comprehensive start with good citation data.

### OpenAlex
**Best for:** Open access papers, cross-disciplinary research, citation analysis

- **Coverage:** All fields, strong in STEM
- **Strengths:**
  - Excellent open access coverage
  - Rich metadata
  - Good citation data
  - Institutional data
- **Limitations:**
  - API can be complex
  - Some metadata quality issues

**Use when:** You want open access papers or need institutional analysis.

### arXiv
**Best for:** Computer science, physics, mathematics, recent preprints

- **Coverage:** STEM fields, particularly CS, physics, math
- **Strengths:**
  - Latest research (preprints)
  - No paywall
  - Strong in AI/ML
- **Limitations:**
  - Not peer-reviewed (preprints)
  - Limited to STEM
  - No citation counts

**Use when:** You need the very latest research, especially in AI/ML/physics.

### CrossRef
**Best for:** DOI resolution, metadata, reference linking

- **Coverage:** All fields with DOIs
- **Strengths:**
  - Comprehensive DOI database
  - Good metadata
  - Reference lists
- **Limitations:**
  - Not a search database per se
  - API requires more processing

**Use when:** You need specific DOI data or reference tracking.

## Field-Specific Recommendations

| Field | Recommended Databases |
|-------|----------------------|
| Computer Science | Semantic Scholar, arXiv, DBLP |
| AI/ML | Semantic Scholar, arXiv |
| Psychology | Semantic Scholar, PsycINFO |
| Biology/Medicine | PubMed, Semantic Scholar |
| Physics | arXiv, Semantic Scholar |
| Social Sciences | Semantic Scholar, OpenAlex |
| Humanities | JSTOR, Google Scholar |

## Multi-Database Strategy

For comprehensive reviews, search multiple databases:

1. **Start with Semantic Scholar** - Good breadth
2. **Add OpenAlex** - Open access and citations
3. **Add arXiv** - If STEM field and need latest
4. **Add specialized** - Field-specific databases

## API Rate Limits

| Database | Limit | Notes |
|----------|-------|-------|
| Semantic Scholar | 100/request, 5000/day | Free tier |
| OpenAlex | 10/second | Polite pool |
| arXiv | 1/3 second | No auth needed |

## Best Practices

1. **Start broad** - Search all relevant databases
2. **Use consistent queries** - Same query across databases
3. **Track sources** - Note which database each paper came from
4. **Deduplicate** - Remove overlaps with aggregation scripts
5. **Document search strategy** - Record queries and dates
