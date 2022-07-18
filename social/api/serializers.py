from rest_framework import serializers
from social.models import *
from accounts.models import *
from django.utils.timezone import now



class SendRequestSerializer(serializers.Serializer):
    def save(self, *args, **kwargs):
        connections=Connections.objects.filter(sender_seeker_id=kwargs['sender_seeker'], receiver_seeker_id=kwargs['receiver_seeker']).first()
        if connections:
            raise Exception("User already requested.")
        connections=Connections.objects.filter(sender_seeker_id=kwargs['receiver_seeker'], receiver_seeker_id=kwargs['sender_seeker'], is_requested=True).first()
        if connections:
            raise Exception("The user which youre requesting has already requested you. You can accept or decline the request.")
        try:
            Connections.objects.create(sender_seeker_id=kwargs['sender_seeker'], receiver_seeker_id=kwargs['receiver_seeker'])
        except:
            raise Exception("Unable to send request.")

class AcceptRequestSerializer(serializers.Serializer):
    def save(self, *args, **kwargs):
        try:
            connections=Connections.objects.filter(sender_seeker_id=kwargs['sender_seeker'], receiver_seeker_id=kwargs['receiver_seeker'], is_requested=True).first()
            connections.is_requested=False
            connections.is_accepted=True
            connections.accept_date=now()
            connections.save()
        except:
            raise Exception("Unable to accept request")

class RejectRequestSerializer(serializers.Serializer):
    def save(self, *args, **kwargs):
        connections=Connections.objects.filter(sender_seeker_id=kwargs['sender_seeker'], receiver_seeker_id=kwargs['receiver_seeker'], is_requested=True).first()
        if connections:
            connections.delete()


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
class ReplyToBlogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReplyToBlog
        fields = '__all__'



class SavedBlogSerializers(serializers.ModelSerializer):
    class Meta:
        model=SavedBlogs
        fields="__all__"


class FeedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Feed
        fields = '__all__'




class SavedFeedSerializers(serializers.ModelSerializer):
    class Meta:
        model=SavedFeed
        fields="__all__"


class ReplyToFeedSerializer(serializers.Serializer):

    class Meta:
        model = ReplyToFeed
        fields = '__all__'

    
