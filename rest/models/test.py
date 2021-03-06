from django.db import models
from django.contrib.postgres import fields
from .user import User
from .status import Status
from .test_kit import TestKit
from .lab_configuration import LabConfiguration
from .machine_type import MachineType
from rest.util.gc_util import get_pooling_matrix_download_url, get_report_download_url, get_result_download_url
import json


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
    err_msg = models.CharField(max_length=255, blank=True, default="none")
    create_time = models.DateTimeField(auto_now_add=True)
    def get_pooling_matrix_url(self):
        payload = {
            "nsamples": self.nsamples,
            "prevalence": self.prevalence,
            "genes": ", ".join(self.test_kit.gene_type),
            "testid": self.id,
            "lab_name": self.assigned_to.lab_id.__str__(),
            "poolingmatrix_filename": self.poolingmatrix_filename
        }
        try:
            resp = get_pooling_matrix_download_url(payload=json.dumps(payload))
        except Exception as e:
            raise(e)
        return resp
    
    def get_report_url(self):
        object_name = self.report_filename
        try:
            resp = get_report_download_url(object_name= object_name)
        except Exception as e:
            raise(e)
        return resp
    
    def get_result_url(self):
        object_name = self.testctresults_filename
        try:
            resp = get_result_download_url(object_name= object_name)
        except Exception as e:
            raise(e)
        return resp

    def save(self, *args, **kwargs):
        if not self.poolingmatrix_filename or self.poolingmatrix_filename == "":
            self.poolingmatrix_filename = LabConfiguration.objects.get(lab_id=self.assigned_to.lab_id).poolingmatrix_filename

        self.poolingscheme_filename, self.pooling_matrix_download_url = self.get_pooling_matrix_url()
        super(Test, self).save(*args, **kwargs)
