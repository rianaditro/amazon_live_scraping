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

def parse(list_tag:list[BeautifulSoup]):
    #for item in list_tag:
    product = list_tag[0].find("a","a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
    product_name = product.text.strip()
    product_url = product["href"]
    return (product_name,product_url)


if __name__=="__main__":

    url = "/Camera-Shy-Kay-Cove-ebook/dp/B0C7QYS91W/ref=sr_1_1?crid=85DM2WL0692G&dib=eyJ2IjoiMSJ9.Tf2Vy2x498pDapzMTCMs7EXp9X0hatZ_cD1qGsa3lOdKHyCbiTedaPIxOY2WBtGdq5MjKn_q_M1cGO51cubHX0z8a_elpJAjmHH_Cla6JpWn38FFrYuemzkR--WzePH7xj5V8twKPEZHqtV1Dj1R9KPIkgxOozzSeEhIrKY0CTSdLb4kiH1lIMcRlYSTiF-qVsiD8JN6z0SyisCI4bLUYbzE0T-l6qhbAclJjpIPRFw.bP2v4Ft8kwO2DaFIeXg_NaXq_p57YAyb5JVQeQGp7HM&dib_tag=se&keywords=camera&qid=1709346093&s=books&sprefix=camera%2Cstripbooks-intl-ship%2C317&sr=1-1"
    print(check_url(url))
    # with open("httpx.html") as file:
    #     html1 = file.read()

    # with open("httpx-boots.html") as file:
    #     html2 = file.read()

    # tag1 = find_tag_list(html1)
    # print(parse(tag1))

    # tag2= find_tag_list(html2)
    # print(parse(tag2))
    
    