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


if __name__ == '__main__':
    app.run(debug=True)
