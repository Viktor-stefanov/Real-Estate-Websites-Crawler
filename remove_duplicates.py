from requests_html import AsyncHTMLSession
from functools import partial
from urllib.parse import urlparse

async def rem_duplicates(url, index):
    r = await asession.get(url)


def remove_duplicates(urls, mappings):
    asession = AsyncHTMLSession()
    # find all the urls gathered from the same website
    for index, url in enumerate(mappings):
        same_site_urls = [site for site in urls if urlparse(site).scheme + urlparse(site).netloc == urlparse(url[0]).scheme + urlparse(url[0]).netloc]

        partials = [partial(rem_duplicates, site, index) for site in same_site_urls]

    asession.close()

    for url in urls:
        pass

    asession.close()