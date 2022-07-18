from django.db import models
import accounts
from accounts.models import Seeker

class WorkExperience(models.Model):
    # seeker=models.ForeignKey("accounts.Seeker", on_delete=models.CASCADE)
    seeker=models.ForeignKey(Seeker, on_delete=models.CASCADE)
    title=models.CharField(max_length=255, null=False, unique=True)
    employee_type=models.CharField(max_length=55)
    company=models.CharField(max_length=255, null=False)
    location=models.CharField(max_length=255, null=True)
    is_currently_working=models.BooleanField(default=False)
    start_date=models.DateField(null=False,blank=True)
    end_date=models.DateField(null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.title


class Education(models.Model):
    # seeker=models.ForeignKey("accounts.Seeker", on_delete=models.CASCADE)
    seeker=models.ForeignKey(Seeker, on_delete=models.CASCADE)
    school=models.CharField(max_length=255, null=False)
    degree=models.CharField(max_length=255, null=False) 
    field_of_study=models.CharField(max_length=255)
    grade=models.CharField(max_length=40)
    grade_type=models.CharField(max_length=15, default="Percentage")
    start_date=models.DateField(null=False)
    end_date=models.DateField(null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.school

class LicenseAndCerification(models.Model):
    # seeker=models.ForeignKey("accounts.Seeker", on_delete=models.CASCADE)
    seeker=models.ForeignKey(Seeker, on_delete=models.CASCADE)
    name=models.CharField(max_length=255, null=False)
    issuing_organisation=models.CharField(max_length=255)
    is_credential_nonexpiry=models.BooleanField(default=True)
    issue_date=models.DateField(null=False)
    expiry_date=models.DateField(null=True, blank=True)
    credential_id=models.CharField(max_length=255)
    credential_url=models.URLField(max_length=255)
    
    def __str__(self):
        return self.name

class Skills(models.Model):
    # seeker=models.ForeignKey("accounts.Seeker", on_delete=models.CASCADE)
    seeker=models.ForeignKey(Seeker, on_delete=models.CASCADE)
    skill=models.CharField(max_length=80, null=False)
    
    def __str__(self):
        return self.skill

class Projects(models.Model):
    # seeker=models.ForeignKey("accounts.Seeker", on_delete=models.CASCADE)
    seeker=models.ForeignKey(Seeker, on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    is_ongoing=models.BooleanField(default=False)
    start_date=models.DateField(null=False)
    end_date=models.DateField(null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    project_url=models.URLField(max_length=200)
    
    def __str__(self):
        return self.name

class HonorsAndAwards(models.Model):
    # seeker=models.ForeignKey("accounts.Seeker", on_delete=models.CASCADE)
    seeker=models.ForeignKey(Seeker, on_delete=models.CASCADE)
    title=models.CharField(max_length=255, null=False)
    issuer=models.CharField(max_length=255)
    issue_date=models.DateField(null=False)
    description=models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.title