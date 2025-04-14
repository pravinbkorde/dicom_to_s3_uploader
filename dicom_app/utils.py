"""
Utility functions for dicom_app
"""
from datetime import datetime
import pydicom
import boto3
from botocore.exceptions import ClientError

def read_dicom_metadata(file_path):
    """
    Read metadata from a DICOM file
    
    Args:
        file_path: Path to the DICOM file
        
    Returns:
        Dictionary containing extracted metadata or None if file can't be read
    """
    try:
        dicom_data = pydicom.dcmread(file_path)
        
        # Extract relevant metadata
        metadata = {}
        
        # PatientID is a required field in DICOM standard
        metadata['patient_id'] = getattr(dicom_data, 'PatientID', None)
        
        # PatientName is a required field, but handle it safely
        if hasattr(dicom_data, 'PatientName'):
            metadata['patient_name'] = str(dicom_data.PatientName)
        else:
            metadata['patient_name'] = None
            
        # Handle study date (convert from DICOM DA format to Python date)
        if hasattr(dicom_data, 'StudyDate') and dicom_data.StudyDate:
            try:
                # DICOM date format is YYYYMMDD
                study_date_str = str(dicom_data.StudyDate)
                metadata['study_date'] = datetime.strptime(study_date_str, '%Y%m%d').date()
            except ValueError:
                metadata['study_date'] = None
        else:
            metadata['study_date'] = None
            
        # UIDs
        metadata['study_instance_uid'] = getattr(dicom_data, 'StudyInstanceUID', None)
        metadata['series_instance_uid'] = getattr(dicom_data, 'SeriesInstanceUID', None)
        metadata['sop_instance_uid'] = getattr(dicom_data, 'SOPInstanceUID', None)
        
        # Other useful metadata
        metadata['modality'] = getattr(dicom_data, 'Modality', None)
        metadata['study_description'] = getattr(dicom_data, 'StudyDescription', None)
        metadata['series_description'] = getattr(dicom_data, 'SeriesDescription', None)
        
        return metadata
        
    except Exception as e:
        print(f"Error reading DICOM file: {str(e)}")
        return None

def upload_to_s3(file_path, access_key, secret_key, bucket_name, object_key):
    """
    Upload a file to AWS S3
    
    Args:
        file_path: Path to local file
        access_key: AWS access key
        secret_key: AWS secret key
        bucket_name: S3 bucket name
        object_key: S3 object key (destination path in S3)
        
    Returns:
        Dictionary with success status and error message if applicable
    """
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        
        # Upload file to S3
        s3_client.upload_file(file_path, bucket_name, object_key)
        
        return {
            'success': True,
            'error': None
        }
        
    except ClientError as e:
        return {
            'success': False,
            'error': str(e)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Unexpected error: {str(e)}"
        }

def check_s3_connection(access_key, secret_key, bucket_name):
    """
    Test AWS S3 connection with given credentials
    
    Args:
        access_key: AWS access key
        secret_key: AWS secret key
        bucket_name: S3 bucket name
        
    Returns:
        Dictionary with connection status and error message if applicable
    """
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        
        # Try to list objects to verify permissions (limit to 1 to minimize data transfer)
        s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
        
        return {
            'success': True,
            'error': None
        }
        
    except ClientError as e:
        return {
            'success': False,
            'error': str(e)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Unexpected error: {str(e)}"
        }
