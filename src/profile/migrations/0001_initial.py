# Generated by Django 5.1.1 on 2024-09-21 23:36

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CurriculumVitae',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='resumes/')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_custom', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FreelancerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curriculum_vitae', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profile.curriculumvitae')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='curriculumvitae',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='freelancer_cv', to='profile.freelancerprofile'),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('freelancer_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio_profile', to='profile.freelancerprofile')),
            ],
        ),
        migrations.AddField(
            model_name='freelancerprofile',
            name='portfolio',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profile.portfolio'),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=100)),
                ('course_description', models.TextField(blank=True)),
                ('organization', models.CharField(blank=True, max_length=100, null=True)),
                ('course_link', models.URLField(blank=True, null=True)),
                ('course_image', models.ImageField(blank=True, null=True, upload_to='courses/')),
                ('expedition_date', models.DateField(blank=True, null=True)),
                ('portfolio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='profile.portfolio')),
            ],
        ),
        migrations.CreateModel(
            name='PortfolioProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=100)),
                ('client', models.CharField(blank=True, max_length=100, null=True)),
                ('project_description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('activities_done', models.TextField()),
                ('attached_files', models.FileField(blank=True, null=True, upload_to='portfolio/')),
                ('external_link', models.URLField(blank=True, null=True)),
                ('project_image', models.ImageField(blank=True, null=True, upload_to='portfolio/projects/')),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='profile.portfolio')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='given_ratings', to=settings.AUTH_USER_MODEL)),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_ratings', to='profile.freelancerprofile')),
            ],
        ),
        migrations.AddField(
            model_name='freelancerprofile',
            name='ratings',
            field=models.ManyToManyField(blank=True, related_name='freelancer_rating', to='profile.rating'),
        ),
        migrations.CreateModel(
            name='RatingResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('rating', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='response', to='profile.rating')),
            ],
        ),
        migrations.AddField(
            model_name='freelancerprofile',
            name='skills',
            field=models.ManyToManyField(blank=True, related_name='freelancers', to='profile.skill'),
        ),
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField()),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='freelancer_work_experience', to='profile.freelancerprofile')),
            ],
        ),
    ]