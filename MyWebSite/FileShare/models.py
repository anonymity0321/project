from django.db import models
from django.utils import timezone
# Create your models here.
class Files(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=255, unique=True)
    files = models.FileField(upload_to='')
    submit_time = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = "文件记录"
        verbose_name_plural = "文件记录"

    def __str__(self):
        return self.key