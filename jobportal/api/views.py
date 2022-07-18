from rest_framework.decorators import api_view
from rest_framework.response import Response
from jobportal.models import *
from rest_framework.generics import CreateAPIView,ListCreateAPIView, GenericAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView,ListAPIView
from jobportal.api.serializer import *
from rest_framework.permissions import AllowAny
from rest_framework import status, permissions, exceptions
from rest_framework.views import APIView
from accounts.views import get_organization, get_seeker
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

#view for creating a job
class JobCreateView(GenericAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.all()

    def post(self, request, *args, **kwargs):
        if not request.user.is_organization:
            return Response({
                "error" : "Unauthorized User"
            }, status=status.HTTP_401_UNAUTHORIZED)

        org = get_organization(pk=request.user)
        serializer = self.get_serializer(data={**request.data, "organization": org.id})
        serializer.is_valid(raise_exception=True)
        job = serializer.save()
        data = JobSerializer(job).data
        return Response(data)


# job retrieve update destroy view
class JobRUDView(RetrieveUpdateDestroyAPIView):

    serializer_class = JobSerializer
    
    def get_object(self):
        try:
            return Job.objects.get(id=self.kwargs['jid'], organization=self.request.user.organization)
        except Exception as e:
            raise exceptions.PermissionDenied(detail="You dont own the job")


#view for applying for job
class ApplyJobView(GenericAPIView):

    def post(self, request, *args, **kwargs):
        try:
            job = Job.objects.get(id=self.kwargs['jid'])
            check = AppliedJobs.objects.filter(seeker=request.user.seeker, job = job).exists()
            if check:
                return Response({
                    "msg" : "Applied"
                })

            applied_job = AppliedJobs.objects.create(
                seeker = request.user.seeker,
                job = Job.objects.get(id=self.kwargs['jid']))

            return Response({
                "msg" : "Applied"
            })
        except Exception as e:
            print(e)
            return Response({"Response": "Invalid user-id or job-id"}, status=status.HTTP_400_BAD_REQUEST)


#get jobs available w/wo applying the filter
class GetJobs(ListAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['state']

    # def get(self, request, *args, **kwargs):
        
    #     parameters = {field_name: value for field_name, value in request.GET.items()}
    
    #     print("running")

    #     if(not parameters):
    #         data = Job.objects.all().order_by('-created_at')
    #         serializer = JobSerializer(data, many=True)
    #         return self.get_paginated_response(self.paginate_queryset(serializer.data))

    #     data = Job.objects.filter(**parameters).order_by('-created_at')
    #     serializer = JobSerializer(data, many=True)
        
    #     return self.get_paginated_response(self.paginate_queryset(serializer))
        
# retrieving the jobs posted by org       
class GetOrgJobs(GenericAPIView):
    serializer_class = JobSerializer
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
    
        if request.user.is_seeker:
            return Response({
                "error" : "Unauthorized"
            }, status=status.HTTP_401_UNAUTHORIZED)

        org = request.user.organization

        data = Job.objects.filter(organization = org).order_by('-created_at')
        serializer = JobSerializer(data, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

#applications for the org job
class GetApplicants(GenericAPIView):
    serializer_class = JobSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        
        job = Job.objects.get(id=self.kwargs['jid'])
        applicants = AppliedJobs.objects.filter(job=job)
        serializer = AppliedJobSerializer(applicants, many=True)
        print(serializer.data)

        return self.get_paginated_response(self.paginate_queryset(serializer.data))

#job applied by seeker
class GetJobListApplicant(GenericAPIView):
    serializer_class = AppliedJobs
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):

        user = request.user
        jobs = AppliedJobs.objects.filter(seeker = user)
        serializer = AppliedJobsSerializerForJobs(jobs, many=True)

        return self.get_paginated_response(self.paginate_queryset(serializer.data))


class QuestionaireView(GenericAPIView):
    serializer_class = QuestionaireSerializer
    permission_classes = [AllowAny]


    def get(self, request, *args, **kwargs):

        user = request.user
        jobId = kwargs["id"]
        obj = Questionaire.objects.get(jobId = jobId)

        serializers = QuestionaireSerializer(obj).data
        return Response(serializers)

    def post(self, request, *args, **kwargs):

        user = request.user
        jobId = kwargs["id"]

        data = {
            "jobId" : jobId,
            "organization" : user.organization.id,
            **request.data
        }

        check = Questionaire.objects.filter(jobId =jobId).exists()

        if check:
            obj = Questionaire.objects.get(jobId=jobId)

            if obj.organization.id == request.user.organization.id:
                data = request.data

            for i in data:
                setattr(obj, i, data[i])
            obj.save()

            return Response("Updated Ratings", status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data)

        return Response({
            "message": "Internal server error"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
    
        jobId = kwargs["id"]
        obj = Questionaire.objects.get(jobId=jobId)

        if obj.organization.id == request.user.organization.id:
            data = request.data

            for i in data:
                setattr(obj, i, data[i])
            obj.save()
            print(obj)

            return Response("Updated Ratings", status=status.HTTP_200_OK)

        return Response("Unauthorised", status=status.HTTP_401_UNAUTHORIZED)


class AnswernaireView(GenericAPIView):
    serializer_class = AnswernaireSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        user = request.user
        jobId = kwargs["id"]
        obj = Answernaire.objects.get(jobId = jobId)

        serializers = AnswernaireSerializer(obj).data
        return Response(serializers)

    def post(self, request, *args, **kwargs):

        user = request.user
        queId = kwargs["id"]

        data = {
            "questionId" : queId,
            "seeker" : user.seeker.id,
            **request.data
        }

        check = Answernaire.objects.filter(questionId = queId).exists()

        if check:
            obj = Questionaire.objects.get(questionId = queId)

            if obj.seeker.id == request.user.seeker.id:
                data = request.data

            for i in data:
                setattr(obj, i, data[i])
            obj.save()

            return Response("Updated Ratings", status=status.HTTP_200_OK)
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data)

        return Response({
            "data" :" asdasd"
        }, status=status.HTTP_200_OK)


#Outsourcing Project
class CreateOutsourcing(GenericAPIView):
    model=Outsourcing
    queryset=Outsourcing.objects.all()
    serializer_class=OutsourcingSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('title',)
   
    def get(self,request):
        queryset=Outsourcing.objects.all()
        
        serializer=OutsourcingSerializer(queryset,many=True).data
        

       #print("hello")
        return Response(serializer)

    def post(self,request,*args,**kwargs):
        user=request.user

        if not user.is_organization:
            return Response("Unauthorised",status=status.HTTP_401_UNAUTHORIZED)
        request.data["user"]=user.id

        serializer=OutsourcingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def patch(self,request,*args,**kwargs):
        user=request.user
        #getting user id
        print(args)
        print(kwargs)
        pk=kwargs["pk"]
        data=Outsourcing.objects.get(id=pk)
        request.data["user"]=user.id
        print(request.data)

        

        if data.user.id==user.id:
            print("True")
            serializer=OutsourcingSerializer(instance=data,data=request.data)
            if serializer.is_valid(raise_exception=True):
                print("Tr")
                serializer.save()
                return Response(serializer.data)
        return Response("Unauthorised",status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self,request,*args,**kwargs):
        user=request.user
        #getting user id
        pk=kwargs["pk"]
        data=Outsourcing.objects.get(id=pk)

        if data.user.id==user.id:
            data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT) 
                
        return Response("Unauthorised",status=status.HTTP_401_UNAUTHORIZED)





#search and order posts by 
class searchOutsourcing(ListCreateAPIView):
    queryset=Outsourcing.objects.all()
    serializer_class=OutsourcingSerializer
    permission_class=[AllowAny]
    filter_backends=(filters.SearchFilter, filters.OrderingFilter)
    search_fields=("^title",)
    ordering_fields=('title','timestamp')

# placing bids for particular Outsourcing
class placeBid(GenericAPIView):
    queryset=BiddingModel.objects.all()
    serializer_class = Bidserializer


    def get(self,request):
        user=request.user
        print(user)
        queryset=BiddingModel.objects.all()
        serializer=Bidserializer(queryset,many=True).data

        

       #print("hello")
        return Response(serializer)

    def post(self,request,*args,**kwargs):
        user=request.user
        print(user)
        obj_Id=kwargs["pk"]
        obj=Outsourcing.objects.get(id=obj_Id)
        request.data["user"]=user.id
        request.data["project"]=obj.id
        print(request.data)

        serializer=Bidserializer(data=request.data)
        #print(serializer.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class myBids(ListCreateAPIView):
    #queryset=BiddingModel.objects.all()
    #serializer_class=Bidserializer

    def get(self,request):
        queryset=BiddingModel.objects.filter(user=request.user.id)
        serializer=Bidserializer(queryset,many=True)

        return Response(serializer.data)





