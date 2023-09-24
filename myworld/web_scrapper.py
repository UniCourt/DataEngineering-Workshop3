import psycopg2
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# For the credentials mentioned below, you may refer to the docker-compose.yml present in myworld.
db_name = 'member_db'
db_user = 'postgres'
db_pass = '123456'
db_host = 'psql-db_1'
db_port = '5432'

# This will create the connection to the PostgreSQL database.
conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)


def add_row_to_blog(title, author, date, time, content, total_comments, recommended_on_google, file_path_html):
    # Parse the time value and convert it to the 'HH:MI:SS' format
    parsed_time = datetime.strptime(time, '%I:%M %p').strftime('%H:%M:%S')

    # Convert total_comments to an integer or use a default value if "No comments found"
    if total_comments.isdigit():
        total_comments = int(total_comments)
    else:
        total_comments = 0

    recommended_on_google = True if recommended_on_google == "recommended" else False


    sql = """
    INSERT INTO members_blog (title, release_date, blog_time, author, created_date, content, total_comments, recommended_on_google, file_path_html)
    VALUES (%s, %s::DATE, %s::TIME, %s, NOW(), %s, %s, %s, %s)
    """
    with conn:
        with conn.cursor() as curs:
            curs.execute(sql, (title, date, parsed_time, author, content, total_comments, recommended_on_google, file_path_html))


def truncate_table():
    # This function will delete the existing entries from the database.
    with conn:
        with conn.cursor() as curs:
            curs.execute("TRUNCATE members_blog CASCADE;")


def start_extraction():
    print("Extraction started")
    url = "https://blog.python.org/"

    # Each time when we add new entry we delete the existing entries.
    truncate_table()
    data = requests.get(url)
    page_soup = BeautifulSoup(data.text, 'html.parser')

    # Getting all the articles
    blogs = page_soup.select('div.date-outer')

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
        content = post.select('.post-body')[0].text.strip()  # Content
        comment_link_span = post_footer.select('.comment-link span')
        if comment_link_span:
            total_comments = comment_link_span[0].text  # Total Comments
        else:
            total_comments = "No comments found"

        
        recommended_on_google = "" 
        file_path_html = ""  

        # Inserting data into the database
        add_row_to_blog(title, author, date, time, content, total_comments, recommended_on_google, file_path_html)

        print("\nTitle:", title.strip('\n'))
        print("Date:", date)
        print("Time:", time)
        print("Author:", author)
        print("Content:", content)
        print("Total Comments:", total_comments)
        print("Recommended on Google:", recommended_on_google)  # Print the value
        print("File saved at:", file_path_html)  # Print the value

        print("\n---------------------------------------------------------------------------------------------------------------\n")


if __name__ == "__main__":
    start_extraction()
