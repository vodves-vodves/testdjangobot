from django.db import models


# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=255, verbose_name='Фамилия Имя')
    vk_id = models.CharField(max_length=255, verbose_name='Вк_Id')

    def __str__(self):
        return self.name
