# Generated by Django 3.1.7 on 2021-07-28 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0033_auto_20210724_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='target',
            name='cred',
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='target',
            name='interface',
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
    ]
