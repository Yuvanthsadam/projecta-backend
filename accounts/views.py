from django.shortcuts import render
from accounts.models import Organization, Seeker

def get_organization(pk):
    return Organization.objects.get(user = pk)

def get_seeker(pk):
    return Seeker.objects.get(user = pk)