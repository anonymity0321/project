from django.db import models
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

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

# 定义信号处理函数
@receiver(post_delete, sender=Files)
def delete_file_on_disk(sender, instance, **kwargs):
    # 获取文件的本地路径
    if instance.files:
        file_path = instance.files.path
        # 检查文件是否存在
        if os.path.exists(file_path):
            # 删除文件
            os.remove(file_path)