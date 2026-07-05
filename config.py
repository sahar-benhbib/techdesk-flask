
class Config:
    SECRET_KEY = 'change-moi-en-production-123'
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///techdesk.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False