# Generated by Django 5.1.6 on 2025-03-25 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('job_seeker', 'Job Seeker'), ('employer', 'Employer')], max_length=20),
        ),
    ]
