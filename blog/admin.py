from django.contrib import admin

from blog.models import Blog


# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "content", "preview", "created_at", "views_count")
    list_filter = ("title", "created_at", "views_count")
    search_fields = ("title", "content")
