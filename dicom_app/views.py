"""
Views for dicom_app
"""
import os
import tempfile
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings

from .models import DicomConfiguration, AWSConfiguration, DicomFile
from .forms import DicomConfigurationForm, AWSConfigurationForm, DicomUploadForm
from .utils import read_dicom_metadata, upload_to_s3, check_s3_connection

def index(request):
    """Home page view"""
    return render(request, 'dicom_app/index.html')

def dicom_config(request):
    """DICOM configuration view"""
    dicom_config_obj = DicomConfiguration.objects.first()
    
    if dicom_config_obj:
        form = DicomConfigurationForm(instance=dicom_config_obj)
    else:
        form = DicomConfigurationForm()
    
    return render(request, 'dicom_app/dicom_config.html', {'form': form})

def aws_config(request):
    """AWS S3 configuration view"""
    aws_config_obj = AWSConfiguration.objects.first()
    
    if aws_config_obj:
        # Don't display the actual secret key for security
        aws_config_obj.secret_key = "********"
        form = AWSConfigurationForm(instance=aws_config_obj)
    else:
        form = AWSConfigurationForm()
    
    return render(request, 'dicom_app/aws_config.html', {'form': form})

def update_dicom_config(request):
    """Update DICOM configuration"""
    if request.method == 'POST':
        dicom_config_obj = DicomConfiguration.objects.first()
        
        if dicom_config_obj:
            form = DicomConfigurationForm(request.POST, instance=dicom_config_obj)
        else:
            form = DicomConfigurationForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "DICOM configuration updated successfully!")
        else:
            messages.error(request, "Error updating DICOM configuration!")
            
    return redirect('dicom_app:dicom_config')

def update_aws_config(request):
    """Update AWS S3 configuration"""
    if request.method == 'POST':
        aws_config_obj = AWSConfiguration.objects.first()
        
        if aws_config_obj:
            # If the secret key field is not modified (still contains asterisks), keep the old value
            if request.POST.get('secret_key') == '********':
                post_data = request.POST.copy()
                post_data['secret_key'] = aws_config_obj.secret_key
                form = AWSConfigurationForm(post_data, instance=aws_config_obj)
            else:
                form = AWSConfigurationForm(request.POST, instance=aws_config_obj)
        else:
            form = AWSConfigurationForm(request.POST)
        
        if form.is_valid():
            config = form.save()
            
            # Test the AWS connection
            connection_status = check_s3_connection(
                config.access_key,
                config.secret_key,
                config.bucket_name
            )
            
            if connection_status['success']:
                messages.success(request, "AWS configuration updated successfully! Connection verified.")
            else:
                messages.warning(request, f"AWS configuration saved, but connection test failed: {connection_status['error']}")
        else:
            messages.error(request, "Error updating AWS configuration!")
            
    return redirect('dicom_app:aws_config')

def upload_dicom(request):
    """Upload DICOM files view"""
    if request.method == 'POST':
        form = DicomUploadForm(request.POST, request.FILES)
        
        # Check if AWS config exists
        aws_config = AWSConfiguration.objects.first()
        if not aws_config:
            messages.error(request, "AWS S3 configuration is missing. Please configure it first.")
            return redirect('dicom_app:aws_config')
        
        # Get files from request
        files = request.FILES.getlist('dicom_file')
        
        if not files:
            messages.error(request, "No files selected for upload.")
            return render(request, 'dicom_app/upload.html', {'form': form})
        
        success_count = 0
        error_count = 0
        
        for dicom_file in files:
            # Save file temporarily
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                for chunk in dicom_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name
            
            try:
                # Read DICOM metadata
                metadata = read_dicom_metadata(temp_file_path)
                
                if not metadata:
                    error_count += 1
                    messages.error(request, f"Failed to read DICOM metadata from {dicom_file.name}")
                    continue
                
                # Upload to S3
                s3_key = f"dicom/{metadata.get('study_instance_uid', 'unknown')}/{dicom_file.name}"
                s3_result = upload_to_s3(
                    temp_file_path,
                    aws_config.access_key,
                    aws_config.secret_key,
                    aws_config.bucket_name,
                    s3_key
                )
                
                if s3_result['success']:
                    # Save metadata to database
                    dicom_obj = DicomFile(
                        file_name=dicom_file.name,
                        s3_object_key=s3_key,
                        patient_id=metadata.get('patient_id'),
                        patient_name=metadata.get('patient_name'),
                        study_date=metadata.get('study_date'),
                        study_instance_uid=metadata.get('study_instance_uid'),
                        series_instance_uid=metadata.get('series_instance_uid'),
                        sop_instance_uid=metadata.get('sop_instance_uid'),
                        modality=metadata.get('modality'),
                        study_description=metadata.get('study_description'),
                        series_description=metadata.get('series_description')
                    )
                    dicom_obj.save()
                    success_count += 1
                else:
                    error_count += 1
                    messages.error(request, f"Failed to upload {dicom_file.name} to S3: {s3_result['error']}")
            
            except Exception as e:
                error_count += 1
                messages.error(request, f"Error processing {dicom_file.name}: {str(e)}")
            
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
        
        if success_count > 0:
            messages.success(request, f"Successfully uploaded {success_count} DICOM file(s).")
        
        if error_count > 0:
            messages.warning(request, f"Failed to upload {error_count} file(s). See error messages for details.")
        
        return redirect('dicom_app:upload_dicom')
    
    else:  # GET request
        form = DicomUploadForm()
        
    return render(request, 'dicom_app/upload.html', {'form': form})
