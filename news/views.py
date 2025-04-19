from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.cloud import bigquery
from .serializers import NewsArticleSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json
import tempfile

class UploadArticleToBigQuery(APIView):
    @swagger_auto_schema(
        operation_description="Upload a single news article and push it to BigQuery",
        request_body=NewsArticleSerializer,
        responses={
            201: openapi.Response(
                description="Article successfully uploaded to BigQuery",
                schema=NewsArticleSerializer
            ),
            400: "Invalid input data",
            500: "BigQuery error"
        },
        tags=["News Articles"]
    )
    def post(self, request):
        serializer = NewsArticleSerializer(data=request.data)
        if serializer.is_valid():
            article = serializer.save()

            client = bigquery.Client()
            # Replace with your actual BigQuery dataset and table ID
            # Ensure that the dataset and table exist in your BigQuery project
            # and that the service account has permission to write to it.
            # Example: "your_project.your_dataset.your_table"
            table_id = "noticias-api-457314.noticias_dataset.news_articles"

            row = {
                "content": article.content,
                "description": article.description,
                "location": article.location,
                "published_at": article.published_at.isoformat(),
                "source": article.source,
                "title": article.title,
                "url": article.url,
            }

            with tempfile.NamedTemporaryFile("w+", suffix=".json") as tmpfile:
                tmpfile.write(json.dumps(row) + "\n")
                tmpfile.seek(0)

                job_config = bigquery.LoadJobConfig(
                    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
                    autodetect=True,
                    write_disposition=bigquery.WriteDisposition.WRITE_APPEND
                )

                load_job = client.load_table_from_file(
                    tmpfile, table_id, job_config=job_config
                )
                load_job.result()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)
