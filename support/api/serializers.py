from rest_framework import serializers
from support.models import *
from accounts.models import User

class FeedBackSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedBack
        fields = ('user','feedback', 'suggestion')


class BugReportSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BugReport
        fields = ('user','description', 'image')
