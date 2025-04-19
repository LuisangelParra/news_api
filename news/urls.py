from django.urls import path
from .views import UploadArticleToBigQuery, TestBigQueryConnection

urlpatterns = [
    path('test-bq/', TestBigQueryConnection.as_view()),
    path('upload-article/', UploadArticleToBigQuery.as_view()),
]