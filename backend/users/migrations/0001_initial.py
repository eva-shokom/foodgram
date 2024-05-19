# Generated by Django 3.2.16 on 2024-04-30 12:15

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(help_text='Введите ваше имя', max_length=254, verbose_name='Имя')),
                ('last_name', models.CharField(help_text='Введите вашу фамилию', max_length=254, verbose_name='Фамилия')),
                ('username', models.CharField(help_text='Придумайте и введите логин. Допускается использование строчных и заглавных букв, цифр, символов "@.+-_". Максимальная длина логина - 50 символов.', max_length=50, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='Логин')),
                ('email', models.EmailField(help_text='Введите ваш адрес электронной почты', max_length=254, unique=True, verbose_name='Email')),
                ('password', models.CharField(help_text='Придумайте и введите пароль', max_length=30, verbose_name='Пароль')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]