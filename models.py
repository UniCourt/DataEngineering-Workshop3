from django.db import models
from django.utils import timezone

BRANCH_CHOICES = (
    ("BA", "BA"),
    ("B.COM", "B.COM"),
    ("MBA", "MBA"),
    ("CA", "CA"),
)

# Create your models here.
class Students(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    roll_number = models.IntegerField()
    mobile = models.CharField(max_length=10)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Blog(models.Model):
    title = models.CharField(max_length=500, default="")  # Default value for 'title'
    release_date = models.DateTimeField('Release Date', default=timezone.now)  # Default value for 'release_date'
    blog_time = models.CharField(max_length=50, default="")  # Default value for 'blog_time'
    author = models.CharField(max_length=200, default="")  # Default value for 'author'
    content = models.TextField(default="")  # Default value for 'content'
    total_comments = models.IntegerField(default=0)  # Default value for 'total_comments'
    recommended_on_google = models.BooleanField(default=False)  # Default value for 'recommended_on_google'
    file_path_html = models.CharField(max_length=500, default="")  # Default value for 'file_path_html'
    created_date = models.DateTimeField('Created Date', default=timezone.now)  # Default value for 'created_date'

    def __str__(self):
        return self.title
