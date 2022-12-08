from bs4 import BeautifulSoup
import requests
from urllib.parse import urlencode, quote_plus
import statistics
import re
from dotenv import load_dotenv
import os

class Crawler:
	def __init__(self, title):
		load_dotenv()

		self.title = title
		self.url_to_scrape = os.getenv("ebay_url")
		
	def ScrapeEbay(self):
		url_encoded_title = urlencode({"nkw": self.title}, quote_via=quote_plus)
		self.url_to_scrape = self.url_to_scrape.format(url_encoded_title)

		res = requests.get(self.url_to_scrape)
		self.soup = BeautifulSoup(res.content, features="lxml")

	def ParseHTMLForAvgRRP(self):
		all_prices = []
		uncleaned_prices = self.soup.find_all("span", {"class": "s-item__price"})

		for i in uncleaned_prices:
			price = i.text.replace(",", "")
			price = re.findall("\d+\.\d+", price)[0]

			try:
				price = float(price)
			except ValueError:
				continue

			all_prices.append(price)

		try:
			self.average_rrp = round(float(statistics.mean(all_prices)), 2)
		except Exception:
			self.average_rpp = 0.0