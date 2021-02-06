from django.db import models


# Create your models here.
class Specialization(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование специальности')

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=255, verbose_name='Номер группы')
    specialnost = models.ForeignKey(Specialization, on_delete=models.CASCADE, verbose_name="специальность", null=True)

    def __str__(self):
        return self.name


class Users(models.Model):
    vk_id = models.CharField(max_length=255, verbose_name='Вк_Id', unique=True)
    name = models.CharField(max_length=255, verbose_name='Фамилия Имя', null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="группа", null=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, verbose_name="специальность", null=True)
    send_message = models.TextField(verbose_name='Отправленное сообщение', null=True)
    send_date = models.CharField(verbose_name='Дата отправки', null=True, max_length=255)

    def __str__(self):
        return str(self.name)


class BlackList(models.Model):
    vk_id = models.CharField(max_length=255, verbose_name='Вк_Id', unique=True)

    def __str__(self):
        return str(self.vk_id)