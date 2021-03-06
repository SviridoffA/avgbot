# Generated by Django 3.1.7 on 2021-04-19 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0008_auto_20210419_1035'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группа',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.ManyToManyField(blank=True, null=True, to='bot.Group'),
        ),
    ]
