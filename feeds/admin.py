from django.contrib import admin
from django.db.models import TextField
from django.forms import Textarea
from django.utils.safestring import mark_safe

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
    date_hierarchy = 'error_time'
    readonly_fields = ('error_time', 'in_feed', 'error_summary', 'error_code',)
    fields = ('error_time', 'in_feed', 'error_summary', 'error_code', 'error_message')

    def has_add_permission(self, request, obj=None):
        return False

    def has_update_permission(self, request, obj=None):
        return False

    formfield_overrides = {
        TextField: dict(widget=Textarea(attrs=dict(readonly=True)))
    }


admin.site.register(models.OutFeed, OutFeedAdmin)
admin.site.register(models.InFeed, InFeedAdmin)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.PollError, PollErrorAdmin)
