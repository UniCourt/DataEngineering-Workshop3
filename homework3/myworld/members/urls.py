from django.urls import path
from . import views

urlpatterns=[
	path('admin/',admin.site.urls),
	path('scrape/',scrape_view),
]
