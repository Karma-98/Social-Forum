# Generated by Django 3.0.1 on 2020-02-01 15:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('followers', '0003_auto_20200201_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followersystem',
            name='current_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
