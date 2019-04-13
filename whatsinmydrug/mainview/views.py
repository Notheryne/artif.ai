from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'mainview/homepage.html')

def get_drug_names(request):
    user_input = request.POST['substances']
    substances = user_input.split(',')
    print(substances)
    return render(request, 'mainview/homepage.html')