# Generated by Django 4.0.3 on 2022-03-11 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='sent',
            field=models.BooleanField(default=False),
        ),
    ]
