# Generated by Django 3.2.16 on 2024-05-03 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20240503_1048'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='ingridients',
            new_name='ingredients',
        ),
    ]