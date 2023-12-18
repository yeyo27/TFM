import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
import fitz
import logging
from readabilipy import simple_json_from_html_string


def get_readable_html(url: str) -> str:
    logging.debug("Requesting HTML")
    response = requests.get(url)
    article = simple_json_from_html_string(response.text, use_readability=False)
    return article["content"]


class HtmlCleaner:
    def __init__(self, html_body: str):
        self.stop_html_elements = ["head", "script", "style",
                                   "footer", "img", "button",
                                   "h1", "h2", "h3",
                                   "header", "web-header", "meta",
                                   "link", "nav"]

        logging.debug("Parsing HTML")
        self.soup = BeautifulSoup(html_body, features="html.parser")
        self.text = None

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

    def extract_text_from_html(self) -> str:
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

    def extract_text_lines(self) -> list[str]:
        """
        Get lines from text
        :return lines: list of lines
        """
        lines = self.extract_text_from_html().splitlines()
        lines = list(filter(lambda line: line != "", lines))
        logging.debug(f"Number of lines {len(lines)}")
        return lines

    def write_file(self, path: str, mode: str = "w") -> None:
        """
        Write html text to file
        :param path:
        :param mode:
        :return:
        """
        logging.debug("Writing file")
        with open(path, mode) as file:
            file.write(self.extract_text_from_html())
        logging.debug("Completed")


class PyMuPdfCleaner:
    def __init__(self,  pdf_path: str = None, mem_file: bytes = None,):
        if mem_file is None:
            self.document = fitz.open(pdf_path)
        else:
            self.document = fitz.open(stream=mem_file, filetype="pdf")

    def extract_text_blocks(self) -> list[str]:
        text_blocks = []

        for page_num in range(self.document.page_count):
            page = self.document[page_num]
            blocks = page.get_text("blocks")

            for block in blocks:
                if len(block[4].split(" ")) > 8:
                    text = block[4].replace("\n", " ")
                    text_blocks.append(text)

        return text_blocks

    def get_metadata(self):
        return self.document.metadata

    def close_document(self):
        self.document.close()


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
    # url = "https://es.wikipedia.org/wiki/Delphinidae"
    url1 = "https://web.dev/howbrowserswork/"
    html_text = get_readable_html(url1)
    cleaner = HtmlCleaner(html_text)
    cleaner.write_file("../test/readabilipy_text.txt")


def pypdf_test():
    logging.basicConfig(level=logging.DEBUG)
    cleaner = PyPdfCleaner("../test/attention-is-all-you-need.pdf")
    print(cleaner.text_from_pages())


def pymupdf_test():
    logging.basicConfig(level=logging.DEBUG)
    cleaner = PyMuPdfCleaner("../test/attention-is-all-you-need.pdf")
    blocks = cleaner.extract_text_blocks()
    print(cleaner.get_metadata())
    for block in blocks[:10]:
        print(block, "\n")
    cleaner.close_document()


if __name__ == "__main__":
    pymupdf_test()
