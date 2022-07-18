from numpy import MAY_SHARE_BOUNDS
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from resume.models import *


def myjson(code, message, result):
    return {
        "code": code,
        "message": message,
        "result": result
    }


class WorkExperienceView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            id = request.data['id']
        except KeyError:
            id = None
        if id:
            try:
                response = WorkExperience.objects.filter(
                    seeker_id=request.user.seeker, id=request.data['id']).values().first()
            except WorkExperience.DoesNotExist:
                raise Exception("No record with this id.")
        else:
            response = WorkExperience.objects.filter(
                seeker=request.user.seeker).values()
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = WorkExperienceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workexperience_id = serializer.save(seeker=request.user.seeker)
        return Response({"id": workexperience_id}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = WorkExperienceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            workexperience_id = serializer.save(seeker=request.user.seeker)
            return Response(workexperience_id, status=status.HTTP_200_OK)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            WorkExperience.objects.filter(
                seeker=request.user.seeker, id=request.data['id']).first().delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request):
    #     we = WorkExperience.objects.all()
    #     we_serializer = WorkExperienceSerializer(we, many=True)
        # resp1 = {
        #     "code": 1,
        #     "message": "GET list success",
        #     "result": we_serializer.data
        # }
        # resp1 = myjson(1, "GET success", we_serializer.data)
        # return Response(data=resp1, status=status.HTTP_200_OK)

    # def post(self, request):
    #     serializer = WorkExperienceSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
            # serializer.save(seeker=request.data)
            # workexperience_id = serializer.save(seeker=request.user)
            # resp2 = {
            #     "code": 1,
            #     "message": "POST success",
            #     "result": workexperience_id.data
            # }
        #     resp2 = myjson(1, "POST success", workexperience_id.data)
        #     return Response(resp2, status=status.HTTP_201_CREATED)
        # else:
        #     resp3 = {
        #         "code": 0,
        #         "message": "POST Unsuccess",
        #         "result": serializer.errors
        #     }
        #     return Response(resp3)


# class WorkExperienceDetailView(APIView):

    # def get(self, request, pk):
    #     we = WorkExperience.objects.get(pk=pk)
    #     we_serializer = WorkExperienceSerializer(we, many=False)
    #     resp4 = {
    #         "code": 1,
    #         "message": " Employee Detail",
    #         "result": we_serializer.data
    #     }
    #     return Response(data=resp4, status=status.HTTP_200_OK)

    # def put(self, request, pk):
    #     we = WorkExperience.objects.get(pk=pk)
    #     we_serializer = WorkExperienceSerializer(we, data=request.data)
    #     if we_serializer.is_valid():
    #         we_serializer.save(seeker=request.user.seeker)
    #         resp4 = {
    #             "code": 1,
    #             "message": "Updated Successfully",
    #             "result": we_serializer.data
    #         }
    #         return Response(data=resp4, status=status.HTTP_200_OK)
    #     else:
    #         return Response(we_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk):
    #     we = WorkExperience.objects.get(pk=pk)
    #     we.delete()
    #     resp6 = {
    #         "code": 1,
    #         "message": "Deleted Successfully",
    #     }
    #     return Response(data=resp6, status=status.HTTP_200_OK)

    # def get(self, request, *args, **kwargs):
    #     try:
    #         id=request.data['id']
    #     except KeyError:
    #         id=None
    #     if id:
    #         try:
    #             response=WorkExperience.objects.filter(seeker_id=request.user.seeker, id=request.data['id']).values().first()
    #         except WorkExperience.DoesNotExist:
    #             raise Exception("No record with this id.")
    #     else:
    #         response=WorkExperience.objects.filter(seeker=request.user.seeker).values()
    #     return Response(response, status=status.HTTP_200_OK)

    # def post(self, request, *args, **kwargs):
    #     serializer=WorkExperienceSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     workexperience_id=serializer.save(seeker=request.user.seeker)
    #     return Response({"id":workexperience_id}, status=status.HTTP_200_OK)

    # def put(self, request, *args, **kwargs):
    #     serializer = WorkExperienceSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     try:
    #         workexperience_id = serializer.save(seeker=request.user.seeker)
    #         return Response(workexperience_id, status=status.HTTP_200_OK)
    #     except:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, *args, **kwargs):
    #     try:
    #         WorkExperience.objects.filter(seeker=request.user.seeker, id=request.data['id']).first().delete()
    #         return Response(status=status.HTTP_200_OK)
    #     except:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)


