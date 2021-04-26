from requests_html import AsyncHTMLSession
from requests_html import HTMLSession
from functools import partial
import json

def normal_crawl():
	async def get_links(index, url):
		''' function to make a request to every website's page and
		return the listing's links. Takes 2 arguments index - to know which
		website's selector to use and the corresponding url
		'''
		r = await asession.get(url)

		# link_sel - selector of the listing's a tags (links)
		link_sel = mappings[index][1]['link_sel']
		# price selector - selector of the price of the listing
		price_sel = mappings[index][1]['price_sel']

		# all the links and price elements found on the web page (should be the same number)
		links = r.html.find(link_sel)
		prices = r.html.find(price_sel)

		# append the link to result only if the link's price is less than 10000 ( some websities woldn't filter <= 3000 correctly )
		result = []
		for price, link in zip(prices, links): # iterating trough (price, link) as pairs !!!Not sure if they correspond to the same listing!!!
			if 'www.superimoti.bg' in url:
				prc = ''.join(filter(str.isdigit, price.text[-7:])) # if we are on this specific website get the last 7 digits of the price tag. I do this because there are sales on this website
			else:
				prc = ''.join(filter(str.isdigit, price.text)) # else get the digits inside the price tag
			# check if prc isn't empty and if not check if it's <= 10000 ( as I said some websites won't filter price <= 3000 and have some crazy prices of 100k+)
			if prc and int(prc) <= 10000:
				result.append(link.attrs['href'])

		r.close()

		return result

	# read the website - selector mappings from the json file and make them into an indexable list
	with open('sites.json') as f:
		mappings = json.load(f)
		mappings = list(mappings.items())
		print(mappings)

	session = HTMLSession()

	# create a dictionary with the keys being every single website page to scrape
	urls = {}
	for i, url in enumerate(mappings):
		urls[i] = [] # urls[i] is the same index as in the mappings list corresponding to the same website only with all the pages not only the first one
		r = session.get(url[0]+'1') # get the first page

		pages_count_link = url[1]["page_sel"]
		pages_count = r.html.find(pages_count_link, first=True)

		if pages_count is None:
			raise Exception("CHANGE IN WEBSITE STRUCTURE. FIX IT!")

		nop = ''
		for num in pages_count[-3:]:
			if num.isdigit():
				nop += num

		for page in range(1, int(nop)+1): # append each new page to the value of the url's key
			urls[i].append(url[0]+str(page))

	session.close()

	asession = AsyncHTMLSession()

	results = []
	for index in urls:
		partials = [partial(get_links, index, url) for url in urls[index]]
		results.extend(asession.run(*partials))

	asession.close()

	# flatten the list
	res = [url for urls in results for url in urls]

	return res

normal_crawl()