from flask import Flask, request, jsonify
from scripts.ebay_crawler import Crawler

app = Flask(__name__)

@app.route("/find-avg-rrp/", methods=["POST"])
def find_avg_rrp():
	body = request.json
	title = body["product-title"]

	crawler = Crawler(title)
	crawler.ScrapeEbay()
	crawler.ParseHTMLForAvgRRP()

	return jsonify(crawler.average_rrp)

app.run(debug=True)