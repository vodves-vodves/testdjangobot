# Generated by Django 3.1.4 on 2021-01-04 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vkbot', '0006_group_specialnost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Номер группы'),
        ),
    ]
