# Generated by Django 2.2.6 on 2021-08-29 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_auto_20210829_1135'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-created',)},
        ),
    ]
