from flask import Flask, render_template, request, render_template_string
from bs4 import BeautifulSoup

from urllib.request import Request, urlopen

def load_soup_from_url(url="") -> BeautifulSoup:
    request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    webpage = urlopen(request_site).read()
    return BeautifulSoup(webpage, "html.parser")

def get_class_element(soup = BeautifulSoup, find_class="", position=0):
    elements = soup.select(find_class)
    if elements:
        return elements[position]
    return None

def all_translatable_elements(soup=BeautifulSoup):
    elements = soup.find_all(["h2","h3", "h4","p", "li"])
    result = [e for e in elements if e.find("img") is None]
    return result

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def square():
    if request.method == 'POST':
        pass
    soup = load_soup_from_url("https://www.cacaniqueisonline.com/analise/betsson/")
    review = get_class_element(soup,'.col-12.col-lg-8.text')
    items = all_translatable_elements(review)
    for item in items:
        print(item)
        item.replace_with(item.text)
    return render_template_string(str(review))


if __name__ == '__main__':
    app.run()