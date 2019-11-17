# Generated by Django 2.2.7 on 2019-11-15 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon', '0004_auto_20191115_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hackathontask',
            name='stage',
        ),
        migrations.RemoveField(
            model_name='hackathonteams',
            name='current_stage',
        ),
        migrations.AddField(
            model_name='hackathontask',
            name='order',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hackathontask',
            name='track',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to='hackathon.Track'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hackathonteams',
            name='current_task',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='active', to='hackathon.HackathonTask'),
        ),
        migrations.AlterField(
            model_name='hackathonteams',
            name='invitation_token',
            field=models.CharField(default='matchbox-chair-obituary-winner', max_length=100),
        ),
        migrations.DeleteModel(
            name='HackathonStage',
        ),
    ]