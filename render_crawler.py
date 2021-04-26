from requests_html import HTMLSession
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from time import sleep
import json

def render_crawl():
    def get_links(driver, index, url):
        ''' function to make a request to every website's page and
        return the listing's links. Takes 3 arguments driver - the web, index - to know which
        website's selector to use and url - the corresponding url
        '''
        driver.get(url)

        # link_sel - selector of the listing's a tags (links)
        link_sel = mappings[index][1]['link_sel']
        # price selector - selector of the price of the listing
        price_sel = mappings[index][1]['price_sel']

        sleep(0.5)
        # all the links and price elements found on the web page (should be the same number)
        links = driver.find_elements_by_css_selector(link_sel)
        prices = driver.find_elements_by_css_selector(price_sel)

        # append the link to result only if the link's price is less than 10000 ( some websities woldn't filter <= 3000 correctly )
        if 'http://imoti.bg/' in url:
            temp = []
            for price, link in zip(prices, links):
                prc = ''
                for letter in price.text:
                    if letter.isdigit():
                        prc += letter
                    else:
                        break
                if prc and int(prc) <= 6000:
                    temp.append(link.get_attribute('href'))
            links = temp
        else:
            temp = []
            for price, link in zip(prices, links):
                prc = ''.join(filter(str.isdigit, price.text))
                if prc and int(prc) <= 6000:
                    temp.append(link.get_attribute('href'))
            links = temp

        return links



    # read the website - selector mappings from the json file and convert them to an indexable list
    with open('render_sites.json') as f:
        mappings = json.load(f)
        mappings = list(mappings.items())

    session = HTMLSession()

    # map every website's name with the number of pages there are
    urls = {}
    for i, url in enumerate(mappings):
        urls[i] = []

        r = session.get(url[0]+'1')
        # using a while loop until timeout is not hit because rendering sometimes timeouts for no reason
        while True:
            try:
                r.html.render(timeout=12)
                break
            except:
                continue
        pages = r.html.find(url[1]['page_sel'])[0].text
        nop = 0
        for num in pages[-3:]:
            if num.isdigit():
                nop += int(num)

        for page in range(1, nop+1):
            urls[i].append(url[0]+str(page)) # append each new page to the value of the url's key

    session.close()

    opts = Options()
    opts.add_argument('--headless')
    driver = webdriver.Chrome(r'C:\Users\viktor\OneDrive\Desktop\Python\projects\mediocre\Epicgames-Website-Project\chromedriver.exe', options=opts)

    results = []
    for index in urls:
        for url in urls[index]:
            results.extend(get_links(driver, index, url))

    driver.quit()

    return results