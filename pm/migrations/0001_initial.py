# Generated by Django 4.2.5 on 2023-11-01 10:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, null=True, unique=True, verbose_name='email address')),
                ('username', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], help_text='Gender', max_length=100, null=True)),
                ('phone', models.CharField(blank=True, help_text='Phone Number', max_length=100, null=True)),
                ('Photo', models.ImageField(blank=True, default='atm_U2G9mVp.png', help_text='Photo', null=True, upload_to='')),
                ('address', models.TextField(blank=True, help_text='Address', max_length=50, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_staff', models.BooleanField(blank=True, default=False, null=True)),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('is_moti', models.BooleanField(blank=True, default=False, null=True)),
                ('is_bank', models.BooleanField(blank=True, default=False, null=True)),
                ('system_summary', models.BooleanField(blank=True, default=False, null=True)),
                ('equipment_usage', models.BooleanField(blank=True, default=False, null=True)),
                ('view_user_list', models.BooleanField(blank=True, default=False, null=True)),
                ('edit_user', models.BooleanField(blank=True, default=False, null=True)),
                ('assign_privilege', models.BooleanField(blank=True, default=False, null=True)),
                ('see_user_detail', models.BooleanField(blank=True, default=False, null=True)),
                ('upload_daily_report', models.BooleanField(blank=True, default=False, null=True)),
                ('view_contact_list', models.BooleanField(blank=True, default=False, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(blank=True, max_length=50, null=True)),
                ('bank_key', models.CharField(blank=True, max_length=40, null=True)),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
            ],
            options={
                'ordering': ['bank_name'],
            },
        ),
        migrations.CreateModel(
            name='Terminal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_district', models.CharField(blank=True, max_length=255, null=True)),
                ('bank_branch', models.CharField(blank=True, max_length=255, null=True)),
                ('moti_district', models.CharField(blank=True, choices=[('NR', 'North'), ('SR', 'South'), ('ER', 'East'), ('WR', 'West'), ('CR', 'Centeral')], max_length=50, null=True)),
                ('tid', models.CharField(blank=True, max_length=30, null=True)),
                ('terminal_name', models.CharField(blank=True, max_length=255, null=True)),
                ('serial_number', models.CharField(blank=True, max_length=200, null=True)),
                ('model', models.CharField(blank=True, max_length=200, null=True)),
                ('disspenser_type', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('bank_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pm.bank')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('PE', 'Pending'), ('WT', 'Waiting'), ('OP', 'Onprogress'), ('CO', 'Completed')], default='PE', max_length=10, null=True)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('priority', models.CharField(blank=True, choices=[('H', 'High'), ('M', 'Medium'), ('L', 'Low')], max_length=10, null=True)),
                ('material_required', models.CharField(blank=True, max_length=255, null=True)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
                ('checklist_photo', models.FileField(blank=True, null=True, upload_to='pm_checklist_pics/')),
                ('closed_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('assign_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('bank_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pm.bank')),
                ('terminal_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pm.terminal')),
            ],
        ),
    ]
