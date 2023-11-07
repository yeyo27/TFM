from bs4 import BeautifulSoup
import logging


class HtmlCleaner:
    def __init__(self, html_body):
        self.stop_html_elements = ["head", "script", "style",
                                   "footer", "img", "button",
                                   "h1", "h2", "h3",
                                   "header", "web-header", "meta",
                                   "link", "nav"]

        logging.debug("Parsing HTML")
        self.soup = BeautifulSoup(html_body, features="html.parser")

    def remove_elements_from_html(self) -> BeautifulSoup:
        """
        :return:
        """
        logging.debug("Removing undesired elements from HTML")
        for element in self.soup.findAll(self.stop_html_elements):
            try:
                element.decompose()
            except AttributeError:
                logging.error(f"{element} not found")
        return self.soup

    def get_text_from_url(self) -> str:
        """
        :return:
        """
        # kill all script and style elements
        self.remove_elements_from_html()
        # get text
        logging.debug("Extracting HTML elements with text")
        text_elements = self.soup.findAll(["p", "ol"])
        logging.debug("Extracting text from elements")
        whole_text = ""
        for text_element in text_elements:
            whole_text += text_element.text + "\n"
        logging.debug("Finished")
        return whole_text

    def write_file(self, path: str, mode: str = "w") -> None:
        logging.debug("Writing file")
        with open(path, mode) as file:
            file.write(self.get_text_from_url())
        logging.debug("Completed")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    url = "https://es.wikipedia.org/wiki/Delphinidae"
    url1 = "https://web.dev/howbrowserswork/"
    with open("../test/readable_web.html", "r") as f:
        html = f.read()
        cleaner = HtmlCleaner(html)
        cleaner.write_file("../test/example_from_readability.txt")
