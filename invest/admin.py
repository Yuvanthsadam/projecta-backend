from django.contrib import admin
from .models import IdeasConnection,savedIdeas

# Register your models here.

admin.site.register(IdeasConnection)
admin.site.register(savedIdeas)