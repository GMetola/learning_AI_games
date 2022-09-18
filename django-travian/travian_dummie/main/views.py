from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .models import Village, Resource, Check
from .forms import CreateNewVillage

# Create your views here.

def home(response):
    return render(response, "main/home.html", {"name":"Home page"})

def dorf(response):
    # resources in main village
    aldea = Village.objects.get(id=3)
    
    # if response.method == 'POST':
    #     modified_resource = Resource(response.POST)
    #     modified_resource.production = 20
    #     modified_resource.save()
    #     messages.info(response, 'You have increased production')
    # else:
    #     pass
    return render(response, "main/production.html",{"aldea":aldea})

def resource(response,id):
    # see resources in different villages
    aldea = Village.objects.get(id=id)
    return render(response, "main/production.html", {"aldea":aldea})

def jaya(request):
    ob = Chek.object.get(id=2)
    return render(request, 'jaya.html', {'ob':ob})

def create(response):
    form = CreateNewVillage()
    return render(response, "main/create.html", {"form":form})
