from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from social.models import *
from .services.mutual_connection import MutualConnectionService
from .services.connection_service import ConnectionService

class SendRequestView(APIView):
    def post(self, request, *args, **kwargs):
        serializer=SendRequestSerializer()
        serializer.save(sender_seeker=request.user.seeker.id, receiver_seeker=request.data['receiver_seeker'])
        return Response(status=status.HTTP_200_OK)

class RequestAcceptView(APIView):
    def post(self, request, *args, **kwargs):
        serializer=AcceptRequestSerializer()
        serializer.save(sender_seeker=request.data['id'], receiver_seeker=request.user.seeker.id)
        return Response(status=status.HTTP_200_OK)


class RequestRejectView(APIView):
    def post(self, request, *args, **kwargs):
        serializer=RejectRequestSerializer()
        serializer.save(sender_seeker=request.data['id'], receiver_seeker=request.user.seeker.id)
        return Response(status=status.HTTP_200_OK)

class MyRequestView(APIView):
    def get(self, request, *args, **kwargs):
        data=Connections.objects.received_requests(id=request.user.seeker.id).values()
        return Response(data, status=status.HTTP_200_OK)

class MyConnectionCountView(APIView):
    permission_classes=[AllowAny]
    def get(self, request, *args, **kwargs):
        count=ConnectionService(id=request.user.seeker).get_connection_count()
        return Response({"count": count}, status=status.HTTP_200_OK)

class MyConnectionDetailView(APIView):
    permission_classes=[AllowAny]
    def get(self, request, *args, **kwargs):
        data=ConnectionService(id=request.user.seeker.id).get_connection_details()
        return Response(data, status=status.HTTP_200_OK)

class FollowView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            Following.objects.create(sender_seeker_id=request.user.seeker.id, organization_id=request.data['organization'])
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UnFollowView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            Following.objects.filter(sender_seeker_id=request.user.seeker, organization_id=request.data['organization']).delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class FollowingView(APIView):
    def get(self, request, *args, **kwargs):
        data=Following.objects.followings(id=request.user.seeker.id).values()
        return Response(data, status=status.HTTP_200_OK)
    
class MutualConnectionCountView(APIView):
    def get(self, request, *args, **kwargs):
        count=MutualConnectionService(seeker_id=request.user.seeker.id, receiver_id=request.data['id']).get_mutual_count()
        return Response({"count":count}, status=status.HTTP_200_OK)
        

class MutualConnectionDetailView(APIView):
    def get(self, request, *args, **kwargs):
        response=MutualConnectionService(seeker_id=request.user.seeker.id, receiver_id=request.data['id']).get_mutual_connection_details()
        return Response(response, status=status.HTTP_200_OK)    

