# Generated by Django 3.2 on 2021-04-16 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_alter_city_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female'), ('other', 'other')], max_length=128, null=True),
        ),
    ]
