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

    # Convert recommended_on_google to a boolean (True or False) based on your logic
    # For example, if it's "recommended," set it to True; otherwise, set it to False
    recommended_on_google = True if recommended_on_google == "recommended" else False

    # This function will add the entry to the database
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
        # loop through each article
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

        # New code to scrape additional information
        content = post.select('.post-body')[0].text.strip()  # Content

        # Check if there are elements with the comment-link span selector
        comment_link_span = post_footer.select('.comment-link span')
        if comment_link_span:
            total_comments = comment_link_span[0].text  # Total Comments
        else:
            total_comments = "No comments found"

        # Add logic to scrape "recommended this on google" and "file path of saved HTML" here
        recommended_on_google = ""  # Replace with actual logic
        file_path_html = ""  # Replace with actual logic

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
