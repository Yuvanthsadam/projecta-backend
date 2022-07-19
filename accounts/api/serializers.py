from rest_framework import serializers
from accounts.models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth import authenticate


User = get_user_model()

# user serializer
class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=68, min_length=4, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

# seeker serializer
class SeekerSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    id = serializers.SerializerMethodField()

    class Meta:
        model = Seeker
        fields = '__all__'

    # overiding the get representation 
    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = data.pop('user')
        data.update({"email" :user['email']})
        return data

    def get_id(self, instance):
        return instance.user.id
    

# organization serializer
class OrganizationSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(read_only=True)
    id = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = '__all__'

    # overiding the get representation 
    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = data.pop('user')
        data.update({"email" :user['email']})
        return data

    def get_id(self, instance):
        return instance.user.id
    
# seeker registration serializer
class SeekerRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    email = serializers.EmailField(max_length=75, allow_blank=False)
    password = serializers.CharField(max_length=75, allow_blank=False, trim_whitespace=True)

    class Meta:
        model = Seeker
        fields = '__all__'
    
    # validate if email already registered
    def validate_email(self, email):
        user = User.objects.filter(email = email).exists()

        if user:
            raise serializers.ValidationError("Email Already registered")     
        return email

    # validating password
    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError("password too Short!!")
        return password

    def create(self, validated_data, *args, **kwargs):
        user = User.objects.create_user(email = validated_data.pop('email'),password= validated_data.pop('password'))
        user.is_seeker = True
        user.save()
        seeker = Seeker.objects.create(user=user, **validated_data)
        return seeker

# organization registration serializer
class OrganizationRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    email = serializers.EmailField(max_length=75, allow_blank=False)
    password = serializers.CharField(max_length=75, allow_blank=False, trim_whitespace=True)

    class Meta:
        model = Organization
        fields = '__all__'

    ## validate if email already registered
    def validate_email(self, email):
        user = User.objects.filter(email = email).exists()
        
        if user:
            raise serializers.ValidationError("Email Already registered")     
        return email

    #validating password
    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError("password too Short!!")
        return password

    def create(self, validated_data, *args, **kwargs):
        user = User.objects.create_user(email = validated_data.pop('email'),password= validated_data.pop('password'))
        user.is_organization = True
        user.save()
        organization = Organization.objects.create(user=user, **validated_data)
        return organization
    
class OrganizationRegistrationDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Organization
        fields = '__all__'

class RatingOrganizationSerializer(serializers.ModelSerializer):

    organization = serializers.CharField()
    # seeker = SeekerSerializer(read_only=True)
    
    class Meta:
        model = RatingOrganization
        fields = '__all__'

  
    def create(self, validated_data, *args, **kwargs):
        
        # user = self.context['request'].user
        user_org = User.objects.get(id=validated_data.pop('organization'))
        organization = Organization.objects.get(user=user_org)
        rating = RatingOrganization.objects.create(organization=organization,  **validated_data)
        return rating


class InvestorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Investor
        fields = '__all__'

    def create(self, validated_data, *args, **kwargs):

        inv = Investor.objects.create(
            user = validated_data.pop('user'),
            budget = validated_data.pop('budget'),
            identification = validated_data.pop('identification'),
            preference = validated_data.pop('preference'),
            category = validated_data.pop('category')
        )

        inv = Investor.objects.create(**validated_data)

        return inv

class EntreprenurSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Entreprenur
        fields = '__all__'

    def create(self, validated_data, *args, **kwargs):

        inv = Investor.objects.create(
            user = validated_data.pop('user'),
            budget = validated_data.pop('budget'),
            identification = validated_data.pop('identification'),
            preference = validated_data.pop('preference'),
            category = validated_data.pop('category')
        )

        inv = Investor.objects.create(**validated_data)

        return inv