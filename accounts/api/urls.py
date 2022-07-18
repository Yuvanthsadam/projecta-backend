from django.urls import path, include
from accounts.api.views import *
from rest_framework.authtoken.views import obtain_auth_token

                                # MAIN_PROJECT_YUVANTH

urlpatterns = [
    
    path('login/', CustomLoginView.as_view()), #working
    path('DeleteAccount/', DeleteAccount.as_view()),
    
    path('seekerdetails/', GetSeeker.as_view()),
    path('seekerdetails/<id>/', GetSeeker.as_view()),
    
    
    path('registerseeker/', RegisterSeekerView.as_view()), # POST method working
    path('getSeeker/<str:name>/', GetSeekerByQuery.as_view()),# Get method working
    
    path('registerorganization/', RegisterOrganizationView.as_view()), #POST method working
    path('ratingorg/', RatingOrgView.as_view()), # GET method working
    # path('ratingorg/<int:id>/', RatingOrgView.as_view()),
    path('ratingorg/<int:pk>/', RatingOrgDetailView.as_view(), name='rating-detail'),# GET,DELETE method working
    path('ratingAvg/<int:id>/', RatingOrgAvgView.as_view()),
    
    path('registerinvestor/', RegisterInvestor.as_view()), #POST method working
    path('registerentreprenur/', RegisterEntreprenur.as_view()),#POST method working
    
    path('job/', include('jobportal.api.urls')),
    path('organizationdetails/', GetOrganization.as_view()),
    path('organizationdetails/<id>', GetOrganization.as_view()),
    
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    
    path('type/', GetType.as_view()),
    
    
    path('getOrganization/<str:name>/', GetOrganizationByQuery.as_view()),# Get Method working
    path('getProfile/', GetProfile.as_view()),
    
]   