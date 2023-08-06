from django.contrib import admin

from .models import Dictionary, Newsletter, RssFeed


class NewsletterAdmin(admin.ModelAdmin):
    pass


class DictionaryAdmin(admin.ModelAdmin):
    search_fields = ("word", "pronunciation")
    list_display = ("word", "pronunciation")


class RssFeedAdmin(admin.ModelAdmin):
    search_fields = ("user", "feed")
    list_display = ("user", "feed")
    readonly_fields = ("feed",)
    raw_id_fields = ("user",)


admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Dictionary, DictionaryAdmin)
admin.site.register(RssFeed, RssFeedAdmin)
