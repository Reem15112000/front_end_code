# Generated by Django 4.2.2 on 2023-07-02 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20230622_0720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
