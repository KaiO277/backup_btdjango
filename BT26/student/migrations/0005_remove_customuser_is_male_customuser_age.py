# Generated by Django 5.0 on 2024-01-09 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_alter_customuser_is_male'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_Male',
        ),
        migrations.AddField(
            model_name='customuser',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
