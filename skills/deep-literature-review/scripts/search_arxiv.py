#!/usr/bin/env python3
"""
Search arXiv for preprints.
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import urllib.error
import re
from datetime import datetime


def search_arxiv(query, year=None, categories=None, limit=10):
    """
    Search arXiv API.

    Args:
        query: Search query string
        year: Year range (e.g., "2020-2024")
        categories: arXiv categories (e.g., "cs.AI,cs.LG")
        limit: Maximum number of results

    Returns:
        List of preprint dictionaries
    """
    base_url = "http://export.arxiv.org/api/query"

    # Build search query
    search_parts = [f"all:{query}"]

    if year:
        if "-" in str(year):
            start_year, end_year = year.split("-")
            # arXiv supports submittedDate range
            search_parts.append(f"submittedDate:[{start_year}0101 TO {end_year}1231]")
        else:
            search_parts.append(f"submittedDate:[{year}0101 TO {year}1231]")

    if categories:
        for cat in categories.split(","):
            search_parts.append(f"cat:{cat.strip()}")

    search_query = " AND ".join(search_parts)

    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": min(limit, 50),  # API limit
        "sortBy": "relevance",
        "sortOrder": "descending"
    }

    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    papers = []
    headers = {
        "Accept": "application/atom+xml"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            xml_content = response.read().decode("utf-8")

            # Simple XML parsing
            entries = re.findall(r'<entry>(.*?)</entry>', xml_content, re.DOTALL)

            for entry in entries:
                # Extract fields using regex
                title_match = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
                summary_match = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
                author_matches = re.findall(r'<name>(.*?)</name>', entry)
                published_match = re.search(r'<published>(.*?)</published>', entry)
                id_match = re.search(r'<id>(.*?)</id>', entry)
                categories_match = re.findall(r'<category term="([^"]+)"', entry)

                title = title_match.group(1).strip() if title_match else ""
                summary = summary_match.group(1).strip() if summary_match else ""
                authors = [a.strip() for a in author_matches]
                published = published_match.group(1)[:10] if published_match else None  # YYYY-MM-DD
                year = int(published[:4]) if published else None
                arxiv_id = id_match.group(1).split("/")[-1] if id_match else ""
                arxiv_url = f"https://arxiv.org/abs/{arxiv_id}"

                papers.append({
                    "title": title,
                    "abstract": summary,
                    "authors": authors,
                    "year": year,
                    "citation_count": 0,  # arXiv doesn't have citation counts
                    "venue": "arXiv preprint",
                    "url": arxiv_url,
                    "paper_id": arxiv_id,
                    "categories": categories_match,
                    "source": "arxiv"
                })

    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

    return papers


def main():
    parser = argparse.ArgumentParser(
        description="Search arXiv for preprints"
    )
    parser.add_argument("query", help="Search query")
    parser.add_argument("--year", help="Year range (e.g., 2020-2024)")
    parser.add_argument("--categories", help="arXiv categories (e.g., cs.AI,cs.LG)")
    parser.add_argument("--limit", type=int, default=10, help="Number of results")
    parser.add_argument("--output", "-o", help="Output JSON file")

    args = parser.parse_args()

    print(f"Searching arXiv for: {args.query}")
    if args.year:
        print(f"Year range: {args.year}")
    if args.categories:
        print(f"Categories: {args.categories}")

    papers = search_arxiv(
        args.query,
        year=args.year,
        categories=args.categories,
        limit=args.limit
    )

    print(f"Found {len(papers)} papers")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump({
                "query": args.query,
                "year_range": args.year,
                "categories": args.categories,
                "count": len(papers),
                "papers": papers
            }, f, ensure_ascii=False, indent=2)
        print(f"Results saved to {args.output}")
    else:
        print(json.dumps({
            "query": args.query,
            "count": len(papers),
            "papers": papers
        }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
