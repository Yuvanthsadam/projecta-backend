from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework import status, permissions, exceptions
from rest_framework.response import Response
from support.api.serializers import *
from accounts.models import User
from support.models import FeedBack


class FeedBackView(GenericAPIView):
    serializer_class = FeedBackSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        fb = FeedBack.objects.filter(user=request.user.id)
        fb_serializer = FeedBackSerializer(fb, many=True)
        resp1 = {
            "code": 1,
            "message": "GET list success",
            "result": fb_serializer.data
        }
        return Response(resp1, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user.id
        serializer = self.get_serializer(data={**request.data, "user": user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            resp2 = {
                "code": 1,
                "message": "POST success",
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


class BugReportView(GenericAPIView):
    serializer_class = BugReportSerializer
    permission_classes = [AllowAny]

    # def get(self, request):
    #     br = BugReport.objects.filter(user=request.user.id)
    #     br_serializer = BugReportSerializer(br, many=True)
    #     resp1 = {
    #         "code": 1,
    #         "message": "GET list success",
    #         "result": br_serializer.data
    #     }
    #     return Response(resp1, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user.id
        serializer = self.get_serializer(
            data={"description": request.data["description"], "image": request.data["image"], "user": user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            resp2 = {
                "code": 1,
                "message": "POST success",
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
