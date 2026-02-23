#!/usr/bin/env python3
"""
Search OpenAlex for academic papers.
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.parse
import urllib.error


def search_openalex(query, from_year=None, to_year=None, limit=10,
                    peer_reviewed=False, sort_by="relevance"):
    """
    Search OpenAlex API.

    Args:
        query: Search query string
        from_year: Start year
        to_year: End year
        limit: Maximum number of results
        peer_reviewed: Only peer-reviewed papers
        sort_by: Sort order (relevance, cited, published)

    Returns:
        List of paper dictionaries
    """
    base_url = "https://api.openalex.org/works"

    # Build filter string
    filters = []
    if from_year or to_year:
        year_range = []
        if from_year:
            year_range.append(f"from_published_date:{from_year}")
        if to_year:
            year_range.append(f"to_published_date:{to_year}")
        filters.append(",".join(year_range))

    if peer_reviewed:
        filters.append("is_paratext:false")

    # Build search query
    search_query = urllib.parse.quote(query)

    params = {
        "search": query,
        "per_page": min(limit, 200),  # API max is 200
        "sort": sort_by if sort_by != "relevance" else "relevance_score:desc",
        "mailto": "research@example.com"  # Polite pool
    }

    if filters:
        params["filter"] = ",".join(filters)

    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    papers = []
    headers = {
        "Accept": "application/json",
        "User-Agent": "LiteratureReviewPlugin/0.1.0 (mailto:research@example.com)"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

            for work in data.get("results", []):
                # Extract authors
                authors = []
                for author in work.get("authorships", [])[:10]:  # Limit authors
                    author_name = author.get("author", {}).get("display_name")
                    if author_name:
                        authors.append(author_name)

                # Extract publication info
                publication_year = work.get("publication_year")
                venue = work.get("host_venue", {}).get("display_name")

                papers.append({
                    "title": work.get("title"),
                    "abstract": work.get("abstract_inverted_index"),  # Note: inverted index format
                    "authors": authors,
                    "year": publication_year,
                    "citation_count": work.get("cited_by_count", 0),
                    "venue": venue,
                    "url": work.get("doi"),
                    "work_id": work.get("id"),
                    "source": "openalex",
                    "open_access": work.get("open_access", {}).get("is_oa", False),
                    "concepts": [c.get("display_name") for c in work.get("concepts", [])[:5]]
                })

    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}", file=sys.stderr)
        if e.code == 429:
            print("Rate limited. Waiting 5 seconds...", file=sys.stderr)
            time.sleep(5)
            return search_openalex(query, from_year, to_year, limit,
                                   peer_reviewed, sort_by)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

    return papers


def main():
    parser = argparse.ArgumentParser(
        description="Search OpenAlex for academic papers"
    )
    parser.add_argument("query", help="Search query")
    parser.add_argument("--from-year", type=int, help="Start year")
    parser.add_argument("--to-year", type=int, help="End year")
    parser.add_argument("--limit", type=int, default=10, help="Number of results")
    parser.add_argument("--peer-reviewed", action="store_true",
                       help="Only peer-reviewed papers")
    parser.add_argument("--sort", default="relevance",
                       choices=["relevance", "cited", "published"],
                       help="Sort order")
    parser.add_argument("--output", "-o", help="Output JSON file")

    args = parser.parse_args()

    print(f"Searching OpenAlex for: {args.query}")
    if args.from_year or args.to_year:
        print(f"Year range: {args.from_year or 'start'}-{args.to_year or 'end'}")

    papers = search_openalex(
        args.query,
        from_year=args.from_year,
        to_year=args.to_year,
        limit=args.limit,
        peer_reviewed=args.peer_reviewed,
        sort_by=args.sort
    )

    print(f"Found {len(papers)} papers")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump({
                "query": args.query,
                "from_year": args.from_year,
                "to_year": args.to_year,
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
