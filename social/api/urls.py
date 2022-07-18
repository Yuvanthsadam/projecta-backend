from django.urls import path, include
from .views import *

urlpatterns = [
    path('request/send/', SendRequestView.as_view()),
    path('request/accept/', RequestAcceptView.as_view()),
    path('request/reject/', RequestRejectView.as_view()),
    path('requests/', MyRequestView.as_view()),
    path('connection/count/', MyConnectionCountView.as_view()),
    path('connection/detail/', MyConnectionDetailView.as_view()),
    path('follow/', FollowView.as_view()),
    path('unfollow/', UnFollowView.as_view()),
    path('followings/', FollowingView.as_view()),
    path('mutual/connections/count/', MutualConnectionCountView.as_view()),
    path('mutual/connections/detail/', MutualConnectionDetailView.as_view()),
    path('blog/', BlogView.as_view()),

    path('blog/<int:id>/', BlogView.as_view()),

    path('saveBlog/', saveBlog.as_view()),
    path('blog/<int:pk>/saveBlog', saveBlog.as_view()),
   

    path('replytoblog/', ReplyToBlogView.as_view()),
    path('replytoblog/<int:id>/', ReplyToBlogView.as_view()),
    path('feed/', FeedView.as_view()),

    path('feed/<int:id>/', FeedView.as_view()),

    path('saveFeed/', saveFeed.as_view()),
    path('feed/<int:pk>/saveFeed', saveFeed.as_view()),
    

    path('replytofeed/', ReplyToFeedView.as_view()),
    path('replytofeed/<int:id>/', ReplyToFeedView.as_view()),
    path('mainfeed/', MainFeed.as_view())
]
