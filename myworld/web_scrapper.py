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

        print("\nTitle:", title.strip('\n'))
        print("Date:", date, )
        print("Time:", time)
        print("Author:", author)

        # print("Number of blogs read:", count)
        print("\n---------------------------------------------------------------------------------------------------------------\n")


if __name__ == "__main__":
    start_extraction()