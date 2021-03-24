import feedparser
import pprint


def feedagg():
    d = feedparser.parse(
        'https://www.enterprisedb.com/blog/rss/feed?author=dave-page')

    for post in d.entries:
        print('ID: {}, published: {}, title: {}, URL: {}'.format(post.id, post.published, post.title, post.link))
        print(post.summary)

    d = feedparser.parse(
        'https://pgsnake.blogspot.com/feeds/posts/default')

    for post in d.entries:
        print('ID: {}, published: {}, title: {}, URL: {}'.format(post.id, post.published, post.title, post.link))
        print(post.summary)

if __name__ == '__main__':
    feedagg()
