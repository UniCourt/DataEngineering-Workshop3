# Web Scrapping Using Python

- Let us scrap the website [Python Insider](https://blog.python.org/).
- Following data need to be extracted out of the website.
    1. Title 
    2. Release Date
    3. Blog Time
    4. Author
    
- We will first write a simple python script to extract and print the above mentioned data from the website.
- Follow the given steps in order to achieve that.

1. Open the project myworld which we have created in our previous workshop. 
2. Create a python file web_scrapper.py which will include the script to scrap the website.

        vi web_scrapper.py 
            or
        gedit web_scrapper.py

3. Write the below script inside that file.

            import requests
            import re
            from bs4 import BeautifulSoup, element
   
            def start_extraction():
                print("Extraction started")
                url = "https://blog.python.org/"
            
                data = requests.get(url)
                page_soup = BeautifulSoup(data.text, 'html.parser')
            
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

4. In order to run this script we need few python packages running in our environment. So we will add it in the dockerfile.
Open the folder dockerfile and edit the file named Dockerfile which is present inside that. You can copy the below content and paste it in Dockerfile.
   

      FROM python:3.10.2-alpine3.15
      # Install required packages
      # For psycopg2
      RUN apk update && \
      apk --no-cache add --virtual build-deps-alpine build-base && \
      apk --no-cache add --virtual postgresql-deps libpq-dev
      # Install requirements
      RUN pip install --upgrade pip
      RUN pip install Django psycopg2==2.9.3 bs4 html5lib requests python-dateutil
      # Create directories
      RUN mkdir -p /root/workspace/src
      COPY ./  /root/workspace/site
      # Switch to project directory
      WORKDIR /root/workspace/site

   - If you compare the previous Dockerfile content you can notice that we have added 4 new packages which we will need to scrap the website.
   - They are
     1. bs4 
     2. html5lib 
     3. requests 
     4. python-dateutil
   
5. Once the docker file is updated, we can build and docker image and bring the containers up . Run the below command in the 
directory where your docker-compose.yml is present
   
       docker-compose up --build -d
6. Now exec into the workshop_web_container container.
   
       docker exec -it workshop_web_container sh
7. Run the below command to run the python script.
         
       python3 web_scrapper.py
8. Now you should be able to see the extracted data printed in your screen.