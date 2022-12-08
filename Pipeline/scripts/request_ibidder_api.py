import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

# pulling data from ibidder api
def pull_data_from_ibidder_api(auction_url):
	body = {
		"auction-url": auction_url
	}

	res = requests.post(os.getenv("ibidder_api_scrape_auction_url"), json=body)
	auction_data = res.json()

	return auction_data