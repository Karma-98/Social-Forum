# Generated by Django 3.0.1 on 2020-01-03 15:55

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200101_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='photo',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='accounts'),
        ),
    ]
