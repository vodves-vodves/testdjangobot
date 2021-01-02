from django.db import models


# Create your models here.
class Users(models.Model):
    vk_id = models.CharField(max_length=255, verbose_name='Вк_Id', unique=True)
    name = models.CharField(max_length=255, verbose_name='Фамилия Имя')

    def __str__(self):
        return self.name


class Specialization(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование специальности')

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=255, verbose_name='Номер группы', unique=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
