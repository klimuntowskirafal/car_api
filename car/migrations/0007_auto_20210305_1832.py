# Generated by Django 2.2.17 on 2021-03-05 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0006_auto_20210304_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='model',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]