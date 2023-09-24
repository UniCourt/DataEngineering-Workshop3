from django.contrib import admin
from .models import Students, Blog

class DjStudentAdmin(admin.ModelAdmin):
   list_display = ("first_name", "last_name", "address", "roll_number", "mobile", "branch")
   list_filter = ("branch",)

class DjBlogAdmin(admin.ModelAdmin):
  list_display = ("title", "release_date", "blog_time", "author", "created_date", "content", "total_comments", "recommended_on_google", "file_path_html")
  list_filter = ("author","recommended_on_google")
  search_fields = ("title", "author", "content")

# Register your models here.
admin.site.register(Blog, DjBlogAdmin)
admin.site.register(Students, DjStudentAdmin)
