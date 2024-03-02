from bs4 import BeautifulSoup

import re

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
        item = items.find_all("div",class_=class_16_data)
    elif items.find_all("div",class_=class_48_data):
        item = items.find_all("div",class_=class_48_data)
    else:
        print("No tag class found")
        raise
    return item

def parse(soup:BeautifulSoup):
    product = find_tag(soup,"a","a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
    product_name = product.text.strip()
    product_url = check_url(product["href"])
    product_image = find_tag(soup,"img","s-image")["src"]
    price = find_tag(soup,"span","a-offscreen").text.replace("$","")
    rating = find_tag(soup,"div","a-row a-size-small").find("span")["aria-label"].replace(" out of 5 stars","")
    return (product_name,product_url,product_image,price,rating)

def find_tag(soup:BeautifulSoup,tag:str,class_name:str):
    try:
        tag = soup.find(tag,class_=class_name)
    except:
        tag = "tag doesn't exist"
    return tag




if __name__=="__main__":
    with open("httpx.html") as file:
        html1 = file.read()

    with open("httpx-boots.html") as file:
        html2 = file.read()

    tag1 = find_tag_list(html1)[5]
    print(parse(tag1))

    tag2= find_tag_list(html2)[5]
    print(parse(tag2))
    
    