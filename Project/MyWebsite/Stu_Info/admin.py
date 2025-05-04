
from django.contrib import admin
from .models import Student


# Register your models here.
class Stu_Info_Admin(admin.ModelAdmin):
    list_display =('department_class','student_id','name','id_number')
    list_filter = ('department_class','student_id','name','id_number');
    search_fields = ('department_class','student_id','name','id_number')
    ordering = ('department_class','student_id')
admin.site.register(Student,Stu_Info_Admin)
