"""
Models for dicom_app
"""
from django.db import models
from django.utils import timezone

class DicomConfiguration(models.Model):
    """DICOM configuration settings model"""
    ae_title = models.CharField(max_length=100, verbose_name="AE Title")
    port_number = models.IntegerField(verbose_name="Port Number")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "DICOM Configuration"
        verbose_name_plural = "DICOM Configuration"

    def __str__(self):
        return f"DICOM Config: {self.ae_title} ({self.port_number})"

class AWSConfiguration(models.Model):
    """AWS S3 configuration settings model"""
    access_key = models.CharField(max_length=255, verbose_name="Access Key")
    secret_key = models.CharField(max_length=255, verbose_name="Secret Key")
    bucket_name = models.CharField(max_length=255, verbose_name="Bucket Name")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AWS Configuration"
        verbose_name_plural = "AWS Configuration"

    def __str__(self):
        return f"AWS Config: {self.bucket_name}"

class DicomFile(models.Model):
    """DICOM file model to store metadata"""
    file_name = models.CharField(max_length=255)
    s3_object_key = models.CharField(max_length=512)
    patient_id = models.CharField(max_length=64, blank=True, null=True)
    patient_name = models.CharField(max_length=255, blank=True, null=True)
    study_date = models.DateField(blank=True, null=True)
    study_instance_uid = models.CharField(max_length=255, blank=True, null=True)
    series_instance_uid = models.CharField(max_length=255, blank=True, null=True)
    sop_instance_uid = models.CharField(max_length=255, blank=True, null=True)
    modality = models.CharField(max_length=16, blank=True, null=True)
    study_description = models.CharField(max_length=255, blank=True, null=True)
    series_description = models.CharField(max_length=255, blank=True, null=True)
    upload_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "DICOM File"
        verbose_name_plural = "DICOM Files"

    def __str__(self):
        return f"{self.file_name} - {self.patient_name or 'Unknown'}"
