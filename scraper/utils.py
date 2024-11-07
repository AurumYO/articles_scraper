import random
import requests
from bs4 import BeautifulSoup
from time import sleep

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from scraper.list_of_urls import list_of_urls
from scraper.models import Article


def scrape_articles(urls=None, domain=None):

    from django.utils import timezone  # import for running from shell
    from django.conf import settings

    urls = urls or list_of_urls
    SCRAPPING_DOMAIN = domain or settings.SCRAPPING_DOMAIN
    new_articles = []

    for url in urls:

        while True:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                articles = soup.find_all("div", class_="bg bgA plant")

                for article in articles:
                    links = article.find_all("a")

                    for link in links:
                        title = link.string.strip('"') if link.string else link["href"]
                        link = SCRAPPING_DOMAIN + link["href"]
                        obj, created = Article.objects.get_or_create(
                            title=title,
                            url=link,
                            defaults={
                                "date_scraped": timezone.now()
                            },  # Set the current date and time
                        )

                        # If the article was created (i.e., it's new), add it to the list
                        if created:
                            new_articles.append({"New title": title, "URL": link})

                next_buton = soup.find("a", string="MORE  »")

                sleep(random.randint(3, 7))

                if next_buton:
                    url = SCRAPPING_DOMAIN + next_buton["href"]
                else:
                    break
    # Send the list of new articles
    if new_articles:
        send_new_articles_email(new_articles)


def send_new_articles_email(new_articles):
    """
    Send an email with a list of new articles found.
    """
    subject = "New Rose Articles Found"
    message = "The following new rose description have been found:\n\n"
    for article in new_articles:
        message += f"{article['New title']}: {article['URL']}\n"

    # Define the recipient email
    from django.conf import settings  # imposrt for running from shell

    recipient_list = [settings.NOTIFICATION_EMAIL]

    # Send the email
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )
