from flask import Flask, render_template, redirect, request
from dotenv import load_dotenv
import mysql.connector
import os
import requests

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home_page():
	return render_template("index.html")

@app.route("/add-auction-url/", methods=["GET", "POST"])
def add_auction_url():
	if request.method == "POST":
		auction_url = request.form.get("auction_url")

		body = {
			"auction-url": auction_url
		}

		requests.post(os.getenv("run_pipeline_url"), json=body)

		return redirect("/")

	return render_template("add_auction_url.html")

@app.route("/auctions-processed/")
def auctions_processed():
	conn = mysql.connector.connect(
		user=os.getenv("db_user"),
		passwd=os.getenv("db_pwd"),
		host=os.getenv("db_host"), 
		port=int(os.getenv("db_port")),
		db=os.getenv("db_database")
	)
	cur = conn.cursor()

	cur.execute("SELECT * FROM auction_uid_to_url")
	auctions_processed_list = cur.fetchall()

	conn.close()

	return render_template("auctions_processed.html", auctions=auctions_processed_list)

@app.route("/auction-data/")
def auction_data():
	auction_uid = request.args.get("auction_uid")

	conn = mysql.connector.connect(
		user=os.getenv("db_user"),
		passwd=os.getenv("db_pwd"),
		host=os.getenv("db_host"), 
		port=int(os.getenv("db_port")),
		db=os.getenv("db_database")
	)
	cur = conn.cursor()

	cur.execute("""
		SELECT lot_uid, lot_url, lot_title, full_cost, avg_resell_price, net_profit, percentage_profit FROM product_data
		WHERE auction_uid = '{}'
	""".format(auction_uid))

	auction_products = cur.fetchall()

	conn.close()

	return render_template("product_data.html", auction_products=auction_products)

app.run(debug=True, port=9999)