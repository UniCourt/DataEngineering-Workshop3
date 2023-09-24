from django.db import models

class ScrapeData(models.Model):
	title=models.CharField(max_length=200)
	posted_date=models.CharField(max_length=50)
	posted_time=models.CharField(max_length=50)
	content=models.TextField()
	author=models.CharField(max_length=100)
	total_comments=models.IntegerField()
	recommended_on_google=models.CharField(max_length=100)
	file_path=models.CharField(max_length=200)
	
	def __str__(self):
		return self.title
