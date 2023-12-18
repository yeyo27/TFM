from sentence_transformers import SentenceTransformer
from time import time
import logging

from src.text_scraping import HtmlCleaner, PyMuPdfCleaner


class EmbeddingsCalculator:
    def __init__(self, model_name="average_word_embeddings_komninos"):
        self.model = SentenceTransformer(model_name)

    def calculate(self, text_unit: str | list[str]) -> list:
        """
        Calculate embeddings using the model
        :param text_unit: the unit or list of units of text to embed.
        :return:
        """
        return self.model.encode(text_unit).tolist()

    def get_questions_embeddings(self, questions: list[str], answers: list[str]) -> list[tuple]:
        """
        Calculates the embeddings of the questions, returning a list containing the questions, embeddings of the
        questions and the corresponding answers.
        :param answers:
        :param questions:
        :return list[tuple]: pairs of lines and their embeddings.
        """
        questions_embeddings = self.calculate(questions)
        return list(zip(questions, questions_embeddings, answers))


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
