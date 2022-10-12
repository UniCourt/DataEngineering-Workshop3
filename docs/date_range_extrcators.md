## Date Range Extractors

- By Date range extractor, we mean a scrapper that scrap the data from the Python Insider blog with release date
within the given start and end date.
  
- To achive this let us build a REST API that accepts the post parameter, start_date and end_date.
- This API should scrap the data from the website that comes within that date range and save the data in the db as well as 
return the data to us as JSON response.
  
- To support this API, let us modify our script which is present in the apps.py file.
- Modify the function start_extraction() which is present inside apps.py file as following

```buildoutcfg
def start_extraction(start_date=None, end_date=None):
    print("Extraction started")
    url = "https://blog.python.org/"
  
    data = requests.get(url)
    page_soup = BeautifulSoup(data.text, 'html.parser')
    
    if start_date:
        start_date = parse(start_date)
    if end_date:
        end_date = parse(end_date)
    
    blogs = page_soup.select('div.date-outer')
    truncate_table()
    for blog in blogs:
        if no_of_articles and counter > int(no_of_articles):
            continue
        date = blog.select('.date-header span')[0].get_text()
    
        converted_date = parse(date)
    
        if start_date and converted_date < start_date:
            continue
        if end_date and converted_date > end_date:
            continue
    
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

```
      
<hr />

- Need to include one more import statement to support a function that is used in the above code ie., parse function. 
So modify the import statements as following
  
```buildoutcfg
from django.apps import AppConfig
import psycopg2
import requests
import re
from bs4 import BeautifulSoup, element
import datetime
from dateutil.parser import parse

```

<hr />

- Let us modify the views.py file to support the REST API. Add the below class to the existing contents in views.py file

```buildoutcfg
@method_decorator(csrf_exempt, name='dispatch')
class BlogView(View):
    def post(self, request):
        start_date = request.POST.get('start_date', None)
        end_date = request.POST.get('end_date', None)

        apps.start_extraction(start_date=start_date, end_date=end_date)

        blog_model_list = Blog.objects.filter()

        blogs = []
        for blog in blog_model_list:
            data = {
                "Title": blog.title,
                "Release Date": blog.release_date,
                "Author": blog.author,
                "Blog time": blog.blog_time
            }
            blogs.append(data)

        return JsonResponse({'status': 'success', "students": blogs}, status=200)
```
        

<hr />

- In order to invoke this API, we need to include the url in urls.py file. Modify the urls.py file as follows

```buildoutcfg
from django.urls import path
from . import views

urlpatterns = [
    path('rest/student/<int:rolno>', views.StudentView.as_view()),
    path('rest/student/', views.StudentView.as_view()),
    path('rest/student/<str:branch>', views.StudentView.as_view()),
    path('start_python_blog_scraping', views.python_blog_scrap, name='triger'),
    path('rest/blog/', views.BlogView.as_view())
]
```


<hr />

- Let us call the API. Make sure the server is running.
- Open a new tab in your terminal and run the below CURL to call the API

        curl -X POST http://0.0.0.0:8000/members/rest/blog/ -d "start_date=2022-06-06&end_date=2022-07-26"

- This should extract only the articles that comes within that date range. You should get the output as JSON response.
- Also verify the data in the database.

<hr />

## Incremental Extractors

- Here we need will be passing the no_of_articles and start_id as parameters. 
- If we pass, say 5 as no_of_artcles, we expect the scrapper to extract just 5 articles. 
- If we also specify the start_id value, say 2. Then we expect the scrapper to extract artcles from 2nd one. 

- To achieve this let us Modify the function start_extraction() which is present inside apps.py file as following

```buildoutcfg
def start_extraction(start_date=None, end_date=None, no_of_articles=None, start_id = None):
  print("Extraction started")
  url = "https://blog.python.org/"
  
  data = requests.get(url)
  page_soup = BeautifulSoup(data.text, 'html.parser')
  
  if start_date:
      start_date = parse(start_date)
  if end_date:
      end_date = parse(end_date)
  
  blogs = page_soup.select('div.date-outer')
  truncate_table()
  article_count = 0
  counter = 1
  for blog in blogs:
      article_count += 1
      if start_id and article_count < int(start_id):
          continue
      if no_of_articles and counter > int(no_of_articles):
          continue
      date = blog.select('.date-header span')[0].get_text()
  
      converted_date = parse(date)
  
      if start_date and converted_date < start_date:
          continue
      if end_date and converted_date > end_date:
          continue
  
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
      counter += 1
```
            

<hr />

- Modify the BlogView class present inside views.py file as follows

```buildoutcfg
@method_decorator(csrf_exempt, name='dispatch')
class BlogView(View):
    def post(self, request):
        start_date = request.POST.get('start_date', None)
        end_date = request.POST.get('end_date', None)
        no_of_articles = request.POST.get('no_of_articles', None)
        start_id = request.POST.get('start_id', None)

        apps.start_extraction(start_date=start_date, end_date=end_date, no_of_articles=no_of_articles, start_id=start_id)

        blog_model_list = Blog.objects.filter()

        blogs = []
        for blog in blog_model_list:
            data = {
                "Title": blog.title,
                "Release Date": blog.release_date,
                "Author": blog.author,
                "Blog time": blog.blog_time
            }
            blogs.append(data)

        return JsonResponse({'status': 'success', "students": blogs}, status=200)
```
        

<hr />

- To test the API, run the below CURL command

        curl -X POST http://0.0.0.0:8000/members/rest/blog/ -d "no_of_articles=1&start_id=5"
  - Make sure server is running.
    
- You can now add different post parameter values and test out our API.