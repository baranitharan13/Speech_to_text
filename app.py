from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
import os
import whisper
from werkzeug.utils import secure_filename
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create user database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Add one default user
def add_default_user():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'admin123'))
        conn.commit()
        print("Default user added: admin / admin123")
    except sqlite3.IntegrityError:
        print("Default user already exists.")
    conn.close()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect('/login')
        except sqlite3.IntegrityError:
            return "Username already exists"
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['username'] = username
            return redirect('/transcription')
        else:
            return "Invalid username or password"
    return render_template('login.html')
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    print("Upload route hit")  # Debug
    if 'username' not in session:
        print("User not logged in")
        return redirect(url_for('login'))

    if request.method == 'POST':
        print("POST request received")  # Debug
        if 'file' not in request.files:
            print("No file part")  # Debug
            return "No file part", 400

        file = request.files['file']
        if file.filename == '':
            print("No selected file")  # Debug
            return "No selected file", 400

@app.route('/transcription', methods=['GET', 'POST'])
def transcription():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        file = request.files['audio']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            model = whisper.load_model("base")
            result = model.transcribe(filepath)
            text = result["text"]

            # Save to PDF
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.pdf")
            doc = SimpleDocTemplate(pdf_path)
            styles = getSampleStyleSheet()
            story = [Paragraph(text, styles["Normal"])]
            doc.build(story)

            return send_file(pdf_path, as_attachment=True)

    return render_template('transcription.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    init_db()
    add_default_user()
    app.run(debug=True)
