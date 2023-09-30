# Generated by Django 4.2.5 on 2023-09-30 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allocation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hall',
            name='picture',
            field=models.ImageField(default='img/bld.jpeg', upload_to=''),
        ),
        migrations.AddField(
            model_name='hall',
            name='status',
            field=models.CharField(choices=[('available', 'available'), ('unavailable', 'unavailable')], default='available', max_length=12),
        ),
    ]
