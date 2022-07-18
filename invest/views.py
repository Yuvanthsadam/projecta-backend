from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from accounts.api.views import RegisterInvestor
from invest.models import IdeasConnection,savedIdeas
from invest.serializers import IdeasSerializer,SavedIdeasSerializers
from rest_framework import status,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from accounts.models import *

class IdeasView(GenericAPIView,mixins.RetrieveModelMixin):
    serializer_class = IdeasSerializer
    permission_classes = [AllowAny]
    queryset= IdeasConnection.objects.all()
    lookup_field = 'id'

    def get(self,request,id=None,*args, **kwargs):
        if id:
            return self.retrieve(request)
        else:
            idea = IdeasConnection.objects.all()
            serializer = IdeasSerializer(idea, many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if not User.is_seeker:
            return Response("Unauthorised", status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        user = request.user
        idx=kwargs['id']
        details=IdeasConnection.objects.get(id=idx)
        request.data["user"]=user.id

        
        if details.user.id == user.id:       
            serializer = IdeasSerializer(details,data=request.data,partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response("BAD Request",status=status.HTTP_400_BAD_REQUEST)    

    
    def delete(self,request,*args,**kwargs):
        user=request.user
        idx=kwargs['id']
        data=IdeasConnection.objects.get(id=idx)

        if data.id == idx:
            data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response("Unauthorised", status=status.HTTP_401_UNAUTHORIZED)
    
    # def get(self, request):
    #     idea = IdeasConnection.objects.all()
    #     idea_serializer = IdeasSerializer(idea, many=True)
    #     resp1 = {
    #         "code": 1,
    #         "message": "GET list success",
    #         "result": idea_serializer.data
    #     }
    #     return Response(data=resp1, status=status.HTTP_200_OK)

    def post(self, request,*args, **kwargs):
        serializer = IdeasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # print(serializer)
            resp2 = {
                "code": 1,
                "message": "Posted Successfully",
                "result": serializer.data
            }
            return Response(resp2, status=status.HTTP_200_OK)
        else:
            resp3 = {
                "code": 0,
                "message": "POST Unsuccess",
                "result": serializer.errors
            }
            return Response(resp3, status=status.HTTP_400_BAD_REQUEST)
    
    
# class IdeasListView(APIView):

#     def get(self, request, pk):
#         idea = IdeasConnection.objects.get(pk=pk)
#         idea_serializer = IdeasSerializer(idea, many=False)
#         resp1 = {
#             "code": 1,
#             "message": "Ideas Detail",
#             "result": idea_serializer.data
#         }
#         return Response(data=resp1, status=status.HTTP_200_OK)

#     def put(self, request, pk):
#         emp = IdeasConnection.objects.get(pk=pk)
#         idea_serializer = IdeasSerializer(emp, data=request.data)
#         if idea_serializer.is_valid():
#             idea_serializer.save()
#             resp4 = {
#                 "code": 1,
#                 "message": "Updated Successfully",
#                 "result": idea_serializer.data
#             }
#             return Response(data=resp4, status=status.HTTP_200_OK)
#         else:
#             resp5 = {
#                 "code": 0,
#                 "message": "NOT Updated",
#                 "result": idea_serializer.data
#             }
#             return Response(resp5, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         emp = IdeasConnection.objects.get(pk=pk)
#         emp.delete()
#         resp6 = {
#             "code": 1,
#             "message": "Deleted Successfully",
#         }
#         return Response(resp6, status=status.HTTP_200_OK)

class saveIdeas(GenericAPIView):
    serializer_class=SavedIdeasSerializers
    
    def get(self,request):
        
        queryset=savedIdeas.objects.filter(user=request.user)
        print(queryset)

        serializer=SavedIdeasSerializers(queryset,many=True).data
        return Response(serializer) 
    
    def post(self,request,*args,**kwargs):
        ideaid=kwargs["pk"]#3
        
            
        try:
            usersavedBlog=savedIdeas.objects.get(user=request.user,ideaId=ideaid)#1
            return Response({"Response": "item Exists"}, status=status.HTTP_400_BAD_REQUEST)
            print(usersavedBlog)
        except savedIdeas.DoesNotExist:

            data={"ideaId":ideaid,"user":request.user.id}

            serializer=SavedIdeasSerializers(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)