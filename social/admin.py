from django.contrib import admin
from .models import Connections, Feed, Blog,SavedBlogs,SavedFeed

# Register your models here.
admin.site.register(Connections)
admin.site.register(Feed)
admin.site.register(Blog)
admin.site.register(SavedBlogs)
admin.site.register(SavedFeed)