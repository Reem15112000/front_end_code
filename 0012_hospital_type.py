# Generated by Django 3.2 on 2023-06-21 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_patient_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='type',
            field=models.CharField(choices=[('private', 'Private'), ('public', 'Public')], default='public', max_length=20),
            preserve_default=False,
        ),
    ]
