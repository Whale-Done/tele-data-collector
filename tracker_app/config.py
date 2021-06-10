# config database uri here
# it is ignored during commits, change gitignore to enable commits

class Config:
    USER_APP_NAME = "Tracker"  # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False  # Disable email authentication
    USER_ENABLE_USERNAME = True  # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = False
    # for deploy
    # REDIS_URL = "redis://leipetushood:1234567890@localhost:6379"
    # SQLALCHEMY_DATABASE_URI = ''
    # for debug
    REDIS_URL = "redis://leipetushood:1234567890@localhost:6379"
    SQLALCHEMY_DATABASE_URI = 'postgresql://leipetushood:1234567890@localhost:5432/whalemoney'