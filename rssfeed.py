import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from flask import Flask, Response

app = Flask(__name__)

@app.route("/cambridge.xml")
def cambridge_feed():
    url = "https://www.cam.ac.uk/news-feed-generator.rss?field_taxonomy_section_tid=3"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "xml")

    fg = FeedGenerator()
    fg.title("Cambridge Research News")
    fg.link(href="https://www.cam.ac.uk/news", rel="alternate")
    fg.description("Cleaned RSS feed for Yodeck")

    for entry in soup.find_all("entry"):
        fe = fg.add_entry()
        fe.title(entry.title.text)
        fe.link(href=entry.link["href"])
        fe.description(entry.summary.text)

    xml = fg.rss_str(pretty=True)
    return Response(xml, mimetype="application/rss+xml")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # use Render's port or default to 5000
    app.run(host="0.0.0.0", port=port)


