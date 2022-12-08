import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

def aggregate_dfs(auction_df, ebay_df):
	auction_df["avg_resell_price"] = ebay_df["avg-resell-price"].tolist()

	return auction_df

def apply_business_logic(main_df):
	IBIDDER_FEES = float(os.getenv("ibidder_fees"))
	SHIPPING = float(os.getenv("shipping_cost"))
	IBIDDER_BASE_URL = os.getenv("ibidder_base_url")

	def calculate_full_cost(price):
		full_cost = price * IBIDDER_FEES

		return full_cost

	def calculate_net_profit(full_cost, resell_price):
		ebay_fees = full_cost * 0.14 + 0.3
		net_profit = resell_price - full_cost - ebay_fees - SHIPPING

		return net_profit

	def calculate_percentage_profit(full_cost, net_profit):
		return net_profit/full_cost * 100

	main_df["lot_url"] = main_df["lot_url"].apply(lambda x: IBIDDER_BASE_URL + x)
	
	main_df["full_cost"] = main_df["lot_price"].apply(lambda x: calculate_full_cost(float(x)))
	main_df["net_profit"] = main_df.apply(lambda x: calculate_net_profit(x.full_cost, x.avg_resell_price), axis=1)
	main_df["percentage_profit"] = main_df.apply(lambda x: calculate_percentage_profit(x.full_cost, x.net_profit), axis=1)

	return main_df

def aggregate(auction_df, ebay_df):
	main_df = aggregate_dfs(auction_df, ebay_df)
	main_df = apply_business_logic(main_df)

	main_df = main_df[["uid", "lot_title", "lot_url", "full_cost", "avg_resell_price", "net_profit", "percentage_profit"]]

	return main_df