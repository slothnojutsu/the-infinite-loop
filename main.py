import easyocr
import cv2 as cv
import numpy as np
import pandas as pd
import os
from datetime import datetime
from flask import Flask
from flask_mysqldb import MySQL

reader = easyocr.Reader(['en'], gpu=False)
results = []

for file in os.listdir("assets"):
    if file.lower().endswith('.jpg'):
        path = os.path.join("assets", file)
        image = reader.readtext(path, 
                                allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        if image is None:
            continue

        # Compute areas
        areas = [cv.contourArea(np.array(bbox, dtype=np.int32)) for bbox, _, _ in image]
        max_idx = int(np.argmax(areas))
        biggest_bbox, biggest_text, biggest_conf = image[max_idx]

        print(f"Detected largest text: {biggest_text!r} (conf={biggest_conf:.2f})")
        
        results.append((file, biggest_text, biggest_conf, datetime.now()))


df = pd.DataFrame(results, columns=["Filename", "License Number", "Confidence", "Timestamp"])
print(df)

# load into mysql
app = Flask(__name__)
app.config.update(
    MYSQL_HOST='localhost',
    MYSQL_USER='root',
    MYSQL_PASSWORD='', #your password
    MYSQL_CURSORCLASS='DictCursor'
)

mysql = MySQL(app)

def ensure_database(db_name='user_info'):
    with app.app_context():
        # connect without selecting a database
        conn = mysql.connection
        cur  = conn.cursor()
        # Create the database if missing
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            
        )
        conn.commit()
        cur.close()
    # tell flask_mysqldb which DB to use going forward
    app.config['MYSQL_DB'] = db_name
# change the database name into where we need to work with web
ensure_database()

def save_dataframe(df: pd.DataFrame, table_name: str):
    # 1) Create table if needed
    with app.app_context():
        conn = mysql.connection
        cur  = conn.cursor()
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS `{table_name}` (
              `filename`       VARCHAR(255) NOT NULL,
              `license_number` VARCHAR(50)  NOT NULL,
              `confidence`     DOUBLE,
              `timestamp`      DATETIME,
              PRIMARY KEY (`filename`)    -- or adjust as needed
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        conn.commit()

        # 2) Bulk insert
        cols         = ["filename","license_number","confidence","timestamp"]
        safe_cols    = ", ".join(f"`{c}`" for c in cols)
        placeholders = ", ".join(["%s"] * len(cols))
        sql          = f"INSERT INTO `{table_name}` ({safe_cols}) VALUES ({placeholders})"

        data = [tuple(row) for row in df[cols].to_numpy()]
        cur.executemany(sql, data)
        conn.commit()
        cur.close()

# Usage:
df = df.rename(columns={
    'Filename':       'filename',
    'License Number': 'license_number',
    'Confidence':     'confidence',
    'Timestamp':      'timestamp'
})
df['timestamp'] = pd.to_datetime(df['timestamp'])

save_dataframe(df, 'car_licenses')
