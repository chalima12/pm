# Generated by Django 4.2.5 on 2023-11-13 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='schedule_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
