from django.contrib import admin
from . import models


class OutFeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'enabled', 'slug')


class InFeedAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'enabled', 'feed_url')


class PostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'published', 'override_pub', 'enabled')
    list_filter = ('enabled', 'in_feed')


class PollErrorAdmin(admin.ModelAdmin):
    list_display = ('error_time', 'in_feed', 'error_summary')
    list_filter = ('in_feed', 'error_code')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(models.OutFeed, OutFeedAdmin)
admin.site.register(models.InFeed, InFeedAdmin)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.PollError, PollErrorAdmin)
