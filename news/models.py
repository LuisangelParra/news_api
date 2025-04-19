from django.db import models

class NewsArticle(models.Model):
    content = models.TextField()
    description = models.TextField()
    location = models.CharField(max_length=255)
    published_at = models.DateTimeField()
    source = models.CharField(max_length=255)
    title = models.CharField(max_length=500)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.title
