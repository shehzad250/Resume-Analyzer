#pip install flask
from flask import Flask, render_template, redirect, url_for, flash, request, send_file, session
from auth import auth_blueprint  # Import auth blueprint
from werkzeug.utils import secure_filename
import os
import json
import pdfplumber #pip install pdfplumber
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key' #your_secret_key
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Folder where resumes will be stored

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Register the auth blueprint
app.register_blueprint(auth_blueprint)
@app.route('/')
def home():
    return render_template('home.html')

# Resume upload route
@app.route('/upload', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        resume = request.files.get('resume')
        session['username'] = name  # Store the name in session

        # Check if the uploaded file is a PDF
        if resume and resume.filename.endswith('.pdf'):
            filename = secure_filename(resume.filename)  
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume.save(file_path) 
            
            flash("Resume uploaded successfully!", "success")
            return redirect(url_for('analyze_resume', filename=filename))
        else:
            flash("Only PDF files are allowed!", "danger")
            return redirect(url_for('upload_resume'))
    return render_template('resume_upload.html')
    
# Analysis route for displaying feedback
@app.route('/analyze/<filename>')
def analyze_resume(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)    
    feedback = analyze_pdf(file_path)
    # Get the user's name from session
    username = session.get('username', 'Anonymous')
    # Store feedback in database
    store_feedback_in_db(username, feedback)
    return redirect(url_for('results_dashboard'))

    # Save feedback to the database
    conn = sqlite3.connect(r'D:\ResumeAnalyzer\database.db')
    # conn = sqlite3.connect('D:/ResumeAnalyzer/database.db')
    # conn = sqlite3.connect('D:\\ResumeAnalyzer\\database.db')
    cursor = conn.cursor()

    # Insert feedback into the database
    cursor.execute("""
        INSERT INTO feedback_table (username, date, feedback_text)
        VALUES (?, datetime('now'), ?)
    """, (session.get('username', 'Anonymous'), json.dumps(feedback)))  # Use the logged-in user's name if available

    conn.commit()
    conn.close()

def store_feedback_in_db(username, feedback):
    conn = sqlite3.connect(r'D:\ResumeAnalyzer\database.db')
    cursor = conn.cursor()

    # Insert the feedback into the feedback_table
    cursor.execute(
        "INSERT INTO feedback_table (username, date, feedback_text) VALUES (?, DATE('now'), ?)",
        (username, json.dumps(feedback))
    )
    conn.commit()
    conn.close()

# Dashboard route for displaying results and download option
@app.route('/dashboard')
def results_dashboard():
    # Retrieve and load feedback from session
    feedback_json = session.get('feedback')
    if feedback_json:
        feedback = json.loads(feedback_json)
    else:
        feedback = {}
    return render_template('dashboard.html', feedback=feedback)

# Optional: Function to handle PDF file download
@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

def analyze_pdf(file_path):
    keywords = ["Python", "Data Analysis", "Flask", "Excel", "Communication", "Decision making"]  # Sample keywords
    suggestions = []
    
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    
    # Calculate word count
    word_count = len(text.split())
    
    # Check for keywords
    found_keywords = [keyword for keyword in keywords if keyword.lower() in text.lower()]
    
    # Suggestions
    if "Python" not in found_keywords:
        suggestions.append("Add more technical keywords like Python")
    if "Decision making" not in found_keywords:
        suggestions.append("Add soft skills like Decision making")
    
    feedback = {
        "word_count": word_count,
        "keywords_found": found_keywords,
        "suggestions": suggestions
    }
    return feedback

@app.route('/view_feedback')
def view_feedback():
    feedback_list = get_feedback_from_db()  # Ye line tumhare database se feedback data fetch karti hai
    return render_template('view_feedback.html', feedback_list=feedback_list)

def get_feedback_from_db():
    # Tumhare database ka naam
    conn = sqlite3.connect(r'D:\ResumeAnalyzer\database.db')
    cursor = conn.cursor()
    
    # Tumhare feedback table ka naam aur columns ke naam
    cursor.execute("SELECT username, date, feedback_text FROM feedback_table")
    feedback_list = cursor.fetchall()  # Sabhi rows ko fetch karo
    conn.close()
    
    formatted_feedback = []
    for feedback in feedback_list:
        # Parse feedback JSON for display
        #feedback_text = json.loads(feedback[2])
        try:
            feedback_text = json.loads(feedback[2])  # JSON parse karo
        except json.JSONDecodeError:
            feedback_text = feedback[2]  # Agar JSON valid nahi hai toh as-is use karo

        formatted_feedback.append({
            'username': feedback[0],
            'date': feedback[1],
            'feedback_text': feedback_text
        })
    return formatted_feedback  

@app.route('/delete_feedback', methods=['POST'])
def delete_feedback():
    username = request.form.get('username')
    date = request.form.get('date')
    
    # Connect to the database and delete the record
    conn = sqlite3.connect(r'D:\ResumeAnalyzer\database.db')  
    cursor = conn.cursor()

    # Delete query
    cursor.execute(
        "DELETE FROM feedback_table WHERE username = ? AND date = ?",
        (username, date)
    )
    conn.commit()
    conn.close()
    
    flash("Feedback deleted successfully!", "success")
    return redirect(url_for('view_feedback'))
  

if __name__ == '__main__':
    app.run(debug=True) #jo bhi error ho, wo terminal mai show hona chahiye, ye code ka kaam hai.
    # app.run(debug=True,port=8000) # hum port change kar sakte hai, is tarah   






