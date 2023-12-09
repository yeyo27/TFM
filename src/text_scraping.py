from bs4 import BeautifulSoup
from pypdf import PdfReader
import fitz
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


class PyMuPdfCleaner:
    def __init__(self, pdf_path: str):
        self.reader = fitz.open(pdf_path)

    def extract_text_blocks(self) -> list:
        text_blocks = []

        for page_num in range(self.reader.page_count):
            page = self.reader[page_num]
            blocks = page.get_text("blocks")

            for block in blocks:
                text = block[4]
                text_blocks.append(text)

        return text_blocks

    def close_reader(self):
        self.reader.close()


class PyPdfCleaner:
    def __init__(self, file_path: str):
        self.reader = PdfReader(file_path)

    def get_metadata(self):
        return self.reader.metadata

    def text_from_pages(self):
        text = ""
        for page in self.reader.pages:
            text += page.extract_text()
        return text


def html_test():
    logging.basicConfig(level=logging.DEBUG)
    url = "https://es.wikipedia.org/wiki/Delphinidae"
    url1 = "https://web.dev/howbrowserswork/"
    with open("../test/html_from_api.html", "r") as f:
        html_text = f.read()
        cleaner = HtmlCleaner(html_text)
        cleaner.write_file("../test/clean_text_from_api.txt")


def pypdf_test():
    logging.basicConfig(level=logging.DEBUG)
    cleaner = PyPdfCleaner("../test/attention-is-all-you-need.pdf")
    print(cleaner.text_from_pages())


def pymupdf_test():
    logging.basicConfig(level=logging.DEBUG)
    cleaner = PyMuPdfCleaner("../test/attention-is-all-you-need.pdf")
    for block in cleaner.extract_text_blocks():
        print(block)
    cleaner.close_reader()


if __name__ == "__main__":
    pymupdf_test()
