# Generated by Django 3.2.16 on 2024-05-07 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20240506_0917'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'verbose_name': 'Ингредиент для рецепта', 'verbose_name_plural': 'Ингредиенты для рецепта'},
        ),
        migrations.AlterModelOptions(
            name='recipetag',
            options={'verbose_name': 'Тэг для рецепта', 'verbose_name_plural': 'Тэги для рецепта'},
        ),
    ]
