from django.contrib import admin
from .models import Students, Blog

class DjStudentAdmin(admin.ModelAdmin):
   list_display = ("first_name", "last_name", "address", "roll_number", "mobile", "branch")
   list_filter = ("branch",)

class DjBlogAdmin(admin.ModelAdmin):
  list_display = ("title", "release_date", "blog_time", "author", "cont_d", "recommend","created_date")
  list_filter = ("author",)

# Register your models here.
admin.site.register(Blog, DjBlogAdmin)
admin.site.register(Students, DjStudentAdmin)
