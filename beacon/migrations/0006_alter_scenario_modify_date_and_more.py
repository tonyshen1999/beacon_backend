# Generated by Django 4.1.5 on 2023-01-29 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("beacon", "0005_alter_scenario_modify_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scenario",
            name="modify_date",
            field=models.DateTimeField(
                blank=True, default="2023-01-29 01:08:44", null=True
            ),
        ),
        migrations.AlterUniqueTogether(
            name="attribute", unique_together={("entity", "attribute_name")},
        ),
        migrations.AlterUniqueTogether(
            name="period", unique_together={("period", "scenario")},
        ),
    ]