from os import getenv
from pathlib import Path
from time import time

from dotenv import load_dotenv
from openai import OpenAI
from transformers import T5Tokenizer, T5ForConditionalGeneration

from src.text_scraping import PyMuPdfCleaner


class QuestionGeneratorTransformers:
    def __init__(self):
        self.tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
        self.model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")
        self.instruction = "Generate a generic question that can be answered using the following text:\n\n"

    def generate_question(self, prompt: str) -> list[str]:
        input_text = self.instruction + prompt
        input_ids = self.tokenizer(input_text, return_tensors="pt").input_ids
        output = self.model.generate(input_ids, max_new_tokens=1000)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

    def generate_questions(self, answers: list[str]):
        questions = []
        for answer in answers:
            questions.append(self.generate_question(answer))
        return questions


class QuestionGeneratorOpenAI:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.template = "Generate one and only one short question per line based on the lines of the following text:\n"

    def completion(self, prompt: str) -> str | None:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are a question creator, skilled in summarizing and returning short questions based on
                    the given lines. The questions will be in the same language as the given text.
                    The questions should be short and concise. The questions you generate will be returned in the same
                    order as the given lines. In the end, we will have the same number of questions as lines of text I gave you.
                    """
                },
                {"role": "user",
                 "content": self.template + prompt}
            ]
        )
        return response.choices[0].message.content

    def query_in_batches(self, fragmented_text: list[str], num_batches: int = 1):
        responses = []
        total_fragments = len(fragmented_text)
        batch_size = int(total_fragments / num_batches)
        for i in range(0, total_fragments, batch_size):
            pos_final = min(i + batch_size, total_fragments)
            prompt = "\n\n".join(fragmented_text[i:pos_final])
            print(prompt)
            questions = self.completion(prompt)
            responses.append(questions)
        return responses


def openai_test():
    load_dotenv(dotenv_path=Path("../.env"))
    api_key = getenv("OPENAI_API_KEY")

    generator = QuestionGeneratorOpenAI(api_key)
    cleaner = PyMuPdfCleaner("../test/attention-is-all-you-need.pdf")

    blocks = cleaner.extract_text_blocks()
    cleaner.close_document()
    start = time()
    responses = generator.query_in_batches(blocks[:10])
    print(blocks[:10])
    print(responses[0])
    print(len(responses[0]))
    print(f"Elapsed time: {time() - start} seconds")


if __name__ == "__main__":
    pass
