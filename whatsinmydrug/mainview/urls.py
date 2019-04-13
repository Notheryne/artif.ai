from django.urls import path
from .views import home, get_drug_names

urlpatterns = [
    path('', home, name='mainview-home'),
    path('search/', get_drug_names, name='search-drugs'),
]