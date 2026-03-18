#!/usr/bin/env python3
"""Wrap each heading + its following content in a <div class="section">."""

from bs4 import BeautifulSoup, NavigableString

FILE = "Investigating + Creating the Report.html"
HEADING_TAGS = {"h1", "h2", "h3", "h4"}


def wrap_sections(soup):
    body = soup.find("body")

    # Collect top-level children as a flat list
    children = list(body.children)

    # Walk through and group: each heading starts a new section
    groups = []
    current = []
    for node in children:
        if isinstance(node, NavigableString):
            if node.strip():
                current.append(node)
            continue
        if node.name in HEADING_TAGS:
            if current:
                groups.append(current)
            current = [node]
        else:
            current.append(node)
    if current:
        groups.append(current)

    # Clear body and rebuild with wrapped sections
    body.clear()
    for group in groups:
        # Detach nodes from tree before re-inserting
        for node in group:
            node.extract()

        div = soup.new_tag("div", **{"class": "section"})
        for node in group:
            div.append(node)
        body.append(div)

    return soup


def main():
    with open(FILE, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    soup = wrap_sections(soup)

    with open(FILE, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    print("Done.")


if __name__ == "__main__":
    main()
