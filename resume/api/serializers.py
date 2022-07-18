from rest_framework import serializers
from resume.models import *

class WorkExperienceSerializer(serializers.Serializer):
    
    class Meta :
        model = WorkExperience
        field = '__all__'
        
    id=serializers.IntegerField(required=False)
    title=serializers.CharField()
    employee_type=serializers.CharField()
    company=serializers.CharField()
    location=serializers.CharField(required=False)
    is_currently_working=serializers.BooleanField()
    start_date=serializers.DateField()
    end_date=serializers.DateField(required=False)
    description=serializers.CharField(required=False)


    def save(self, seeker, *args, **kwargs):
        try:
            id=self.validated_data['id']
        except:
            id=None
        if self.validated_data["is_currently_working"]:
            end_date=None
        else:
            end_date=self.validated_data['end_date']
        try:
            employee_type=self.validated_data["employee_type"]
        except:
            employee_type=None

        try:
            location=self.validated_data["location"]
        except:
            location=None

        try:
            description=self.validated_data["description"]
        except:
            description=None
        company=self.validated_data["company"]
        start_date=self.validated_data["start_date"]
        is_currently_working=self.validated_data["is_currently_working"]
        title=self.validated_data["title"]


        if id :
            try:
                workexperience=WorkExperience.objects.get(id=id)
            except WorkExperience.DoesNotExist:
                raise Exception("Invalid ID")
            workexperience.title=title
            workexperience.employee_type=employee_type
            workexperience.company=company
            workexperience.location=location
            workexperience.is_currently_working=is_currently_working
            workexperience.start_date=start_date
            workexperience.end_date=end_date
            workexperience.description=description
            workexperience.save()
        else:
            try:
                workexperience=WorkExperience.objects.create(
                    seeker=seeker,
                    title=title,
                    employee_type=employee_type,
                    company=company,
                    location=location,
                    is_currently_working=is_currently_working,
                    start_date=start_date,
                    end_date=end_date,
                    description=description
                )
                workexperience.save()
            except:
                raise Exception("Unable to add work experience.")
            return workexperience

     
class EducationSerializer(serializers.Serializer):
    id=serializers.IntegerField(required=False)
    school=serializers.CharField()
    degree=serializers.CharField()
    field_of_study=serializers.CharField()
    grade=serializers.DecimalField(max_digits=4, decimal_places=2)
    grade_type=serializers.CharField()
    start_date=serializers.DateField()
    end_date=serializers.DateField()
    description=serializers.CharField(required=False)

    def save(self, seeker, *args, **kwargs):
        try:
            id=self.validated_data['id']
        except:
            id=None
        school=self.validated_data["school"]
        degree=self.validated_data["degree"]
        field_of_study=self.validated_data["field_of_study"]
        grade=self.validated_data["grade"]
        grade_type=self.validated_data["grade_type"]
        start_date=self.validated_data["start_date"]
        end_date=self.validated_data["end_date"]
        try:
            description=self.validated_data["description"]
        except:
            description=None


        if id:
            try:
                education=Education.objects.get(id=id)
            except Education.DoesNotExist:
                raise Exception("Invalid ID")
            education.school=school
            education.degree=degree
            education.field_of_study=field_of_study
            education.grade=grade
            education.grade_type=grade_type
            education.start_date=start_date
            education.end_date=end_date
            education.description=description
            education.save()
        else:
            try:
                education=Education.objects.create(
                    seeker=seeker,
                    school=school,
                    degree=degree,
                    field_of_study=field_of_study,
                    grade=grade,
                    grade_type=grade_type,
                    start_date=start_date,
                    end_date=end_date,
                    description=description
                )
                education.save()
            except:
                raise Exception("Unable to add education.")
            return education.id

