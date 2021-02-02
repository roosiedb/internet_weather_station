import feedparser

rss_articles = []

rss_url = "https://www.nu.nl/rss/Algemeen"

def downloadRss():
    newsfeed = feedparser.parse(rss_url)
    rss_articles.clear()
    print("============================================")
    for article in newsfeed.entries:
        rss_articles.append(
            {"title":       article.title,
             "description": article.description,
             "published":     article.published
            }
        )
        print("title:          " + article.title)
        #print("description:    " + article.description)
        print("published:      " + article.published)

        






