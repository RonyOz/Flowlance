# Generated by Django 5.1.1 on 2024-09-18 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0003_remove_course_profile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolioproject',
            name='project_image',
            field=models.ImageField(blank=True, null=True, upload_to='portfolio/projects/'),
        ),
    ]
