# Generated by Django 2.2.7 on 2019-11-16 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon', '0016_auto_20191115_2202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskresponse',
            name='announcement_desc',
        ),
        migrations.RemoveField(
            model_name='taskresponse',
            name='announcement_title',
        ),
        migrations.RemoveField(
            model_name='taskresponse',
            name='file_path',
        ),
        migrations.AlterField(
            model_name='hackathonteams',
            name='invitation_token',
            field=models.CharField(default='dimly-skirt-hacking-crafter', max_length=100),
        ),
    ]
