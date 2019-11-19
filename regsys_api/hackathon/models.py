from django.db import models
from django.utils.timezone import utc
import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
from xkcdpass import xkcd_password as xp
import json

from threading import Thread

from regsys_api.authsys.models import User
import requests

def getxkcdpass():
    wordfile = xp.locate_wordfile()
    config = xp.generate_wordlist(wordfile=wordfile, min_length=5, max_length=8)
    return (xp.generate_xkcdpassword(config, acrostic=False , delimiter="-", numwords=4))

class Track(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    closed_date = models.DateTimeField(null=True)
    team_max_member = models.IntegerField(default=1)
    team_min_member = models.IntegerField(default=1)
    slug_name = models.CharField(max_length=50)
    biaya_pendaftaran = models.IntegerField()

    def __str__(self):
        return self.name

    @property
    def isExpired(self):
        if self.closed_date:
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            if(now > self.closed_date):
                return True
            else:
                return False

    class Meta:
        verbose_name = 'Kompetisi'
        verbose_name_plural = 'Kompetisi'

class HackathonTask(models.Model):

    FILE_SUBMISSION = 'file_uploader'
    PAYMENT_SUBMISSION = 'payment_verification'
    ANNOUNCEMENT = 'pengumuman'
    TYPE_CHOICES = (
        (FILE_SUBMISSION, 'File Uploader'),
        (PAYMENT_SUBMISSION, 'Verifikasi Pembayaran'),
        (ANNOUNCEMENT, 'Pengumuman')
    )

    order = models.IntegerField()
    track = models.ForeignKey(to=Track, related_name='tracks', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    deskripsi = models.TextField()
    deadline = models.DateTimeField(null=True)
    task_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    require_validation = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {}".format(self.track, self.name)

    class Meta:
        verbose_name = 'Task Lomba'
        verbose_name_plural = 'Task Lomba'

class HackathonTeams(models.Model):

    track = models.ForeignKey(
        to=Track, related_name='teams', on_delete=models.PROTECT)
    name = models.CharField(max_length=100, unique=True)
    institution = models.CharField(max_length=100)
    alamat_institusi = models.CharField(max_length=500)
    """
    Field kontak pendamping
    """

    nama_pendamping = models.CharField(max_length=50)
    nomor_telepon_pendamping = models.CharField(max_length=20)

    """
    token
    """

    invitation_token = models.CharField(max_length=100, default=getxkcdpass())

    current_task = models.ForeignKey(to=HackathonTask, related_name='active', on_delete=models.PROTECT)

    members = models.ManyToManyField(
        to=User, related_name='teams', through='HackathonTeamsMember')
    team_leader = models.ForeignKey(to=User, related_name='team_leader', on_delete=models.PROTECT)
    is_blacklisted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def sudah_selesai_current_task(self):
        current_task_count = self.current_task
        update_current_task_count = self.task_response.filter(task=self.current_task, status=TaskResponse.DONE)
        return current_task_count == update_current_task_count

    @property
    def task_list(self):
        return HackathonTask.objects.filter(track=self.track).all()

    @property
    def task_response_list(self):
        return TaskResponse.objects.filter(team=self).all()

    @property
    def jumlah_member(self):
        return self.members.count()
        
    @property
    def bisa_up_task(self):
        if(self.members.count() >= self.track.team_min_member):
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        if self.pk is None and not hasattr(self, 'current_task'):
            self.current_task = HackathonTask.objects.filter(track=self.track).first()

        super(HackathonTeams, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Tim'
        verbose_name_plural = 'Tim'

class HackathonTeamsMember(models.Model):

    team = models.ForeignKey(to=HackathonTeams, related_name='team_members', on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, related_name='team_member', null=True, blank=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s (%s)' % (self.team.name, self.user.full_name, self.user.email)
    
    class Meta:
        unique_together = (('team', 'user'),)
        get_latest_by = 'created_at'
        verbose_name = 'Anggota Tim'
        verbose_name_plural = 'Anggota Tim'


class TaskResponse(models.Model):

    WAITING = 'menunggu_verifikasi'
    DONE = 'selesai'
    REJECTED = 'ditolak'
    STATUS_CHOICES = (
        (WAITING, 'Menunggu Verifikasi'),
        (DONE, 'Selesai'),
        (REJECTED, 'Ditolak'),
    )

    task = models.ForeignKey(to=HackathonTask, related_name='task_response', on_delete=models.PROTECT)
    team = models.ForeignKey(to=HackathonTeams, related_name='task_response', on_delete=models.CASCADE)
    response = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    updated_at = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {}".format(self.task.name, self.team.name)

    def save(self, *args, **kwargs):
        if self.pk is None and (self.status is None or self.status == ''):
            if self.task.require_validation:
                self.status = self.WAITING
                self.is_verified = False
            else:
                self.status = self.DONE
                self.is_verified = True

            #if self.task.track.pk != self.team.track.pk:
                #raise ValidationError('Track Kompetisi dan Track Tim haruslah sama.')
            #else:
        
        super(TaskResponse, self).save(*args, **kwargs)

    class Meta:
        unique_together = (('task', 'team'),)
        get_latest_by = 'created_at'
        verbose_name = 'Respon Task Tim'
        verbose_name_plural = 'Respon Task Tim'
