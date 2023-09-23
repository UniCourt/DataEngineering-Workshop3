import requests
import re
from bs4 import BeautifulSoup, element
import psycopg2

# For the credentials mentioned below, you may refer the docker-compose.yml present in myworld .
db_name = 'member_db2'
db_user = 'postgres'
db_pass = '123456'
db_host = 'psql-db2.0'
db_port = '5432'
        
# This will create the connection the to postgres database.
conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)
        
        
def add_row_to_blog(title, date, time, author, content, recommended, html):
    # This function will add the entry to database
    sql = """INSERT INTO members_blog (title, release_date, blog_time, author,created_date,  content, recommended, html) VALUES (%s, %s::DATE,    		 %s::TIME, %s, NOW(), %s, %s, %s)"""
            
    with conn:
        with conn.cursor() as curs:
            time=time.replace('\u202f',"")
            curs.execute(sql, (title, date, time, author, content, recommended, html))
        
        
def truncate_table():
    # This function will delete the existing entries from the database.
    with conn:
        with conn.cursor() as curs:
            curs.execute("TRUNCATE members_blog CASCADE;")
        

def start_extraction():
    print("Extraction started")
    url = "https://blog.python.org/"
    data = requests.get(url)
    page_soup = BeautifulSoup(data.text, 'html.parser')

    blogs = page_soup.select('div.date-outer')

    for blog in blogs:
        date = blog.select('span', class_='date-header')[0].get_text()

        post = blog.select('.post')[0]
       # print(post)
       # post_time = blog.find('abbr', class_='published')
       
       # title = blog.h3.a.text
        #print(title)

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

        post_header = post.select('.post-header')[0]
        
        #contents = page_soup.find_all('div',class_='date-posts')
        #print(contents)
        #for con in contents:
        content = post.select('.post-body')[0].text
        html = 'S:\web_scraping\python_blogs.html'
        with open(html, 'w', encoding='utf-8') as f:
            f.write(data.text)
        
       
        #con = content.find('p', class_='post-body entry-content').p.text
 
        #contents =post_header.select('div', class_='post-body entry-content')
        google = page_soup.find_all('div', class_='widget LinkList', id='LinkList1')
        # print(google)
        for gg in google:
           recommended = gg.select('.widget-content')[0].li.a['href']
            #rem2 = gg.find('div', class_='widget-content')
            #print(rem2)
        
        #print(rem2)
        # Inserting data into database
        add_row_to_blog(title, date, time, author, content, recommended, html)
        print("\nTitle:", title.strip('\n'))
        print(f'''Posted date: {date}
        Posted time: {time}
        Author: {author}
        Content: {content}
        Recommended this on google: {recommended}
        HTML saved to: {html}''')

       # print("Number of blogs read:", count)
        print("\n---------------------------------------------------------------------------------------------------------------\n")


if __name__ == "__main__":
    start_extraction()
