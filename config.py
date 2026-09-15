import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///resume_analyzer.db'
    DEBUG = True