import requests
from bs4 import BeautifulSoup
from myapp.models import BlogPost  # Replace 'myapp' with your app name

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

        post_footer = post.select('.post-footer')[0]

        author = post_footer.select('.post-author span')[0].text
        time = post_footer.select('abbr')[0].text

        # Extract content, total comments, recommended on Google, and file path
        content = post.select('.post-body')[0].text
        total_comments = int(post_footer.select('.comment-link a')[0].text.split()[0])
        recommended_on_google = int(post_footer.select('.goog-inline-block')[0].text)
        file_path = "path/to/saved.html"  # You can update this with the actual file path

        # Create a BlogPost object and save it to the database
        blog_post = BlogPost(
            title=title.strip('\n'),
            posted_date=date,
            posted_time=time,
            author=author,
            content=content,
            total_comments=total_comments,
            recommended_on_google=recommended_on_google,
            file_path=file_path
        )
        blog_post.save()

        print("\nTitle:", title.strip('\n'))
        print("Date:", date)
        print("Time:", time)
        print("Author:", author)
        print("Content:", content)
        print("Total Comments:", total_comments)
        print("Recommended on Google:", recommended_on_google)
        print("File Path:", file_path)

        print("\n---------------------------------------------------------------------------------------------------------------\n")

if __name__ == "__main__":
    start_extraction()

