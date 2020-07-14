from django.db import models
from django.contrib.postgres import fields
from .labmember import LabMember
from .status import Status
from .test_kit import TestKit
from .machine_type import MachineType
from .file import File
from .matrix import Matrix

class Test(models.Model):
    assigned_to = models.ForeignKey(LabMember, on_delete = models.CASCADE)
    status = models.ForeignKey(Status, on_delete = models.CASCADE)
    samples = models.SmallIntegerField()
    suspected_samples = models.SmallIntegerField()
    positive_samples = models.SmallIntegerField()
    test_kit = models.ForeignKey(TestKit, on_delete = models.CASCADE)
    machine_type = models.ForeignKey(MachineType, on_delete = models.CASCADE)
    remark = models.TextField()
    file = models.ForeignKey(File, on_delete = models.CASCADE)
    pooling_matrix = models.ForeignKey(Matrix, on_delete = models.CASCADE, related_name='pooling_matrix')
    mastermix_matrix = models.ForeignKey(Matrix, on_delete = models.CASCADE, related_name='mastermix_matrix')
    patient_id_map = fields.JSONField()
    results_1 = models.TextField()
    results_2 = models.TextField()
