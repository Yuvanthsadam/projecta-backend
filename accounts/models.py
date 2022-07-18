from wsgiref.validate import validator
from click import password_option
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from scipy.fft import fftfreq
from jobportal.models import Job, AppliedJobs
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from jobportal.data.location import state
# from django_countries import countries
# from django_countries.fields import CountryField
from django.db.models import BigAutoField
# from django_countries import countries
from django.core.validators import FileExtensionValidator
# custom base user manager for email as unique field


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

# adding flags for types of user


class User(AbstractUser):
    is_seeker = models.BooleanField(default=False)
    is_organization = models.BooleanField(default=False)
    is_investor = models.BooleanField(default=False)
    is_entreprenur = models.BooleanField(default=False)
    is_ratingorganization = models.BooleanField(default=False)
    email = models.EmailField(verbose_name='email address', unique=True)
    is_verified = models.BooleanField(default=False)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# seeker user type model


class Seeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=155)
    last_name = models.CharField(max_length=155)
    # country = CountryField(default="IN")
    phone_regex = RegexValidator(regex=r'^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$',
                                 message="Phone number must be entered in the format: '+919999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=15, null=False, unique=True)
    gender = models.CharField(max_length=6, null=False)
    date_of_birth = models.DateField(null=True, blank=True)
    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True, default=True)
    password = models.CharField(max_length=155, default=True)
    rating = models.CharField(max_length=55, null=True, blank=True)

    # rating field(for all models)

    def __str__(self):
        return self.user.email

    def get_appliedjob_list(self):
        data = AppliedJobs.objects.filter(seeker=self.id)
        return data

    @property
    def completion(self):
        percent = {
            'workexperience': 10,
            'education': 20,
            'skills': 15,
            'projects': 10,
            'honorsandawards': 10,
            'certifications': 10,
            'phoneNo': 20,
        }

        total = 0

        if self.education_set.all():
            total += percent.get('education', 0)
            print('inside this')
        if self.workexperience_set.all():
            total += percent.get('workexperience', 0)
        if self.licenseandcerification_set.all():
            total += percent.get('certifications', 0)
        if self.skills_set.all():
            total += percent.get('skills', 0)
        if self.honorsandawards_set.all():
            total += percent.get('honorsandawards', 0)
        if self.projects_set.all():
            total += percent.get('projects', 0)
        if self.phone_number:
            total += percent.get('phoneNo', 0)

        return total


# upload path
def upload_directory_path(instance, filename):
    return 'UPLOADS/{0}/{1}'.format(instance.organization_name, filename)


# organization user type model
class Organization(models.Model):

    industry_choice = (
        ('A', 'IT'),
        ('B', 'Mechanical'),
        ('C', 'Chemical')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=155)
    # details = models.CharField(max_length=255)  # has to be remved
    size = models.IntegerField()
    year = models.CharField(max_length=155)
    industry = models.CharField(choices=industry_choice, max_length=2)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=55)
    zipcode = models.IntegerField()
    sector = models.CharField(max_length=255)
    state = models.CharField(max_length=255, choices=state,  default="MH")
    # country = models.CharField(max_length=255)
    website = models.CharField(max_length=155)
    is_approved = models.BooleanField(default=False)
    email = models.EmailField(unique=True, default=True)
    password = models.CharField(max_length=155, default=True)
    organization_emp_name = models.CharField(max_length=55)
    designation = models.CharField(max_length=155)
    org_reg_certificate = models.FileField(
        upload_to=upload_directory_path, blank=True, null=True, max_length=255, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg'])])
    org_pan = models.FileField(
        upload_to=upload_directory_path, blank=True, null=True, max_length=255, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg'])])
    other_uploads = models.FileField(
        upload_to=upload_directory_path, blank=True, null=True, max_length=255, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg'])])

    def __str__(self):
        return self.organization_name

    def get_job_list(self):
        data = Job.objects.filter(organization=self.id)
        return data


class RatingOrganization(models.Model):

    experience = (
        ('A', 'Interview'),
        ('B', 'Ex-Employee'),
        ('C', 'Employee')
    )

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    experience = models.CharField(max_length=155, choices=experience)
    rating = models.IntegerField()
    seeker = models.ForeignKey(Seeker, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=255)
    created_at = models.DateTimeField(
        auto_now_add=True)  # for ordering (sorting)

    def __str__(self):
        return self.organization.organization_name

    def get_avg(self, instance):
        org = instance.Organization
        avg = RatingOrganization.objects.filter(
            organization=org).aggregate(org('rating'))
        print(avg)

        return avg


def inv_upld_pth(instance, filename):
    return 'UPLOADS/investor/{}'.format(instance.user.email)


class Investor(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.CharField(max_length=155)  # has to be choice field
    identification = models.FileField(
        upload_to=inv_upld_pth, blank=True, null=True, max_length=255, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg'])])
    preference = models.CharField(max_length=155)  # has to be choice field
    category = models.CharField(max_length=155)  # has to be choice field

    def __str__(self):
        return '{}'.format(self.user.email)


class Entreprenur(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business = models.BooleanField(default=False)
    idea = models.CharField(max_length=255)  # change to text area


def __str__(self):
    return '{}'.format(self.user.email)
