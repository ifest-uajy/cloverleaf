# Generated by Django 2.2.6 on 2019-11-03 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authsys', '0008_auto_20191103_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nomor_telepon',
            field=models.IntegerField(),
        ),
    ]