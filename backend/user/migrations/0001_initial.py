# Generated by Django 3.1.1 on 2020-09-07 18:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=120, unique=True)),
                ('first_name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=60)),
                ('age', models.IntegerField(default=0)),
                ('dob', models.DateField(max_length=8, null=True)),
                ('gender', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=60)),
                ('state', models.CharField(max_length=60)),
                ('country', models.CharField(max_length=60)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('admin', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productivity', models.BooleanField(verbose_name=False)),
                ('self_help', models.BooleanField(verbose_name=False)),
                ('self_improvement', models.BooleanField(verbose_name=False)),
                ('personal_development', models.BooleanField(verbose_name=False)),
                ('spirituality', models.BooleanField(verbose_name=False)),
                ('motivation', models.BooleanField(verbose_name=False)),
                ('positivity', models.BooleanField(verbose_name=False)),
                ('career', models.BooleanField(verbose_name=False)),
                ('discipline', models.BooleanField(verbose_name=False)),
                ('relationships', models.BooleanField(verbose_name=False)),
                ('success', models.BooleanField(verbose_name=False)),
                ('depression', models.BooleanField(verbose_name=False)),
                ('anxiety', models.BooleanField(verbose_name=False)),
                ('ptsd', models.BooleanField(verbose_name=False)),
                ('alcohol', models.BooleanField(verbose_name=False)),
                ('internet_addiction', models.BooleanField(verbose_name=False)),
                ('bipolar_disorder', models.BooleanField(verbose_name=False)),
                ('social_anxiety_disorder', models.BooleanField(verbose_name=False)),
                ('stress', models.BooleanField(verbose_name=False)),
                ('sleep_disorder', models.BooleanField(verbose_name=False)),
                ('empathy_deficit_disorder', models.BooleanField(verbose_name=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
