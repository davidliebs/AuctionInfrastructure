from bs4 import BeautifulSoup
import requests
from urllib.parse import urlencode, quote_plus
import statistics
import re
from dotenv import load_dotenv
import os
import asyncio
import aiohttp
import time

load_dotenv()

def generate_urls(titles):
	urls = {}
	for uid in titles:
		url_encoded_title = os.getenv("ebay_url").format(urlencode({"nkw": titles[uid]}, quote_via=quote_plus))
		urls[uid] =url_encoded_title
	
	return urls

async def get(uid, url, session):
	try:
		async with session.get(url=url) as response:
			res = await response.read()
			return (uid, res)
	except Exception as e:
		pass


async def main(urls):
	async with aiohttp.ClientSession() as session:
		response = await asyncio.gather(*[get(uid, urls[uid], session) for uid in urls])

	return response

def run_fetch_urls(urls):
	response = asyncio.run(main(urls))
	
	return response

def ParseHTMLForAvgRRP(soup):
	all_prices = []
	uncleaned_prices = soup.find_all("span", {"class": "s-item__price"})

	for i in uncleaned_prices:
		price = i.text.replace(",", "")
		price = re.findall("\d+\.\d+", price)[0]

		try:
			price = float(price)
		except ValueError:
			continue

		all_prices.append(price)

	try:
		average_resell = round(float(statistics.mean(all_prices)), 2)
	except Exception:
		average_resell = 0.0

	return average_resell

def run(responses):
	uid_resell_price_dict = {}
	for res in responses:
		uid, html = res[0], res[1].decode()
		soup = BeautifulSoup(html, features="html.parser")

		uid_resell_price_dict[uid] = ParseHTMLForAvgRRP(soup)

	return uid_resell_price_dict