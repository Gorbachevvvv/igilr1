# Generated by Django 4.2.13 on 2024-06-04 01:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('myparking', '0014_news_news_long_alter_news_news'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=20, verbose_name='Имя пользователя')),
                ('phone_number', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Номер телефона')),
                ('city', models.CharField(max_length=20, verbose_name='Город')),
                ('adress', models.CharField(max_length=100, verbose_name='Адрес')),
                ('email', models.EmailField(max_length=254, verbose_name='Почта')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=20, verbose_name='Имя пользователя')),
                ('companyname', models.CharField(max_length=20, verbose_name='Название компании')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
            ],
        ),
    ]
