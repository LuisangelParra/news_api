from django.urls import path
from .views import UploadArticleToBigQuery

urlpatterns = [
    path('upload-article/', UploadArticleToBigQuery.as_view()),
]