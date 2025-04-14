"""
Admin configuration for dicom_app
"""
from django.contrib import admin
from .models import DicomConfiguration, AWSConfiguration, DicomFile

@admin.register(DicomConfiguration)
class DicomConfigurationAdmin(admin.ModelAdmin):
    """Admin interface for DICOM configuration"""
    list_display = ('ae_title', 'port_number', 'modified_date')

@admin.register(AWSConfiguration)
class AWSConfigurationAdmin(admin.ModelAdmin):
    """Admin interface for AWS configuration"""
    list_display = ('bucket_name', 'modified_date')
    
@admin.register(DicomFile)
class DicomFileAdmin(admin.ModelAdmin):
    """Admin interface for DICOM files"""
    list_display = ('file_name', 'patient_name', 'study_date', 'upload_date')
    search_fields = ('file_name', 'patient_name', 'study_date')
    list_filter = ('upload_date', 'study_date')
