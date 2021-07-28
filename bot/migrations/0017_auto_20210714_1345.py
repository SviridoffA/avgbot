# Generated by Django 3.1.7 on 2021-07-14 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0016_auto_20210621_1802'),
    ]

    operations = [
        migrations.CreateModel(
            name='Org',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Организации',
                'verbose_name_plural': 'Организации',
            },
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'Группы устройств', 'verbose_name_plural': 'Группы устройств'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='group',
        ),
        migrations.AddField(
            model_name='target',
            name='org',
            field=models.ManyToManyField(blank=True, null=True, to='bot.Org'),
        ),
        migrations.AddField(
            model_name='user',
            name='org',
            field=models.ManyToManyField(blank=True, null=True, to='bot.Org'),
        ),
    ]
