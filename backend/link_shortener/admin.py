from django.contrib import admin

from link_shortener.models import Link


# Register your models here.
@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("id", "url", "short_url_hash")
    search_fields = ("url", "short_url_hash")
    list_filter = ("short_url_hash",)
    readonly_fields = ("short_url_hash",)
    fieldsets = ((None, {"fields": ("url", "short_url_hash")}),)
