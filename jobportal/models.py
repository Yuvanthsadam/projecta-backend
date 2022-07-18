from django.db import models
from django_countries import countries
# from django_countries.fields import CountryField
from django.utils.timezone import now
from datetime import datetime

from .countrystates import states 
from django.utils.timezone import now, datetime, timedelta
from .data.location import state
def get_deadline():
    return datetime.today().date() + timedelta(days=20)

class Job(models.Model):
    job_type_choice = (
        ('A', "FULL TIME"),
        ('B', "PART TIME")
    )

    contract_type_choice = (
        ('A', 'Temporary'),
        ('B', "Permanent")
    )

    # organization = models.ForeignKey("accounts.Organization", on_delete=models.CASCADE)
    title = models.CharField(max_length=155)
    description = models.CharField(max_length=255)
    job_type = models.CharField(choices=job_type_choice, max_length=2)
    contract_type = models.CharField(choices=contract_type_choice, max_length=2)
    skills = models.CharField(max_length=255)
    work_from_home = models.BooleanField(default=False)
    vacancies = models.IntegerField()
    rounds = models.IntegerField()
    country = models.CharField(max_length=255, default="") # arrayField
    state = models.CharField(max_length=255,choices=state,  default="MH") # arrayField, for filtering
    city = models.CharField(max_length=155, default="Navi Mumbai") # arrayField , for filtering
    experience = models.CharField(max_length=255, default="")
    education = models.CharField(max_length=255, default="")
    last_date = models.DateTimeField(default=get_deadline)
    is_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) # for ordering (sorting)

    class Meta:
        default_related_name = 'Jobs'

    def __str__(self):
        return "{} : {} : {}".format(self.id, self.organization, self.title)

class AppliedJobs(models.Model):
    status_choice = (
            ('A', "Applied"),
            ('B', "Seen"),
            ('C', "In touch"),
            ('D', "Under review"),
            ('E', "Not selected"),
        )

    # seeker=models.ForeignKey("accounts.Seeker",on_delete=models.CASCADE)
    job=models.ForeignKey("jobportal.Job", on_delete=models.CASCADE)
    apply_date=models.DateTimeField(default=now, blank=True)
    status=models.CharField(choices=status_choice, max_length=2, default='A')

    def __str__(self):
        return str(self.seeker) + " " + str(self.job) + " " + str(self.apply_date)


class Outsourcing(models.Model):
    BUDGET_CHOICE=(
        ('smallproject','smallproject'),
        ('mediumproject','mediumproject'),
        ('largeproject','largeproject'),
    )

    PAY_CHOICE=(
        ('fixed','fixed'),
        ('hourly','hourly'),
    )
    # user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
   
    description=models.CharField(max_length=300)
    upload=models.FileField(upload_to='media/date/%Y/%M/%D/')
    skills=models.CharField(max_length=100)
    
    budget=models.CharField(max_length=100,choices=BUDGET_CHOICE)
    payment=models.CharField(max_length=100,choices=PAY_CHOICE)
    bids=models.BooleanField(default=False)
    time_reqd=models.CharField(max_length=100)
    timestamp=models.DateField(default=now)
    end_bids=models.DateField(default=get_deadline)
    status=models.BooleanField(default=True)
    # country=CountryField(default="IN")
    States=models.CharField(max_length=100,choices=states,default="Delhi")
    
class Questionaire(models.Model):
    
    jobId = models.ForeignKey("jobportal.Job", on_delete=models.CASCADE)
    # organization = models.ForeignKey("accounts.Organization", on_delete=models.CASCADE)
    question = models.CharField(max_length=255, blank=True, null=True)  
    question2 = models.CharField(max_length=255, blank=True, null=True)  
    question3 = models.CharField(max_length=255, blank=True, null=True)  
    question4 = models.CharField(max_length=255, blank=True, null=True)  
    question5 = models.CharField(max_length=255, blank=True, null=True)  


    def __str__(self):
        return str(self.organization) 

class Answernaire(models.Model):

    questionId = models.ForeignKey("jobportal.Questionaire", on_delete=models.CASCADE)
    # seeker = models.ForeignKey("accounts.Seeker",on_delete=models.CASCADE)
    answer = models.CharField(max_length=255, blank=True, null=True)
    answer2 = models.CharField(max_length=255, blank=True, null=True)
    answer3 = models.CharField(max_length=255, blank=True, null=True)
    answer4 = models.CharField(max_length=255, blank=True, null=True)
    answer5 = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return '{}:{}'.format(self.questionId, self.seeker)
    def __str__(self):
        return self.title

    def active(self):
        currentdate=datetime.today()
        self.status=True
        if self.end_bids<currentdate:
            self.status=False
        else:
            self.status=True
        
        return self.status

class BiddingModel(models.Model):
    # user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    project=models.ForeignKey("jobportal.Outsourcing",on_delete=models.CASCADE)
    skills=models.CharField(max_length=300)
    budget=models.CharField(max_length=300)
    weeklylimit=models.IntegerField()
    
    def __str__(self):
        return "{}".format(self.user.email)
