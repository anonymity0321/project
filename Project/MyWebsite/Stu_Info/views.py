from django.shortcuts import render
from .models import Student
# Create your views here.
def Show_info(request):
    students = Student.objects.all()
    return render(request, template_name="Show_info.html", context={'students': students})


