from flask import Flask, render_template, redirect, url_for, request, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from googleapiclient.discovery import build

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# MongoDB Configuration
app.config['MONGO_URI'] = 'mongodb+srv://tdhawit:3nZVInKf4dKHEZi6@ai.8j5zxwx.mongodb.net/<your-database-name>?retryWrites=true&w=majority&appName=AI'
mongo = PyMongo(app)

# Initialize the YouTube Data API client
api_key = 'AIzaSyCfj-CW0UONOJO4vp5aGjkmOWhN_U6LuA4'
youtube = build('youtube', 'v3', developerKey=api_key)

def search_videos(topic, count=3):
    query = f"{topic} tutorial"
    request = youtube.search().list(
        part="snippet",
        maxResults=count,
        q=query,
        type="video"
    )
    response = request.execute()

    video_recommendations = []
    for item in response['items']:
        title = item['snippet']['title']
        video_id = item['id']['videoId']
        thumbnail_url = item['snippet']['thumbnails']['default']['url']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_recommendations.append({
            'title': title,
            'url': video_url,
            'thumbnail': thumbnail_url
        })

    return video_recommendations

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = mongo.db.users.find_one({'email': email})

        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            return redirect(url_for('quiz'))

        return redirect(url_for('login', error='Invalid credentials'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        mongo.db.users.insert_one({
            'username': username,
            'email': email,
            'password': password
        })

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            user_answers = request.form.to_dict()
            quiz_id = user_answers.pop('quiz_id')  # Remove quiz_id from user_answers
            print(f"Quiz ID: {quiz_id}")
            print(f"User Answers: {user_answers}")

            # Convert the quiz_id to ObjectId
            try:
                quiz_id = ObjectId(quiz_id)
            except Exception as e:
                print(f"Invalid ObjectId: {e}")
                return "Invalid Quiz ID", 400

            # Fetch the quiz data from the database
            quiz = mongo.db.quizzes.find_one({"_id": quiz_id})
            if not quiz:
                print("No quiz found for the given ID")
                return "No quiz found for the given ID", 404

            total_score = 0
            topic_scores = {}

            for topic_data in quiz['questions']:
                topic = topic_data['topic']
                for i, question in enumerate(topic_data['questions']):
                    selected_option = user_answers.get(f'answer-{topic}-{i}')
                    if selected_option == question['answer']:
                        total_score += 1
                        if topic not in topic_scores:
                            topic_scores[topic] = 0
                        topic_scores[topic] += 1

            session['quiz_score'] = total_score
            session['quiz_taken'] = True

            for topic, score in topic_scores.items():
                mongo.db.quiz_results.insert_one({
                    'user_id': ObjectId(session['user_id']),
                    'topic': topic,
                    'score': score
                })

            return redirect(url_for('dashboard'))
        except Exception as e:
            return f"An error occurred while processing the quiz submission: {e}", 500

    quiz = mongo.db.quizzes.find_one()
    if not quiz:
        return "No quiz found in the database", 404

    return render_template('quiz.html', quiz=quiz, enumerate=enumerate)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    return render_template('dashboard.html')

@app.route('/resources')
def resources():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    # Fetch the user's quiz results from the database
    quiz_results = mongo.db.quiz_results.find_one({'user_id': ObjectId(user_id)})

    # Check if quiz results exist
    if not quiz_results:
        return render_template('resources.html', recommendations=[])

    # Topics where the user scored low (assuming score < 5 is low)
    low_score_topics = [result['topic'] for result in quiz_results['results'] if result['score'] < 5]

    # Generate video recommendations based on low-scoring topics
    video_recommendations = []
    for topic in low_score_topics:
        video_recommendations.extend(search_videos(topic, 3))

    return render_template('resources.html', recommendations=video_recommendations)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