class BlogView(GenericAPIView):
    serializer_class = BlogSerializer

    def get(self, request, *args, **kwargs):
        res = Blog.objects.filter(user = request.user.id)

        data = BlogSerializer(res, many=True)
        return Response(data.data, status=status.HTTP_200_OK)

        serializer = BlogSerializer(res, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):

        data = { 'user' : request.user.id , **request.data}
        serializer = self.get_serializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request, *args, **kwargs):
        obj_id = kwargs["id"]
        obj = Blog.objects.get(id=obj_id)

        if obj.user.id == request.user.id:
            data = request.data

            for i in data:
                setattr(obj, i, data[i])
            obj.save()
            print(obj)

            return Response("Updated Ratings", status=status.HTTP_200_OK)

        return Response("Unauthorised", status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        obj_id = kwargs["id"]
        obj = Blog.objects.get(id=obj_id)

        if obj.user.id == request.user.id:
            obj.delete()

            return Response(
                {
                    "status" : "Succesfull"
                }, status=status.HTTP_200_OK
            )
        return Response("Unauthorised", status=status.HTTP_401_UNAUTHORIZED)

class saveBlog(GenericAPIView):
    serializer_class=SavedBlogSerializers
    
    def get(self,request):
        
        queryset=SavedBlogs.objects.filter(user=request.user)
        print(queryset)

        serializer=SavedBlogSerializers(queryset,many=True).data
        return Response(serializer) 
    
    def post(self,request,*args,**kwargs):
        blogid=kwargs["pk"]#3
        
            
        try:
            usersavedBlog=SavedBlogs.objects.get(user=request.user,blogId=blogid)#1
            return Response({"Response": "item Exists"}, status=status.HTTP_400_BAD_REQUEST)
            print(usersavedBlog)
        except SavedBlogs.DoesNotExist:

            data={"blogId":blogid,"user":request.user.id}

            serializer=SavedBlogSerializers(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)




class ReplyToBlogView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        blg_id = kwargs.get('pk')
        user = request.user.id
        blog = Blog.objects.get(id = blg_id)
        rpls = ReplyToBlog.objects.filter(user= user, blog = blog)

        data = ReplyToBlogSerializer(rpls, many=True).data
        
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        blg_id = kwargs.get('pk')
        user = request.user.id
        data = {
            "blog" : blg_id,
            "user": user.id,
            **request.data
        }
        serializer = self.get_serializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        obj_id = kwargs["id"]
        obj = ReplyToBlog.objects.get(id=obj_id)

        if obj.user.id == request.user.id:
            data = request.data

            for i in data:
                setattr(obj, i, data[i])
            obj.save()
            print(obj)

            return Response("Updated Ratings", status=status.HTTP_200_OK)

        return Response("Unauthorised", status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        obj_id = kwargs["id"]
        obj = ReplyToBlog.objects.get(id=obj_id)

        if obj.user.id == request.user.id:
            obj.delete()

            return Response(
                {
                    "status" : "Succesfull"
                }, status=status.HTTP_200_OK
            )
        return Response("Unauthorised", status=status.HTTP_401_UNAUTHORIZED)


class FeedView(GenericAPIView):
    serializer_class = FeedSerializer 

    def get(self, request, *args, **kwargs):
        res = Feed.objects.filter(user = request.user.id)
        serializer = FeedSerializer(res, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        
        data = { 'user' : request.user.id , **request.data}
        serializer = self.get_serializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        obj_id = kwargs["id"]
        obj = Feed.objects.get(id=obj_id)

        if obj.user.id == request.user.id:
            data = request.data

            for i in data:
                setattr(obj, i, data[i])
            obj.save()
            print(obj)

            return Response("Updated Feed", status=status.HTTP_200_OK)

        return Response("Unauthorised", status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, *args, **kwargs):
        obj_id = kwargs["id"]
        obj = Feed.objects.get(id=obj_id)

        if obj.user.id == request.user.id:
            obj.delete()

            return Response(
                {
                    "status" : "Succesfull"
                }, status=status.HTTP_200_OK
            )
        return Response("Unauthorised", status=status.HTTP_401_UNAUTHORIZED)



class saveFeed(GenericAPIView):
    serializer_class=SavedFeedSerializers
    
    def get(self,request):
        
        queryset=SavedFeed.objects.filter(user=request.user)
        print(queryset)

        serializer=SavedFeedSerializers(queryset,many=True).data
        return Response(serializer) 
    
    def post(self,request,*args,**kwargs):
        feedid=kwargs["pk"]#3
        
            
        try:
            usersavedFeed=SavedFeed.objects.get(user=request.user,feedId=feedid)#1
            return Response({"Response": "item Exists"}, status=status.HTTP_400_BAD_REQUEST)
            print(usersavedFeed)
        except SavedFeed.DoesNotExist:

            data={"feedId":feedid,"user":request.user.id}

            serializer=SavedFeedSerializers(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)




class ReplyToFeedView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        feed_id = kwargs.get('pk')
        user = request.user.id
        feed = Feed.objects.get(id = feed_id)
        rpls = ReplyToFeed.objects.filter(user= user, feed = feed)

        data = ReplyToFeedSerializer(rpls, many=True).data
        
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        blg_id = kwargs.get('pk')
        user = request.user.id
        data = {
            "blog" : blg_id,
            "user": user.id,
            **request.data
        }
        serializer = self.get_serializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        obj_id = kwargs["id"]
        obj = ReplyToFeed.objects.get(id=obj_id)

        if obj.user.id == request.user.id:
            data = request.data

            for i in data:
                setattr(obj, i, data[i])
            obj.save()
            print(obj)

            return Response("Updated Ratings", status=status.HTTP_200_OK)

        return Response("Unauthorised", status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        obj_id = kwargs["id"]
        obj = ReplyToFeed.objects.get(id=obj_id)

        if obj.user.id == request.user.id:
            obj.delete()

            return Response(
                {
                    "status" : "Succesfull"
                }, status=status.HTTP_200_OK
            )
        return Response("Unauthorised", status=status.HTTP_401_UNAUTHORIZED)

    
class MainFeed(GenericAPIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        qs = Connections.objects.filter(Q(sender_seeker = user) | Q(receiver_seeker = user))   
        follows = [user]
        for obj in qs:
            follows.append(obj.receiver_seeker)
        x = Blog.objects.filter(user__in=follows).order_by('-timestamp') 
        serializers = BlogSerializer(x, many=True).data
        return Response(serializers, status=status.HTTP_200_OK)
 