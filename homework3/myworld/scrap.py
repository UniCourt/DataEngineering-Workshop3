
import requests
from bs4 import BeautifulSoup
import psycopg2

#function to scrape and save data to database
def scrape_and_save_to_db():
	url='https://blog.python.org/'
	response= requests.get(url)
	if response.status_code==200:
		html_content=response.content
		soup= BeautifulSoup(html_content,'html.parser')
		
		#extracting data
		title=soup.find('h2',class_='entry-title')
		posted_date=soup.find('span',class_='entry-date')
		posted_time=soup.find('span',class_='entry-time')
		content=soup.find('div',class_='entry-content')
		author=soup.find('span',class_='author')
		total_comments=len(soup.find_all('li',class_='comment'))
		recommended_on_google=soup.find('span',class_='google-recommend')
		
		#save data to Postgresql DB
		conn=psycopg2.connect(
			database="pythoninsider_db",
			user="postgres",
			password="123456",
			host="psql-db",
			port="5432"
		)
		
		cursor=conn.cursor()
		cursor.execute(
			"INSERT INTO scraped_data(title,posted_date,posted_time,content,author,total_comments,recommended_on_google) VALUES(%s,%s,%s,%s,%s,%s,%s)",(title,posted_date,posted_time,content,author,total_comments,recommended_on_google)
		)
		
		conn.commit()
		conn.close()	
		
		print("Data scraped and saved to database.")

#calling function to scrap and save
scrape_and_save_to_db()


