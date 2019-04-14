from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from .scraper import *
from .ocr_util_v2 import *
from .forms import ImageUploadForm
from .models import PhotoModel
from .get_vitamins import *
from django.core.files.storage import FileSystemStorage
from py_translator import Translator
import re

def care_ocr_output(ocr_otput):
    ocr_otput = [x for x in ocr_otput if ord(x) < 128]
    s2 = ''.join(ocr_otput)
    s2 = re.sub('\\n',' ',s2)
    ocr_otput = s2
    print("FIRST CAREING : ",ocr_otput)
   # ocr_otput = Translator().translate(text=ocr_otput, dest='en').text
    print("AFTER ")
    ocr_otput = ocr_otput.lower()
    ocr_otput = ocr_otput.split(' ')
    ocr_otput = [x for x in ocr_otput if len(x)>3]
    
    return ocr_otput

def home(request):
    return render(request, 'mainview/homepage.html')

def home_fruits(request):
    return render(request, 'mainview/homepage-fruits.html')

def fruits_vitamins(request):
    print("I'm here!!")
    user_input = request.POST['fruit-name']
    print("I'm here1")
    print(type(user_input))
    info = get_Vitamins(user_input.strip())
    print("I'm here2")
    substances = info["fruit_name"]
    print(substances)
    scraping_result = get_full_list(substances)
    data = scraping_result[0]
    articles = scraping_result[1]
    names = [i['Name'] for i in data]
    return render(request, 'mainview/search-result.html', {"substances": names, "data": data, "articles": articles})

def get_drug_names(request):

    if 'image-input' in request.POST:
        if request.method == 'POST' and request.FILES['image']:
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            recognized_text = ocr_core2(uploaded_file_url)
            print("Found: ",recognized_text.encode('utf-8'))
            formatted_text = care_ocr_output(recognized_text)
            print("formatted: ", formatted_text)
            scraping_result = get_full_list(formatted_text)
            data = scraping_result[0]
            articles = scraping_result[1]
            articles = ["No articles found"]
            names = [i['Name'] for i in data]
            return render(request, 'mainview/search-result.html', {"substances": names, "data": data, "articles": articles})
        else:
            return render(request, 'mainview/search-result.html')

    elif 'text-input':
        user_input = request.POST['substances']
        substances = user_input.split(',')
        scraping_result = get_full_list(substances)
        data = scraping_result[0]
        articles = scraping_result[1]
        names = [i['Name'] for i in data]
        return render(request, 'mainview/search-result.html', {"substances": names, "data": data, "articles": articles})
    else:
        return render(request, 'mainview/search-result.html')
    