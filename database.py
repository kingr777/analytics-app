from pymongo import MongoClient
import streamlit as st

def get_database():
    try:
        # Get MongoDB URI from Streamlit secrets
        MONGO_URI = st.secrets["MONGO_URI"]
        
        client = MongoClient(MONGO_URI)
        # Test the connection
        client.server_info()
        db = client['dashboard_db']  # specify database name
        print("Successfully connected to MongoDB")
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        st.error("Failed to connect to database. Please check your connection string.")
        raise Exception("Could not connect to database") 