from django.shortcuts import render
from django.http import HttpResponse
from .scraper import *
import json

def home(request):
    return render(request, 'mainview/homepage.html')

def get_drug_names(request):
    user_input = request.POST['substances']
    substances = user_input.split(',')
    print(substances)
    names = get_full_list(substances)
    print(names)
    return HttpResponse(json.dumps(names))
    #return render(request, 'mainview/homepage.html')
    