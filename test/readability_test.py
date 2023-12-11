import requests
from readabilipy import simple_json_from_html_string
req = requests.get("https://web.dev/articles/howbrowserswork")
article = simple_json_from_html_string(req.text, use_readability=True)
print(article["content"])
with open("readability.html", "w") as f:
    f.write(article["content"])
