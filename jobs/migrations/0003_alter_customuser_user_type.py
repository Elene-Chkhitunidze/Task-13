# Generated by Django 5.1.6 on 2025-03-25 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_remove_job_employer_job_deadline_job_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('job_seeker', 'მაძიებელი'), ('employer', 'დამსაქმებელი')], max_length=20),
        ),
    ]
