from flask import Flask, request, jsonify
import scripts.ebay_crawler as ebay_crawler

app = Flask(__name__)

@app.route("/find-avg-rrp/", methods=["POST"])
def find_avg_rrp():
	body = request.json
	uids_and_titles = body["uids_and_titles"]

	urls = ebay_crawler.generate_urls(uids_and_titles)
	responses = ebay_crawler.run_fetch_urls(urls)
	uid_price_dict = ebay_crawler.run(responses)
	
	return jsonify(uid_price_dict)

app.run(debug=True)