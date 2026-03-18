#!/usr/bin/env python3
"""Move image-only <li> elements inside the preceding <li>."""

from bs4 import BeautifulSoup

FILE = "Investigating + Creating the Report.html"


def fix(soup):
    changed = True
    while changed:
        changed = False
        for li in soup.find_all("li"):
            real_children = [c for c in li.children if str(c).strip()]
            if len(real_children) != 1:
                continue
            img = real_children[0]
            if getattr(img, "name", None) != "img":
                continue

            prev = li.find_previous_sibling("li")
            if prev:
                # Append img to the end of the previous li
                img.extract()
                prev.append(img)
                li.decompose()
            else:
                # No previous sibling — img is first item in a sub-list.
                # Move it up into the parent <li> and remove the now-empty list.
                parent_list = li.parent  # the <ul> or <ol>
                parent_li = parent_list.parent if parent_list else None
                if parent_li and parent_li.name == "li":
                    img.extract()
                    parent_li.append(img)
                    li.decompose()
                    if not parent_list.find("li"):
                        parent_list.decompose()

            changed = True
            break  # restart after each mutation

    return soup


def main():
    with open(FILE, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    soup = fix(soup)

    with open(FILE, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    print("Done.")


if __name__ == "__main__":
    main()
