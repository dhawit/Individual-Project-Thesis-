from pymongo import MongoClient

# Use the MongoDB Atlas connection URI
mongo_uri = 'mongodb+srv://tdhawit:3nZVInKf4dKHEZi6@ai.8j5zxwx.mongodb.net/?retryWrites=true&w=majority&appName=AI'

# Connect to the MongoDB server
client = MongoClient(mongo_uri)

# Access the database and collection
db = client['e_learning_db']
users_collection = db['users']
