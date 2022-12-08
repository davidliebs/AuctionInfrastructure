import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def load_data(df):
	conn = mysql.connector.connect(
		user=os.getenv("db_user"),
		passwd=os.getenv("db_pwd"),
		host=os.getenv("db_host"), 
		port=int(os.getenv("db_port")),
		db=os.getenv("db_database")
	)
	cur = conn.cursor()

	for _,row in df.iterrows():
		row = row.tolist()

		print(row)

		cur.execute("""
			INSERT INTO product_data
			(record_uid, lot_title, lot_url, full_cost, avg_resell_price, net_profit, percentage_profit)
			VALUES ({}, '{}', '{}', {}, {}, {}, {})
		""".format(*row))

	conn.commit()
	conn.close()