# Generated by Django 3.0.3 on 2020-02-26 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("osusu_system", "0006_claim_date")]

    operations = [
        migrations.AlterField(model_name="claim", name="date", field=models.DateField())
    ]
