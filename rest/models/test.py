from django.db import models
from django.contrib.postgres import fields
from .user import User
from .status import Status
from .test_kit import TestKit
from .machine_type import MachineType
from rest.util.gc_util import get_pooling_matrix_download_url
import json


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

    def get_pooling_matrix_url(self):
        payload = {
            "nsamples": self.nsamples,
            "prevalence": self.prevalence,
            "genes": ", ".join(self.test_kit.gene_type),
            "testid": self.id,
            "lab_name": self.assigned_to.lab_id.__str__()
            "poolingscheme_filename": self.poolingscheme_filename
        }
        return get_pooling_matrix_download_url(payload=json.dumps(payload))

    def save(self, *args, **kwargs):
        self.poolingmatrix_filename, self.pooling_matrix_download_url = self.get_pooling_matrix_url()
        super(Test, self).save(*args, **kwargs)
