# Generated by Django 3.2 on 2023-05-18 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20230518_0210'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='type',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
