# Generated by Django 4.1.5 on 2023-01-20 19:07

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
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="beacon.country",
                    ),
                ),
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
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("scn_id", models.IntegerField(default=1)),
                ("name", models.CharField(max_length=200)),
                (
                    "description",
                    models.TextField(blank=True, max_length=500, null=True),
                ),
                ("version", models.IntegerField(default=1)),
                (
                    "modify_date",
                    models.DateTimeField(
                        blank=True, default="2023-01-20 19:07:32", null=True
                    ),
                ),
            ],
            options={"unique_together": {("scn_id", "version")},},
        ),
        migrations.CreateModel(
            name="Relationship",
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
                ("ownership_percentage", models.FloatField()),
                (
                    "child",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="child",
                        to="beacon.entity",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parent",
                        to="beacon.entity",
                    ),
                ),
                (
                    "period",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="beacon.period"
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
            model_name="period",
            name="scenario",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="beacon.scenario"
            ),
        ),
        migrations.AddField(
            model_name="entity",
            name="scenario",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="beacon.scenario"
            ),
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
                    "entity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="beacon.entity"
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
            name="entity", unique_together={("name", "scenario")},
        ),
        migrations.AlterUniqueTogether(
            name="account", unique_together={("account_name", "scenario", "entity")},
        ),
    ]
