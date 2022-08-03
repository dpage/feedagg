import feedparser
import dateutil.parser as dup
import pytz
import re
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand

from feeds.models import OutFeed, InFeed, Post


class Command(BaseCommand):
    help = 'Poll all the active inbound feeds and get any new posts.'

    def handle(self, *args, **options):
        # Get all the enabled feeds
        feeds = InFeed.objects.filter(enabled=True)
        recents = {}

        for feed in feeds:
            data = feedparser.parse(feed.feed_url)

            if 'entries' not in data:
                continue

            # Iterate each item, and insert/update as appropriate
            for entry in data.entries:
                # Set the timezone to UTC
                ts = dup.parse(entry.published)
                ts = ts.replace(tzinfo=pytz.UTC)

                # Strip out some bare text for the description
                soup = BeautifulSoup(entry.summary, features="html.parser")
                description = soup.text
                description = (description[:1000] + '...') if \
                    len(description) > 1000 else description
                description = description.replace('\n', '<br/> ')

                # Ensure we have a space following any full stops
                description = re.sub(r"\.(?=\S)", ". ", description)

                if 'author' in entry:
                    author = entry.author
                else:
                    author = 'Unknown'

                values = {'title': entry.title,
                          'author': author,
                          'description': description,
                          'link': entry.link,
                          'published': ts
                          }

                try:
                    post = Post.objects.get(in_feed=feed, guid=entry.id)
                    for key, value in values.items():
                        setattr(post, key, value)
                    post.save()
                except Post.DoesNotExist:
                    values['enabled'] = False
                    if feed.auto_publish:
                        values['enabled'] = True
                    values['in_feed'] = feed
                    values['guid'] = entry.id
                    post = Post(**values)
                    post.save()

                # Stash the latest publication date
                if post.enabled:
                    if feed.out_feed.id not in recents:
                        recents[feed.out_feed.id] = ts
                    else:
                        if ts > recents[feed.out_feed.id]:
                            recents[feed.out_feed.id] = ts

        for feed, latest in recents.items():
            out_feed = OutFeed.objects.get(id=feed)
            out_feed.updated=latest
            out_feed.save()





