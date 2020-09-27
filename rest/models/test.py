from django.db import models
from django.contrib.postgres import fields
from .user import User
from .status import Status
from .test_kit import TestKit
from .lab_configuration import LabConfiguration
from .machine_type import MachineType


class Test(models.Model):
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        default=1,
        blank=True,
        null=True
    )
    nsamples = models.SmallIntegerField()
    prevalence = models.FloatField()
    remark = models.TextField(blank=True)
    test_kit = models.ForeignKey(TestKit, on_delete=models.CASCADE)
    machine_type = models.ForeignKey(MachineType, on_delete=models.CASCADE)
    max_poolsize = models.SmallIntegerField()
    poolingmatrix_filename = models.CharField(max_length=255, blank=True)
    poolingscheme_filename = models.CharField(max_length=255, blank=True)
    testctresults_filename = models.CharField(max_length=255, blank=True)
    npositive = models.SmallIntegerField(blank=True, null=True)
    ninconclusive = models.SmallIntegerField(blank=True, null=True)
    nnegative = models.SmallIntegerField(blank=True, null=True)
    positive = fields.JSONField(blank=True, null=True)
    negative = fields.JSONField(blank=True, null=True)
    inconclusive = fields.JSONField(blank=True, null=True)
    report_filename = models.CharField(max_length=255, blank=True)
    pooling_matrix_download_url = None

    def save(self, *args, **kwargs):
        if not self.poolingmatrix_filename or self.poolingmatrix_filename == "":
            self.poolingmatrix_filename = LabConfiguration.objects.get(lab_id=self.assigned_to.lab_id).poolingmatrix_filename
        super(Test, self).save(*args, **kwargs)
