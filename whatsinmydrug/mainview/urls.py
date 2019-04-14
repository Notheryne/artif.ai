from django.urls import path
from .views import home, get_drug_names, home_fruits, fruits_vitamins

urlpatterns = [
    path('', home, name='mainview-home'),
    #path('fruits/', home_fruits, name='mainview-fruits'),
    #path('fruits/search', fruits_vitamins, name='fruits-vitamins'),
    path('search/', get_drug_names, name='search-drugs'),
]