"""
Application configuration for dicom_app
"""
from django.apps import AppConfig


class DicomAppConfig(AppConfig):
    """App configuration for the DICOM application"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dicom_app'
