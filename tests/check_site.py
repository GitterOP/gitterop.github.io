#!/usr/bin/env python3
"""Check the SDD's publishing boundaries and the generated site's local links."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "_site"


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.publications = []
        self.current_projects = []
        self.current = None
        self.h1_count = 0
        self.errors = []
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.errors.append(f"Duplicate HTML id: {attrs['id']}")
            self.ids.add(attrs["id"])
        if tag == "h1":
            self.h1_count += 1
        if tag == "html" and attrs.get("lang") != "en":
            self.errors.append("The approved language must be English")
        if tag == "img" and not attrs.get("alt"):
            self.errors.append("Research image has no alternative text")
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "img" and attrs.get("src"):
            self.links.append(attrs["src"])
        if tag == "script" and attrs.get("src"):
            self.links.append(attrs["src"])
        if tag == "link" and attrs.get("rel") in {"stylesheet", "icon"}:
            self.links.append(attrs["href"])
        if "data-publication" in attrs:
            self.publications.append(attrs["data-publication"])
        if "data-current-project" in attrs:
            self.current = {"id": attrs["data-current-project"], "text": ""}
            self.current_projects.append(self.current)
        if self.current and tag in {"a", "img", "figure", "video", "iframe", "object", "details"}:
            self.errors.append(f"Unpublished project exposes material: {self.current['id']} ({tag})")

    def handle_data(self, text):
        if self.current is not None:
            self.current["text"] += text

    def handle_endtag(self, tag):
        if tag == "article":
            self.current = None


def main():
    errors = []
    if not SITE.is_dir():
        raise SystemExit(f"Build the site first. Missing: {SITE}")
    pages = {}
    for path in SITE.rglob("*.html"):
        text = path.read_text()
        page = Page(text)
        pages[path.resolve()] = page
        errors.extend(f"{path.relative_to(SITE)}: {error}" for error in page.errors)
        if page.h1_count != 1:
            errors.append(f"{path.relative_to(SITE)}: expected one main heading")
        if "/home/jd/" in text or "libfile_" in text:
            errors.append(f"{path.relative_to(SITE)}: private source reference leaked")

    required = ["index.html", "research/index.html", "publications/index.html", "cv/index.html", "404.html"]
    for relative in required:
        if not (SITE / relative).is_file():
            errors.append(f"Required page missing: {relative}")

    checked = 0
    for path, page in pages.items():
        for link in page.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            target = (SITE / unquote(parsed.path).lstrip("/")) if parsed.path.startswith("/") else path.parent / unquote(parsed.path)
            if not parsed.path:
                target = path
            if target.is_dir():
                target /= "index.html"
            target = target.resolve()
            if not target.is_relative_to(SITE.resolve()):
                errors.append(f"{path.relative_to(SITE)}: link leaves public output: {link}")
            elif not target.is_file():
                errors.append(f"{path.relative_to(SITE)}: broken link: {link}")
            elif parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
                errors.append(f"{path.relative_to(SITE)}: missing anchor: {link}")
            checked += 1

    publications = pages.get((SITE / "publications/index.html").resolve())
    expected_papers = {"dreamerv2_objetos", "subset_hsi", "presidential_sentiment", "impacto_migracion", "estimacion_heridos", "mcqueen", "desercion_universitaria_scoping"}
    if not publications or len(publications.publications) != len(expected_papers) or set(publications.publications) != expected_papers:
        errors.append(f"Expected the {len(expected_papers)} approved publications, once each")
    elif len({link for link in publications.links if link.startswith("https://doi.org/")}) != len(expected_papers):
        errors.append(f"Expected {len(expected_papers)} distinct publication DOI links")

    research = pages.get((SITE / "research/index.html").resolve())
    expected_current = {"thesis_unmixing", "wetland_segmentation", "slbot"}
    if not research or len(research.current_projects) != 3 or {p["id"] for p in research.current_projects} != expected_current:
        errors.append("Expected exactly three approved projects in progress")
    else:
        for project in research.current_projects:
            if "In progress" not in project["text"]:
                errors.append(f"Missing in-progress label: {project['id']}")
            if re.search(r"\d|https?://|github|\.pdf", project["text"], re.I):
                errors.append(f"Unexpected results or links in unpublished project: {project['id']}")

    pdfs = list(SITE.rglob("*.pdf"))
    if len(pdfs) != len(expected_papers) + 1:
        errors.append(f"Expected CV plus {len(expected_papers)} papers; found {len(pdfs)} PDFs")
    for path in pdfs:
        with path.open("rb") as document:
            if document.read(5) != b"%PDF-":
                errors.append(f"Invalid PDF: {path.relative_to(SITE)}")
    if publications and "Accepted author version" not in (SITE / "publications/index.html").read_text():
        errors.append("JSTARS author-version label is missing")

    forbidden = {".aws", ".codex", ".agents", "specs", "tests", "scripts", "vendor", ".bundle", ".git", ".github"}
    for path in SITE.rglob("*"):
        relative = path.relative_to(SITE)
        if any(part in forbidden for part in relative.parts):
            errors.append(f"Internal material in public output: {relative}")
        if path.is_file() and path.suffix in {".json", ".jsonl", ".pth", ".pt", ".tif", ".zip"}:
            errors.append(f"Unexpected data or model file in public output: {relative}")

    if errors:
        print("\n".join(f"FAIL: {error}" for error in errors))
        raise SystemExit(1)
    print(f"PASS: {len(pages)} pages, {checked} local links, {len(expected_papers)} publications, three summary-only projects, {len(pdfs)} PDFs; public-output boundaries verified.")


if __name__ == "__main__":
    main()
