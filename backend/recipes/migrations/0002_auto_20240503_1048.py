# Generated by Django 3.2.16 on 2024-05-03 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingridient',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='tag',
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingridients',
            field=models.ManyToManyField(through='recipes.RecipeIngredient', to='recipes.Ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(through='recipes.RecipeTag', to='recipes.Tag', verbose_name='Тэги'),
        ),
    ]