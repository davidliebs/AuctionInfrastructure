from flask import Flask, request, jsonify
from scripts.ibidder_crawler import Crawler
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/scrape-auction/", methods=["POST"])
def scrape_auction():
	body = request.json
	auction_url = body["auction-url"]

	crawler = Crawler(auction_url)
	crawler.DetermineNumberOfPages()
	crawler.GenerateUrls()
	crawler.DownloadPages()
	crawler.ParseHTML()

	return jsonify(crawler.product_data)

app.run(port=int(os.getenv("api_port")))