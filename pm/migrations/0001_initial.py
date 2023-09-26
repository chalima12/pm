# Generated by Django 4.2.5 on 2023-09-26 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=50)),
                ('bank_key', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Engineer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('phoneNumber', models.IntegerField()),
                ('email', models.EmailField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('region', models.CharField(choices=[('NR', 'North'), ('SR', 'South'), ('ER', 'East'), ('WR', 'West'), ('CR', 'Centeral'), ('NN', 'None')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Terminal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_district', models.CharField(max_length=255, null=True)),
                ('bank_branch', models.CharField(max_length=255)),
                ('moti_district', models.CharField(choices=[('NR', 'North'), ('SR', 'South'), ('ER', 'East'), ('WR', 'West'), ('CR', 'Centeral'), ('NN', 'None')], max_length=50)),
                ('tid', models.CharField(max_length=30)),
                ('terminal_name', models.CharField(max_length=255)),
                ('serial_number', models.CharField(max_length=200)),
                ('model', models.CharField(max_length=200, null=True)),
                ('disspenser_type', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('bank_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pm.bank')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(verbose_name='Start date')),
                ('status', models.CharField(choices=[('0', 'Pending'), ('1', 'Onprogress'), ('3', 'Completed'), ('4', 'Cancled')], default=('0', 'Pending'), max_length=2)),
                ('description', models.CharField(max_length=300)),
                ('terminal_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pm.terminal')),
            ],
        ),
        migrations.CreateModel(
            name='BankBranch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(choices=[('NR', 'North'), ('SR', 'South'), ('ER', 'East'), ('WR', 'West'), ('CR', 'Centeral'), ('NN', 'None')], max_length=2)),
                ('district', models.CharField(max_length=30)),
                ('branch_name', models.CharField(max_length=255)),
                ('branch_key', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=255)),
                ('bank_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pm.bank')),
            ],
        ),
    ]
