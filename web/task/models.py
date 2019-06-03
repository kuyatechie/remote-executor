from django.db import models


class Task(models.Model):
    uid = models.UUIDField(null=False)
    created = models.DateTimeField(null=False)
    script = models.CharField(max_length=50)
    arguments = models.CharField(max_length=100)
    started = models.DateTimeField(null=True)
    finished = models.DateTimeField(null=True)
    diskspace_before = models.IntegerField(null=True)
    diskspace_after = models.IntegerField(null=True)
    retcode = models.IntegerField(null=True)

    class Meta:
        ordering = ('created', )
