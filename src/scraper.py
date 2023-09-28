from urllib.request import urlopen
from bs4 import BeautifulSoup
import logging
import re


class UrlCleaner:
    def __init__(self, url):
        self.stop_html_elements = ["script", "style", "nav", "footer",
                                   "img", "button", "h1", "h2", "header",
                                   "web-header", "meta", "link", "web-snackbar-container"]

        logging.debug("Reading HTML from URL")
        self.url = url
        html = urlopen(url).read()
        self.soup = BeautifulSoup(html, features="html.parser")

    def remove_elements_from_html(self) -> None:
        """
        :return:
        """
        logging.debug("Removing undesired elements from HTML")
        for stop_html_element in self.stop_html_elements:
            for element in self.soup(stop_html_element):
                try:
                    element.clear()
                    element.decompose()
                except AttributeError:
                    logging.error(f"{element} not found")

    def get_text_from_url(self) -> str:
        """
        :return:
        """
        # kill all script and style elements
        self.remove_elements_from_html()
        # get text
        logging.debug("Getting text from HTML")
        text = '\n'.join(self.soup.stripped_strings)
        logging.debug("Finished")
        return text

    def write_file(self, path: str, mode: str = "w") -> None:
        logging.debug("Writing file")
        with open(path, mode) as file:
            file.write(self.get_text_from_url())
        logging.debug("Completed")


def camel_case_split(s: str) -> str:
    result = ""
    start = 0
    for i, c in enumerate(s[1:], 1):
        if c.isupper():
            result = result + s[start:i] + " "
            start = i
    result += s[start:]
    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    url = "https://es.wikipedia.org/wiki/Delphinidae"
    url1 = "https://web.dev/howbrowserswork/"
    cleaner = UrlCleaner(url1)
    cleaner.write_file("example.txt")
