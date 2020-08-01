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
    samples = models.SmallIntegerField()
    inconclusive_samples = models.SmallIntegerField(blank=True, null=True)
    positive_samples = models.SmallIntegerField(blank=True, null=True)
    remark = models.TextField(blank=True)
    test_kit = models.ForeignKey(TestKit, on_delete=models.CASCADE)
    machine_type = models.ForeignKey(MachineType, on_delete=models.CASCADE)
    file = models.ForeignKey(
        File,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    pooling_matrix = models.ForeignKey(
        Matrix,
        on_delete=models.CASCADE,
        related_name='pooling_matrix',
        blank=True,
        null=True
    )
    mastermix_matrix = models.ForeignKey(
        Matrix,
        on_delete=models.CASCADE,
        related_name='mastermix_matrix',
        blank=True,
        null=True
    )
    patient_id_map = fields.JSONField()
    results_1 = models.TextField(blank=True)
    results_2 = models.TextField(blank=True)
    prevalence = models.FloatField()

    def get_pooling_matrix_url(self):
        payload = {
            "nsamples": self.samples,
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