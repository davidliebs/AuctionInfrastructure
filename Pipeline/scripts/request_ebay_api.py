import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd

load_dotenv()

# pulling data from ebay api
def pull_data_from_ebay_api(auction_df):
	ebay_data = []
	for index, row in auction_df.iterrows():
		product_title = row["lot_title"]

		body = {
			"product-title": product_title
		}

		res = requests.post(os.getenv("ebay_api_fetch_product_rrp_url"), json=body)
		resell_price = res.json()
		
		ebay_data.append([row["uid"], resell_price])

	ebay_df = pd.DataFrame(ebay_data, columns=["uid", "avg-resell-price"])

	return ebay_df