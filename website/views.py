from flask import Flask, request, render_template, Blueprint, jsonify
import sqlite3


views = Blueprint('views', __name__)


@views.route('/submit', methods=['POST'])
def submit_form():
    race = request.form['race']
    living_status = request.form['living_status']
    occupation = request.form['occupation']
    gender = request.form['gender']
    
    # Fetch updated scores based on input
    model_scores = get_average_scores(race, living_status, occupation, gender)

    # Return scores as JSON instead of redirecting
    return jsonify(model_scores)

def get_average_scores(race, living_status, occupation, gender):
    db_path = 'data/prompt_database.db'
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = '''
            SELECT model, AVG(query_response) AS avg_score
            FROM Prompts
            WHERE race = ? AND living_status = ? AND occupation = ? AND gender = ?
            GROUP BY model
            ORDER BY model
        '''
        cursor.execute(query, (race, living_status, occupation, gender))
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print("SQLite error:", e)
        results = []
    finally:
        conn.close()
    
    return results

@views.route('/')
def home():
    # Extract parameters from query string or default to None
    race = request.args.get('race')
    living_status = request.args.get('living_status')
    occupation = request.args.get('occupation')
    gender = request.args.get('gender')
    
    # Default empty model_scores if not all parameters are present
    model_scores = []
    if all([race, living_status, occupation, gender]):
        model_scores = get_average_scores(race, living_status, occupation, gender)

    data = {
        'races': ['Anglo', 'Arabic', 'Black', 'Chinese', 'Hispanic', 'Indian', 'Jewish', 'None-Control'],
        'living_statuses': ['None-control', 'just myself', 'my family with kids', 'my pet and I', 'my roommate and I', 'my spouse and I'],
        'occupations': ['None-control', 'accountant', 'college student', 'construction worker', 'doctor', 'food service worker', 'government worker', 'retail associate', 'software engineer', 'teacher', 'unemployed'],
        'genders': ['Gender-Neutral', 'Man', 'Woman']
    }
    
    return render_template("home.html", **data, model_scores=model_scores)
