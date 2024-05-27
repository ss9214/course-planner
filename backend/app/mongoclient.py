from pymongo import MongoClient

client = MongoClient("mongodb+srv://srihari21:Minisrij%40921@courseplanner.rq8rthg.mongodb.net/?retryWrites=true&w=majority&appName=CoursePlanner")
# Create a new client and connect to the server
# Send a ping to confirm a successful connection

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["Course_Planner"]
coursesdb = db["Courses"]
prereqsdb = db["Prerequisites"]


