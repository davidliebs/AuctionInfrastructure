import mysql.connector
import os
import hashlib
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def load_data(auction_url, df):
	# creating unique identifier for auction url
	hash = hashlib.sha1()
	hash.update(str(datetime.now()).encode())
	auction_uid = hash.hexdigest()

	conn = mysql.connector.connect(
		user=os.getenv("db_user"),
		passwd=os.getenv("db_pwd"),
		host=os.getenv("db_host"), 
		port=int(os.getenv("db_port")),
		db=os.getenv("db_database")
	)
	cur = conn.cursor()

	# inserting auction uid hash into table
	cur.execute("INSERT INTO auction_uid_to_url(auction_uid, auction_url) VALUES('{}', '{}')".format(auction_uid, auction_url))
	conn.commit()

	# inserting product data
	for _,row in df.iterrows():
		row = row.tolist()

		cur.execute("""
			INSERT INTO product_data
			(auction_uid, lot_uid, lot_title, lot_url, full_cost, avg_resell_price, net_profit, percentage_profit)
			VALUES ('{}', {}, '{}', '{}', {}, {}, {}, {})
		""".format(auction_uid, *row))

	conn.commit()
	conn.close()