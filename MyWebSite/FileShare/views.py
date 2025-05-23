# project/MyWebSite/FileShare/views.py
from django.shortcuts import render,redirect
from .models import Files
from .forms import FileUploadForm, FolderUploadForm
import hashlib
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.encoding import escape_uri_path
import os
def upload_file(request):
    if request.method == 'POST':
        for file in request.FILES.getlist('files'):
            hash_object = hashlib.sha256()
            for chunk in file.chunks():
                hash_object.update(chunk)
            file_hash = hash_object.hexdigest()

            # 检查文件哈希值是否已存在
            if Files.objects.filter(key=file_hash).exists():
                messages.warning(request, f'文件 {file.name} 已存在，未重复上传。')
                continue

            new_file = Files()
            new_file.key = file_hash
            new_file.files.save(file.name, file)
            new_file.save()

        if any(message.level == messages.WARNING for message in messages.get_messages(request)):
            return redirect('upload_file')
        return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'fileshare/upload_file.html', {'form': form})

def file_list(request):
    query = request.GET.get('q', '')
    if query:
        files = Files.objects.filter(files__icontains=query)
    else:
        files = Files.objects.all()
    return render(request, 'fileshare/file_list.html', {'files': files, 'query': query})

def upload_folder(request):
    if request.method == 'POST':
        form = FolderUploadForm(request.POST, request.FILES)
        if form.is_valid():
            folder = request.FILES.getlist('folder')
            for file in folder:
                hash_object = hashlib.sha256()
                for chunk in file.chunks():
                    hash_object.update(chunk)
                file_hash = hash_object.hexdigest()

                # 检查文件哈希值是否已存在
                if Files.objects.filter(key=file_hash).exists():
                    messages.warning(request, f'文件 {file.name} 已存在，未重复上传。')
                    continue

                new_file = Files()
                new_file.key = file_hash
                # 处理文件夹结构
                relative_path = file.name
                new_file.files.save(relative_path, file)
                new_file.save()

            if any(message.level == messages.WARNING for message in messages.get_messages(request)):
                return redirect('upload_folder')
            return redirect('file_list')
    else:
        form = FolderUploadForm()
    return render(request, 'fileshare/upload_folder.html', {'form': form})


force_download_types = ['.html', '.htm', '.svg', '.md']
def download_file(request, file_id):
    # 获取文件对象
    file_obj = get_object_or_404(Files, id=file_id)
    
    # 检查文件是否存在
    if not os.path.exists(file_obj.files.path):
        raise Http404("文件不存在")
    
    # 打开文件
    with open(file_obj.files.path, 'rb') as f:
        response = HttpResponse(f, content_type='application/octet-stream')
        
        # 获取文件名和扩展名
        filename = os.path.basename(file_obj.files.name)
        name, ext = os.path.splitext(filename)
        
        # 对于特定类型的文件，强制下载
        if ext.lower() in force_download_types:
            # 使用escape_uri_path处理文件名，确保中文等特殊字符正确编码
            response['Content-Disposition'] = f'attachment; filename="{escape_uri_path(filename)}"'
        else:
            # 非强制下载类型使用默认行为
            response['Content-Disposition'] = f'inline; filename="{escape_uri_path(filename)}"'
        
        return response
    