from django.urls import path, include
from invest.views import *

urlpatterns = [
    path('ideas/', IdeasView.as_view()),
    path('ideas/<int:pk>/', IdeasView.as_view()), 
    path('savedidea', saveIdeas.as_view()),
    path('ideas/<int:pk>/saveidea', saveIdeas.as_view()), 
] 