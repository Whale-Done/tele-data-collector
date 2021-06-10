# config database uri here
# it is ignored during commits, change gitignore to enable commits

class Config:
    USER_APP_NAME = "Tracker"  # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False  # Disable email authentication
    USER_ENABLE_USERNAME = True  # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = False
    # for deploy
    REDIS_URL = "redis://:p22272393a04e83e3c4b7cbe21faa98ac3d93cf57e55203ffa43eef0f3a2d5113@ec2-54-221-249-45.compute-1.amazonaws.com:14060"
    SQLALCHEMY_DATABASE_URI = 'postgres://uhnjiuiznnyqsb:e0118cc80785491f69f8e54cf16d7fef8837745aa5b5b19d93c0a0e8d0adf251@ec2-3-224-7-166.compute-1.amazonaws.com:5432/d38r95t4r9dm9a'
    # for debug
    # REDIS_URL = "redis://leipetushood:1234567890@localhost:6379"
    # SQLALCHEMY_DATABASE_URI = 'postgresql://leipetushood:1234567890@localhost:5432/whalemoney'
