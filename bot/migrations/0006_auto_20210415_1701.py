# Generated by Django 3.1.7 on 2021-04-15 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_message_step'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='organization',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
