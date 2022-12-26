# Generated by Django 4.1.4 on 2022-12-26 10:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("zmiany_aranz", "0002_alter_building_id_alter_cost_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customerofprocedure",
            name="shares",
            field=models.FloatField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0.0),
                    django.core.validators.MaxValueValidator(1.0),
                ],
            ),
        ),
    ]
