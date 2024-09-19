# Generated by Django 5.1.1 on 2024-09-18 03:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assigment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('priority', models.CharField(max_length=50)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigments_created', to=settings.AUTH_USER_MODEL)),
                ('responsible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigments_tasked', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='milestone',
            name='assigments',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='milestone', to='project.assigment'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]