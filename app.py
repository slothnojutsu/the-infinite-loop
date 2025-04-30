import easyocr
import cv2 as cv
import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta
import random
from flask import Flask, render_template, url_for, request, redirect, session
from flask_mysqldb import MySQL

# Initialize OCR reader
reader = easyocr.Reader(['en'], gpu=False)
results = []

# Loop through images in folder
for file in os.listdir("static/case"):
    if file.lower().endswith('.jpg'):
        path = os.path.join("static/case", file)
        image = reader.readtext(path, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        if image is None or len(image) == 0:
            continue

        # Get the largest bounding box (biggest text area)
        areas = [cv.contourArea(np.array(bbox, dtype=np.int32)) for bbox, _, _ in image]
        max_idx = int(np.argmax(areas))
        biggest_bbox, biggest_text, _ = image[max_idx]

        # Generate random entry and exit times
        base_time = datetime.now().replace(hour=8, minute=0, second=0)
        entry_offset = timedelta(minutes=random.randint(0, 480))  # up to 8 hours
        exit_offset = entry_offset + timedelta(minutes=random.randint(15, 180))  # exit after entry

        entry_time = base_time + entry_offset
        exit_time = base_time + exit_offset

        # Append path and license plate with entry/exit times
        results.append((path, biggest_text, entry_time, exit_time))

# Convert to DataFrame
df = pd.DataFrame(results, columns=["path", "license_plate", "entry_time", "exit_time"])
print(df)

# Flask and MySQL configuration
app = Flask(__name__)
app.secret_key = 'nottoosure'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = "@Finish213"
app.config['MYSQL_DB'] = 'Project_details'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Save data to MySQL
def save_dataframe_to_mysql(df: pd.DataFrame):
    with app.app_context():
        conn = mysql.connection
        cur = conn.cursor()

        # Ensure table exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS car_plates (
                id INT AUTO_INCREMENT PRIMARY KEY,
                path VARCHAR(255) NOT NULL,
                license_plate VARCHAR(50) NOT NULL UNIQUE,
                entry_time DATETIME,
                exit_time DATETIME
            );
        """)
        conn.commit()

        # Insert data (skip duplicates using INSERT IGNORE)
        sql = """
            INSERT IGNORE INTO car_plates (path, license_plate, entry_time, exit_time)
            VALUES (%s, %s, %s, %s)
        """
        cur.executemany(sql, list(df.itertuples(index=False, name=None)))

        conn.commit()
        cur.close()

# Save the processed records
save_dataframe_to_mysql(df)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Connect to DB and check credentials
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['email'] = email
            return redirect('/')
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        phone_number = request.form['pnum']
        license_plate = request.form['lpnum']

        if password != confirm_password:
            return "Passwords do not match."

        cursor = mysql.connection.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (name, email, password, phone_number, license_plate) VALUES (%s, %s, %s, %s, %s)",
                (name, email, password, phone_number, license_plate)
            )
            mysql.connection.commit()

            # Store in session
            session['name'] = name
            session['email'] = email
            session['pnum'] = phone_number
            session['lpnum'] = license_plate

            return redirect('/profile')

        except Exception as e:
            mysql.connection.rollback()
            if "Duplicate entry" in str(e):
                return "This email is already registered."
            return f"An error occurred: {e}"
        finally:
            cursor.close()

    return render_template('register.html')

@app.route('/zip') #availability 
def zip():
    return render_template('zip.html')

@app.route('/profile')
def profile():
    if 'email' not in session:
        return redirect('/login')  # or wherever you want unauthenticated users to go

    return render_template('profile.html',
                           name=session.get('name'),
                           email=session.get('email'),
                           pnum=session.get('pnum'),
                           lpnum=session.get('lpnum'))


@app.route('/payment', methods=['GET', 'POST'])
def payment():
  return render_template('payment.html')
if __name__ == '__main__':
    app.run(debug=True)