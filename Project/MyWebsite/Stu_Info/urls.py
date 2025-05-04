from django.urls import path
from .views import Show_info
urlpatterns = [
    path('Show_info/',Show_info,name='Show_info'),
	
]