# Generated by Django 3.1.4 on 2021-01-03 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vkbot', '0003_users_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='specialization',
        ),
        migrations.AddField(
            model_name='users',
            name='specialization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vkbot.specialization', verbose_name='специальность'),
        ),
    ]
