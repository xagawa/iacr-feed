import feedparser
from email.utils import formatdate
from feedgen.feed import FeedGenerator
from pathlib import Path

SOURCE = "https://eprint.iacr.org/rss/rss.xml?order=recent"

feed = feedparser.parse(SOURCE)

fg = FeedGenerator()
fg.title("IACR ePrint Recent")
fg.link(href="https://eprint.iacr.org/")
fg.description("Mirror feed for Slack")
fg.language("en")

for entry in feed.entries[:100]:

    fe = fg.add_entry()

    fe.title(entry.get("title", ""))

    link = entry.get("link", "")
    fe.link(href=link)

    fe.guid(link, permalink=True)

    if "published_parsed" in entry:
        fe.pubDate(formatdate())

    summary = entry.get("summary", "")
    fe.description(summary)

Path("docs").mkdir(exist_ok=True)

fg.rss_file("docs/feed.xml")
