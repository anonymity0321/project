from django.contrib import admin
from .models import Files
# Register your models here.



@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    list_display = ['files', 'key', 'submit_time']  # 优先显示 files，再显示 key 和提交时间
    fields = ['files', 'key', 'submit_time']  # 同时确保编辑页字段顺序一致（若之前未完全调整）
    search_fields = ['files', 'key', 'submit_time']
    ordering = ['files', 'key', 'submit_time']
