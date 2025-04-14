"""
Forms for dicom_app
"""
from django import forms
from .models import DicomConfiguration, AWSConfiguration, DicomFile

class DicomConfigurationForm(forms.ModelForm):
    """Form for DICOM configuration settings"""
    class Meta:
        model = DicomConfiguration
        fields = ['ae_title', 'port_number']
        widgets = {
            'ae_title': forms.TextInput(attrs={'class': 'form-control'}),
            'port_number': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '65535'}),
        }

class AWSConfigurationForm(forms.ModelForm):
    """Form for AWS S3 configuration settings"""
    class Meta:
        model = AWSConfiguration
        fields = ['access_key', 'secret_key', 'bucket_name']
        widgets = {
            'access_key': forms.TextInput(attrs={'class': 'form-control'}),
            'secret_key': forms.PasswordInput(attrs={'class': 'form-control'}),
            'bucket_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class DicomUploadForm(forms.Form):
    """Form for uploading DICOM files"""
    dicom_file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Select DICOM files"
    )
