# Generated by Django 5.1.1 on 2024-09-21 03:11

import datetime
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
            name='Milestone',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Assigment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('state', models.CharField(default='INICIADO', max_length=50)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigments_created', to=settings.AUTH_USER_MODEL)),
                ('responsible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigments_tasked', to=settings.AUTH_USER_MODEL)),
                ('milestone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigments', to='project.milestone')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.CharField(blank=True, max_length=500)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('requirements', models.TextField()),
                ('budget', models.DecimalField(decimal_places=2, max_digits=10)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='milestone',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='milestones', to='project.project'),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('end_date', models.DateField()),
                ('priority', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('milestone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='project.milestone')),
                ('responsible', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TimelineChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_description', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timeline_changes', to='project.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
