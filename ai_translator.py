from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from slugify import slugify
import os
import json
from text_manipulator import TextManipulator
import hashlib


class AiTranslator:

    def __init__(self, url="https://www.cacaniqueisonline.com/analise/betsson/", selector=".col-12.col-lg-8.text",
                 position=0, token="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",
                 from_language="Brazilian Portuguese",
                 to_language="German"):
        self.node = None
        self.url = url
        self.selector = selector
        self.token = token
        self.from_language = from_language
        self.to_language = to_language
        self.position = position
        self.filename = slugify(self.url + self.selector) + ".json"
        self.text_manipulator = TextManipulator(
            filename=slugify(self.url + self.selector) + "-" + str(self.position) + ".json")
        self.data = {"url": self.url, "selector": self.selector, "filename": self.filename}
        self.open_file()
        self.load_html_from_url()
        self.soup = BeautifulSoup(self.data.get("html"), "html.parser")
        self.get_node()
        self.get_all_translatable_elements()

        # self.soup = self.load_soup_from_url(self.url)

    def open_file(self):
        if not os.path.isfile(self.filename):
            return
        f = open(self.filename, encoding="utf8")
        self.data = json.load(f)

    def save_file(self):
        with open(self.filename, "w", encoding='utf8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def load_html_from_url(self, overwrite=False):
        if "html" in self.data.keys() and not overwrite:
            return
        request_site = Request(self.url, headers={"User-Agent": "Mozilla/5.0"})
        webpage = urlopen(request_site).read()
        soup = BeautifulSoup(webpage, "html.parser")
        self.data["html"] = str(soup)
        self.save_file()

    def get_node(self):
        elements = self.soup.select(self.selector)
        if elements:
            self.node = elements[self.position]
            return
        self.node = None

    def get_all_translatable_elements(self):
        elements = self.node.find_all(["h1", "h2", "h3", "h4", "p", "li"])
        self.translatable_elements = [e for e in elements if e.find("img") is None]
        self.data["translatable_elements"] = []
        for e in self.translatable_elements:
            self.data["translatable_elements"].append({"html": str(e), "text_original": e.text})
            prompt = f"Please translate the following text from {self.from_language if self.from_language else 'the detected language'} to {self.to_language} (no notes): {e.text}"
            job_hash = hashlib.md5(prompt.encode()).hexdigest()

            # self.text_manipulator.new_task(task_name=str(job_hash), prompt=prompt)
        self.save_file()

    def split_html_elements(self):
        pass


def count_tokens(filename="https-www-cacaniqueisonline-com-analise-betsson-col-12-col-lg-8-text-0.json"):
    f = open(filename, encoding="utf8")
    data = json.load(f)
    sum_tokens = 0
    sum_words = 0
    for k in data.keys():
        if (type(data[k][0]) is dict):
            tokens = data[k][0].get("log").get("usage").get("total_tokens")
            sum_tokens += tokens
            sum_words += len(data[k][0].get("response").split())
            print(data[k][0].get("response"))
            print(f"Token: {sum_tokens}")
            print(f"Words: {sum_words}")


def split_node(node=BeautifulSoup, max_characters=4000):
    result = {"split": BeautifulSoup, "rest": BeautifulSoup}
    result["split"] = node
    while len(result["split"]) > max_characters:
        pass
    return result


if __name__ == '__main__':
    a = AiTranslator()
    print(len(str(a.node)))
    split_node(a.node)
    p = f"""
Please translate the text inside the html snippet below from Brazilian Portuguese to German.

{str(a.node)}
    """
    # print(p)
    # a.text_manipulator.new_task(prompt=p)
    # count_tokens()
    # soup = load_soup_from_url("https://www.cacaniqueisonline.com/analise/betsson/")
    # review = get_class_element(soup,'.col-12.col-lg-8.text')
    # items = all_translatable_elements(review)
    # for item in items:
    #    print(item.text)
    #    item.replace_with(item.text)
    pass
