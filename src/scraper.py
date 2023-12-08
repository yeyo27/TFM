from bs4 import BeautifulSoup
import logging


class HtmlCleaner:
    def __init__(self, html_body: str):
        self.stop_html_elements = ["head", "script", "style",
                                   "footer", "img", "button",
                                   "h1", "h2", "h3",
                                   "header", "web-header", "meta",
                                   "link", "nav"]

        logging.debug("Parsing HTML")
        self.soup = BeautifulSoup(html_body, features="html.parser")

    def remove_elements_from_html(self) -> BeautifulSoup:
        """
        Remove undesired elements from HTML
        :return A beautiful soup object:
        """
        logging.debug("Removing undesired elements from HTML")
        for element in self.soup.findAll(self.stop_html_elements):
            try:
                element.decompose()
            except AttributeError:
                logging.error(f"{element} not found")
        return self.soup

    def get_text_from_html(self) -> str:
        """
        Get text from HTML, selecting paragraphs and lists
        :return clean text: elements joined by carriage return
        """
        # kill all script and style elements
        self.remove_elements_from_html()
        # get text
        logging.debug("Extracting HTML elements with text")
        text_elements = self.soup.findAll(["p", "ol", "ul", "blockquote"])
        logging.debug("Extracting text from elements")
        whole_text = ""
        for text_element in text_elements:
            whole_text += text_element.text + "\n"
        logging.debug("Finished")
        return whole_text

    def write_file(self, path: str, mode: str = "w") -> None:
        """
        Write html text to file
        :param path:
        :param mode:
        :return:
        """
        logging.debug("Writing file")
        with open(path, mode) as file:
            file.write(self.get_text_from_html())
        logging.debug("Completed")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    url = "https://es.wikipedia.org/wiki/Delphinidae"
    url1 = "https://web.dev/howbrowserswork/"
    with open("../test/html_from_api.html", "r") as f:
        html_text = f.read()
        cleaner = HtmlCleaner(html_text)
        cleaner.write_file("../test/clean_text_from_api.txt")
