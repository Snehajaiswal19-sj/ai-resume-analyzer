from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

uri = os.getenv('mongodb+srv://sneha_jaiswal00:Sneha1905@cluster0.opdtagu.mongodb.net/?appName=Cluster0')
print("Connection string found:", "Yes" if uri else "No")

if uri:
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("✅ MongoDB Atlas connected successfully!")
        
        # Test database operations
        db = client['resume_analyzer']
        collections = db.list_collection_names()
        print(f"✅ Database 'resume_analyzer' accessible")
        print(f"Collections: {collections}")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
else:
    print("❌ MONGODB_URI not found in .env file")