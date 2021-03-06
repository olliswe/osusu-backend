# Generated by Django 3.0.3 on 2020-02-17 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Claim",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("open", "Open"),
                            ("approved", "Approved"),
                            ("approved_paid", "Approved & Paid"),
                            ("rejected", "Rejected"),
                        ],
                        max_length=50,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Fund",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "actual_amount",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=100,
                        verbose_name="Actual Amount (filled by bank)",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Garage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=500, verbose_name="Garage Name")),
            ],
        ),
        migrations.CreateModel(
            name="Part",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Part name")),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=100,
                        verbose_name="Part Amount (SLL)",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tricycle",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "full_name",
                    models.CharField(max_length=100, verbose_name="Full Name"),
                ),
                ("start_date", models.DateField(verbose_name="Start Date")),
                (
                    "maintenance",
                    models.BooleanField(default=True, verbose_name="In Maintenance"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=100, verbose_name="amount"
                    ),
                ),
                ("date", models.DateField(verbose_name="payment date")),
                (
                    "tricycle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="osusu_system.Tricycle",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PartClaim",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.IntegerField()),
                (
                    "claim",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="osusu_system.Claim",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="claim",
            name="garage",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="osusu_system.Garage"
            ),
        ),
        migrations.AddField(
            model_name="claim",
            name="tricycle",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="osusu_system.Tricycle"
            ),
        ),
    ]
