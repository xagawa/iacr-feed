import re
from pathlib import Path

import feedparser
from feedgen.feed import FeedGenerator

SOURCE = "https://eprint.iacr.org/rss/rss.xml?order=recent"

feed = feedparser.parse(SOURCE)

fg = FeedGenerator()
fg.title("IACR ePrint Recent")
fg.link(href="https://eprint.iacr.org/")
fg.description("Mirror feed for Slack")
fg.language("en")

for entry in feed.entries[:50]:

    fe = fg.add_entry()

    title = entry.get("title", "")
    link = entry.get("link", "")

    fe.title(title)
    fe.link(href=link)
    fe.guid(link, permalink=True)

    # get numbers from link
    paper_id = ""
    m = re.search(r"eprint\.iacr\.org/(\d{4}/\d+)", link)
    if m:
        paper_id = m.group(1)

    # get authors 
    authors = []

    if "authors" in entry:
        authors = [
            a.get("name", "")
            for a in entry.authors
            if a.get("name")
        ]

    author_text = ", ".join(authors)

    # get original description
    summary = entry.get("summary", "")

    description = (
        f"[{paper_id}]\n"
        f"Authors: {author_text}\n\n"
        f"{summary}"
    )

    fe.description(description)

Path("docs").mkdir(exist_ok=True)

fg.rss_file("docs/feed.xml")