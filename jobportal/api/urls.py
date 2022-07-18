from django.urls import path, include
from jobportal.api.views import *

urlpatterns = [
    path('create-job/', JobCreateView.as_view()),
    path('RUD/<int:jid>/', JobRUDView.as_view()),
    path('apply/<int:jid>/', ApplyJobView.as_view()),
    path('getJobs/', GetJobs.as_view()),
    path('getOrgJobs/', GetOrgJobs.as_view()),
    path('getApplicants/<int:jid>/', GetApplicants.as_view()),
    path('getAppliedJobs/', GetJobListApplicant.as_view()),
    path('questionaire/<int:id>/', QuestionaireView.as_view()),
    path('answernaire/<int:id>/', AnswernaireView.as_view()),
    path('Outsourcing/', CreateOutsourcing.as_view()), 
    path('Outsourcing/<int:pk>', CreateOutsourcing.as_view()), 
    path('searchOutsourcing/', searchOutsourcing.as_view()),
    path('Outsourcing/<int:pk>/placeBid/', placeBid.as_view()), 
    path('myBids/', myBids.as_view()), 
] 