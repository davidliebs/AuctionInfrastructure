import scripts.request_ibidder_api as ibidder_api
import scripts.request_ebay_api as ebay_api
import scripts.clean_data as clean_data
import scripts.aggregate as aggregate_data
import scripts.load_data as load_data
import pandas as pd
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/run-pipeline/", methods=["POST"])
def run_pipeline():
	body = request.json
	auction_url = body["auction-url"]

	raw_auction_data = ibidder_api.pull_data_from_ibidder_api(auction_url)
	auction_df = clean_data.clean_data(raw_auction_data)
	ebay_prices = ebay_api.pull_data_from_ebay_api(auction_df)
	main_df = aggregate_data.aggregate(auction_df, ebay_prices)
	load_data.load_data(main_df)

	return "1"

app.run(port=int(os.getenv("api_port")))