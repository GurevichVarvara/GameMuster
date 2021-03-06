# Generated by Django 3.1.7 on 2021-04-30 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="birthday",
            field=models.DateField(
                blank=True, default=None, null=True, verbose_name="Birthday"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
