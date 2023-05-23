from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
from blog_scraper.models import BlogPost
from bs4 import BeautifulSoup
import requests

def scrape_and_save(request):
    url = "https://example.com/python-insider-blog"  # Replace with the actual URL of the Python Insider Blog page
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")

    # Extract the required data from the HTML using BeautifulSoup

    # Create a new instance of the BlogPost model and save it to the database
    blog_post = BlogPost(
        title=title,
        posted_date=posted_date,
        posted_time=posted_time,
        content=content,
        author=author,
        total_comments=total_comments,
        recommended_on_google=recommended_on_google,
        html_file_path=file_path
    )
    blog_post.save()

    return HttpResponse("Scraping completed and data saved to the database.")

