# Generated by Django 4.1.1 on 2022-09-17 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_resource_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='production',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]