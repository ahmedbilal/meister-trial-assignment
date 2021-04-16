# Generated by Django 3.2 on 2021-04-16 11:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_auto_20210416_1124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(blank=True, max_length=256, null=True)),
                ('sales_number', models.IntegerField(blank=True, null=True)),
                ('revenue', models.FloatField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
