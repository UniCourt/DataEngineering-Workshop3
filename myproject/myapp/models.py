from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    posted_date = models.DateField()
    posted_time = models.TimeField()
    author = models.CharField(max_length=100)
    content = models.TextField()
    total_comments = models.IntegerField()
    recommended_on_google = models.IntegerField()
    file_path = models.CharField(max_length=255)  # Use CharField for file path

