# Generated by Django 4.1.5 on 2023-01-14 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Attribute",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("attribute_name", models.CharField(max_length=100)),
                ("attribute_value", models.CharField(max_length=50)),
                ("begin_date", models.DateField()),
                ("end_date", models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Currency",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=5)),
                ("begin_date", models.DateField(null=True)),
                ("end_date", models.DateField(null=True)),
                ("avg_rate", models.FloatField(null=True)),
                ("end_spot_rate", models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Period",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("period", models.CharField(max_length=10)),
                ("begin_date", models.DateField()),
                ("end_date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Scenario",
            fields=[
                ("scn_id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=200)),
                (
                    "description",
                    models.TextField(blank=True, max_length=500, null=True),
                ),
                ("version", models.IntegerField()),
                ("periods", models.ManyToManyField(to="beacon.period")),
            ],
        ),
        migrations.CreateModel(
            name="Entity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("entity_type", models.CharField(max_length=50)),
                (
                    "country",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="beacon.country",
                    ),
                ),
                (
                    "scenario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="beacon.scenario",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="country",
            name="currency",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="beacon.currency",
            ),
        ),
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("account_name", models.CharField(max_length=100)),
                ("amount", models.FloatField()),
                ("collection", models.CharField(max_length=100, null=True)),
                ("acc_class", models.CharField(max_length=100, null=True)),
                ("data_type", models.IntegerField(null=True)),
                (
                    "currency",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="beacon.currency",
                    ),
                ),
                (
                    "entity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="beacon.entity"
                    ),
                ),
                (
                    "period",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="beacon.period"
                    ),
                ),
            ],
        ),
    ]
