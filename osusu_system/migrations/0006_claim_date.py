# Generated by Django 3.0.3 on 2020-02-26 13:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [("osusu_system", "0005_auto_20200221_0954")]

    operations = [
        migrations.AddField(
            model_name="claim",
            name="date",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        )
    ]
