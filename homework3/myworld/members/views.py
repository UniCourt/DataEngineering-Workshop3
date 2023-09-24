from django.shortcuts import render
from django.http import HttpResponse

def scrape_view(request):
	scrape_and_save_to_db()
	return HttpResponse("scraping and saving complete.")
