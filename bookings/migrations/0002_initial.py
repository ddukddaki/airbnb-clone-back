# Generated by Django 4.1 on 2023-01-03 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("experiences", "0001_initial"),
        ("bookings", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="experience",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="experiences.experience",
            ),
        ),
    ]