import re
from pathlib import Path
from email.utils import parsedate_to_datetime

import feedparser
from feedgen.feed import FeedGenerator

SOURCE = "https://eprint.iacr.org/rss/rss.xml?order=recent"

feed = feedparser.parse(SOURCE)

fg = FeedGenerator()
fg.title("IACR ePrint Recent")
fg.link(href="https://eprint.iacr.org/")
fg.description("Mirror feed for Slack")
fg.language("en")
fg.ttl(180)

#
# Sort by pubDate in descending order (newest first)
#
entries = sorted(
    feed.entries,
    key=lambda e: e.get("published_parsed", (0,) * 9),
    reverse=True,
)

for entry in entries:

    fe = fg.add_entry()

    title = entry.get("title", "")
    link = entry.get("link", "")

    fe.title(title)
    fe.link(href=link)
    fe.guid(link, permalink=True)

    #
    # Use the original pubDate from the RSS feed
    #
    pub_date = entry.get("published", "")
    if pub_date:
        fe.pubDate(parsedate_to_datetime(pub_date))

    #
    # Paper ID
    #
    paper_id = ""
    m = re.search(r"eprint\.iacr\.org/(\d{4}/\d+)", link)
    if m:
        paper_id = m.group(1)

    #
    # List of authors
    #
    authors = []

    if "authors" in entry:
        authors = [
            a.get("name", "")
            for a in entry.authors
            if a.get("name")
        ]

    author_text = ", ".join(authors)

    #
    # Original summary
    #
    summary = entry.get("summary", "")

    description = (
        f"Paper: {paper_id}\n\n"
        f"Authors: {author_text}\n\n"
        f"Summary: {summary}"
    )

    fe.description(description)

Path("docs").mkdir(exist_ok=True)

fg.rss_file("docs/feed.xml")