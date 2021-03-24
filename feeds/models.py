from django.db import models
from django.template.defaultfilters import slugify


class OutFeed(models.Model):
    """
    Represents an outbound RSS feed
    """
    title = models.CharField(null=False, blank=False, max_length=1024,
                             help_text="The title of the feed.")
    slug = models.SlugField(null=False, blank=True, max_length=100,
                            unique=True,
                            help_text="The string to use to identify this feed"
                                      " in URLs. Leave blank to auto-generate "
                                      " from the title.")
    enabled = models.BooleanField(null=False, blank=False,
                                  help_text="Determines whether or not this "
                                            "item is enabled.",
                                  verbose_name="Enabled?")
    description = models.TextField(null=False, blank=False,
                                   help_text="The description of the feed.")
    updated = models.DateTimeField(auto_now=False, auto_now_add=False,
                                   null=False,
                                   help_text="The date/time the content of the"
                                             " feed last changed.")

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super(OutFeed, self).save(*args, **kwargs)


class InFeed(models.Model):
    """
    Represents an inbound RSS feed
    """
    name = models.CharField(null=False, blank=False, max_length=1024,
                            help_text="The name of the feed.")
    enabled = models.BooleanField(null=False, blank=False,
                                  help_text="Determines whether or not this"
                                            " item is enabled.",
                                  verbose_name="Enabled?")
    out_feed = models.ForeignKey(OutFeed, on_delete=models.CASCADE,
                                 help_text="Select the outbound feed to which"
                                           " this feed will be linked.")
    feed_url = models.CharField(null=False, blank=False, max_length=1024,
                                help_text="The URL of the feed.")
    auto_publish = models.BooleanField(null=False, blank=False, default=False,
                                       help_text="Automatically publish posts"
                                                 " from this feed?",
                                       verbose_name="Auto publish?")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name + ' -> ' + self.out_feed.title


class Post(models.Model):
    """
    Represents an individual blog post
    """
    in_feed = models.ForeignKey(InFeed, on_delete=models.CASCADE,
                                help_text="The inbound found from where the"
                                          " post originated.")
    enabled = models.BooleanField(null=False, blank=False, default=False,
                                  help_text="Determines whether or not this"
                                            " item is enabled.",
                                  verbose_name="Enabled?")
    title = models.CharField(null=False, blank=False, max_length=1024,
                             help_text="The title of the post.")
    author = models.CharField(null=False, blank=False, max_length=1024,
                              help_text="The author of the post.")
    description = models.TextField(null=False, blank=False,
                                   help_text="The description or summary of"
                                             " the post.")
    override_desc = models.TextField(null=True, blank=False,
                                     help_text="The description or summary of"
                                               " the post. Overrides the auto-"
                                               "fetched description.")
    link = models.CharField(null=False, blank=False, max_length=1024,
                            help_text="The URL of the post.")
    guid = models.CharField(null=False, blank=False, max_length=1024,
                            help_text="The unique ID of the post.")
    published = models.DateTimeField(auto_now=False, auto_now_add=False,
                                     null=False,
                                     help_text="The publication date/time of"
                                               " the post.")

    class Meta:
        ordering = ['-published', 'in_feed__name', 'title']
        unique_together = [['in_feed', 'guid']]

    def __str__(self):
        return self.in_feed.name + ': ' + self.title
