# Generated by Django 3.2.16 on 2024-05-04 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_rename_measure_unit_ingredient_measurement_unit'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='ingredient',
            name='Уникальная комбинация ингредиент - единица измерения',
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_name_measurement_unit'),
        ),
    ]
