
from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    posted_date = models.DateField()
    posted_time = models.TimeField()
    content = models.TextField()
    author = models.CharField(max_length=100)
    total_comments = models.IntegerField()
    recommended_on_google = models.BooleanField()
    html_file_path = models.CharField(max_length=200)

    def __str__(self):
        return self.title

