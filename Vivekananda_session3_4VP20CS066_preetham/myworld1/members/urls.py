from django.urls import path
from . import views

urlpatterns = [
    path('students/<int:rolno>', views.StudentView.as_view()),
    path('students/', views.StudentView.as_view()),
    path('students/<str:branch>', views.StudentView.as_view()),
    path('start_python_blog_scraping', views.python_blog_scrap, name='triger'),
    path('rest/blog/', views.BlogView.as_view()),
    ]
