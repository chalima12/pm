# Generated by Django 4.2.5 on 2023-10-17 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0006_remove_user_is_user_schedule_comment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='comment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='status',
            field=models.CharField(blank=True, choices=[('PE', 'Pending'), ('OP', 'Onprogress'), ('CO', 'Completed')], default='PE', max_length=10, null=True),
        ),
    ]
