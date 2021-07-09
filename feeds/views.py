from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from feedgen.feed import FeedGenerator

from .models import OutFeed, InFeed, Post


def index(request):
    """
    Return the index page
    :param request: The request object.
    :return: The rendered page.
    """
    feeds = OutFeed.objects.filter(enabled=True)
    context = {'feeds': feeds}
    return render(request, 'feeds/index.html', context)


def posts(request, slug):
    """
    Return the list of posts for a given feed
    :param request: The request object.
    :param slug: The slug for the feed.
    :return: The rendered page.
    """
    feed = OutFeed.objects.get(enabled=True, slug=slug)
    posts = Post.objects.filter(enabled=True, in_feed__out_feed__slug=slug)
    context = {'feed': feed, 'posts': posts}
    return render(request, 'feeds/posts.html', context)


def feed(request, slug):
    """
    Return an RSS feed
    :param request: The request object.
    :param slug: The slug for the requested feed.
    :return: The rendered feed.
    """
    out_feed = get_object_or_404(OutFeed, slug=slug)

    url = "{}://{}{}".format(request.scheme, request.get_host(),
                             reverse('posts', args=[slug]))

    fg = FeedGenerator()
    fg.id(url)
    fg.title(out_feed.title)
    fg.link(href=url, rel='alternate')
    fg.description(out_feed.description)
    fg.pubDate(out_feed.updated)

    in_feeds = InFeed.objects.filter(out_feed=out_feed, enabled=True)
    posts = Post.objects.filter(in_feed__in=[f.id for f in in_feeds],
                                enabled=True)

    for post in posts:
        if post.override_desc is not None and post.override_desc != '':
            description = post.override_desc
        else:
            description = post.description

        description = description + ' [<a href="{}">Continue reading...</a>]'.\
            format(post.link)

        fe = fg.add_entry()
        fe.id(post.id)
        fe.title(post.title)
        fe.description(description)
        fe.author({'name': post.author})
        fe.link(href=post.link)
        fe.guid(post.guid)

        if post.override_pub is not None:
            fe.pubDate(post.override_pub)
            fe.updated(post.override_pub)
        else:
            fe.pubDate(post.published)
            fe.updated(post.published)

    data = fg.atom_str(pretty=True)

    response = HttpResponse(data, content_type='application/rss+xml')
    response['Content-Length'] = len(data)

    return response
