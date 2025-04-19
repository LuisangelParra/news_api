from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.cloud import bigquery
from .models import NewsArticle
from .serializers import NewsArticleSerializer

class TestBigQueryConnection(APIView):
    def get(self, request):
        try:
            client = bigquery.Client()
            datasets = list(client.list_datasets())
            dataset_names = [ds.dataset_id for ds in datasets]
            return Response({"datasets": dataset_names})
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class UploadArticleToBigQuery(APIView):
    def post(self, request):
        serializer = NewsArticleSerializer(data=request.data)
        if serializer.is_valid():
            article = serializer.save()  # Save to Django DB

            # BigQuery Client
            client = bigquery.Client()

            # CHANGE THIS TO YOUR TABLE ID
            # For example: project_id.dataset_id.table_id
            table_id = "noticias-api-457314.noticias_dataset.news_articles"

            # Row to insert
            row_to_insert = [{
                "content": article.content,
                "description": article.description,
                "location": article.location,
                "published_at": article.published_at.isoformat(),
                "source": article.source,
                "title": article.title,
                "url": article.url
            }]

            # Insert to BigQuery
            errors = client.insert_rows_json(table_id, row_to_insert)

            if not errors:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"bigquery_error": errors}, status=500)

        return Response(serializer.errors, status=400)