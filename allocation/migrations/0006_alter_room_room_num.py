# Generated by Django 4.2.5 on 2023-10-01 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allocation', '0005_room_allocatedrooms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_num',
            field=models.IntegerField(unique=True),
        ),
    ]
