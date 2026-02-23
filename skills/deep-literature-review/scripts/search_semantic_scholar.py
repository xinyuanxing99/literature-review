#!/usr/bin/env python3
"""
Search Semantic Scholar for academic papers.
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.parse
import urllib.error


def search_semantic_scholar(query, year=None, field=None, limit=10, offset=0):
    """
    Search Semantic Scholar API.

    Args:
        query: Search query string
        year: Year range (e.g., "2020-2024" or "2020")
        field: Field of study (e.g., "Computer Science", "Psychology")
        limit: Maximum number of results
        offset: Offset for pagination

    Returns:
        List of paper dictionaries
    """
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": query,
        "limit": min(limit, 100),  # API max is 100
        "offset": offset,
        "fields": "title,abstract,authors,year,citationCount,venue,url,paperId"
    }

    if year:
        if "-" in str(year):
            start_year, end_year = year.split("-")
            params["year"] = f"{start_year},{end_year}"
        else:
            params["year"] = f"{year},{year}"

    if field:
        params["fields"] += ",fieldsOfStudy"
        # Note: Semantic Scholar doesn't support field filter directly in search
        # We'll filter results after fetching

    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    papers = []
    headers = {
        "Accept": "application/json"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

            for paper in data.get("data", []):
                # Filter by field if specified
                if field:
                    paper_fields = paper.get("fieldsOfStudy", [])
                    if field.lower() not in [f.lower() for f in paper_fields]:
                        continue

                papers.append({
                    "title": paper.get("title"),
                    "abstract": paper.get("abstract"),
                    "authors": [a.get("name") for a in paper.get("authors", []) if a.get("name")],
                    "year": paper.get("year"),
                    "citation_count": paper.get("citationCount", 0),
                    "venue": paper.get("venue"),
                    "url": paper.get("url"),
                    "paper_id": paper.get("paperId"),
                    "source": "semantic_scholar"
                })

    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}", file=sys.stderr)
        if e.code == 429:
            print("Rate limited. Waiting 5 seconds...", file=sys.stderr)
            time.sleep(5)
            return search_semantic_scholar(query, year, field, limit, offset)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

    return papers


def main():
    parser = argparse.ArgumentParser(
        description="Search Semantic Scholar for academic papers"
    )
    parser.add_argument("query", help="Search query")
    parser.add_argument("--year", help="Year range (e.g., 2020-2024)")
    parser.add_argument("--field", help="Field of study")
    parser.add_argument("--limit", type=int, default=10, help="Number of results")
    parser.add_argument("--offset", type=int, default=0, help="Offset for pagination")
    parser.add_argument("--output", "-o", help="Output JSON file")

    args = parser.parse_args()

    print(f"Searching Semantic Scholar for: {args.query}")
    if args.year:
        print(f"Year range: {args.year}")
    if args.field:
        print(f"Field: {args.field}")

    papers = search_semantic_scholar(
        args.query,
        year=args.year,
        field=args.field,
        limit=args.limit,
        offset=args.offset
    )

    print(f"Found {len(papers)} papers")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump({
                "query": args.query,
                "year_range": args.year,
                "field": args.field,
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
