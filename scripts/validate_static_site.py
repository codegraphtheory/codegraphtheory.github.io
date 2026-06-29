#!/usr/bin/env python3
"""Validate GraphTheory static site metadata and sitemap files."""

from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE_HOST = "graphtheory.xyz"
ORIGINAL_PROJECTS = {
    "hermes-profile-template",
    "heavy-coder",
    "context-forge-rag",
    "chainforge",
    "solana-rug",
    "codegraphtheory",
}
FORK_NAMES = {
    "octra",
    "hermes-agent",
    "hermes-profiles",
    "hermes-profile-kit",
    "agent-profiles",
    "awesome-rag-resources",
    "awesome-blockchain",
    "Supra-AI",
    "awesome-hermes-agent",
    "awesome-solana-oss",
    "awesome-solana",
    "awesome-solana-ai",
    "soul.md",
    "awesome-openclaw-agents",
}


class HeadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self._in_title = False
        self.meta: dict[str, str] = {}
        self.links: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {k: v or "" for k, v in attrs}
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            key = data.get("name") or data.get("property")
            if key:
                self.meta[key] = data.get("content", "")
        if tag == "link" and data.get("rel"):
            self.links[data["rel"]] = data.get("href", "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def parse_xml(path: Path) -> ET.Element:
    require(path.exists(), f"missing XML file: {path.relative_to(ROOT)}")
    return ET.parse(path).getroot()


def validate_html() -> None:
    html_path = ROOT / "index.html"
    parser = HeadParser()
    parser.feed(html_path.read_text(encoding="utf-8"))
    require("GraphTheory" in parser.title, "index title must name GraphTheory")
    require(bool(parser.meta.get("description")), "index needs meta description")
    require(parser.meta.get("og:image", "").startswith("https://graphtheory.xyz/assets/"), "index needs canonical OG image")
    require(parser.meta.get("twitter:card") == "summary_large_image", "index needs large Twitter card")
    require(parser.links.get("canonical") == "https://graphtheory.xyz/", "index needs canonical root link")


def validate_sitemaps() -> None:
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    index = parse_xml(ROOT / "sitemap.xml")
    require(index.tag == ns + "sitemapindex", "sitemap.xml must be a sitemap index")
    child_locs = [node.findtext(ns + "loc") or "" for node in index.findall(ns + "sitemap")]
    require(bool(child_locs), "sitemap.xml must list child sitemaps")
    require("https://graphtheory.xyz/sitemap-pages.xml" in child_locs, "sitemap index must include flat page sitemap")
    for loc in child_locs:
        parsed = urlparse(loc or "")
        require(parsed.scheme == "https" and parsed.netloc == SITE_HOST, f"bad sitemap loc: {loc}")
        child_path = ROOT / parsed.path.lstrip("/")
        child = parse_xml(child_path)
        require(child.tag == ns + "urlset", f"child sitemap must be urlset: {child_path.relative_to(ROOT)}")
        urls = [node.findtext(ns + "loc") or "" for node in child.findall(ns + "url")]
        require(bool(urls), f"child sitemap has no URLs: {child_path.relative_to(ROOT)}")
        for url in urls:
            parsed_url = urlparse(url or "")
            require(parsed_url.scheme == "https" and parsed_url.netloc == SITE_HOST, f"bad page URL: {url}")
            require(not parsed_url.fragment, f"sitemap URL must not contain fragment: {url}")
            for fork_name in FORK_NAMES:
                require(f"/{fork_name}/" not in parsed_url.path, f"fork surfaced in sitemap: {url}")
    for project in ORIGINAL_PROJECTS:
        require((ROOT / project / "index.html").exists(), f"missing project doc page: {project}/index.html")
        require(f"https://graphtheory.xyz/sitemaps/{project}.xml" in child_locs, f"missing project sitemap: {project}")


def validate_manifest() -> None:
    manifest = json.loads((ROOT / "assets" / "site.webmanifest").read_text(encoding="utf-8"))
    require(manifest.get("name"), "webmanifest needs name")
    require(manifest.get("start_url") in {"/", "."}, "webmanifest needs root start_url")


def main() -> None:
    validate_html()
    validate_sitemaps()
    validate_manifest()
    print("static site validation passed")


if __name__ == "__main__":
    main()
