# Generated by Django 4.2.5 on 2024-01-25 05:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0002_alter_user_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Moti_district',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district_name', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('region', models.CharField(blank=True, choices=[('NR', 'North'), ('SR', 'South'), ('ER', 'East'), ('WR', 'West'), ('CR', 'Centeral')], max_length=50, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='terminal',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pm.moti_district'),
        ),
    ]
