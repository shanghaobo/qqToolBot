from django.db import models

# Create your models here.


'''
0空闲状态
1短连接
2二维码生成
'''
#用户当前状态
class UserStatus(models.Model):
    qq = models.CharField(max_length=15, verbose_name='用户QQ',primary_key=True)
    status = models.CharField(max_length=5,verbose_name='用户状态')
    class Meta:
        verbose_name_plural = '用户状态'
    def __str__(self):
        return self.qq