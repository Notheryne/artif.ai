from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from .scraper import *
from .forms import ImageUploadForm
from .models import PhotoModel
from django.core.files.storage import FileSystemStorage

def home(request):
    return render(request, 'mainview/homepage.html')

def get_drug_names(request):
    if 'image-input' in request.POST:
        if request.method == 'POST' and request.FILES['image']:
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            return render(request, 'mainview/search-result.html')
        else:
            return render(request, 'mainview/search-result.html')
    elif 'text-input':
        user_input = request.POST['substances']
        substances = user_input.split(',')
        data = get_full_list(substances)
        return render(request, 'mainview/search-result.html', {"substances": substances, "data": data})
    else:
        return render(request, 'mainview/search-result.html')
    
#def handle_uploaded_file(request):
#    return