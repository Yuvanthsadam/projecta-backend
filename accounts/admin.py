from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Seeker, Organization, RatingOrganization, User,Investor, Entreprenur

# Register your models here.

User = get_user_model()

admin.site.register(User)
admin.site.register(Seeker)
admin.site.register(Organization)
admin.site.register(RatingOrganization)
admin.site.register(Investor)
admin.site.register(Entreprenur)