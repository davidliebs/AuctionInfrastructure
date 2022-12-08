import json, requests, os
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

load_dotenv()

class Crawler:
	def __init__(self, auction_url):
		chrome_options = Options()
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--window-size=1420,1080')
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--disable-gpu')
		self.driver = webdriver.Chrome(os.getenv("chromedriver_filepath"), options=chrome_options)

		self.auction_url = auction_url

		res = requests.get(self.auction_url)
		self.soup = BeautifulSoup(res.content, features="lxml")

		self.PATH_TO_DUMP = os.getenv("path_to_dump")

	def DetermineNumberOfPages(self):
		product_count_string = self.soup.find("div", {"class": "listing-page-header"}).text
		product_count = [int(i) for i in product_count_string.split() if i.isdigit()][0]
		self.no_pages = (product_count // 240) + 1

	def GenerateUrls(self):
		self.urls = []
		for page_no in range(1, self.no_pages + 1):
			url = self.auction_url + f"/search-filter?pagesize=240&page={page_no}"
			self.urls.append(url)

	def DownloadPages(self):
		self.soups = []
		for url in self.urls:
			self.driver.get(url)
			self.soups.append(BeautifulSoup(self.driver.page_source, features="lxml"))

	def ParseHTML(self):
		self.product_data = []

		for soup in self.soups:
			for i in soup.find_all("div", {"class": "lot-single"}):
				try:
					lot_url = i.find("a").get("href")
					lot_title = i.find("span", {"class": "lot-title"}).text
					lot_price = i.find("li", {"class": "current-price"}).find_all("span")[2].text
					if lot_price.strip() == "None":
						lot_price = i.find("li", {"class": "opening-price"}).find_all("span")[2].text

					self.product_data.append({"lot_url": lot_url, "lot_title": lot_title, "lot_price": lot_price})
				except Exception:
					continue