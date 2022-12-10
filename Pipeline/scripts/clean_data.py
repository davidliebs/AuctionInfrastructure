import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd
from random import randint

load_dotenv()

# cleaning data
def clean_lot_prices(price_string):
	price_string = price_string.strip()
	price_string = price_string.replace("GBP", "")
	price_string = price_string.replace(",", "")
	
	return float(price_string)

def clean_lot_titles(title):
	title = title.replace("'", "")

	return title

def generate_uid():
	return int("".join([str(randint(0,9)) for i in range(5)]))

def clean_data(raw_auction_data):
	df = pd.DataFrame(raw_auction_data)

	df["lot_price"] = df["lot_price"].apply(lambda x: clean_lot_prices(x))
	df["lot_title"] = df["lot_title"].apply(lambda x: clean_lot_titles(x))

	df = df.sort_values("lot_price").drop_duplicates("lot_title", keep='first')
	df["uid"] = df["lot_url"].apply(lambda x: generate_uid())
	
	return df