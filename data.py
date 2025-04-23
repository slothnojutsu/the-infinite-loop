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
    # Wrap table and column names in backticks to avoid reserved-word issues:
    safe_table = f"`{table_name}`"
    safe_cols  = ", ".join(f"`{col}`" for col in df.columns)

    # Build the placeholder string (%s per column):
    placeholders = ", ".join(["%s"] * len(df.columns))
    sql = f"INSERT INTO {safe_table} ({safe_cols}) VALUES ({placeholders})"

    print("DEBUG SQL:", sql)  # print the exact statement for debugging

    # Convert DataFrame to list of tuples
    data = [tuple(row) for row in df.to_numpy()]

    with app.app_context():
        conn = mysql.connection
        cur = conn.cursor()
        try:
            cur.executemany(sql, data)
            conn.commit()
        except Exception as e:
            print("INSERT ERROR:", e)   # log the full error
            conn.rollback()
            raise
        finally:
            cur.close()

save_dataframe(df_sql, "Car License Number")
