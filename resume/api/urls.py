from django.urls import path, include
from .views import *

urlpatterns = [
    
    path('experience/', WorkExperienceView.as_view()),# GET, POST method working
    # path('experience/<int:pk>', WorkExperienceDetailView.as_view()), # GET, DELETE method working
    
    
    path('education/', EducationView.as_view()),
    path('education/<int:pk>', EducationDetailView.as_view()),
    
    
    path('certification/', LicenseAndCerificationView.as_view()),
    path('skill/', SkillsView.as_view()),
    path('project/', ProjectsView.as_view()),
    path('award/', HonorsAndAwardsView.as_view()),
]