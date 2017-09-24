# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-24 21:20
from __future__ import unicode_literals

import dashboard.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='interviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(default='', max_length=1000)),
                ('yearOfExperience', models.CharField(default='', max_length=1000)),
                ('highestQualification', models.CharField(default='', max_length=1000)),
                ('anyonmousStat', models.CharField(choices=[('1', '1'), ('0', '0')], default='0', max_length=50)),
                ('processOfInterview', models.TextField(default='')),
                ('month', models.CharField(default='', max_length=200)),
                ('year', models.CharField(default='', max_length=200)),
                ('source', models.CharField(default='', max_length=500)),
                ('howfind', models.CharField(choices=[('easy', 'easy'), ('difficult', 'difficult'), ('very_difficult', 'very_difficult')], default='easy', max_length=100)),
                ('getOfferstat', models.CharField(choices=[('yes', 'yes'), ('no', 'no'), ('awaiting', 'awaiting')], default='yes', max_length=100)),
                ('otherComment', models.TextField(default='')),
                ('showStat', models.CharField(choices=[('1', '1'), ('0', '0')], default='0', max_length=50)),
                ('submittedDate', models.DateField(auto_now_add=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.companies')),
                ('submittedBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='questionsAsked',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questions', models.TextField()),
                ('interview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.interviews')),
            ],
        ),
        migrations.CreateModel(
            name='userinformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userProfileImage', models.ImageField(default='https://eliaslealblog.files.wordpress.com/2014/03/user-200.png', upload_to=dashboard.models.get_profile_image)),
                ('current_job_profile', models.CharField(default='', max_length=500)),
                ('current_location', models.CharField(default='', max_length=500)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
