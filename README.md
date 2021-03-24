# feedagg

A relatively simple RSS feed aggregator. Allows you to setup one or more 
outbound feeds that are made available via RSS and some simple HTML pages.
Each outbound feed is fed by one or more inbound feeds that are can be 
periodically polled using a Django admin command (pollinfeeds). Each inbound
feed can be set to auto approve new posts or require manually approval, in case
the feed isn't entirely trusted to include relevant posts only.

The description of posts can be overridden to account for poor quality upstream 
feeds. 