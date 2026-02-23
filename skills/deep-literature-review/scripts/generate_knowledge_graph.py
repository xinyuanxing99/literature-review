#!/usr/bin/env python3
"""
Generate a knowledge graph visualization from literature results.
"""

import argparse
import json
import sys
from pathlib import Path


def load_papers(filepath):
    """Load papers from JSON file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict) and "papers" in data:
                return data["papers"]
            elif isinstance(data, list):
                return data
            return []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading file: {e}", file=sys.stderr)
        return []


def extract_keywords(papers, top_n=50):
    """Extract most common keywords from paper titles and abstracts."""
    from collections import Counter
    import re

    stopwords = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "as", "is", "was", "are", "were", "been",
        "be", "have", "has", "had", "do", "does", "did", "will", "would",
        "could", "should", "may", "might", "must", "shall", "can", "need",
        "this", "that", "these", "those", "it", "its", "they", "them", "their",
        "we", "our", "you", "your", "he", "she", "him", "her", "his",
        "study", "research", "paper", "using", "based", "approach", "method"
    }

    words = []
    for paper in papers:
        # Combine title and abstract
        text = ""
        if paper.get("title"):
            text += paper["title"] + " "
        if paper.get("abstract"):
            text += str(paper["abstract"]) + " "

        # Extract words
        tokens = re.findall(r'\b[a-z]{3,}\b', text.lower())
        words.extend([w for w in tokens if w not in stopwords])

    # Count and get top keywords
    word_counts = Counter(words)
    return word_counts.most_common(top_n)


def generate_simple_graph(papers, output_path):
    """Generate a simple ASCII/text knowledge graph."""
    keywords = extract_keywords(papers, top_n=20)

    lines = []
    lines.append("=" * 60)
    lines.append("KNOWLEDGE GRAPH - Literature Overview")
    lines.append("=" * 60)
    lines.append("")

    # Top keywords
    lines.append("KEY THEMES:")
    lines.append("-" * 40)
    for i, (word, count) in enumerate(keywords[:10], 1):
        bar = "█" * min(count // 5, 20)
        lines.append(f"{i:2}. {word:<20} {bar} ({count})")
    lines.append("")

    # Papers by year
    lines.append("PUBLICATION TIMELINE:")
    lines.append("-" * 40)
    years = {}
    for paper in papers:
        year = paper.get("year")
        if year:
            years[year] = years.get(year, 0) + 1

    for year in sorted(years.keys()):
        bar = "█" * min(years[year], 20)
        lines.append(f"{year}: {bar} ({years[year]})")
    lines.append("")

    # Top cited papers
    lines.append("TOP CITED PAPERS:")
    lines.append("-" * 40)
    sorted_papers = sorted(papers, key=lambda p: p.get("citation_count", 0), reverse=True)
    for i, paper in enumerate(sorted_papers[:10], 1):
        title = paper.get("title", "Unknown")[:40]
        citations = paper.get("citation_count", 0)
        lines.append(f"{i}. {title}... ({citations} citations)")

    lines.append("")
    lines.append("=" * 60)

    # Write to file
    with open(output_path.replace(".png", ".txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Knowledge graph saved to {output_path.replace('.png', '.txt')}")

    # Try to generate PNG if matplotlib available
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        from matplotlib import cm

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle("Literature Review Knowledge Graph", fontsize=14, fontweight="bold")

        # 1. Keywords word cloud style (bar chart)
        ax1 = axes[0, 0]
        kw_words = [w for w, c in keywords[:15]]
        kw_counts = [c for w, c in keywords[:15]]
        colors = cm.viridis([i/len(kw_words) for i in range(len(kw_words))])
        ax1.barh(kw_words[::-1], kw_counts[::-1], color=colors[::-1])
        ax1.set_xlabel("Frequency")
        ax1.set_title("Key Themes")

        # 2. Publication timeline
        ax2 = axes[0, 1]
        ax2.bar(years.keys(), years.values(), color="steelblue")
        ax2.set_xlabel("Year")
        ax2.set_ylabel("Papers")
        ax2.set_title("Publication Timeline")

        # 3. Top cited papers
        ax3 = axes[1, 0]
        top_papers = sorted_papers[:10]
        titles = [p.get("title", "")[:30] for p in top_papers]
        citations = [p.get("citation_count", 0) for p in top_papers]
        colors3 = cm.Reds([c/max(citations) if max(citations) > 0 else 0 for c in citations])
        ax3.barh(titles[::-1], citations[::-1], color=colors3[::-1])
        ax3.set_xlabel("Citations")
        ax3.set_title("Top Cited Papers")

        # 4. Source distribution
        ax4 = axes[1, 1]
        sources = {}
        for paper in papers:
            source = paper.get("source", "unknown")
            sources[source] = sources.get(source, 0) + 1
        ax4.pie(sources.values(), labels=sources.keys(), autopct="%1.1f%%",
               colors=plt.cm.Set3.colors[:len(sources)])
        ax4.set_title("Sources")

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        print(f"Visualization saved to {output_path}")

    except ImportError:
        print("Note: matplotlib not available. Text version generated.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate knowledge graph from literature results"
    )
    parser.add_argument("input_file", help="Input JSON file with papers")
    parser.add_argument("--output", "-o", help="Output image file (PNG)")
    parser.add_argument("--max-papers", type=int, default=100,
                       help="Maximum papers to include")

    args = parser.parse_args()

    # Determine output path
    output_path = args.output
    if not output_path:
        input_name = Path(args.input_file).stem
        output_path = f"{input_name}_knowledge_graph.png"

    # Load papers
    papers = load_papers(args.input_file)
    if not papers:
        print("No papers found in input file", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(papers)} papers")

    # Limit papers
    papers = papers[:args.max_papers]
    print(f"Processing {len(papers)} papers")

    # Generate graph
    generate_simple_graph(papers, output_path)


if __name__ == "__main__":
    main()
