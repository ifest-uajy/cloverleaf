# Generated by Django 2.2.7 on 2019-11-15 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_pengirim', models.CharField(max_length=50)),
                ('email_pengirim', models.CharField(max_length=50)),
                ('pesan', models.CharField(max_length=500)),
                ('recieved_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
