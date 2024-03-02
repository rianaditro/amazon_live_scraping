from bs4 import BeautifulSoup

import re

def check_url(url:str)->str:
    pattern = r"(.*?)/(?!.*?)"
    match = re.search(pattern, text)

    if match:
        extracted_text = match.group(1)
    else:
        pass

def find_tag_list(html:str)->list[BeautifulSoup]:
    soup = BeautifulSoup(html,"html.parser")
    items = soup.find("div","s-main-slot s-result-list s-search-results sg-row")
    class_16_data = "sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"
    class_48_data = "sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20"
    if items.find_all("div",class_=class_16_data):
        item = items.find_all("div",class_=class_16_data)
    elif items.find_all("div",class_=class_48_data):
        item = items.find_all("div",class_=class_48_data)
    else:
        print("No tag class found")
        raise
    return item

def parse(list_tag:list[BeautifulSoup]):
    #for item in list_tag:
    product = list_tag[0].find("a","a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
    product_name = product.text.strip()
    product_url = product["href"]
    return (product_name,product_url)


if __name__=="__main__":
    with open("httpx.html") as file:
        html1 = file.read()

    with open("httpx-boots.html") as file:
        html2 = file.read()

    tag1 = find_tag_list(html1)
    print(parse(tag1))

    tag2= find_tag_list(html2)
    print(parse(tag2))
    
    