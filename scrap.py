from bs4 import BeautifulSoup

import re, httpx, pandas


class Scraper():
    def __init__(self):
        self.session = httpx.Client()
    
    def get_html(self,url):
        r = self.session.get(url)
        print(r.status_code)
        html = r.text
        return html

def check_url(url:str)->str:
    prefix = "https://www.amazon.com"
    pattern = r"(/[^/]+/dp/[^/]+)/"
    match = re.search(pattern, url)

    if match:
        shorten_url = match.group(1)
    else:
        shorten_url = url

    if prefix not in shorten_url:
        complete_url = prefix+shorten_url
        return complete_url
    else:
        return shorten_url

def find_tag_list(html:str)->list[BeautifulSoup]:
    soup = BeautifulSoup(html,"html.parser")
    items = soup.find("div","s-main-slot s-result-list s-search-results sg-row")
    class_16_data = "sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"
    class_48_data = "sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20"
    if items.find_all("div",class_=class_16_data):
        list_of_tag = items.find_all("div",class_=class_16_data)
    elif items.find_all("div",class_=class_48_data):
        list_of_tag = items.find_all("div",class_=class_48_data)
    else:
        print("No tag class found")
        raise
    return list_of_tag

def parse(soup:BeautifulSoup)->dict:
    product_name = find_tag(soup,"a","a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
    product_url = find_tag(soup,"a","a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal","href")
    product_image = find_tag(soup,"img","s-image","src")
    price = find_tag(soup,"span","a-offscreen")
    rating = soup.find("div","a-row a-size-small")
    rating = find_tag(soup=rating,tag="span",attr="aria-label")
    
    item = {"product_name":product_name,
            "price":price.replace("$",""),
            "rating":rating.replace(" out of 5 stars",""),
            "image":product_image,
            "product_url":check_url(product_url)}
    return item

def find_tag(soup:BeautifulSoup,tag:str,class_name="",attr="")->str:
    try:
        tag = soup.find(tag,class_=class_name)
        if attr == "":
            text = tag.text.strip()
        else:
            text = tag[attr]
    except AttributeError:
        text = ""
    return text

def extract_html(html:str)->list[dict]:
    list_of_tag = find_tag_list(html)
    all_data = [parse(item) for item in list_of_tag]
    return all_data

def keyword_to_url(str_input)->str:
    text = str_input.replace(" ","+")
    url = f"https://www.amazon.com/s?k={text}"
    return url

def main(keyword):
    url = keyword_to_url(keyword)
    scraper = Scraper()
    html = scraper.get_html(url)
    result = extract_html(html)
    return result

def download(format_file, file):
    if format_file == "csv":
        df = pandas.DataFrame(file)
        filename = "result.csv"
        df.to_csv(filename,index=False)
    elif format_file == "excel":
        df = pandas.DataFrame(file)
        filename = "result.xlsx"
        df.to_excel(filename, index=False)
    print(f"saved to {filename}")


if __name__=="__main__":
    keyword = input("Input keyword: ")
    print(main(keyword))

    