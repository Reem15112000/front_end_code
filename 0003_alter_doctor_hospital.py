# Generated by Django 3.2 on 2023-05-13 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_doctor_work_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='main.hospital'),
        ),
    ]
