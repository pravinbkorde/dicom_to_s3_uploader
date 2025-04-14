"""
URL patterns for dicom_app
"""
from django.urls import path
from . import views

app_name = 'dicom_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('dicom-config/', views.dicom_config, name='dicom_config'),
    path('aws-config/', views.aws_config, name='aws_config'),
    path('upload/', views.upload_dicom, name='upload_dicom'),
    path('update-dicom-config/', views.update_dicom_config, name='update_dicom_config'),
    path('update-aws-config/', views.update_aws_config, name='update_aws_config'),
]
