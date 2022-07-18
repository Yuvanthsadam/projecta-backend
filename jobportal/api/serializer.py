from accounts.api.serializers import OrganizationRegistrationSerializer
from accounts.models import Organization
from jobportal.models import *
from rest_framework import serializers

class JobSerializer(serializers.ModelSerializer):
    
    organization_id = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = '__all__'
        extra_kwargs = {'organization':{'write_only': True}}

    def get_organization_id(self, instance):
        return instance.organization.id
 
class AppliedJobSerializer(serializers.ModelSerializer):

    seeker = serializers.SerializerMethodField()
    job_id = serializers.SerializerMethodField()
    class Meta:
        model = AppliedJobs
        fields = ('seeker','job_id','apply_date', 'status')

    def get_seeker(self, instance):
        data = {
            "id" : instance.seeker.id,
            "name" : instance.seeker.name,
            "email" : instance.seeker.user.email
        }

        return data

    def get_job_id(self, instance):
        return instance.job.id


class AppliedJobsSerializerForJobs(serializers.ModelSerializer):

    job = JobSerializer()

    class Meta:
        model = AppliedJobs
        fields = ('job')
        
class OutsourcingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Outsourcing
        fields=['id','user','title','description','upload','skills','budget','payment','bids','time_reqd',"timestamp","end_bids","status","country"]
    
    
class QuestionaireSerializer(serializers.ModelSerializer):

    class Meta:
        model = Questionaire
        fields = '__all__'




class AnswernaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionaire
        fields = '__all__'
class Bidserializer(serializers.ModelSerializer):
    class Meta:
        model = BiddingModel
        fields=["id","user","project","skills","budget","weeklylimit"]
