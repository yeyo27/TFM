from time import time

from transformers import T5Tokenizer, T5ForConditionalGeneration
from src.text_scraping import PyMuPdfCleaner

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

cleaner = PyMuPdfCleaner("../test/attention-is-all-you-need.pdf")
blocks = cleaner.extract_text_blocks()
cleaner.close_document()

instruction = "Generate a generic question that can be answered using the following text:\n\n"
start = time()
for block in blocks[:50]:
    input_text = instruction + block
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    outputs = model.generate(input_ids, max_new_tokens=1000)
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))
print(f"Elapsed time: {time() - start} seconds")
