from django.db import models

# Create your models here.

class Student(models.Model):
    department_class = models.CharField(max_length=100)  # 院系班级
    student_id = models.CharField(max_length=20, unique=True)  # 学号
    name = models.CharField(max_length=50)  # 姓名
    id_number = models.CharField(max_length=18, unique=True)  # 身份证号

    def __str__(self):
        return self.name
    class Meta:
        verbose_name='学生信息'
        verbose_name_plural='学生信息'