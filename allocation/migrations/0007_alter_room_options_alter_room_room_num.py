# Generated by Django 4.2.5 on 2023-10-01 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allocation', '0006_alter_room_room_num'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['room_num']},
        ),
        migrations.AlterField(
            model_name='room',
            name='room_num',
            field=models.IntegerField(),
        ),
    ]
