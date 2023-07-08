from urllib.request import urlopen
from bs4 import BeautifulSoup
import logging


def get_text_from_url(url: str):
    logging.debug("Reading HTML from URL")
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    logging.debug("Removing scripts and styles from HTML")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    logging.debug("Getting text from HTML")
    text = soup.get_text()

    logging.debug("Formatting...")
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    text = '\n'.join(line for line in lines if line)
    logging.debug("Formatted")
    return text


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    url = "https://es.wikipedia.org/wiki/Delphinidae"
    print(get_text_from_url(url))
