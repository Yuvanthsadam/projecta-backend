from django.contrib import admin
from .models import Job, AppliedJobs,Outsourcing, BiddingModel, Questionaire
# Register your models here.

admin.site.register(Job)
admin.site.register(AppliedJobs)
admin.site.register(Questionaire)
admin.site.register(Outsourcing)
admin.site.register(BiddingModel)

