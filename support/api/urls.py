from django.urls import path, include
from support.api.views import *

urlpatterns = [
    path('feedback/', FeedBackView.as_view()),
    path('BugReport/', BugReportView.as_view()), 
] 