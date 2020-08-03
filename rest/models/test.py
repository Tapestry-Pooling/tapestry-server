from django.db import models
from django.contrib.postgres import fields
from .user import User
from .status import Status
from .test_kit import TestKit
from .machine_type import MachineType
from .file import File
from .matrix import Matrix
from .lab import Lab
from rest.util.gcf_call import pooling_matrix_gcf
import json


class Test(models.Model):
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    lab_id = models.SmallIntegerField(default=0)
    nsamples = models.SmallIntegerField()
    prevalence = models.FloatField()
    remark = models.TextField(blank=True)
    test_kit = models.ForeignKey(TestKit, on_delete=models.CASCADE)
    machine_type = models.ForeignKey(MachineType, on_delete=models.CASCADE)
    poolingscheme_filename = models.TextField(blank=True)
    testctresults_filename = models.TextField(blank=True)
    ninconclusive = models.SmallIntegerField(blank=True, null=True)
    npositive = models.SmallIntegerField(blank=True, null=True)
    positive = fields.JSONField(null=True)
    inconclusive = fields.JSONField(null=True)

    def get_pooling_matrix_url(self):
        payload = {
            "nsamples": self.nsamples,
            "prevalence": self.prevalence,
            "genes": ", ".join(self.test_kit.gene_type),
            "testid": self.id,
            "lab_name": self.assigned_to.lab_id.__str__()
        }
        status_code, signed_url = pooling_matrix_gcf(payload=json.dumps(payload))
        return signed_url

    def save(self, *args, **kwargs):
        super(Test, self).save(*args, **kwargs)
        self.pooling_matrix_url = self.get_pooling_matrix_url()
