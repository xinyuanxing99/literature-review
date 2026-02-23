#!/usr/bin/env python3
"""
Aggregate and deduplicate results from multiple literature search sources.
"""

import argparse
import json
import sys
from pathlib import Path


def load_papers_from_file(filepath):
    """Load papers from a JSON file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict) and "papers" in data:
                return data["papers"]
            elif isinstance(data, list):
                return data
            else:
                print(f"Warning: Unknown format in {filepath}", file=sys.stderr)
                return []
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filepath}: {e}", file=sys.stderr)
        return []


def normalize_title(title):
    """Normalize title for comparison."""
    if not title:
        return ""
    return "".join(c.lower() for c in title if c.isalnum() or c.isspace()).strip()


def is_duplicate(paper1, paper2, threshold=0.85):
    """Check if two papers are duplicates based on title similarity."""
    title1 = normalize_title(paper1.get("title", ""))
    title2 = normalize_title(paper2.get("title", ""))

    if not title1 or not title2:
        return False

    # Exact match
    if title1 == title2:
        return True

    # Simple word overlap check
    words1 = set(title1.split())
    words2 = set(title2.split())

    if not words1 or not words2:
        return False

    overlap = len(words1 & words2) / min(len(words1), len(words2))
    return overlap >= threshold


def deduplicate_papers(papers):
    """Remove duplicate papers from the list."""
    unique_papers = []
    seen_titles = []

    for paper in papers:
        is_dup = False
        for seen_title in seen_titles:
            if is_duplicate(paper, {"title": seen_title}):
                is_dup = True
                break

        if not is_dup:
            unique_papers.append(paper)
            seen_titles.append(normalize_title(paper.get("title", "")))

    return unique_papers


def merge_papers(paper_lists):
    """Merge multiple lists of papers."""
    all_papers = []
    for papers in paper_lists:
        all_papers.extend(papers)
    return all_papers


def sort_papers(papers, sort_by="citation"):
    """Sort papers by specified criteria."""
    if sort_by == "citation":
        return sorted(papers, key=lambda p: p.get("citation_count", 0), reverse=True)
    elif sort_by == "year":
        return sorted(papers, key=lambda p: p.get("year", 0) if p.get("year") else 0, reverse=True)
    elif sort_by == "title":
        return sorted(papers, key=lambda p: p.get("title", "").lower())
    else:
        return papers


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate and deduplicate literature search results"
    )
    parser.add_argument("input_files", nargs="+", help="Input JSON files")
    parser.add_argument("--deduplicate", action="store_true",
                       help="Remove duplicate papers")
    parser.add_argument("--sort", default="citation",
                       choices=["citation", "year", "title"],
                       help="Sort order")
    parser.add_argument("--output", "-o", help="Output JSON file")

    args = parser.parse_args()

    # Load papers from all files
    all_papers = []
    for filepath in args.input_files:
        papers = load_papers_from_file(filepath)
        all_papers.extend(papers)
        print(f"Loaded {len(papers)} papers from {filepath}")

    print(f"Total papers before processing: {len(all_papers)}")

    # Deduplicate if requested
    if args.deduplicate:
        original_count = len(all_papers)
        all_papers = deduplicate_papers(all_papers)
        print(f"Removed {original_count - len(all_papers)} duplicates")

    # Sort
    all_papers = sort_papers(all_papers, args.sort)

    print(f"Final count: {len(all_papers)} papers")

    # Output
    output_data = {
        "total_count": len(all_papers),
        "sort_by": args.sort,
        "sources": args.input_files,
        "papers": all_papers
    }

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"Results saved to {args.output}")
    else:
        print(json.dumps(output_data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
