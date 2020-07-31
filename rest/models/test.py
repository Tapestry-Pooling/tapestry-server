from django.db import models
from django.contrib.postgres import fields
from .user import User
from .status import Status
from .test_kit import TestKit
from .machine_type import MachineType
from .file import File
from .matrix import Matrix


class Test(models.Model):
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    nsamples = models.SmallIntegerField()
    prevalence = models.FloatField()
    remark = models.TextField(blank=True)
    test_kit = models.ForeignKey(TestKit, on_delete=models.CASCADE)
    machine_type = models.ForeignKey(MachineType, on_delete=models.CASCADE)
    filename = models.TextField(blank=True)
    ninconclusive = models.SmallIntegerField(blank=True, null=True)
    npositive = models.SmallIntegerField(blank=True, null=True)
    positive = fields.JSONField(null=True)
    inconclusive = fields.JSONField(null=True)
