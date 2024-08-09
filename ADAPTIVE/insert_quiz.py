from pymongo import MongoClient

# Replace with your MongoDB connection string
client = MongoClient('mongodb://localhost:27017/')
db = client.yourdatabase  # Replace 'yourdatabase' with your actual database name

# Sample quiz data
quiz_data = {
    "questions": [
        {
            "question": "What is the capital of France?",
            "options": ["Paris", "London", "Berlin", "Madrid"],
            "answer": "Paris"
        },
        {
            "question": "What is 2 + 2?",
            "options": ["3", "4", "5", "6"],
            "answer": "4"
        }
    ]
}

# Insert the quiz data into the 'quizzes' collection
db.quizzes.insert_one(quiz_data)
print("Quiz data inserted successfully!")
