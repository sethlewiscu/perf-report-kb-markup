#!/usr/bin/env python3
"""Clean up ClickUp-exported HTML into plain semantic HTML."""

import re
import sys
from bs4 import BeautifulSoup, NavigableString, Tag

INPUT = "html Investigating + Creating the Report-20260317070122.html"
OUTPUT = "Investigating + Creating the Report.html"


def unwrap_if_exists(soup, selector):
    for el in soup.select(selector):
        el.unwrap()


def remove_if_exists(soup, selector):
    for el in soup.select(selector):
        el.decompose()


def strip_attrs(tag, keep=None):
    keep = keep or []
    for attr in list(tag.attrs.keys()):
        if attr not in keep:
            del tag[attr]


def clean(soup):
    # 1. Replace <head> with minimal version
    title_tag = soup.find("title")
    title_text = title_tag.get_text(strip=True) if title_tag else "Document"
    head = soup.find("head")
    if head:
        head.clear()
        new_meta = soup.new_tag("meta", charset="UTF-8")
        new_title = soup.new_tag("title")
        new_title.string = title_text
        head.append(new_meta)
        head.append(new_title)

    # 2. Fix <body> class
    body = soup.find("body")
    if body and "class" in body.attrs:
        del body["class"]

    # 3. Remove custom ClickUp elements entirely
    for tag_name in ["cu-table-content-inline-dynamic", "cu-doc-page-avatar-dynamic"]:
        for el in soup.find_all(tag_name):
            el.decompose()

    # Remove SVG elements referencing ClickUp sprites (UI chrome, not content)
    for el in soup.find_all("svg"):
        use = el.find("use")
        href = use.get("xlink:href", "") if use else ""
        if "svg-sprite-cu" in href or "svg-sprite" in href:
            # Remove parent <a> if it only contains this svg
            parent = el.parent
            el.decompose()
            if parent and parent.name == "a" and not parent.get_text(strip=True):
                parent.decompose()

    # 4. Remove cu-table-content__anchor links (internal shims)
    for el in soup.find_all("a", class_="cu-table-content__anchor"):
        el.decompose()

    # 5. Unwrap structural wrapper divs (order matters: innermost last)
    for cls in [
        "cu-editor-wrapper",
        "cu-editor-content",
        "cu-editor",
        "ql-editor",
        "page-0",
    ]:
        for el in soup.find_all(class_=cls):
            el.unwrap()

    # 6. Convert ql-advanced-banner divs to <blockquote>
    for banner in soup.find_all("div", class_="ql-advanced-banner"):
        # Drop the icon child
        for icon in banner.find_all(class_="ql-advanced-banner__icon"):
            icon.decompose()
        banner.name = "blockquote"
        banner.attrs = {}

    # 7. Simplify headings — strip all attrs
    for tag_name in ["h1", "h2", "h3", "h4"]:
        for el in soup.find_all(tag_name):
            el.attrs = {}

    # 8. Simplify lists and list items — strip all attrs
    for tag_name in ["ul", "ol", "li"]:
        for el in soup.find_all(tag_name):
            el.attrs = {}

    # 9. Unwrap cu-mention links — keep inner text
    for el in soup.find_all("a", class_=lambda c: c and "cu-mention" in " ".join(c)):
        el.unwrap()

    # 10. Images — remove drake meme images and datadog emoji images; keep only src on rest
    for el in soup.find_all("img"):
        src = el.get("src", "")
        if any(x in src for x in ["drake-like", "drake-dislike", "emojis/333/datadog"]):
            el.decompose()
            continue
        el.attrs = {}
        if src:
            el["src"] = src

    # 11. Links — keep only href
    for el in soup.find_all("a"):
        href = el.get("href", "")
        el.attrs = {}
        if href:
            el["href"] = href

    # 12. Paragraphs and divs — strip all attrs
    for tag_name in ["p", "div"]:
        for el in soup.find_all(tag_name):
            el.attrs = {}

    # 13. Spans — strip cu-/ql- classes; remove span entirely if no attrs remain
    for el in soup.find_all("span"):
        el.attrs = {}
        el.unwrap()

    # 14. Strip any remaining data-* and cu-/ql- classes from all tags
    for el in soup.find_all(True):
        # Remove data-* attrs
        for attr in list(el.attrs.keys()):
            if attr.startswith("data-"):
                del el[attr]
        # Clean classes
        if "class" in el.attrs:
            classes = el["class"]
            cleaned = [
                c for c in classes
                if not c.startswith("cu-") and not c.startswith("ql-") and not c.startswith("doc-")
            ]
            if cleaned:
                el["class"] = cleaned
            else:
                del el["class"]

    # 15. Remove empty block elements (multiple passes)
    block_tags = {"p", "div", "li", "blockquote"}
    changed = True
    while changed:
        changed = False
        for el in soup.find_all(block_tags):
            if not el.get_text(strip=True) and not el.find(["img", "a"]):
                el.decompose()
                changed = True

    # 16. Unwrap any leftover wrapper divs with no class/attrs
    for el in soup.find_all("div"):
        el.unwrap()

    return soup


def main():
    with open(INPUT, encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    soup = clean(soup)

    # Pretty-print output
    output = soup.prettify()

    # Collapse excessive blank lines
    output = re.sub(r"\n{3,}", "\n\n", output)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"Done. Written to: {OUTPUT}")
    # Quick stats
    import os
    orig_size = os.path.getsize(INPUT)
    new_size = os.path.getsize(OUTPUT)
    print(f"Size: {orig_size:,} bytes → {new_size:,} bytes ({100*new_size//orig_size}% of original)")


if __name__ == "__main__":
    main()
