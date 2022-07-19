from accounts.api.serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_protect
from rest_framework import generics, views
from rest_framework.generics import RetrieveAPIView
from accounts.models import *
from django.contrib.auth import login, authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from jobportal.api.serializer import JobSerializer
from dj_rest_auth.views import LoginView
from accounts.utils import send_email
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from django.db.models import Avg
from resume.models import *
from resume.api.serializers import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from rest_framework.authtoken.serializers import AuthTokenSerializer


# seeker registration
# class RegisterSeekerView(generics.GenericAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = SeekerRegistrationSerializer
#     queryset = Seeker.objects.all()

# def post(self, request, *args, **kwargs):

#     serializer = self.get_serializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     seeker = serializer.save()  # saving in db
#     data = request.data
#     # authenticating user
#     user = authenticate(username=data['email'], password=data['password'])
#     jwt_tokens = RefreshToken.for_user(user)

#     jwt_tokens['type'] = '1'

#     tokens = {
#         'refresh_token': str(jwt_tokens),
#         'access_token': str(jwt_tokens.access_token),
#     }

#     # email setup:
#     current_site = get_current_site(request).domain
#     relativeLink = reverse('email-verify')
#     absurl = 'http://'+current_site+relativeLink + \
#         "?token="+str(jwt_tokens.access_token)

#     email_body = 'Hi ' + user.seeker.first_name + \
#         ' Use the link below to verify your email \n' + absurl
#     data = {'email_body': email_body, 'to_email': user.email,
#             'email_subject': 'Verify your email'}

#     res = send_email(data)

#     print(res)

#     if res['status'] == "error":  # if email sending error
#         user.delete()  # delete user is email not sent
#         return Response({  # send response as error
#             "error": "Internal Server Error"
#         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     return Response(tokens)

# def patch(self, request, *args, **kwargs):

#     obj_id = kwargs["id"]
#     obj = Seeker.objects.get(id=obj_id)

#     if obj.user.id == request.user.id:
#         data = request.data

#         for i in data:
#             setattr(obj, i, data[i])
#         obj.save()

#         print(obj)

#         return Response("Updated Seeker", status=status.HTTP_200_OK)

#     return Response("Unauthorised", status=status.HTTP_401_UNAUTHORIZED)

class RegisterSeekerView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SeekerRegistrationSerializer
    queryset = Seeker.objects.all()

    def get(self, request):
        seeker = Seeker.objects.all()
        seeker_serializer = SeekerRegistrationSerializer(seeker, many=True)
        resp1 = {
            "code": 1,
            "message": "GET list success",
            "result": seeker_serializer.data
        }

        return Response(data=resp1, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SeekerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = request.data
            print("-----------serializer-----------" + str(serializer))
            print("--data-----------" + str(data))
            resp2 = {
                "code": 1,
                "message": "Registered successfully",
                "result": serializer.data
            }
            user = authenticate(
                username=data['email'], password=data['password'])
            jwt_tokens = RefreshToken.for_user(user)
            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            absurl = 'http://'+current_site+relativeLink + \
                "?token="+str(jwt_tokens.access_token)

            email_body = 'Hi ' + user.seeker.first_name + \
                ' Use the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email'}

            res = send_email(data)

            print(res)
            return Response(resp2, status=status.HTTP_201_CREATED)
        else:
            resp3 = {
                "code": 0,
                "message": "Not Registered",
                "result": serializer.errors
            }
            return Response(resp3)


# Organization registration
class RegisterOrganizationView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrganizationRegistrationSerializer
    queryset = Organization.objects.all()

    def get(self, request):
        org = Organization.objects.all()
        org_serializer = OrganizationRegistrationSerializer(
            org, many=True)
        resp1 = {
            "code": 1,
            "message": "GET list success",
            "result": org_serializer.data
        }

        return Response(data=resp1, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrganizationRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = request.data
            resp2 = {
                "code": 1,
                "message": "POST success",
                "result": serializer.data
            }
            # email setup:
            user = authenticate(
                username=data['email'], password=data['password'])
            jwt_tokens = RefreshToken.for_user(user)
            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            absurl = 'http://'+current_site+relativeLink + \
                "?token="+str(jwt_tokens.access_token)

            email_body = 'Hi ' + user.organization.organization_name + \
                ' Use the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email'}

            res = send_email(data)

        # if res['status'] == "error":  # if email sending error
        #     user.delete()  # delete user is email not sent
        #     return Response({  # send response as error
        #         "error": "Internal Server Error",
        #         "message": res['message']
        #     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # email setup done
            return Response(resp2, status=status.HTTP_201_CREATED)

        else:
            resp3 = {
                "code": 0,
                "message": "POST Unsuccess",
                "result": serializer.errors
            }
            return Response(resp3)

class RegisterOrganizationDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = OrganizationRegistrationSerializer

    def get(self, request, pk):
        org = Organization.objects.get(pk=pk)
        org_serializer = OrganizationRegistrationSerializer(org, many=False)
        resp1 = {
            "code": 1,
            "message": " Employee Detail",
            "result": org_serializer.data
        }
        return Response(data=resp1, status=status.HTTP_200_OK)

    def put(self, request, pk):
        org = Organization.objects.get(pk=pk)
        org_serializer = OrganizationRegistrationDetailSerializer(org, data=request.data)
        if org_serializer.is_valid():
            org_serializer.save()
            resp2 = {
                "code": 1,
                "message": "Updated Successfully",
                "result": org_serializer.data
            }
            return Response(data=resp2, status=status.HTTP_200_OK) 
        else:
            return Response(org_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     seeker = serializer.save()  # saving in db
    #     data = request.data
    #     # authenticating the user
    #     user = authenticate(username=data['email'], password=data['password'])

    #     jwt_tokens = RefreshToken.for_user(user)
    #     jwt_tokens['type'] = '2'

    #     tokens = {
    #         'refresh_token': str(jwt_tokens),
    #         'access_token': str(jwt_tokens.access_token),
    #     }

    #     # email setup:
    #     current_site = get_current_site(request).domain
    #     relativeLink = reverse('email-verify')
    #     absurl = 'http://'+current_site+relativeLink + \
    #         "?token="+str(jwt_tokens.access_token)

    #     email_body = 'Hi ' + user.organization.organization_name + \
    #         ' Use the link below to verify your email \n' + absurl
    #     data = {'email_body': email_body, 'to_email': user.email,
    #             'email_subject': 'Verify your email'}

    #     res = send_email(data)

    #     if res['status'] == "error":  # if email sending error
    #         user.delete()  # delete user is email not sent
    #         return Response({  # send response as error
    #             "error": "Internal Server Error",
    #             "message": res['message']
    #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     # email setup done

    #     return Response(tokens, status=status.HTTP_200_OK)

    # def patch(self, request, *args, **kwargs):

    #     obj_id = kwargs["id"]
    #     obj = Organization.objects.get(id=obj_id)

    #     if obj.user.id == request.user.id:
    #         data = request.data

    #         for i in data:
    #             setattr(obj, i, data[i])
    #         obj.save()

    #         print(obj)

    #         return Response("Updated Organization", status=status.HTTP_200_OK)

    #     return Response("Unauthorised", status=status.HTTP_401_UNAUTHORIZED)


class RegisterInvestor(generics.GenericAPIView):
    serializer_class = InvestorSerializer

    def post(self, request):
        serializer = InvestorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            resp2 = {
                "code": 1,
                "message": "POST success",
                "result": serializer.data
                }
            return Response(resp2, status=status.HTTP_201_CREATED)
        else:
            resp3 = {
                "code": 0,
                "message": "POST Unsuccess",
                "result": serializer.errors
                }
            return Response(resp3)

    # def post(self, request, *args, **kwargs):
    #     user = request.user

    #     if user.is_seeker:
    #         return Response({
    #             "status": "Failed"
    #         }, status=status.HTTP_401_UNAUTHORIZED)

    #     data = {'user': user.id, **request.data}
    #     serializer = self.get_serializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     ch_user = User.objects.get(email=request.user.email)
    #     ch_user.is_investor = True
    #     ch_user.save()

    #     return Response({
    #         "status": "Success"
    #     })


class RegisterEntreprenur(generics.GenericAPIView):
    serializer_class = EntreprenurSerializer

    def post(self, request):
        serializer = EntreprenurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            resp2 = {
            "code": 1,
            "message": "POST success",
            "result": serializer.data
            }
            return Response(resp2, status=status.HTTP_201_CREATED)
        else:
            resp3 = {
            "code": 0,
            "message": "POST Unsuccess",
            "result": serializer.errors
            }
            return Response(resp3)

    # def post(self, request, *args, **kwargs):

    #     user = request.user

    #     if user.is_organization:
    #         return Response({
    #             "status": "Failed"
    #         }, status=status.HTTP_401_UNAUTHORIZED)

    #     data = {'user': user.id, **request.data}
    #     serializer = self.get_serializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     ch_user = User.objects.get(email=request.user.email)
    #     ch_user.is_entreprenur = True
    #     ch_user.save()

    #     return Response({
    #         "status": "Success"
    #     })

# get seeker details


class GetSeeker(generics.GenericAPIView):
    serializer_class = SeekerSerializer
    queryset = Seeker.objects.all()

#     def get(self, request):
#         seeker = Seeker.objects.all()
#         seeker_serializer = SeekerSerializer(
#             seeker, many=True)
#         resp1 = {
#             "code": 1,
#             "message": "GET list success",
#             "result": seeker_serializer.data
#         }

#         return Response(data=resp1, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):

        if not request.user.is_verified:
            return Response({
                "error": "Not Verified User"
            })

        if 'id' in kwargs:
            seeker = User.objects.get(id=kwargs['id']).seeker
            data = SeekerSerializer(seeker).data
            # getting job list of current user
            applied_job_list = seeker.get_appliedjob_list()
            list_data = []

            for i in applied_job_list:  # creating a list of job id for organization
                list_data.append(i.id)

            return Response({**data, "applied_job_list": list_data})

        seeker = Seeker.objects.get(user=request.user)
        data = SeekerSerializer(seeker).data
        # getting job list of current user
        applied_job_list = seeker.get_appliedjob_list()
        list_data = []

        for i in applied_job_list:  # creating a list of job id for organization
            list_data.append(i.id)

        completion = seeker.completion

        if request.user.is_entreprenur:
            inv_obj = Entreprenur.objects.get(user=request.user)
            json_data = EntreprenurSerializer(inv_obj).data
            del json_data['user']
            return Response({**data, **json_data, 'completion': completion, "applied_job_list": list_data})

        return Response({**data, 'completion': completion, "applied_job_list": list_data})

# get organization details


class GetOrganization(generics.GenericAPIView):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()

    # def get(self, request):
    #     seeker = Seeker.objects.all()
    #     seeker_serializer = OrganizationSerializer(
    #         seeker, many=True)
    #     resp1 = {
    #         "code": 1,
    #         "message": "GET list success",
    #         "result": seeker_serializer.data
    #     }

    #     return Response(data=resp1, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):

        if request.user.is_verified:
            return Response({
                "error": "Not Verified User"
            })
        if 'id' in kwargs:
            organization = User.objects.get(id=kwargs['id']).organization
            data = OrganizationSerializer(organization).data
            # code updated by nitin
            # get_appliedjob_list() # getting job list of current user
            applied_job_list = organization.get_job_list()
            list_data = []

            for i in applied_job_list:  # creating a list of job id for organization
                list_data.append(i.id)

            return Response({**data, "applied_job_list": list_data})

        organization = Organization.objects.get(
            user=request.user)  # getting organization details
        # serializing the organization data
        data = OrganizationSerializer(organization).data
        job_list = organization.get_job_list()  # getting job list of current user
        list_data = []
        for i in job_list:  # creating a list of job id for organization
            list_data.append(i.id)

        if request.user.is_investor:
            inv_obj = Investor.objects.get(user=request.user)
            json_data = InvestorSerializer(inv_obj).data
            del json_data['user']
            return Response({**data, **json_data, "job_list": list_data})

        return Response({**data, "job_list": list_data})


class VerifyEmail(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        verify_token = request.GET.get('token')  # get token
        jwt = JWTAuthentication()
        token = bytes('Bearer ' + str(verify_token), 'utf-8')
        y = jwt.get_raw_token(token)
        z = jwt.get_validated_token(y)
        a = jwt.get_user(z)

        if not a.is_verified:
            a.is_verified = True
            if a.is_seeker:
                a.seeker.is_email_verified = True
                a.save()

        return Response({
            "status": "Verified"
        })


class CustomLoginView(LoginView):
    def get_response(self):
        orginal_response = super().get_response()
        orginal_response.data.pop('user')  # poping user out of login
        return orginal_response


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(
        reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        # "noreply@somehost.local",
        "sd1.bugdroid.yt@gmail.com",
        # to:
        [reset_password_token.user.email],
        fail_silently=False
    )


class GetType(views.APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        role = ""
        if user.is_seeker:
            role = "Seeker"
        if user.is_organization:
            role = "Organization"

        return Response({
            "type": role
        }, status=status.HTTP_200_OK)


class RatingOrgView(views.APIView):

    def get(self, request):
        ratings = RatingOrganization.objects.filter()
        serializer = RatingOrganizationSerializer(ratings, many=True)
        resp1 = {
            "code": 1,
            "message": "GET list success",
            "result": serializer.data
        }

        return Response(data=resp1, status=status.HTTP_200_OK)

    # def post(self, request):
    #     serializer = RatingOrganizationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         resp2 = {
    #             "code": 1,
    #             "message": "POST success",
    #             "result": serializer.data
    #         }
    #         return Response(resp2, status=status.HTTP_200_OK)
    #     else:
    #         resp3 = {
    #             "code": 0,
    #             "message": "POST Unsuccess",
    #             "result": serializer.errors
    #         }
    #         return Response(resp3)

    # def get(self, request, *args, **kwargs):
    #     # permission_classes = [AllowAny]

    #     user = User.objects.get(id=self.kwargs['id'])

    #     if user.is_seeker:
    #         return Response({
    #             "error": "Seeker doesn't have ratings"
    #         })

    #     ratings = RatingOrganization.objects.filter(
    #         organization=user.organization)
    #     serializer = RatingOrganizationSerializer(ratings, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = RatingOrganizationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "error": "Organization can't rate other Organization"
            })

        context = {
            "request": request
        }
        serializer = RatingOrganizationSerializer(
            data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        rating = serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    # def patch(self, request, *args, **kwargs):
    #     obj_id = kwargs["id"]
    #     obj = RatingOrganization.objects.get(id=obj_id)

    #     if obj.user.id == request.user.id:
    #         data = request.data

    #         for i in data:
    #             setattr(obj, i, data[i])
    #         obj.save()
    #         print(obj)

    #         return Response("Updated Ratings", status=status.HTTP_200_OK)

        # return Response("Unauthorised", status=status.HTTP_401_UNAUTHORIZED)


class RatingOrgDetailView(APIView):

    def get(self, request, pk):
        rating = RatingOrganization.objects.get(pk=pk)
        rating_serializer = RatingOrganizationSerializer(rating, many=False)
        resp1 = {
            "code": 1,
            "message": " Ratings Detail",
            "result": rating_serializer.data
        }
        return Response(data=resp1, status=status.HTTP_200_OK)

    def put(self, request, pk):
        rating = RatingOrganization.objects.get(pk=pk)
        rating_serializer = RatingOrganizationSerializer(
            rating, data=request.data)
        if rating_serializer.is_valid():
            rating_serializer.save()
            resp4 = {
                "code": 1,
                "message": "Updated Successfully",
                "result": rating_serializer.data
            }
            return Response(data=resp4, status=status.HTTP_200_OK)
        # return Response(emp_serializer.data)
        else:
            return Response(rating_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        rating = RatingOrganization.objects.get(pk=pk)
        rating.delete()
        resp5 = {
            "code": 1,
            "message": "Deleted Successfully",
        }
        return Response(data=resp5, status=status.HTTP_200_OK)


class RatingOrgAvgView(views.APIView):

    def get(self, request, *args, **kwargs):
        permission_classes = [AllowAny]

        user = User.objects.get(id=self.kwargs['id'])

        if user.is_seeker:
            return Response({
                "error": "Seeker doesn't have ratings"
            })

        ratings = RatingOrganization.objects.filter(
            organization=user.organization).aggregate(Avg('rating'))
        avg = (ratings['rating__avg']/5)*100
        return Response({"average": avg}, status=status.HTTP_200_OK)


class GetSeekerByQuery(generics.GenericAPIView):
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):

        name = self.kwargs['name']
        # getting the objects containing same name
        data = Seeker.objects.filter(first_name__icontains=name)
        print(data)
        serializer = SeekerSerializer(data, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))


class GetOrganizationByQuery(generics.GenericAPIView):
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):

        name = self.kwargs['name']
        # getting the objects containing same name
        data = Organization.objects.filter(organization_name__icontains=name)
        serializer = OrganizationSerializer(data, many=True)
        print(serializer.data)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))


