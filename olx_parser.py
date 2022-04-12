import requests
from bs4 import BeautifulSoup
from time import sleep
from multiprocessing import Pool

def get_listing(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    html = None
    links = None
    try:
        r = requests.get(url, headers=headers, timeout=10)
    
        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            listing_section = soup.select('.ba608fb8.de8df3a3 >li > article > div > a')
            links = [link['href'].strip() for link in listing_section]
    except Exception as ex:
        print(str(ex))
    finally:
        return links


# parse a single item to get information
def parse(URL):
    url = 'https://www.olx.com.pk/'+ URL
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    info = []

    try:
        r = requests.get(url, headers=headers, timeout=10)
        sleep(2)

        if r.status_code == 200:
            print('Processing..' + url)
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            title = soup.find('h1')
            if title is not None:
                title.text.strip()
            all_det = soup.find_all('div', class_="_676a547f")
            
            for ele in all_det:
                spans = ele.find_all('span')
                keys = spans[0].text
                values = spans[1].text
                dic = {keys:values}
                info.append(dic)
            
    except Exception as ex:
        print(str(ex))
    return info

car_links = None
cars_info = []
cars_links = get_listing('https://www.olx.com.pk/cars/')


p = Pool(5)  # Pool tells how many at a time
records = p.map(parse, cars_links)
p.terminate()
p.join()

