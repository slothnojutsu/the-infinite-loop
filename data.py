import sqlite3
import pandas as pd

# Connect to the same database
conn = sqlite3.connect('plates.db')
df_sql = pd.read_sql(f'SELECT * FROM "Car License Number"', conn)
print(df_sql)
conn.close()


from flask import Flask, render_template, url_for, request, redirect, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'nottoosure' #for session mangement 

#mysql configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = "@Finish213"
app.config['MYSQL_DB'] = 'user_info'

mysql = MySQL(app)

def save_dataframe(df, table_name):
    cols = ", ".join(df.columns)
    placeholders = ", ".join(["%s"] * len(df.columns))
    sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

    with app.app_context():
        conn = mysql.connection
        cur = conn.cursor()
        # Convert each DataFrame row to a tuple
        data = [tuple(row) for row in df.to_numpy()]
        # Bulk‐insert all rows
        cur.executemany(sql, data)
        conn.commit()
        cur.close()

save_dataframe(df_sql, "Car License Number")