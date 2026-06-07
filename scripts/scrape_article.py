"""Usage: python scripts/scrape_article.py "https://support.renewedvision.com/..."

Fetch one ProPresenter documentation article and save the cleaned article body
as a Markdown file in documents/.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, Tag
from markdownify import markdownify as md


DOCUMENTS_DIR = Path("documents")
PRODUCT_NAME = "ProPresenter"
DOC_TYPE = "official_docs"
USER_AGENT = "CodePath-RAG-Article-Scraper/1.0"


class ScrapeError(Exception):
    """Raised when the article cannot be fetched or parsed."""


def fetch_html(url: str) -> str:
    """Fetch the page HTML for a single documentation URL."""
    parsed_url = urlparse(url)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise ScrapeError(f"Invalid URL: {url}")

    try:
        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=20,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ScrapeError(f"Could not fetch page: {exc}") from exc

    return response.text


def parse_article(html: str) -> tuple[str, Tag]:
    """Extract the article title and body using Schema.org Article metadata."""
    soup = BeautifulSoup(html, "html.parser")

    article = soup.select_one('article[itemtype="http://schema.org/Article"]')
    search_root: BeautifulSoup | Tag = article if article else soup

    title_element = search_root.select_one('[itemprop="name"]')
    body_element = search_root.select_one('[itemprop="articleBody"]')

    if title_element is None:
        title_element = soup.select_one("h1")
    if title_element is None:
        title_element = soup.select_one("title")

    title = title_element.get_text(" ", strip=True) if title_element else ""
    if not title:
        raise ScrapeError("Could not find an article title.")
    if body_element is None:
        raise ScrapeError(
            'Could not find the article body. Expected an element with itemprop="articleBody".'
        )

    return title, body_element


def clean_body(body_element: Tag) -> Tag:
    """Remove elements that should not become part of the article Markdown."""
    body_copy = BeautifulSoup(str(body_element), "html.parser")
    copied_body = body_copy.select_one('[itemprop="articleBody"]') or body_copy

    unwanted_selectors = (
        "script",
        "style",
        "nav",
        "footer",
        "aside",
        "form",
        ".comments",
        ".comment",
        ".related-articles",
        ".article-votes",
        ".article-more-questions",
        ".pagination",
        '[rel="prev"]',
        '[rel="next"]',
    )
    for unwanted in copied_body.select(",".join(unwanted_selectors)):
        unwanted.decompose()

    return copied_body


def html_to_markdown(body_element: Tag) -> str:
    """Convert the cleaned article body HTML to Markdown."""
    cleaned_body = clean_body(body_element)
    markdown = md(
        str(cleaned_body),
        heading_style="ATX",
        bullets="-",
        strip=["script", "style"],
    )
    return normalize_markdown(markdown)


def normalize_markdown(markdown: str) -> str:
    """Trim excess blank lines while preserving readable Markdown spacing."""
    markdown = markdown.replace("\r\n", "\n").replace("\r", "\n")
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    return markdown.strip()


def slugify(title: str) -> str:
    """Create a filesystem-safe Markdown filename from an article title."""
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug or "article"


def yaml_quote(value: str) -> str:
    """Quote a short string for simple YAML frontmatter."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def save_markdown(title: str, source_url: str, body_markdown: str) -> Path:
    """Save the article as a Markdown file in documents/."""
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DOCUMENTS_DIR / f"{slugify(title)}.md"

    frontmatter = "\n".join(
        [
            "---",
            f"title: {yaml_quote(title)}",
            f"source: {yaml_quote(source_url)}",
            f"type: {yaml_quote(DOC_TYPE)}",
            f"product: {yaml_quote(PRODUCT_NAME)}",
            "---",
            "",
            f"# {title}",
            "",
        ]
    )

    output_path.write_text(f"{frontmatter}{body_markdown}\n", encoding="utf-8")
    return output_path


def scrape_article(url: str) -> Path:
    """Fetch, parse, convert, and save one article URL."""
    html = fetch_html(url)
    title, body_element = parse_article(html)
    body_markdown = html_to_markdown(body_element)

    if not body_markdown:
        raise ScrapeError("Article body was found, but it did not contain readable content.")

    return save_markdown(title, url, body_markdown)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape one ProPresenter documentation article into Markdown."
    )
    parser.add_argument("url", help="One support.renewedvision.com documentation URL")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        output_path = scrape_article(args.url)
    except ScrapeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Saved article to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
