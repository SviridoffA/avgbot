# Generated by Django 3.1.7 on 2021-07-30 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0037_auto_20210730_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='target',
            name='service',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
