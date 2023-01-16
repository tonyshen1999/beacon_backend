# Generated by Django 4.1.5 on 2023-01-16 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
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
                ("collection", models.CharField(blank=True, max_length=100, null=True)),
                ("acc_class", models.CharField(blank=True, max_length=100, null=True)),
                ("data_type", models.IntegerField(blank=True, null=True)),
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
                ("begin_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("avg_rate", models.FloatField(blank=True, null=True)),
                ("end_spot_rate", models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Scenario",
            fields=[
                (
                    "scn_id",
                    models.IntegerField(default=1, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=200)),
                (
                    "description",
                    models.TextField(blank=True, max_length=500, null=True),
                ),
                ("version", models.IntegerField(default=1)),
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
                (
                    "scenario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="beacon.scenario",
                    ),
                ),
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
                ("name", models.CharField(max_length=200, unique=True)),
                ("entity_type", models.CharField(max_length=50)),
                (
                    "country",
                    models.ForeignKey(
                        blank=True,
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
                on_delete=django.db.models.deletion.CASCADE, to="beacon.currency"
            ),
        ),
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
                (
                    "scenario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="beacon.scenario",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Adjustment",
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
                ("adj_type", models.CharField(max_length=100)),
                (
                    "adj_collection",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("adj_class", models.CharField(blank=True, max_length=100, null=True)),
                ("adj_percentage", models.FloatField(blank=True, null=True)),
                ("adj_amount", models.FloatField(null=True)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="beacon.account"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="account",
            name="currency",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="beacon.currency",
            ),
        ),
        migrations.AddField(
            model_name="account",
            name="entity",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="beacon.entity"
            ),
        ),
        migrations.AddField(
            model_name="account",
            name="period",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="beacon.period"
            ),
        ),
        migrations.AddField(
            model_name="account",
            name="scenario",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="beacon.scenario"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="account", unique_together={("account_name", "scenario")},
        ),
    ]