class EducationView(APIView):

    def get(self, request):
        edu = Education.objects.all()
        edu_serializer = EducationSerializer(edu, many=True)
        resp1 = {
            "code": 1,
            "message": "GET list success",
            "result": edu_serializer.data
        }

        return Response(data=resp1, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(seeker=request.user.seeker)
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
            return Response(resp3)


class EducationDetailView(APIView):

    def get(self, request, pk):
        edu = Education.objects.get(pk=pk)
        edu_serializer = EducationSerializer(edu, many=False)
        resp4 = {
            "code": 1,
            "message": " Employee Detail",
            "result": edu_serializer.data
        }
        return Response(data=resp4, status=status.HTTP_200_OK)

    # def put(self, request, pk):
    #     edu = Education.objects.get(pk=pk)
    #     edu_serializer = EducationSerializer(edu, data=request.data)
    #     if edu_serializer.is_valid():
    #         edu_serializer.save(seeker=request.user.seeker)
    #         resp4 = {
    #             "code": 1,
    #             "message": "Updated Successfully",
    #             "result": edu_serializer.data
    #         }
    #         return Response(data=resp4, status=status.HTTP_200_OK)
    #     else:
    #         return Response(edu_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        edu = Education.objects.get(pk=pk)
        edu.delete()
        resp6 = {
            "code": 1,
            "message": "Deleted Successfully",
        }
        return Response(data=resp6, status=status.HTTP_200_OK)

    # def get(self, request, *args, **kwargs):
    #     try:
    #         id=request.data['id']
    #     except KeyError:
    #         id=None
    #     if id:
    #         try:
    #             response=Education.objects.filter(seeker_id=request.user.seeker, id=request.data['id']).values().first()
    #         except Education.DoesNotExist:
    #             raise Exception("No record with this id.")
    #     else:
    #         response=Education.objects.filter(seeker=request.user.seeker).values()
    #     return Response(response, status=status.HTTP_200_OK)

    # def post(self, request, *args, **kwargs):
    #     serializer=EducationSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     try:
    #         education_id=serializer.save(seeker=request.user.seeker)
    #         return Response({"id":education_id}, status=status.HTTP_200_OK)
    #     except:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        edu_serializer = EducationSerializer(data=request.data)
        edu_serializer.is_valid(raise_exception=False)
        try:
            edu_id = edu_serializer.save(seeker=request.user.seeker)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(edu_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, *args, **kwargs):
    #     try:
    #         Education.objects.filter(seeker=request.user.seeker, id=request.data['id']).first().delete()
    #         return Response(status=status.HTTP_200_OK)
    #     except:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)


class LicenseAndCerificationView(APIView):

    # def my_json(code, message):
    #     return {"code": code, "message": message}

    def get(self, request, *args, **kwargs):
        # id = request.data['id']
        print(request.user.seeker)
        # serializer = LicenseAndCerificationSerializer(data=request.data)
        # serializer.is_valid(raise_exception=False)
        try:
            id = request.data

            # return Response(resp, status=status.HTTP_200_OK)
        except KeyError:
            id = None
        if id:
            try:
                response = LicenseAndCerification.objects.filter(
                    seeker=request.user.seeker, id=request.data['id']).values().first()
                resp = {
                    "code": 1,
                    "message": "GET LIST",
                    "result": response
                }
                return Response(resp, status=status.HTTP_200_OK)
            except LicenseAndCerification.DoesNotExist:
                raise Exception("No record with this id.")
        else:
            response = LicenseAndCerification.objects.filter(
                seeker=request.user.seeker).values()
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = LicenseAndCerificationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            cerification_id = serializer.save(seeker=request.user.seeker)
            resp = {
                "code": 1,
                "message": "POST Success",
                "result": serializer.data
            }
            return Response(resp, status=status.HTTP_200_OK)
        # return Response({"id":cerification_id}, status=status.HTTP_200_OK)
        else:
            resp = {
                "code": 0,
                "message": "POST Unsuccess",
                "result": serializer.errors
            }
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        serializer = LicenseAndCerificationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            cerification_id = serializer.save(seeker=request.user.seeker)
            resp = {
                "code": 1,
                "message": "Updated Successfully",
                "result": serializer.data
            }
            return Response(resp, status=status.HTTP_200_OK)
        else:
            resp = {
                "code": 0,
                "message": "NOT Updated",
                "result": serializer.errors
            }
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        if LicenseAndCerification.objects.filter(
                seeker=request.user.seeker, id=request.data['id']).first().delete():
            resp = {
                "code": 1,
                "message": "Deleted Successfully",
            }
            return Response(resp, status=status.HTTP_200_OK)
        else:
            resp = {
                "code": 0,
                "message": "Delete UnSuccess",
            }
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SkillsView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            id = request.data['id']
        except KeyError:
            id = None
        if id:
            try:
                response = Skills.objects.filter(
                    seeker_id=request.user.seeker, id=request.data['id']).values().first()
            except Skills.DoesNotExist:
                raise Exception("No record with this id.")
        else:
            response = Skills.objects.filter(
                seeker=request.user.seeker).values()
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = SkillsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            skill_id = serializer.save(seeker=request.user.seeker)
            return Response({"id": skill_id}, status=status.HTTP_200_OK)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            Skills.objects.filter(seeker=request.user.seeker,
                                  id=request.data['id']).first().delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProjectsView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            id = request.data['id']
        except KeyError:
            id = None
        if id:
            try:
                response = Projects.objects.filter(
                    seeker_id=request.user.seeker, id=request.data['id']).values().first()
            except Projects.DoesNotExist:
                raise Exception("No record with this id.")
        else:
            response = Projects.objects.filter(
                seeker=request.user.seeker).values()
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ProjectsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            project_id = serializer.save(seeker=request.user.seeker)
            return Response({"id": project_id}, status=status.HTTP_200_OK)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        serializer = ProjectsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            project_id = serializer.save(seeker=request.user.seeker)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            Projects.objects.filter(
                seeker=request.user.seeker, id=request.data['id']).first().delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class HonorsAndAwardsView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            id = request.data['id']
        except KeyError:
            id = None
        if id:
            try:
                response = HonorsAndAwards.objects.filter(
                    seeker_id=request.user.seeker, id=request.data['id']).values().first()
            except HonorsAndAwards.DoesNotExist:
                raise Exception("No record with this id.")
        else:
            response = HonorsAndAwards.objects.filter(
                seeker=request.user.seeker).values()
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = HonorsAndAwardsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            honor_id = serializer.save(seeker=request.user.seeker)
            return Response({"id": honor_id}, status=status.HTTP_200_OK)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        serializer = HonorsAndAwardsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            honor_id = serializer.save(seeker=request.user.seeker)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            HonorsAndAwards.objects.filter(
                seeker=request.user.seeker, id=request.data['id']).first().delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
