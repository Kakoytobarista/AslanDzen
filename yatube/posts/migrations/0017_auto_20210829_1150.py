# Generated by Django 2.2.6 on 2021-08-29 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0016_auto_20210829_1147'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created']},
        ),
    ]