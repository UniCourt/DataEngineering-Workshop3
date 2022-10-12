## Integrate the script to Django admin.

- Let us view the scrapped data in the Django-admin. Follow the below steps to achieve that.

1. Open the admin.py file which is present in the same path as that of models.py. Currently it will include the Student model.

        vi admin.py
2. Add the below class to admin.py

```buildoutcfg
class DjBlogAdmin(admin.ModelAdmin):
  list_display = ("title", "release_date", "blog_time", "author", "created_date")
  list_filter = ("author",)
```


3. Register the Blog model

        admin.site.register(Blog, DjBlogAdmin)
4. After modifying the admin.py file will look like this

```buildoutcfg
from django.contrib import admin
from .models import Students, Blog

class DjStudentAdmin(admin.ModelAdmin):
   list_display = ("first_name", "last_name", "address", "roll_number", "mobile", "branch")
   list_filter = ("branch",)

class DjBlogAdmin(admin.ModelAdmin):
  list_display = ("title", "release_date", "blog_time", "author", "created_date")
  list_filter = ("author",)

# Register your models here.
admin.site.register(Blog, DjBlogAdmin)
admin.site.register(Students, DjStudentAdmin)
```

   
5. In order to view the data in the admin, let us run the server. For that go to the tab where  workshop_web_container is running
and run the below command
        
        python manage.py runserver 0:8000
6. Now open the webpage and check if you can view the data

        http://0.0.0.0:8000/admin/

<hr />

- Now let us move our script to apps.py and run the script as a view. Follow the below steps

1. Open the apps.py file present in the same path where admin.py and models.py is present. 
2. Add our script to the file. Do not delete the existing contents. You can copy the below given content and paste it.

```buildoutcfg
from django.apps import AppConfig
   
import psycopg2
import requests
import re
from bs4 import BeautifulSoup, element

db_name = 'member_db'
db_user = 'postgres'
db_pass = '123456'
db_host = 'psql-db'
db_port = '5432'

conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)

def add_row_to_blog(title, author, date, time):
    sql = """INSERT INTO members_blog (title, release_date, blog_time, author, created_date) VALUES (%s, %s::DATE, %s::TIME, %s, NOW())"""

    with conn:
        with conn.cursor() as curs:
            curs.execute(sql, (title, date, time, author))

def truncate_table():
    print("Truncating contents all the tables")
    with conn:
        with conn.cursor() as curs:
            curs.execute("TRUNCATE members_blog CASCADE;")

def start_extraction():
    print("Extraction started")
    url = "https://blog.python.org/"

    data = requests.get(url)
    page_soup = BeautifulSoup(data.text, 'html.parser')


    blogs = page_soup.select('div.date-outer')
    truncate_table()
    for blog in blogs:
        date = blog.select('.date-header span')[0].get_text()

        post = blog.select('.post')[0]

        title = ""
        title_bar = post.select('.post-title')
        if len(title_bar) > 0:
            title = title_bar[0].text
        else:
            title = post.select('.post-body')[0].contents[0].text

        # getting the author and blog time
        post_footer = post.select('.post-footer')[0]

        author = post_footer.select('.post-author span')[0].text

        time = post_footer.select('abbr')[0].text

        add_row_to_blog(title, author, date, time)

        print("\nTitle:", title.strip('\n'))
        print("Date:", date, )
        print("Time:", time)
        print("Author:", author)

        # print("Number of blogs read:", count)
        print(
            "\n---------------------------------------------------------------------------------------------------------------\n")

if __name__ == "__main__":
    start_extraction()

class MembersConfig(AppConfig):
    name = 'members'

```


<hr />

3. Now let us modify the views.py file to include the view to scrap the data. Open the views.py file present inside the same
folder as that of models.py and add the below function at the bottom of the file (Do not delete the existing contents)
   
```buildoutcfg
def python_blog_scrap(request):
   apps.start_extraction()
   return JsonResponse({'status': 'sucess', "message" : "Extracted and populated the table."}, status=200)

```
         
4. Need to include few import statements. Modify the import statements as below

```buildoutcfg
from django.views import View
from .models import Students, Blog
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from . import apps
```

5. Now to access this view through Django-admin, we will have to modify the urls.py file which is present in the same folder. 
Modify the urls.py as given below
   
```buildoutcfg
from django.urls import path
from . import views

urlpatterns = [
    path('rest/student/<int:rolno>', views.StudentView.as_view()),
    path('rest/student/', views.StudentView.as_view()),
    path('rest/student/<str:branch>', views.StudentView.as_view()),
    path('start_python_blog_scraping', views.python_blog_scrap, name='triger')
         ]
```

6. `start_python_blog_scraping` is going to be the pattern by which we will run our script.
7. Now let us run this view. Make sure your server is running in workshop_web_container. If not, run the server

      python manage.py runserver 0:8000
   
8. Now copy the below url in the webpage.

       http://0.0.0.0:8000/members/start_python_blog_scraping
9. If your script ran fine, you should get a message

       {
         "status": "sucess",
         "message": "Extracted and populated the table."
       }
10. To verify if the extractions had happened fine, you may open the admin page and check the data. 

         http://0.0.0.0:8000/admin/
   - Check for the created_date of the entries in the table. If the script ran fine, the entries will have the latest date as created_Date