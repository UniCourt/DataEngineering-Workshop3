from django.apps import AppConfig
import psycopg2
import requests
from bs4 import BeautifulSoup, element
from datetime import datetime
from dateutil.parser import parse

db_name = 'member_db'
db_user = 'postgres'
db_pass = '123456'
db_host = 'psql-db_1'
db_port = '5432'

conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)

def add_row_to_blog(title, author, date, time, content, total_comments, recommended_on_google, file_path_html):
    sql = """INSERT INTO members_blog (title, release_date, blog_time, author, created_date, content, total_comments, recommended_on_google, file_path_html)
             VALUES (%s, %s::DATE, %s::TIME, %s, NOW(), %s, %s, %s, %s)"""

    with conn:
        with conn.cursor() as curs:
            curs.execute(sql, (title, date, time, author, content, total_comments, recommended_on_google, file_path_html))

def truncate_table():
    print("Truncating contents of all the tables")
    with conn:
        with conn.cursor() as curs:
            curs.execute("TRUNCATE members_blog CASCADE;")

def start_extraction(start_date=None, end_date=None, no_of_articles=None, start_id=None):
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

        # Getting the author and blog time
        post_footer = post.select('.post-footer')[0]

        author = post_footer.select('.post-author span')[0].text

        time = post_footer.select('abbr')[0].text.replace('\u202f', '')

        # New code to scrape additional information
        content = post.select('.post-body')[0].text.strip()  # Content

        # Check if there are elements with the comment-link span selector
        comment_link_span = post_footer.select('.comment-link span')
        if comment_link_span:
            total_comments = comment_link_span[0].text  # Total Comments
            # Check if the value is "No comments found" and replace it with a default value (e.g., 0)
            if total_comments == "No comments found":
                total_comments = 0
        else:
            total_comments = 0  # Default value if comments are not found

        # Assuming that recommended_on_google and file_path_html are boolean fields
        # Set their values to False by default
        recommended_on_google = False
        file_path_html = False

        # Continue with the rest of the code

        # ...

if __name__ == "__main__":
    start_extraction()

class MembersConfig(AppConfig):
    name = 'members'
