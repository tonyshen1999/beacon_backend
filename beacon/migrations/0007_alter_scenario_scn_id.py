# Generated by Django 4.1.5 on 2023-01-14 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("beacon", "0006_alter_account_scenario"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scenario",
            name="scn_id",
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]