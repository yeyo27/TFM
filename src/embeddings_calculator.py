from sentence_transformers import SentenceTransformer
from time import time
import logging


class EmbeddingsCalculator:
    def __init__(self, model_name="average_word_embeddings_komninos"):
        self.model = SentenceTransformer(model_name)

    def calculate(self, sentence: str | list[str]) -> list:
        """
        Calculate embeddings using the model
        :param sentence: the sentence to embed
        :return:
        """
        return self.model.encode(sentence).tolist()

    def calculate_text_embeddings(self, text: str) -> tuple[list[str], list]:
        lines = text.splitlines()
        logging.debug(f"Number of lines {len(lines)}")
        return lines, self.calculate(lines)

    def get_lines_embeddings_pairs(self, text: str) -> list[tuple]:
        """
        Get the lines along with their embeddings in pairs
        :param text:
        :return:
        """
        lines, embeddings = self.calculate_text_embeddings(text)
        return list(zip(lines, embeddings))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    with open("../test/example_from_readability.txt") as f:
        logging.debug("Creating embeddings calculator...")
        emb_calc = EmbeddingsCalculator()
        logging.debug("Calculator created")
        start = time()
        text = f.read()
        logging.debug("Calculating embeddings...")
        embeddings = emb_calc.get_lines_embeddings_pairs(text)
        logging.debug(f"Calculation finished. Elapsed time: {time() - start} seconds")
        print(embeddings[0])
