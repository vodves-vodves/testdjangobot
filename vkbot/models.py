from django.db import models


# Create your models here.
class Specialization(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование специальности')

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=255, verbose_name='Номер группы', unique=True)

    def __str__(self):
        return self.name


class Users(models.Model):
    vk_id = models.CharField(max_length=255, verbose_name='Вк_Id', unique=True)
    name = models.CharField(max_length=255, verbose_name='Фамилия Имя', null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="группа", null=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, verbose_name="специальность", null=True)

    def __str__(self):
        return self.name
