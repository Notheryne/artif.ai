from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from .scraper import *
from .forms import ImageUploadForm
from .models import PhotoModel

def home(request):
    return render(request, 'mainview/homepage.html')

def get_drug_names(request):
    if 'image-input' in request.POST:
        #print("There is a file: ", request.POST['image'])
        #handle_uploaded_file(request)
        #return render(request, 'mainview/search-result.html')
        form = ImageUploadForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            m = PhotoModel.objects.get(pk=course_id)
            m.photo = form.cleaned_data['image-input']
            m.save()
            return HttpResponse('image upload success')
        else:
            return render(request, 'mainview/search-resul.html')
    elif 'text-input':
        user_input = request.POST['substances']
        substances = user_input.split(',')
        data = get_full_list(substances)
        return render(request, 'mainview/search-result.html', {"substances": substances, "data": data})
    else:
        return render(request, 'mainview/search-result.html')
    
def handle_uploaded_file(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = PhotoModel.objects.get(pk=course_id)
            m.photo = form.cleaned_data['image-input']
            m.save()
            return HttpResponse('image upload success')
    return HttpResponseForbidden('allowed only via POST')