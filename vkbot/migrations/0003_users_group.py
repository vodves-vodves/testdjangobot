# Generated by Django 3.1.4 on 2021-01-03 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vkbot', '0002_auto_20210102_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vkbot.group', verbose_name='группа'),
        ),
    ]