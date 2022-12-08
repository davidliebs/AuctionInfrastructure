import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd

load_dotenv()

# pulling data from ebay api
def pull_data_from_ebay_api(auction_df):
	uids, titles = auction_df["uid"].tolist(), auction_df["lot_title"].tolist()

	body = {
		"uids_and_titles": {uids[i]:titles[i] for i in range(len(uids))}
	}

	res = requests.post(os.getenv("ebay_api_fetch_product_rrp_url"), json=body)
	returned_data = res.json()

	return returned_data