from sentence_transformers import SentenceTransformer
from time import time
import logging

from src.text_scraping import HtmlCleaner, PyMuPdfCleaner


class EmbeddingsCalculator:
    def __init__(self, model_name="paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)

    def calculate(self, text_unit: str | list[str]) -> list:
        """
        Calculate embeddings using the model
        :param text_unit: the unit or list of units of text to embed.
        :return:
        """
        return self.model.encode(text_unit).tolist()

    def get_text_embeddings_pairs(self, text_unit: str | list[str]) -> list[tuple]:
        """
        Get the text fragments along with their embeddings, in pairs.
        :param text_unit: the unit or list of units of text to embed.
        :return list[tuple]: pairs of lines and their embeddings.
        """
        embeddings = self.calculate(text_unit)
        return list(zip(text_unit, embeddings))


def html_test():
    logging.basicConfig(level=logging.DEBUG)
    with open("../test/html_from_api.html", "r") as f:
        logging.debug("Cleaning html...")
        html_text = f.read()
        cleaner = HtmlCleaner(html_text)
        lines = cleaner.extract_text_lines()
        logging.debug("Creating embeddings calculator...")
        emb_calc = EmbeddingsCalculator()
        logging.debug("Calculator created")
        start = time()
        logging.debug("Calculating embeddings...")
        embeddings = emb_calc.get_text_embeddings_pairs(lines)
        logging.debug(f"Calculation finished. Elapsed time: {time() - start} seconds")
        logging.debug(embeddings)


def pdf_test():
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Cleaning html...")
    cleaner = PyMuPdfCleaner("../test/attention-is-all-you-need.pdf")
    blocks = cleaner.extract_text_blocks()
    cleaner.close_document()
    logging.debug("Creating embeddings calculator...")
    emb_calc = EmbeddingsCalculator()
    logging.debug("Calculator created")
    start = time()
    logging.debug("Calculating embeddings...")
    embeddings = emb_calc.get_text_embeddings_pairs(blocks)
    logging.debug(f"Calculation finished. Elapsed time: {time() - start} seconds")
    logging.debug(embeddings)


if __name__ == "__main__":
    pdf_test()