class LicenseAndCerificationSerializer(serializers.Serializer):
    id=serializers.IntegerField(required=False)
    name=serializers.CharField()
    issuing_organisation=serializers.CharField()
    is_credential_nonexpiry=serializers.BooleanField()
    issue_date=serializers.DateField()
    expiry_date=serializers.DateField()
    credential_id=serializers.CharField()
    credential_url=serializers.URLField()

    def  save(self, seeker, *args, **kwargs):
        try:
            id=self.validated_data['id']
        except:
            id=None
        try:
            expiry_date=self.validated_data["expiry_date"]
        except:
            expiry_date=None
        name=self.validated_data["name"]
        issuing_organisation=self.validated_data["issuing_organisation"]
        is_credential_nonexpiry=self.validated_data["is_credential_nonexpiry"]
        credential_id=self.validated_data["credential_id"]
        credential_url=self.validated_data["credential_url"]
        issue_date=self.validated_data["issue_date"]
        




        if id:
            try:
                certification=LicenseAndCerification.objects.get(id=id)
            except LicenseAndCerification.DoesNotExist:
                raise Exception("Invalid ID")
            certification.name=name
            certification.issuing_organisation=issuing_organisation
            certification.is_credential_nonexpiry=is_credential_nonexpiry
            certification.credential_id=credential_id
            certification.credential_url=credential_url
            certification.issue_date=issue_date
            certification.expiry_date=expiry_date
            certification.save()
        else:
            try:
                certification=LicenseAndCerification.objects.create(
                    seeker=seeker,
                    name=name,
                    issuing_organisation=issuing_organisation,
                    is_credential_nonexpiry=is_credential_nonexpiry,
                    credential_id=credential_id,
                    credential_url=credential_url,
                    issue_date=issue_date,
                    expiry_date=expiry_date
                )
                certification.save()
            except:
                raise Exception("Unable to add License and certification.")
            return certification.id

class SkillsSerializer(serializers.Serializer):
    id=serializers.IntegerField(required=False)
    skill=serializers.CharField()
    def  save(self, seeker, *args, **kwargs):
        if Skills.objects.filter(seeker=seeker, skill=self.validated_data['skill']).first():
            raise serializers.ValidationError("Skill already exists.")
        try:
            skill=Skills.objects.create(
                seeker=seeker, 
                skill=self.validated_data["skill"]
            )
            skill.save()
        except:
            raise Exception("Unable to add skills.")
        return skill.id

class ProjectsSerializer(serializers.Serializer):
    id=serializers.IntegerField(required=False)
    name=serializers.CharField()
    is_ongoing=serializers.BooleanField()
    start_date=serializers.DateField()
    end_date=serializers.DateField(required=False)
    description=serializers.CharField(required=False)
    project_url=serializers.URLField()

    def  save(self, seeker, *args, **kwargs):
        try:
            id=self.validated_data['id']
        except:
            id=None
        try:
            end_date=self.validated_data["end_date"]
        except:
            end_date=None
        try:
            description=self.validated_data["description"]
        except:
            description=None
        name=self.validated_data["name"]
        is_ongoing=self.validated_data["is_ongoing"]
        project_url=self.validated_data["project_url"]
        start_date=self.validated_data["start_date"]


        if id:
            try:
                project=Projects.objects.get(id=id)
            except Projects.DoesNotExist:
                raise Exception("Invalid ID")
            project.name=name
            project.is_ongoing=is_ongoing
            project.project_url=project_url
            project.start_date=start_date
            project.end_date=end_date
            project.description=description
            project.save()
        else:
            try:
                project=Projects.objects.create(
                    seeker=seeker,
                    start_date=start_date,
                    end_date=end_date,
                    description=description,
                    is_ongoing=is_ongoing,
                    project_url=project_url
                )
                project.save()
            except:
                raise Exception("Unable to add Project.")
            return project.id


class HonorsAndAwardsSerializer(serializers.Serializer):
    id=serializers.IntegerField(required=False)
    title=serializers.CharField()
    issuer=serializers.CharField()
    issue_date=serializers.DateField()
    description=serializers.CharField(required=False)

    def  save(self, seeker, *args, **kwargs):
        try:
            id=self.validated_data['id']
        except:
            id=None
        try:
            description=self.validated_data["description"]
        except:
            description=None
        title=self.validated_data["title"]
        issuer=self.validated_data["issuer"]
        issue_date=self.validated_data["issue_date"]



        if id:
            try:
                honors=HonorsAndAwards.objects.get(id=id)
            except Projects.DoesNotExist:
                raise Exception("Invalid ID")
            honors.title=title
            honors.issuer=issuer
            honors.issue_date=issue_date
            honors.description=description
            honors.save()
        else:
            try:
                honor=HonorsAndAwards.objects.create(
                    seeker=seeker, 
                    title=title,
                    issuer=issuer,
                    issue_date=issue_date,
                    description=description
                )
                honor.save()
            except:
                raise Exception("Unable to add honors and awards.")
            return honor.id
