"""Usage: python3 scripts/scrape_articles.py URL [URL ...]

Scrape multiple ProPresenter documentation article URLs by reusing
scripts/scrape_article.py for each URL.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scrape_article import ScrapeError, scrape_article


def scrape_articles(urls: list[str]) -> tuple[list[Path], list[tuple[str, str]]]:
    """Scrape each URL and collect successes and failures."""
    saved_paths: list[Path] = []
    failures: list[tuple[str, str]] = []

    for index, url in enumerate(urls, start=1):
        print(f"[{index}/{len(urls)}] Scraping {url}")

        try:
            output_path = scrape_article(url)
        except ScrapeError as exc:
            failures.append((url, str(exc)))
            print(f"  Error: {exc}", file=sys.stderr)
            continue

        saved_paths.append(output_path)
        print(f"  Saved article to {output_path}")

    return saved_paths, failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape multiple ProPresenter documentation articles into Markdown."
    )
    parser.add_argument("urls", nargs="+", help="One or more documentation URLs")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    saved_paths, failures = scrape_articles(args.urls)

    print()
    print(f"Done. Saved {len(saved_paths)} article(s).")

    if failures:
        print(f"Failed to scrape {len(failures)} URL(s):", file=sys.stderr)
        for url, error in failures:
            print(f"- {url}: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
