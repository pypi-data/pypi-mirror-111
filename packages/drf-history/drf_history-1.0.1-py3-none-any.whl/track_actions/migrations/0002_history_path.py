# Generated by Django 2.2.3 on 2019-12-23 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track_actions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='path',
            field=models.CharField(default='', editable=False, max_length=255),
        ),
    ]