class GetProfile(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        try:
            id = request.data["id"]
            user = User.objects.get(id=id).id
        except KeyError:
            user = request.user.seeker

        work = WorkExperience.objects.filter(seeker=user).values().first()
        education = Education.objects.filter(seeker=user).values().first()
        lac = LicenseAndCerification.objects.filter(
            seeker=user).values().first()
        skills = Skills.objects.filter(seeker=user).values().first()
        projects = Projects.objects.filter(seeker=user).values().first()
        honors = HonorsAndAwards.objects.filter(seeker=user).values().first()

        data = {
            "work": work,
            "education": education,
            "lac": lac,
            "skills": skills,
            "project": projects,
            "honors": honors
        }

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        if request.data["work"] != "null":
            work = WorkExperienceSerializer(data=request.data["work"])
            print("////////////////////////////////"+str(request.data["work"]))
            work.is_valid(raise_exception=True)
            try:
                workexperience = work.save(seeker=request.user.seeker)
            except:
                return Response(work.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.data["education"] != "null":
            education = EducationSerializer(data=request.data["education"])
            education.is_valid(raise_exception=True)
            try:
                education_id = education.save(seeker=request.user.seeker)
            except:
                return Response(education.errors, status=status.HTTP_400_BAD_REQUEST)

        print(request.data["lac"] != "null")

        if request.data["lac"] != "null":
            print("inside lac")
            lac = LicenseAndCerificationSerializer(data=request.data["lac"])
            lac.is_valid(raise_exception=True)
            try:
                cerification_id = lac.save(seeker=request.user.seeker)

            except:
                return Response(lac.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.data["skills"] != "null":
            skills = SkillsSerializer(data=request.data["skills"])
            skills.is_valid(raise_exception=True)
            try:
                skill_id = skills.save(seeker=request.user.seeker)

            except:
                return Response(skills.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.data["project"] != "null":
            project = ProjectsSerializer(data=request.data["project"])
            project.is_valid(raise_exception=True)
            try:
                project_id = project.save(seeker=request.user.seeker)

            except:
                return Response(project.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.data["honors"] != "null":
            honors = HonorsAndAwardsSerializer(data=request.data["honors"])
            honors.is_valid(raise_exception=True)
            try:
                honor_id = honors.save(seeker=request.user.seeker)

            except:
                return Response(honors.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message": "Success"
        }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):

        if request.data["work"] != "null":
            work = WorkExperienceSerializer(data=request.data["work"])
            work.is_valid(raise_exception=True)
            try:
                workexperience = work.save(seeker=request.user.seeker)
            except:
                return Response(work.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.data["education"] != "null":
            education = EducationSerializer(data=request.data["education"])
            education.is_valid(raise_exception=True)
            try:
                education_id = education.save(seeker=request.user.seeker)
            except:
                return Response(education.errors, status=status.HTTP_400_BAD_REQUEST)

        print(request.data["lac"] != "null")

        if request.data["lac"] != "null":
            print("inside lac")
            lac = LicenseAndCerificationSerializer(data=request.data["lac"])
            lac.is_valid(raise_exception=True)
            try:
                cerification_id = lac.save(seeker=request.user.seeker)

            except:
                return Response(lac.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.data["skills"] != "null":
            skills = SkillsSerializer(data=request.data["skills"])
            skills.is_valid(raise_exception=True)
            try:
                skill_id = skills.save(seeker=request.user.seeker)

            except:
                return Response(skills.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.data["project"] != "null":
            project = ProjectsSerializer(data=request.data["project"])
            project.is_valid(raise_exception=True)
            try:
                project_id = project.save(seeker=request.user.seeker)

            except:
                return Response(project.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.data["honors"] != "null":
            honors = HonorsAndAwardsSerializer(data=request.data["honors"])
            honors.is_valid(raise_exception=True)
            try:
                honor_id = honors.save(seeker=request.user.seeker)

            except:
                return Response(honors.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message": "Success"
        }, status=status.HTTP_200_OK)


class DeleteAccount(generics.GenericAPIView):
    def delete(self, request, *args, **kwargs):
        user = request.user
        # getting user id

        data = User.objects.get(id=user.id)
        print(data)
        user.is_active = False

        print(user.is_active)
        user.save()
        # if data.user.id==user.id:
        # print(data.is_active)
        return Response("account disabled", status=status.HTTP_204_NO_CONTENT)

        # return Response("Unauthorised",status=status.HTTP_401_UNAUTHORIZED)
