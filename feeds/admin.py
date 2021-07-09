from django.contrib import admin
from . import models


class OutFeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'enabled', 'slug')


class InFeedAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'enabled', 'feed_url')


class PostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'published', 'override_pub', 'enabled')
    list_filter = ('enabled', 'in_feed')


admin.site.register(models.OutFeed, OutFeedAdmin)
admin.site.register(models.InFeed, InFeedAdmin)
admin.site.register(models.Post, PostAdmin)
