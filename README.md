# DICOM Manager

A Django-based DICOM file management system with AWS S3 integration for medical imaging file storage.

## Features

- DICOM Configuration: Set up AE Title and Port Number
- AWS S3 Configuration: Configure Access Key, Secret Key, and Bucket Name
- DICOM File Upload: Upload DICOM files and extract metadata
- Storage: Store DICOM files in AWS S3 with organized paths
- Metadata: Extract and store DICOM metadata in database

## Requirements

- Django (5.0.0 or later)
- pydicom (3.0.0 or later)
- boto3 (1.37.0 or later)

## Installation

1. Clone this repository
2. Install the required packages:
   ```
   pip install django pydicom boto3
   ```
3. Apply migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Run the development server:
   ```
   python manage.py runserver 0.0.0.0:5000
   ```

## Usage

1. Configure DICOM settings (AE Title and Port Number) under "DICOM Config"
2. Set up AWS S3 credentials (Access Key, Secret Key, Bucket Name) under "AWS S3 Config"
3. Upload DICOM files through the "Upload DICOM" page
4. The system extracts metadata from the files and uploads them to AWS S3

## Database

The application uses Django's default SQLite database to store:
- DICOM configuration settings
- AWS S3 configuration
- DICOM file metadata

## AWS S3 Integration

The system uses boto3 to connect to AWS S3 and:
- Verify AWS credentials and bucket access
- Upload DICOM files with organized paths based on Study Instance UID
- Store S3 object keys in the database for future reference
