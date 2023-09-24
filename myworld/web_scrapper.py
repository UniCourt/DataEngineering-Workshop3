import psycopg2
import requests
import re
from bs4 import BeautifulSoup, element
        
# For the credentials mentioned below, you may refer the docker-compose.yml present in myworld .
db_name = 'member_db'
db_user = 'postgres'
db_pass = '123456'
db_host = 'psql-db'
db_port = '5432'
        
# This will create the connection the to postgres database.
conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)
        
        
def add_row_to_blog(title, author, date, time,cont_d,recommend):
    # This function will add the entry to database
    sql = """INSERT INTO members_blog (title, release_date, blog_time, author, cont_d, recommend, created_date) VALUES (%s, %s::DATE, %s::TIME, %s,%s,%s, NOW())"""
            
    with conn:
        with conn.cursor() as curs:
            curs.execute(sql, (title, date, time, author,cont_d,recommend))
        
        
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
        
        
        content = blog.select('.post p')
        cont_d=""
        i=0
        
        while i<len(content):
        	cont_d+=content[i].text+'\n'
        	i=i+1
        recommend=blog.select('.post p a')[0].text
        title = ""
        title_bar = post.select('.post-title')
        if len(title_bar) > 0:
            title = title_bar[0].text
        else:
            title = post.select('.post-body')[0].contents[0].text
        
        # getting the author and blog time
        post_footer = post.select('.post-footer')[0]
        
        author = post_footer.select('.post-author span')[0].text
        
        time = post_footer.select('abbr')[0].text.replace("\u202f"," ")
        # Inserting data into database
        add_row_to_blog(title, author, date, time, cont_d, recommend)
        
        
        print("\nTitle:", title.strip('\n'))
        print("Date:", date, )
        print("Time:", time)
        print("Author:", author)
        print("Content:\n",cont_d)
        print("Recommended:\n",recommend)
        
        # print("Number of blogs read:", count)
        print(
            "\n---------------------------------------------------------------------------------------------------------------\n")
                
        
if __name__ == "__main__":
    start_extraction()
