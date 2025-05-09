from django.urls import path
from .views import upload_file, file_list, upload_folder, download_file

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('file_list', file_list, name='file_list'),
    path('upload_folder/', upload_folder, name='upload_folder'),
     path('download/<int:file_id>/', download_file, name='download_file'),
]